from time import time
from collections import Counter

# when intaking corpi, the words that don't need to be classified
CORPUS_IGNORE = ("PUNCT", "X", "NOUN", "PROPN")
# POS classes that have a fixed number of words
CLOSED_CLASSES = ("ADP", "AUX", "CCONJ", "DET", "PART", "PRON", "SCONJ")

def rate_pos(pos):
    ratings = {
        "NOUN": 1.5,
        "VERB": 1.25,
        "X": 1.0,
        "ADJ": 0.75,
        "ADV": 0.25,
        "NUM": 0
    }

    return ratings[pos] if pos in ratings else 0.5

class ClassifierNode:
    def __init__(self):
        self.branches = {}

        # when word ends here, associated data
        self.end = False
        self.pos_freq = Counter()

    def pos(self):
        return self.pos_freq.most_common(1)[0][0]

    def put(self, word, pos, index = 0):
        if index == len(word):
            if not self.end:
                self.end = True
                self.pos_freq[pos] += 1
        else:
            if word[index] not in self.branches:
                self.branches[word[index]] = ClassifierNode()

            self.branches[word[index]].put(word, pos, index + 1)

    # either finds the exact word, or makes its best guess based on other words
    # returns tuple of (word, was_guess)
    def classify(self, word, index = 0, last_pos = "X"):
        if self.end:
            # reached end of a stored word, record its pos
            maybe_pos = self.pos()

            if not (maybe_pos in CLOSED_CLASSES and index != len(word)):
                last_pos = maybe_pos

        if index == len(word):
            # reached end of word
            return (last_pos, not self.end)
        else:
            if word[index] in self.branches:
                # continue down tree
                return self.branches[word[index]].classify(
                    word, index + 1, last_pos
                )
            else:
                # end of branch, word still has characters
                return (last_pos, False)

    # iterator for (word, pos) tuples
    def extract(self, word = ""):
        if self.end:
            yield (word, self.pos())

        for letter, branch in sorted(self.branches.items()):
            yield from branch.extract(word + letter)

    def count(self):
        count = 1 if self.end else 0

        for branch in self.branches.values():
            count += branch.count()

        return count

class Classifier:
    inst = None # singleton instance

    """
    given a list of .conllu corpi, loads .casefold()ed words in and stores their
    part of speech data. words are stored in a Trie in reversed order, in order
    to associate them by their endings.
    """
    def __init__(self, corpi):
        cf_time = time()

        self.root = ClassifierNode()

        for corpus in corpi:
            self.load_corpus(corpus)

        self.closed_words = self._gen_closed_words()

        cf_time = time() - cf_time
        print(f"loaded {self.count()} words to classifier in {cf_time:.2f}s")

    # loads a .conllu file
    def load_corpus(self, filename):
        with open(filename, "r") as f:
            for line in f.readlines():
                line = line.strip()

                if line and line[0] != '#':
                    # classify word from this sentence
                    columns = line.split()

                    pos = columns[3]

                    if pos not in CORPUS_IGNORE:
                        word = columns[1]

                        self.root.put(word.casefold()[::-1], pos)

    # returns the list of known closed class words
    def _gen_closed_words(self):
        return [
            word[::-1]
            for word, pos in self.root.extract()
            if pos in CLOSED_CLASSES
        ]

    # will never produce PROPN, only NOUN
    def classify(self, word):
        if word[0].isdigit():
            return "NUM"

        classified, guessed = self.root.classify(word.casefold()[::-1])

        if (guessed or classified == 'X') and word.istitle():
            return "NOUN"

        return classified

    def print(self):
        for word, pos in self.root.extract():
            print(f"{word[::-1]}/{pos}", end = " ")

        print()

    def count(self):
        return self.root.count()

Classifier.inst = Classifier([
    "corpi/de_hdt-ud-train-a-1.conllu",
    "corpi/de_hdt-ud-train-a-2.conllu"
])
