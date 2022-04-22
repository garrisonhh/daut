#!/usr/bin/env python3
import os
import sys
from document import Document
from classifier import Classifier

TEMPLATE = ""

def init():
    global TEMPLATE

    Classifier.load()

    with open("template.html", "r") as f:
        TEMPLATE = f.read()

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

    print("=== document 1 ===");

    doc = documents[0]
    words = doc.best_words(30)
    phrases = doc.best_phrases(30)

    print("\n--- topical words ---")

    for word in words:
        print(f"{word.word:70}{word.topicality():10.2f}")

    print("\n--- topical phrases ---")

    for phrase in phrases:
        print(f"{str(phrase):70}{phrase.topicality():10.2f}")

def make_html():
    doc = Document.from_file("files/art2.txt")
    html = TEMPLATE

    # construct html body
    body = f"<h1>{doc.title}</h1>"

    for paragraph in doc.text.splitlines():
        if len(paragraph):
            body += f"<p>{paragraph}</p>"

    html = html.replace("%DOCUMENT%", body)

    # construct wortliste
    vocab = "<h2>words</h2>"

    for word in doc.best_words(10):
        vocab += f"<p>{word.word}</p>"

    vocab += "<h2>phrases</h2>"

    for phrase in doc.best_phrases(10):
        vocab += f"<p>{str(phrase)}</p>"

    html = html.replace("%VOCAB%", vocab)

    with open("demo.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    init()
    make_html() # main()
