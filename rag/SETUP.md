# RAG pipeline setup

## Layout

```
├── rag/
│   ├── config.py      # model names, paths, chunking/retrieval settings
│   ├── chunking.py     # frontmatter parsing + chunking
│   ├── embeddings.py    # Gemini embedding calls (gemini-embedding-001)
│   ├── ingest.py         # builds rag/chroma_db (dense) + rag/bm25_index.pkl (keyword)
│   ├── retrieval.py       # hybrid dense + BM25 search with score fusion
│   ├── qa.py               # retrieval + Gemini generation (gemini-3.5-flash)
│   └── evaluate.py          # retrieval smoke tests
└── app.py              # Streamlit chat UI
```

(Dependencies for all of this live in the root `requirements.txt`, alongside
the dataset generator's — Streamlit Cloud only auto-installs that one file,
so this repo keeps everything in it rather than splitting out a second
requirements file.)

## 1. Get a Gemini API key

Create one at [Google AI Studio](https://aistudio.google.com/apikey).

## 2. Build the index locally

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your-key-here
python3 -m rag.ingest       # builds rag/chroma_db/ and rag/bm25_index.pkl
python3 -m rag.evaluate     # retrieval smoke test
streamlit run app.py        # chat UI at http://localhost:8501
```

`rag/chroma_db/` and `rag/bm25_index.pkl` are meant to be committed to the
repo (the corpus is small, so the index is small) so the Streamlit app can
load them directly without rebuilding at startup.

## 3. Keep the index up to date with GitHub Actions

`.github/workflows/build_rag_index.yml` runs automatically after the
`Generate Dataset` workflow finishes (or on manual dispatch): it installs
`requirements.txt`, runs `rag.ingest` to rebuild the index, runs
`rag.evaluate` as a smoke test, and commits `rag/chroma_db/` and
`rag/bm25_index.pkl` back into the repo (tagged `[skip ci]`, same pattern as
the dataset-generation commit).

Add your key under **Settings → Secrets and variables → Actions** as
`GEMINI_API_KEY`.

## 4. Deploy the chat app on Streamlit Community Cloud

1. Push this repo to GitHub (with `rag/chroma_db/` and `rag/bm25_index.pkl`
   already committed by the Action above).
2. On [share.streamlit.io](https://share.streamlit.io), create a new app
   pointing at this repo, branch `main`, main file `app.py`. It picks up
   `requirements.txt` automatically.
3. Under **App settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
4. Deploy. Every time the GitHub Action pushes a new index commit, redeploy
   (or enable Streamlit Cloud's auto-rerun-on-push) to pick it up.

## Tuning knobs

All in `rag/config.py`:

- `WHOLE_DOC_CHAR_THRESHOLD` / `TARGET_CHUNK_CHARS` / `CHUNK_OVERLAP_CHARS` — chunking behavior
- `HYBRID_DENSE_WEIGHT` — balance between dense and BM25 scores in `retrieval.py` (0 = pure keyword, 1 = pure dense)
- `DENSE_TOP_K` / `BM25_TOP_K` / `FINAL_TOP_K` — how many candidates each retriever pulls before fusion, and how many make it into the final context
- `EMBEDDING_MODEL` / `GENERATION_MODEL` — swap Gemini model versions here if Google deprecates the pinned ones
