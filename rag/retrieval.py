"""Hybrid retrieval: dense (Chroma/Gemini embeddings) + BM25 keyword search.

Plain dense search struggles with exact tokens like document IDs
("LW-0031") or precise numbers -- BM25 catches those. We normalize each
ranking to [0, 1] and combine with config.HYBRID_DENSE_WEIGHT.
"""

import pickle

import chromadb

from rag import config
from rag.embeddings import embed_query

_collection = None
_bm25_data = None


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=config.CHROMA_DIR)
        _collection = client.get_collection(config.COLLECTION_NAME)
    return _collection


def _get_bm25():
    global _bm25_data
    if _bm25_data is None:
        with open(config.BM25_INDEX_PATH, "rb") as f:
            _bm25_data = pickle.load(f)
    return _bm25_data


def _normalize(scores: dict[str, float]) -> dict[str, float]:
    if not scores:
        return {}
    lo, hi = min(scores.values()), max(scores.values())
    if hi == lo:
        return {k: 1.0 for k in scores}
    return {k: (v - lo) / (hi - lo) for k, v in scores.items()}


def dense_search(query: str, top_k: int = config.DENSE_TOP_K) -> dict[str, dict]:
    """Returns {chunk_id: {text, metadata, score}} where score is cosine similarity."""
    query_vec = embed_query(query)
    collection = _get_collection()
    result = collection.query(query_embeddings=[query_vec], n_results=top_k)
    out = {}
    for chunk_id, doc, meta, dist in zip(
        result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        out[chunk_id] = {"text": doc, "metadata": meta, "score": 1 - dist}  # cosine distance -> similarity
    return out


def bm25_search(query: str, top_k: int = config.BM25_TOP_K) -> dict[str, dict]:
    data = _get_bm25()
    scores = data["bm25"].get_scores(query.lower().split())
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    out = {}
    for i in ranked:
        if scores[i] <= 0:
            continue
        chunk_id = data["chunk_ids"][i]
        out[chunk_id] = {"text": data["documents"][i], "metadata": data["metadatas"][i], "score": scores[i]}
    return out


def hybrid_search(query: str, top_k: int = config.FINAL_TOP_K) -> list[dict]:
    dense = dense_search(query)
    keyword = bm25_search(query)

    dense_norm = _normalize({k: v["score"] for k, v in dense.items()})
    keyword_norm = _normalize({k: v["score"] for k, v in keyword.items()})

    all_ids = set(dense) | set(keyword)
    combined = []
    for chunk_id in all_ids:
        source = dense.get(chunk_id) or keyword.get(chunk_id)
        fused = (
            config.HYBRID_DENSE_WEIGHT * dense_norm.get(chunk_id, 0.0)
            + (1 - config.HYBRID_DENSE_WEIGHT) * keyword_norm.get(chunk_id, 0.0)
        )
        combined.append({
            "chunk_id": chunk_id,
            "text": source["text"],
            "metadata": source["metadata"],
            "score": fused,
            "in_dense": chunk_id in dense,
            "in_bm25": chunk_id in keyword,
        })
    combined.sort(key=lambda r: r["score"], reverse=True)
    return combined[:top_k]
