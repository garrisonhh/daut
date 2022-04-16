#!/usr/bin/env python3
import os
import sys
from document import Document
from classifier import Classifier

def init():
    Classifier.load()

def main():
    documents = [
        Document.from_file("files/art1.txt"),
        Document.from_file("files/art2.txt"),
        Document.from_file("files/art3.txt"),
    ]

    for i, doc in enumerate(documents):
        j = i + 1
        for doc2 in documents[j:]:
            print(f"{i} <-> {j}: {doc.compare(doc2) * 100:.2f}% similar")
            j += 1

    return

    words = doc2.best_words(30)
    phrases = doc2.best_phrases(30)

    print("\n--- topical words ---")

    for word in words:
        print(f"{word.word:70}{word.topicality():10.2f}")

    print("\n--- topical phrases ---")

    for phrase in phrases:
        print(f"{str(phrase):70}{phrase.topicality():10.2f}")

if __name__ == "__main__":
    init()
    main()
