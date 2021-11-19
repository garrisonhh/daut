import re
from time import time
from dataclasses import dataclass
from nltk.tokenize import sent_tokenize

from classifier import *

MAX_PHRASE_VALUE = 2 # max 'valuable' words per phrase
EXCUSABLE_DIFFERING_POSTFIX = 3 # max ignorable postfix len when comparing words

VALUABLE_POS = ("NOUN", "VERB")
PREFIX_POS = ("DET", "ADJ", "ADV", "ADP")

def clauses(text):
    return re.split(r"(?:[,.:;]\W)|(?:\s-\s)", text)

def word_iter(text):
    for match in re.finditer(r"\w+", text):
        yield match[0]

@dataclass
class WordRecord:
    word: str
    folded: str

    pos: str = None
    closed: bool = False
    freq: int = 1

    def __post_init__(self):
        self.pos = Classifier.inst.classify(self.word)
        self.closed = self.folded in Classifier.inst.closed_words

    def similar_to(self, other):
        if self.folded == other.folded:
            # exactly equivalent
            return True

        if self.closed or other.closed:
            return False

        # both open classed words, compare the size of the differing endings
        max_len = len(self.folded)
        min_len = len(other.folded)
        max_index = 0

        if max_len < min_len:
            max_len, min_len = min_len, max_len

        for i in range(min_len):
            if self.folded[i] != other.folded[i]:
                break

            max_index = i

        return (max_len - max_index) <= EXCUSABLE_DIFFERING_POSTFIX

    def merge(self, other):
        if len(other.folded) < len(self.folded):
            self.word = other.word
            self.folded = other.folded

        if self.freq < other.freq:
            self.pos = other.pos
            self.closed = other.closed

        self.freq += other.freq

    def is_valuable(self):
        return self.pos in VALUABLE_POS

    def uniqueness(self):
        return (len(self.folded) / self.freq) * rate_pos(self.pos)

    def topicality(self):
        return len(self.folded) * self.freq * rate_pos(self.pos)

class WRTrieNode:
    def __init__(self):
        self.branches = {}
        self.record = None

    def put(self, record, index = 0):
        if index == len(record.folded):
            # add record to this node
            if self.record:
                self.record.merge(record)
            else:
                self.record = record
        elif self.record and self.record.similar_to(record):
            # merge similar records
            self.record.merge(record)
        else:
            # continue down branch
            if record.folded[index] not in self.branches:
                self.branches[record.folded[index]] = WRTrieNode()

            self.branches[record.folded[index]].put(record, index + 1)

    def find_closest(self, record, index = 0):
        # match found
        if index == len(record.folded) \
          or (self.record and self.record.similar_to(record)):
            return self.record

        # no possible match
        if record.folded[index] not in self.branches:
            return None

        # find a possible match down branch
        return self.branches[record.folded[index]].find_closest(
            record, index + 1
        )

    def extract(self):
        if self.record:
            yield self.record

        for node in self.branches.values():
            yield from node.extract()

class WRTrie:
    """
    use to turn a list of records into a list of unique records, using the
    WordRecord.similar_to() function

    note to self: do NOT add a put() function, records MUST be ordered by
    ascending length as of now for the expected result
    """
    def __init__(self, records):
        self.root = WRTrieNode()

        for record in sorted(records, key = lambda rec: len(rec.folded)):
            self.root.put(record)

    def find_closest(self, record):
        return self.root.find_closest(record)

    def extract(self):
        return self.root.extract()

@dataclass
class PhraseRecord:
    stringified: str
    records: tuple[WordRecord]

    hashable: tuple[int] = None
    freq: int = 1

    def __post_init__(self):
        self.hashable = tuple(
            id(rec)
            for rec in self.records
            if not rec.closed
        )

    def merge(self, other):
        if len(other.stringified) < len(self.stringified):
            self.stringified = other.stringified

        self.freq += other.freq

    def uniqueness(self):
        avg_u = sum(map(WordRecord.uniqueness, self.records))
        avg_u /= len(self.records)

        return avg_u * self.freq

    def topicality(self):
        avg_t = sum(map(WordRecord.topicality, self.records))
        avg_t /= len(self.records)

        return avg_t * self.freq

    def __repr__(self):
        return f"PhraseRecord(\"{self.stringified}\", freq={self.freq})"

    def __str__(self):
        return self.stringified

class Document:
    def __init__(self, title, text):
        t = time()

        self.title = title
        self.wrtrie = None
        self.phrase_records = {}

        self.load_text(text)

        t = time() - t
        print(f"processed text \"{self.title}\" in {t:.2f}s")

    def load_text(self, text):
        """
        load rough list of WordRecords and rough list of PhraseRecords from
        the sentencized text
        """
        word_records = {} # folded => WordRecord
        phrases = [] # list of tuples of (word, record)

        for clause in clauses(text):
            clause_records = [] # tuple of (word, record)

            # log individual words
            for word in word_iter(clause):
                folded = word.casefold()

                # count words
                if folded in word_records:
                    word_records[folded].freq += 1
                else:
                    word_records[folded] = WordRecord(word, folded)

                # regularize word representation
                if word_records[folded].pos == "NOUN":
                    word = word.title()
                else:
                    word = folded

                clause_records.append((word, word_records[folded]))

            # extract phrases from sentence
            for i in range(len(clause_records)):
                # phrase should stem from a valuable word pos
                if not clause_records[i][1].is_valuable():
                    continue

                phrase = []

                # grab potentially related non-valuable pre-phrase words
                j = i - 1

                while j >= 0 and clause_records[j][1].pos in PREFIX_POS:
                    phrase.insert(0, clause_records[j])

                    j -= 1

                # generate phrase by adding words from clause until
                # MAX_PHRASE_VALUE valuable words are reached.
                value = 0
                j = i

                while value < MAX_PHRASE_VALUE and j < len(clause_records):
                    phrase.append(clause_records[j])

                    if clause_records[j][1].is_valuable():
                        value += 1

                        if value > 1:
                            phrases.append(tuple(phrase))

                    j += 1

        """
        collapse generated words and phrases into only their unique records
        using a WRTrie

        TODO use levenshtein distance algorithm for searching the trie?

        may be able to do something similar for phrases as well?
        """
        self.wrtrie = WRTrie(word_records.values())

        for phrase in phrases:
            record = PhraseRecord(
                " ".join(word for word, _ in phrase),
                tuple(self.wrtrie.find_closest(rec) for _, rec in phrase)
            )

            if record.hashable in self.phrase_records:
                self.phrase_records[record.hashable].merge(record)
            else:
                self.phrase_records[record.hashable] = record

    def best_words(self, n):
        return list(filter(
            lambda w: not w.closed,
            sorted(
                self.wrtrie.extract(),
                key = WordRecord.topicality,
                reverse = True
            )
        ))[:n]

    def best_phrases(self, n):
        return list(sorted(
            self.phrase_records.values(),
            key = PhraseRecord.topicality,
            reverse = True
        ))[:n]
