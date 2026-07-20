"""Retrieval-augmented answer generation over the Londiani Worshippers corpus."""

import time

from google.genai import types
from google.genai.errors import ServerError

from rag import config
from rag.embeddings import get_client
from rag.retrieval import hybrid_search

# Gemini's generation endpoint occasionally returns 503 UNAVAILABLE during
# demand spikes (more common on newer/popular models). These are transient
# and Google's own error message recommends retrying, so back off and retry
# a few times before giving up -- mirrors the 429 handling in embeddings.py.
GENERATION_MAX_RETRIES = 4
GENERATION_RETRY_BASE_SECONDS = 2.0

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
    response = None
    for attempt in range(1, GENERATION_MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=config.GENERATION_MODEL,
                contents=f"Context:\n\n{context}\n\nQuestion: {question}",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                ),
            )
            break
        except ServerError:
            if attempt == GENERATION_MAX_RETRIES:
                raise
            time.sleep(GENERATION_RETRY_BASE_SECONDS * attempt)

    return {
        "question": question,
        "answer": response.text,
        "sources": [{"doc_id": h["metadata"]["doc_id"], "category": h["metadata"]["category"]} for h in hits],
        "hits": hits,
    }
