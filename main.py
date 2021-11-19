#!/usr/bin/env python3
import os
import sys
from document import Document
from classifier import Classifier

def main():
    with open("files/art3.txt", "r") as f:
        doc = Document("name", f.read())

    words = doc.best_words(30)
    phrases = doc.best_phrases(30)

    print("\n--- words ---")

    for word in words:
        print(f"{word.word:70}{word.topicality():10.2f}")

    print("\n--- phrases ---")

    for phrase in phrases:
        print(f"{str(phrase):70}{phrase.topicality():10.2f}")

if __name__ == "__main__":
    main()
