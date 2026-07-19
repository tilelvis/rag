"""Uniqueness tracker to prevent duplicate content across the dataset."""


class UniquenessTracker:
    def __init__(self):
        self.used_ids = set()
        self.used_openings = set()
        self.used_closings = set()
        self.used_scriptures = set()
        self.used_names = set()
        self.used_first_sentences = set()

    def add_id(self, doc_id):
        self.used_ids.add(doc_id)

    def add_opening(self, text):
        opening = text[:60].strip().lower()
        self.used_openings.add(opening)

    def add_closing(self, text):
        closing = text[-60:].strip().lower()
        self.used_closings.add(closing)

    def add_scripture(self, scripture):
        self.used_scriptures.add(scripture)

    def add_name(self, name):
        self.used_names.add(name)

    def add_first_sentence(self, sentence):
        self.used_first_sentences.add(sentence.strip().lower()[:80])
