"""Configuration for the RAG pipeline: models, paths, chunking thresholds.

Reads GEMINI_API_KEY from the environment (set as a repo secret in GitHub
Actions, and as a Streamlit secret in the deployed app).
"""

import os

# --- Gemini models -----------------------------------------------------
# Pinned to stable, GA model IDs. Update these if Google deprecates them
# (see https://ai.google.dev/gemini-api/docs/models).
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_OUTPUT_DIM = 768  # Matryoshka truncation: cheaper to store/search than 3072
GENERATION_MODEL = "gemini-3.5-flash"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# --- Paths ---------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_DIR = os.path.join(REPO_ROOT, "output", "corpus")
CHROMA_DIR = os.path.join(REPO_ROOT, "rag", "chroma_db")
COLLECTION_NAME = "londiani_worshippers"
BM25_INDEX_PATH = os.path.join(REPO_ROOT, "rag", "bm25_index.pkl")

# --- Chunking --------------------------------------------------------------
# Every synthetic document is short (under ~2K chars / ~500 tokens), so most
# documents fit comfortably in a single chunk (and well under the 8K-token
# embedding input limit). Only the longer outliers (some board-minutes and
# counseling/bible-study docs) get split, and only along their natural
# item/paragraph boundaries so a motion, agenda item, or lesson section is
# never cut in half.
WHOLE_DOC_CHAR_THRESHOLD = 1600
TARGET_CHUNK_CHARS = 700
CHUNK_OVERLAP_CHARS = 100

# --- Retrieval ---------------------------------------------------------
DENSE_TOP_K = 8
BM25_TOP_K = 8
FINAL_TOP_K = 5
# Weight given to the dense-similarity score vs. the BM25 score when the two
# rankings are combined (0.0 = pure keyword search, 1.0 = pure dense search).
HYBRID_DENSE_WEIGHT = 0.6
