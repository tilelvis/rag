"""Utility functions for randomization, formatting, and text generation."""

import random
from datetime import datetime, timedelta, timezone

from dataset_generator import config


def pick(seq, rng):
    return rng.choice(seq)


def pick_unique(seq, n, rng):
    return rng.sample(seq, min(n, len(seq)))


def random_timestamp(rng):
    date_start = datetime(config.DATE_START_YEAR, 1, 1, tzinfo=timezone.utc)
    date_end = datetime(config.DATE_END_YEAR, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    delta = date_end - date_start
    offset = rng.randint(0, int(delta.total_seconds()))
    dt = date_start + timedelta(seconds=offset)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def random_name(rng):
    return f"{pick(config.FIRST_NAMES, rng)} {pick(config.LAST_NAMES, rng)}"


def random_scripture(rng, ot_chance=0.5):
    if rng.random() < ot_chance:
        book = pick(config.BOOKS_OT, rng)
    else:
        book = pick(config.BOOKS_NT, rng)
    chapter = rng.randint(1, 150 if book == "Psalms" else 30)
    verse = rng.randint(1, 25)
    return f"{book} {chapter}:{verse}"


def random_scripture_range(rng):
    if rng.random() < 0.5:
        book = pick(config.BOOKS_OT, rng)
    else:
        book = pick(config.BOOKS_NT, rng)
    chapter = rng.randint(1, 50)
    v1 = rng.randint(1, 15)
    v2 = v1 + rng.randint(2, 12)
    return f"{book} {chapter}:{v1}-{v2}"


def maybe_swahili(rng, chance=0.15):
    if rng.random() < chance:
        return pick(config.SWAHILI_EXPRESSIONS, rng) + " "
    return ""


def maybe_local_context(rng, chance=0.3):
    if rng.random() < chance:
        return pick(config.LOCAL_CONTEXT, rng)
    return None


def format_kes(amount, rng):
    if rng.random() < 0.5:
        return f"KES {amount:,}"
    else:
        return f"Ksh {amount:,}"


def generate_unique_names(count, rng):
    names = []
    seen = set()
    while len(names) < count:
        candidate = random_name(rng)
        if candidate not in seen:
            seen.add(candidate)
            names.append(candidate)
    return names
