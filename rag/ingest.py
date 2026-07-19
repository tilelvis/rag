"""Builds the vector + keyword indexes from output/corpus/.

Usage:
    python3 -m rag.ingest

Requires GEMINI_API_KEY in the environment. Writes:
  - rag/chroma_db/         (persisted Chroma collection, committed to git)
  - rag/bm25_index.pkl     (pickled BM25 index over the same chunks)
"""

import argparse
import logging
import pickle
import shutil

import chromadb
from rank_bm25 import BM25Okapi

from rag import config
from rag.chunking import chunk_all_documents
from rag.embeddings import embed_texts

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("ingest")


def _tokenize(text: str) -> list[str]:
    return text.lower().split()


def build_index(fresh: bool = True) -> None:
    chunks = chunk_all_documents()
    log.info("Loaded %d chunks from %d source documents", len(chunks), len({c.doc_id for c in chunks}))

    if fresh:
        shutil.rmtree(config.CHROMA_DIR, ignore_errors=True)

    client = chromadb.PersistentClient(path=config.CHROMA_DIR)
    try:
        client.delete_collection(config.COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    log.info("Embedding %d chunks via %s ...", len(chunks), config.EMBEDDING_MODEL)
    vectors = embed_texts([c.text for c in chunks], task_type="RETRIEVAL_DOCUMENT")

    collection.add(
        ids=[c.chunk_id for c in chunks],
        embeddings=vectors,
        documents=[c.text for c in chunks],
        metadatas=[{"doc_id": c.doc_id, "category": c.category, **c.metadata} for c in chunks],
    )
    log.info("Persisted %d vectors to %s", len(chunks), config.CHROMA_DIR)

    # BM25 keyword index, over the same chunk set/order, for hybrid search
    # (handles exact document IDs like "LW-0031" that dense embeddings tend
    # to blur together). Note: tracking IDs only appear in each file's
    # frontmatter/filename, not in the body text itself, so the doc_id is
    # prepended here to make ID lookups ("what's in LW-0031?") matchable.
    tokenized = [_tokenize(f"{c.doc_id} {c.text}") for c in chunks]
    bm25 = BM25Okapi(tokenized)
    with open(config.BM25_INDEX_PATH, "wb") as f:
        pickle.dump({
            "bm25": bm25,
            "chunk_ids": [c.chunk_id for c in chunks],
            "documents": [c.text for c in chunks],
            "metadatas": [{"doc_id": c.doc_id, "category": c.category, **c.metadata} for c in chunks],
        }, f)
    log.info("Persisted BM25 index to %s", config.BM25_INDEX_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-fresh", action="store_true", help="Don't wipe the existing Chroma dir first")
    args = parser.parse_args()
    build_index(fresh=not args.no_fresh)
