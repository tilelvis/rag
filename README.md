# Londiani Worshippers Synthetic Church Dataset Generator

Generates a synthetic dataset of 225 church-related documents (15 categories × 15
documents each) for the fictional "Londiani Worshippers" church, with Kenyan
place names, local context, and occasional Swahili phrases mixed into
English-language text.

## Structure

```
├── .github/
│   └── workflows/
│       └── generate_dataset.yml
├── dataset_generator/
│   ├── __init__.py
│   ├── config.py            # Constants, lists, and configuration
│   ├── utils.py              # Helper functions (randomizers, formatters)
│   ├── tracker.py            # Uniqueness tracking class
│   ├── core.py                # Main orchestration logic
│   ├── validator.py          # Dataset validation logic
│   └── generators/            # Category generator modules
│       ├── __init__.py        # Generator registry
│       ├── worship_teaching.py
│       ├── admin_planning.py
│       └── community_care.py
├── generate_dataset.py        # CLI entry point
├── requirements.txt
└── README.md
```

## Usage

Generate the dataset (writes `output/londiani_worshippers_dataset.json` by default):

```bash
python3 generate_dataset.py
```

Options:

```bash
python3 generate_dataset.py \
  --output-dir output \
  --output-file londiani_worshippers_dataset.json \
  --seed 42 \
  --log-level INFO
```

Validate an existing dataset file without regenerating it:

```bash
python3 generate_dataset.py --validate-only --input-file output/londiani_worshippers_dataset.json
```

## RAG-ready export

After generating the dataset, export it into formats suited for retrieval-augmented
generation pipelines:

```bash
python3 export_corpus.py --output-dir output
```

This produces, alongside `output/londiani_worshippers_dataset.json`:

- `output/corpus/<category>/<id>.txt` — one file per document, with YAML
  frontmatter metadata (id, category, timestamp, author, audience, location,
  keywords) followed by the body text. Drop this directory straight into
  LangChain's `DirectoryLoader` / LlamaIndex's `SimpleDirectoryReader` — each
  file becomes one source document, frontmatter becomes metadata.
- `output/londiani_worshippers_dataset.jsonl` — one JSON object per line, for
  custom embedding/ingestion scripts.

## Continuous integration

`.github/workflows/generate_dataset.yml` runs on every push to `main`
(and on manual dispatch): it regenerates the dataset, exports the RAG corpus,
uploads both as a downloadable workflow artifact, and commits `output/` back
into the repository so the generated files stay live on GitHub. The commit
step tags its own commit message with `[skip ci]` and the trigger ignores
changes under `output/**`, so the auto-commit doesn't retrigger the workflow.

## Output format

Each document is a JSON object:

```json
{
  "id": "LW-0001",
  "category": "sermon_transcript_snippet",
  "timestamp": "2023-06-11T09:12:00Z",
  "raw_text": "...",
  "inferred_metadata": {
    "author": "...",
    "target_audience": "...",
    "location_tag": "...",
    "language_mix": "...",
    "document_style": "...",
    "keywords": ["..."]
  }
}
```

## Categories (15, 15 docs each — 225 total)

`sermon_transcript_snippet`, `weekly_bulletin_announcement`, `bible_study_guide`,
`financial_tithe_report`, `ministry_leader_update`, `community_outreach_log`,
`facility_booking_request`, `counseling_intake_summary`, `prayer_request_wall`,
`sunday_school_curriculum`, `choir_rehearsal_schedule`, `church_board_minutes_excerpt`,
`event_calendar_entry`, `volunteer_roster_notice`, `visitor_welcome_followup`

## Validation checks

`validator.py` checks: total document count, category count and per-category count,
no missing/extra categories, unique `LW-NNNN` IDs, required fields present on every
document, well-formed timestamps within the configured date range, minimum
`raw_text` length, and no exact-duplicate documents.

## RAG pipeline (`rag/`)

Turns `output/corpus/` into a queryable, grounded Q&A system, using Gemini for
both embeddings and generation:

```
├── rag/
│   ├── config.py        # model names, paths, chunking/retrieval settings
│   ├── chunking.py       # frontmatter parsing + chunking (whole-doc for short
│   │                     # docs, item-boundary splitting for longer ones)
│   ├── embeddings.py      # Gemini embedding calls (gemini-embedding-001)
│   ├── ingest.py           # builds rag/chroma_db (dense) + rag/bm25_index.pkl (keyword)
│   ├── retrieval.py         # hybrid dense + BM25 search with score fusion
│   ├── qa.py                 # retrieval + Gemini generation (gemini-3.5-flash)
│   └── evaluate.py            # retrieval smoke tests
├── app.py                # Streamlit chat UI
└── requirements-rag.txt
```

### 1. Get a Gemini API key

Create one at [Google AI Studio](https://aistudio.google.com/apikey).

### 2. Build the index locally

```bash
pip install -r requirements.txt -r requirements-rag.txt
export GEMINI_API_KEY=your-key-here
python3 -m rag.ingest       # builds rag/chroma_db/ and rag/bm25_index.pkl
python3 -m rag.evaluate     # retrieval smoke test
streamlit run app.py        # chat UI at http://localhost:8501
```

`rag/chroma_db/` and `rag/bm25_index.pkl` are meant to be committed to the
repo (the corpus is small, so the index is small) so the Streamlit app can
load them directly without rebuilding at startup.

### 3. Keep the index up to date with GitHub Actions

`.github/workflows/build_rag_index.yml` runs automatically after the
`Generate Dataset` workflow finishes (or on manual dispatch): it installs
`requirements-rag.txt`, runs `rag.ingest` to rebuild the index, runs
`rag.evaluate` as a smoke test, and commits `rag/chroma_db/` and
`rag/bm25_index.pkl` back into the repo (tagged `[skip ci]`, same pattern as
the dataset-generation commit).

Add your key under **Settings → Secrets and variables → Actions** as
`GEMINI_API_KEY`.

### 4. Deploy the chat app on Streamlit Community Cloud

1. Push this repo to GitHub (with `rag/chroma_db/` and `rag/bm25_index.pkl`
   already committed by the Action above).
2. On [share.streamlit.io](https://share.streamlit.io), create a new app
   pointing at this repo, branch `main`, main file `app.py`.
3. Under **Advanced settings → Requirements file**, point it at
   `requirements-rag.txt` (or merge its contents into `requirements.txt`
   before deploying, since Streamlit Cloud only installs one requirements
   file by default).
4. Under **App settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
5. Deploy. Every time the GitHub Action pushes a new index commit, redeploy
   (or enable Streamlit Cloud's auto-rerun-on-push) to pick it up.

### Design notes

- **Chunking**: every document in this corpus is short (see length stats
  produced by `dataset_generator`), so short docs are embedded whole; only
  the handful of longer `church_board_minutes_excerpt`, `bible_study_guide`,
  and `counseling_intake_summary` outliers get split, along blank-line
  boundaries so a single motion or lesson section is never cut in half.
- **Hybrid retrieval**: tracking IDs like `LW-0031` appear in each file's
  frontmatter/filename but not in the body text, so dense embeddings alone
  can't do exact ID lookups. `rag/ingest.py` prepends the `doc_id` into the
  BM25 tokenization specifically to handle that case, and `retrieval.py`
  fuses normalized dense + BM25 scores (see `HYBRID_DENSE_WEIGHT` in
  `rag/config.py` to tune the balance).
- **Grounding**: `rag/qa.py`'s system prompt instructs Gemini to answer only
  from the retrieved context and say so when the context is insufficient,
  rather than filling gaps from general knowledge.
