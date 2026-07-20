# Londiani Worshippers Synthetic Church Dataset Generator

Generates a synthetic dataset of 225 church-related documents (15 categories × 15
documents each) for the fictional "Londiani Worshippers" church, with Kenyan
place names, local context, and occasional Swahili phrases mixed into
English-language text. It also includes a hybrid-retrieval RAG pipeline
(`rag/`) and a Streamlit chat UI on top of that corpus.

**Live demo:** [add your Streamlit Cloud URL]

## Why this project

A RAG pipeline where retrieval quality is measured, not assumed — built
around a labeled evaluation set instead of eyeballing chat outputs.

- **Hybrid retrieval, tuned deliberately**: dense (Gemini embeddings) + BM25,
  combined with a configurable weight, because dense search alone misses
  exact-ID and exact-number queries, and BM25 alone misses paraphrase/semantic ones.
- **Evaluation-driven, not vibes-driven**: `rag/evaluate.py` runs labeled
  queries against the index and checks expected doc IDs land in top-k —
  this is what caught the BM25 tokenization bug described below, before it
  reached the UI.
- **Chunking strategy shaped by the actual corpus**, not a fixed token count:
  most documents are short enough to embed whole; only outliers get split,
  and only on natural boundaries, so no motion or lesson section is ever cut
  mid-way.
- **Synthetic dataset generation**: 225 documents across 15 categories, with
  a uniqueness tracker and a validation pass before anything is written to disk.
- **Handles a flaky external API like production code**: retry-with-backoff
  on both embedding rate limits (429) and generation-endpoint overload (503).

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

Once the corpus existed, the obvious next step was making it queryable — sermons, board minutes, choir schedules, all of it, answerable through actual questions instead of grepping through `.txt` files.

I went with Gemini for both ends: `gemini-embedding-001` for the vectors, `gemini-3.5-flash` for the actual answers. Chroma holds the index locally, and since the whole corpus barely amounts to anything once embedded, I just commit it straight into the repo instead of standing up a hosted vector service — didn't feel worth the extra moving part for 225 documents.

Chunking took more thought than I expected. Almost every document here is short, a page or less, so splitting them felt like it would just water down retrieval for no reason. I kept short docs whole and only split the longer outliers (a handful of board minutes, bible studies, counseling summaries) along their natural item breaks, so a single motion or lesson section never gets cut in half.

The part that actually bit me: tracking IDs like `LW-0031` only live in each file's frontmatter, never in the body text. First pass at searching "what's in LW-0031?" came back empty, which made no sense until I checked what was actually being indexed. Fixed it by folding the doc_id into what gets tokenized for BM25. Dense search still does the semantic heavy lifting; BM25 catches the exact-ID and exact-number cases dense embeddings tend to smear over.

For generation I kept the system prompt strict — answer only from what got retrieved, say so plainly when the context doesn't cover it. Didn't want it inventing plausible-sounding church history.

Getting a key, running the ingest script, wiring up the GitHub Action, deploying on Streamlit — all of that is in [`rag/SETUP.md`](rag/SETUP.md).
