"""Retrieval-augmented answer generation over the Londiani Worshippers corpus."""

from google.genai import types

from rag import config
from rag.embeddings import get_client
from rag.retrieval import hybrid_search

SYSTEM_PROMPT = """You are an assistant answering questions about the internal \
records of "Londiani Worshippers" church, using ONLY the excerpts provided \
below as context.

Rules:
- Answer using only information present in the context. Do not use outside \
knowledge, and do not guess or infer facts that are not stated.
- If the context does not contain enough information to answer, say so \
plainly instead of speculating.
- When useful, cite the source document id(s) in parentheses, e.g. (LW-0151).
- Keep answers concise and directly responsive to the question.
"""


def _build_context(hits: list[dict]) -> str:
    blocks = []
    for h in hits:
        meta = h["metadata"]
        blocks.append(
            f"[{meta.get('doc_id')} | {meta.get('category')} | {meta.get('timestamp', '')}]\n{h['text']}"
        )
    return "\n\n---\n\n".join(blocks)


def answer(question: str, top_k: int = config.FINAL_TOP_K) -> dict:
    hits = hybrid_search(question, top_k=top_k)
    context = _build_context(hits)

    client = get_client()
    response = client.models.generate_content(
        model=config.GENERATION_MODEL,
        contents=f"Context:\n\n{context}\n\nQuestion: {question}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
        ),
    )
    return {
        "question": question,
        "answer": response.text,
        "sources": [{"doc_id": h["metadata"]["doc_id"], "category": h["metadata"]["category"]} for h in hits],
        "hits": hits,
    }
