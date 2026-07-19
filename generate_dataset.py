#!/usr/bin/env python3
"""
CLI entry point for the Londiani Worshippers Synthetic Church Dataset Generator.
"""

import argparse
import logging
import os
import sys

# Ensure the repository root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataset_generator.core import generate_dataset
from dataset_generator.validator import validate_dataset


def main():
    parser = argparse.ArgumentParser(
        description="Londiani Worshippers Synthetic Church Dataset Generator"
    )
    parser.add_argument(
        "--output-dir", type=str, default="output",
        help="Directory for the output JSON file",
    )
    parser.add_argument(
        "--output-file", type=str, default="londiani_worshippers_dataset.json",
        help="Name of the output JSON file",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "--log-level", type=str, default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Only validate an existing dataset file (do not generate)",
    )
    parser.add_argument(
        "--input-file", type=str, default=None,
        help="Input file for validation mode",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log = logging.getLogger(__name__)

    if args.validate_only:
        input_path = args.input_file or os.path.join(args.output_dir, args.output_file)
        if not os.path.exists(input_path):
            log.error(f"Input file not found: {input_path}")
            raise SystemExit(1)

        log.info(f"Validating dataset: {input_path}")
        with open(input_path, "r", encoding="utf-8") as f:
            import json
            data = json.load(f)

        success = validate_dataset(data, log)
        raise SystemExit(0 if success else 1)

    log.info(f"Generating dataset with seed={args.seed}")
    dataset = generate_dataset(seed=args.seed)

    log.info("Running validation on generated dataset...")
    success = validate_dataset(dataset, log)

    if not success:
        log.error("Generated dataset failed validation. Aborting write.")
        raise SystemExit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    output_path = os.path.join(args.output_dir, args.output_file)

    import json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    file_size = os.path.getsize(output_path)
    log.info(f"Dataset written to: {output_path}")
    log.info(f"File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

    from collections import Counter
    cats = Counter(d["category"] for d in dataset)
    years = Counter(d["timestamp"][:4] for d in dataset)
    avg_len = sum(len(d["raw_text"]) for d in dataset) / len(dataset)

    log.info("=" * 60)
    log.info("DATASET SUMMARY")
    log.info("=" * 60)
    log.info(f"Total documents: {len(dataset)}")
    log.info(f"Categories: {len(cats)}")
    log.info(f"Years covered: {sorted(years.keys())}")
    log.info(f"Avg raw_text length: {avg_len:.0f} chars")
    log.info(f"Min raw_text length: {min(len(d['raw_text']) for d in dataset)} chars")
    log.info(f"Max raw_text length: {max(len(d['raw_text']) for d in dataset)} chars")

    for cat, count in sorted(cats.items()):
        log.info(f"  {cat}: {count}")

    log.info("=" * 60)
    log.info("✅ Generation complete!")


if __name__ == "__main__":
    main()
