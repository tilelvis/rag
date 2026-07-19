"""Parses corpus .txt files (YAML frontmatter + body) and chunks them.

Chunking strategy
------------------
Every doc in this corpus is short (see output/corpus/**/*.txt). Splitting
short docs would only hurt retrieval (less context per hit, more near-
duplicate vectors), so:

  * Docs <= WHOLE_DOC_CHAR_THRESHOLD chars -> kept as a single chunk.
  * Longer docs (some church_board_minutes_excerpt, counseling_intake_summary,
    bible_study_guide entries) are split on blank-line-separated blocks
    (an item, motion, agenda point, or lesson section), which are then
    packed into ~TARGET_CHUNK_CHARS windows with a small char overlap so a
    single motion/item is never split mid-way.

Every chunk carries the parent document's id/category/metadata plus a
chunk_index, so a hit can always be traced back to e.g. LW-0151.txt.
"""

import glob
import os
import re
from dataclasses import dataclass, field

from rag import config

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n\n?(.*)$", re.DOTALL)


@dataclass
class Chunk:
    chunk_id: str          # e.g. "LW-0151#0"
    doc_id: str             # e.g. "LW-0151"
    category: str
    text: str
    metadata: dict = field(default_factory=dict)


def _parse_frontmatter(raw: str) -> tuple[dict, str]:
    """Very small YAML-frontmatter parser tailored to export_corpus.py's output.

    Avoids adding a PyYAML dependency for a handful of flat key: value /
    key: [list, of, items] lines.
    """
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return {}, raw

    fm_block, body = match.groups()
    meta = {}
    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",") if v.strip()]
            meta[key] = items
        else:
            meta[key] = value.strip('"').strip("'")
    return meta, body.strip()


def load_documents(corpus_dir: str = config.CORPUS_DIR) -> list[dict]:
    """Reads every output/corpus/<category>/<id>.txt file into a dict."""
    docs = []
    for path in sorted(glob.glob(os.path.join(corpus_dir, "*", "*.txt"))):
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        meta, body = _parse_frontmatter(raw)
        category = os.path.basename(os.path.dirname(path))
        doc_id = meta.get("id") or os.path.splitext(os.path.basename(path))[0]
        docs.append({
            "doc_id": doc_id,
            "category": meta.get("category", category),
            "body": body,
            "metadata": meta,
            "source_path": path,
        })
    return docs


def _split_into_blocks(body: str) -> list[str]:
    """Splits on blank lines, keeping list-item continuations attached."""
    raw_blocks = re.split(r"\n\s*\n", body)
    return [b.strip() for b in raw_blocks if b.strip()]


def _pack_blocks(blocks: list[str], target_chars: int, overlap_chars: int) -> list[str]:
    """Greedily packs blocks into ~target_chars windows without splitting a block."""
    packed, current = [], []
    current_len = 0
    for block in blocks:
        block_len = len(block)
        if current and current_len + block_len > target_chars:
            packed.append("\n\n".join(current))
            # carry the tail of the previous window forward for overlap/context
            overlap_text = packed[-1][-overlap_chars:]
            current = [overlap_text, block] if overlap_text else [block]
            current_len = len(overlap_text) + block_len
        else:
            current.append(block)
            current_len += block_len
    if current:
        packed.append("\n\n".join(current))
    return packed


def chunk_document(doc: dict) -> list[Chunk]:
    body = doc["body"]
    if len(body) <= config.WHOLE_DOC_CHAR_THRESHOLD:
        texts = [body]
    else:
        blocks = _split_into_blocks(body)
        texts = _pack_blocks(blocks, config.TARGET_CHUNK_CHARS, config.CHUNK_OVERLAP_CHARS)

    chunks = []
    for i, text in enumerate(texts):
        chunks.append(Chunk(
            chunk_id=f"{doc['doc_id']}#{i}",
            doc_id=doc["doc_id"],
            category=doc["category"],
            text=text,
            metadata={
                **{k: v for k, v in doc["metadata"].items() if isinstance(v, (str, int, float))},
                "keywords": ", ".join(doc["metadata"].get("keywords", [])),
                "chunk_index": i,
                "num_chunks": len(texts),
            },
        ))
    return chunks


def chunk_all_documents(corpus_dir: str = config.CORPUS_DIR) -> list[Chunk]:
    all_chunks = []
    for doc in load_documents(corpus_dir):
        all_chunks.extend(chunk_document(doc))
    return all_chunks
