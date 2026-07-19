"""Core orchestration logic for dataset generation."""

import random

from dataset_generator import config
from dataset_generator.tracker import UniquenessTracker
from dataset_generator.generators import GENERATORS


def generate_dataset(seed: int = 42) -> list[dict]:
    """Generate the complete 225-document dataset."""
    rng = random.Random(seed)
    tracker = UniquenessTracker()
    documents = []

    doc_index = 0
    for category in config.CATEGORIES:
        generator = GENERATORS[category]
        for _ in range(config.DOCS_PER_CATEGORY):
            doc = generator(doc_index, rng, tracker)

            # Overwrite ID to ensure strict sequential numbering
            doc["id"] = f"LW-{doc_index + 1:04d}"
            doc["category"] = category

            # Enforce raw_text minimum length
            if len(doc["raw_text"]) < 121:
                extension = (
                    f"\n\nAdditional note: This record is part of the Londiani Worshippers "
                    f"church archive. For more information, contact the church office. "
                    f"Mungu akubariki."
                )
                doc["raw_text"] += extension

            # Track uniqueness
            tracker.add_opening(doc["raw_text"])
            tracker.add_closing(doc["raw_text"])

            documents.append(doc)
            doc_index += 1

    return documents
