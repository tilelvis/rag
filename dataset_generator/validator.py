"""Validation logic for the generated dataset."""

import re
import logging
from datetime import datetime
from collections import Counter

from dataset_generator import config


def validate_dataset(data: list[dict], log: logging.Logger) -> bool:
    """Validate the generated dataset against all quality constraints."""
    valid = True

    # 1. Count check
    if len(data) != config.TOTAL_DOCS:
        log.error(f"Expected {config.TOTAL_DOCS} documents, got {len(data)}")
        valid = False
    else:
        log.info(f"✅ Document count: {len(data)}")

    # 2. Category count check
    cats = Counter(d["category"] for d in data)
    if len(cats) != config.CATEGORIES_COUNT:
        log.error(f"Expected {config.CATEGORIES_COUNT} categories, got {len(cats)}")
        valid = False
    else:
        log.info(f"✅ Category count: {len(cats)}")

    # 3. Per-category count check
    for cat, count in cats.items():
        if count != config.DOCS_PER_CATEGORY:
            log.error(f"Category '{cat}' has {count} docs, expected {config.DOCS_PER_CATEGORY}")
            valid = False
    if all(c == config.DOCS_PER_CATEGORY for c in cats.values()):
        log.info(f"✅ All categories have exactly {config.DOCS_PER_CATEGORY} documents")

    # 4. Missing categories check
    missing = set(config.CATEGORIES) - set(cats.keys())
    extra = set(cats.keys()) - set(config.CATEGORIES)
    if missing:
        log.error(f"Missing categories: {missing}")
        valid = False
    if extra:
        log.error(f"Extra categories: {extra}")
        valid = False
    if not missing and not extra:
        log.info("✅ All expected categories present, no extras")

    # 5. Unique IDs
    ids = [d["id"] for d in data]
    if len(ids) != len(set(ids)):
        dup_ids = [i for i in ids if ids.count(i) > 1]
        log.error(f"Duplicate IDs found: {set(dup_ids)}")
        valid = False
    else:
        log.info("✅ All IDs are unique")

    # 6. ID format check
    id_pattern = re.compile(r"^LW-\d{4}$")
    bad_ids = [d["id"] for d in data if not id_pattern.match(d["id"])]
    if bad_ids:
        log.error(f"Bad ID format: {bad_ids}")
        valid = False
    else:
        log.info("✅ All IDs match pattern LW-NNNN")

    # 7. Required fields check
    required_fields = ["id", "category", "timestamp", "raw_text", "inferred_metadata"]
    missing_fields_found = False
    for doc in data:
        for field in required_fields:
            if field not in doc:
                log.error(f"Document {doc.get('id', '?')} missing field: {field}")
                missing_fields_found = True
                valid = False
    if not missing_fields_found:
        log.info("✅ All documents contain required fields")

    # 8. Timestamp format and range check
    bad_timestamps = []
    for doc in data:
        try:
            ts = datetime.strptime(doc["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            if not (config.DATE_START_YEAR <= ts.year <= config.DATE_END_YEAR):
                bad_timestamps.append(doc["id"])
        except (ValueError, KeyError):
            bad_timestamps.append(doc.get("id", "?"))
    if bad_timestamps:
        log.error(f"Documents with invalid/out-of-range timestamps: {bad_timestamps}")
        valid = False
    else:
        log.info("✅ All timestamps are well-formed and in range")

    # 9. Minimum raw_text length check
    short_docs = [d["id"] for d in data if len(d.get("raw_text", "")) < 121]
    if short_docs:
        log.error(f"Documents shorter than minimum length (121 chars): {short_docs}")
        valid = False
    else:
        log.info("✅ All documents meet the minimum raw_text length")

    # 10. Uniqueness check (no two documents should have identical raw_text)
    raw_texts = [d["raw_text"] for d in data]
    dup_texts = {t for t in raw_texts if raw_texts.count(t) > 1}
    if dup_texts:
        log.error(f"Found {len(dup_texts)} exact duplicate document(s)")
        valid = False
    else:
        log.info("✅ No exact duplicate documents")

    if valid:
        log.info("✅ Dataset passed all validation checks")
    else:
        log.error("❌ Dataset failed one or more validation checks")

    return valid