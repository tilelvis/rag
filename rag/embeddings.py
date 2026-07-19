"""Thin wrapper around the Gemini embedding API (google-genai SDK)."""

from google import genai
from google.genai import types

from rag import config

_client = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        if not config.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Export it locally, add it as a "
                "GitHub Actions secret, or set it in Streamlit secrets."
            )
        _client = genai.Client(api_key=config.GEMINI_API_KEY)
    return _client


def embed_texts(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embeds a batch of texts. task_type should be RETRIEVAL_DOCUMENT for
    corpus chunks at index time and RETRIEVAL_QUERY for user queries at
    search time -- Gemini embeddings are asymmetric and this materially
    affects retrieval quality.
    """
    client = get_client()
    # The API accepts a max batch size per call; keep batches modest so a
    # single failure doesn't force re-embedding hundreds of chunks.
    batch_size = 32
    vectors: list[list[float]] = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        result = client.models.embed_content(
            model=config.EMBEDDING_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=config.EMBEDDING_OUTPUT_DIM,
            ),
        )
        vectors.extend([e.values for e in result.embeddings])
    return vectors


def embed_query(text: str) -> list[float]:
    return embed_texts([text], task_type="RETRIEVAL_QUERY")[0]
