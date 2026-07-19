"""Retrieval evaluation: does hybrid search surface the right chunks?

Usage:
    python3 -m rag.evaluate

Each case gives a query and the doc_id(s) we expect to see in the top-k
hybrid results. This isn't a rigorous benchmark -- it's a fast smoke test to
catch retrieval regressions (e.g. after changing the chunking strategy or
the dense/BM25 weighting) before they reach the Streamlit app.
"""

import logging

from rag.retrieval import bm25_search, dense_search, hybrid_search

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("evaluate")

# (query, expected doc_id substring) -- edit/extend with real LW-XXXX ids
# from your generated corpus once it exists.
CASES = [
    ("What time does choir rehearsal start on Tuesday?", None, "choir_rehearsal_schedule"),
    ("What motions were passed in the church board meeting?", None, "church_board_minutes_excerpt"),
    ("Tell me about document LW-0031", "LW-0031", None),
    ("What was discussed in LW-0151?", "LW-0151", None),
    ("How much was approved for community outreach?", None, "church_board_minutes_excerpt"),
]


def run() -> None:
    hits_ok, total = 0, 0
    for query, expected_id, expected_category in CASES:
        total += 1
        results = hybrid_search(query, top_k=5)
        found_ids = [r["metadata"]["doc_id"] for r in results]
        found_categories = [r["metadata"]["category"] for r in results]

        ok = True
        if expected_id and expected_id not in found_ids:
            ok = False
        if expected_category and expected_category not in found_categories:
            ok = False

        hits_ok += ok
        log.info("%s  %-60s -> %s", "PASS" if ok else "FAIL", query, found_ids)

    log.info("\n%d/%d retrieval smoke-test cases passed", hits_ok, total)

    # Compare dense vs. keyword individually for the ID-lookup cases, since
    # that's the scenario dense search alone tends to miss.
    log.info("\nDense vs. BM25 on an exact-ID query:")
    dense = dense_search("LW-0031", top_k=5)
    bm25 = bm25_search("LW-0031", top_k=5)
    log.info("  dense hits: %s", [m["metadata"]["doc_id"] for m in dense.values()])
    log.info("  bm25 hits:  %s", [m["metadata"]["doc_id"] for m in bm25.values()])


if __name__ == "__main__":
    run()
