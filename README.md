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
