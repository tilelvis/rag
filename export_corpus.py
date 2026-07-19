#!/usr/bin/env python3
"""
Export the generated dataset into RAG-friendly formats:
  - output/corpus/<category>/<id>.txt  (one file per document, YAML frontmatter + body)
  - output/londiani_worshippers_dataset.jsonl  (one JSON object per line)

Run this after generate_dataset.py has produced output/londiani_worshippers_dataset.json.
"""

import argparse
import json
import os


def yaml_escape(value):
    if isinstance(value, list):
        return "[" + ", ".join(f'"{v}"' for v in value) + "]"
    return f'"{value}"'


def export_corpus(input_path: str, output_dir: str) -> int:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    corpus_dir = os.path.join(output_dir, "corpus")
    os.makedirs(corpus_dir, exist_ok=True)

    for doc in data:
        cat_dir = os.path.join(corpus_dir, doc["category"])
        os.makedirs(cat_dir, exist_ok=True)

        frontmatter = ["---", f'id: "{doc["id"]}"', f'category: "{doc["category"]}"',
                       f'timestamp: "{doc["timestamp"]}"']
        for key, value in doc["inferred_metadata"].items():
            frontmatter.append(f"{key}: {yaml_escape(value)}")
        frontmatter.append("---")

        content = "\n".join(frontmatter) + "\n\n" + doc["raw_text"] + "\n"
        with open(os.path.join(cat_dir, f'{doc["id"]}.txt'), "w", encoding="utf-8") as out:
            out.write(content)

    jsonl_path = os.path.join(output_dir, "londiani_worshippers_dataset.jsonl")
    with open(jsonl_path, "w", encoding="utf-8") as out:
        for doc in data:
            out.write(json.dumps(doc, ensure_ascii=False) + "\n")

    return len(data)


def main():
    parser = argparse.ArgumentParser(description="Export dataset to RAG-friendly formats")
    parser.add_argument("--input-file", type=str, default="output/londiani_worshippers_dataset.json")
    parser.add_argument("--output-dir", type=str, default="output")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise SystemExit(f"Input file not found: {args.input_file} (run generate_dataset.py first)")

    count = export_corpus(args.input_file, args.output_dir)
    print(f"Exported {count} documents to {args.output_dir}/corpus/ and {args.output_dir}/londiani_worshippers_dataset.jsonl")


if __name__ == "__main__":
    main()
