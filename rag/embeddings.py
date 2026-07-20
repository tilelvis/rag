"""Thin wrapper around the Gemini embedding API (google-genai SDK)."""

import logging
import time

from google import genai
from google.genai import types
from google.genai.errors import ClientError

from rag import config

log = logging.getLogger(__name__)

_client = None

BATCH_SIZE = 20
BATCH_DELAY_SECONDS = 3       # pause between successful batches -- the free
                                # tier's embed_content quota is easy to burst
                                # through even at a handful of requests/sec
MAX_RETRIES = 6
DEFAULT_RETRY_SECONDS = 15.0


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


def _retry_delay_seconds(exc: ClientError) -> float:
    """Pulls Google's suggested retryDelay (e.g. "13s") out of the error
    details, falling back to a fixed default if it's missing."""
    try:
        for detail in exc.details.get("error", {}).get("details", []):
            if detail.get("@type", "").endswith("RetryInfo"):
                delay = detail.get("retryDelay", "")
                if delay.endswith("s"):
                    return float(delay[:-1]) + 1  # small buffer
    except (AttributeError, ValueError, TypeError):
        pass
    return DEFAULT_RETRY_SECONDS


def _embed_batch(client: genai.Client, batch: list[str], task_type: str) -> list[list[float]]:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = client.models.embed_content(
                model=config.EMBEDDING_MODEL,
                contents=batch,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=config.EMBEDDING_OUTPUT_DIM,
                ),
            )
            return [e.values for e in result.embeddings]
        except ClientError as exc:
            if exc.code != 429:
                raise
            wait = _retry_delay_seconds(exc)
            if attempt == MAX_RETRIES or wait > 120:
                # A short retryDelay (~13s, as returned for per-minute rate
                # limits) is worth waiting out; a long one usually means the
                # daily quota is exhausted and retrying won't help within
                # this job -- fail with a clear message instead of hanging.
                raise RuntimeError(
                    f"Gemini embedding requests are being rate-limited (429) after "
                    f"{attempt} attempt(s); last suggested wait was {wait:.0f}s. "
                    f"This is usually a free-tier quota limit -- check "
                    f"https://ai.dev/rate-limit or upgrade the API key's plan."
                ) from exc
            log.warning(
                "Rate limited by Gemini (attempt %d/%d), waiting %.1fs before retrying...",
                attempt, MAX_RETRIES, wait,
            )
            time.sleep(wait)
    raise RuntimeError("unreachable")  # loop always returns or raises


def embed_texts(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embeds a batch of texts. task_type should be RETRIEVAL_DOCUMENT for
    corpus chunks at index time and RETRIEVAL_QUERY for user queries at
    search time -- Gemini embeddings are asymmetric and this materially
    affects retrieval quality.
    """
    client = get_client()
    vectors: list[list[float]] = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        vectors.extend(_embed_batch(client, batch, task_type))
        if i + BATCH_SIZE < len(texts):
            time.sleep(BATCH_DELAY_SECONDS)
    return vectors


def embed_query(text: str) -> list[float]:
    return embed_texts([text], task_type="RETRIEVAL_QUERY")[0]
