#!/usr/bin/env python3
import os
import sys
from document import Document, WordRecord, PhraseRecord
from classifier import Classifier

TEMPLATE = ""

def init():
    global TEMPLATE

    Classifier.load()

    with open("template.html", "r") as f:
        TEMPLATE = f.read()

def main():
    # run one of these!

    grab_phrases()
    # compare_documents()
    # make_md_table()
    # make_html()

# spits out some of the most topical words and phrases from a file
def grab_phrases():
    doc = Document.from_file("files/waeldern-grenze-ukraine.txt")
    words = doc.best_words(30)
    phrases = doc.best_phrases(30)

    print("\n--- topical words ---")

    for word in words:
        print(f"{word.word:70}{word.topicality():10.2f}")

    print("\n--- topical phrases ---")

    for phrase in phrases:
        print(f"{str(phrase):70}{phrase.topicality():10.2f}")

# compares different documents with each other
def compare_documents():
    documents = [
        Document.from_file("files/berlin-wahl.txt"),
        Document.from_file("files/pandemie.txt"),
        Document.from_file("files/sebastian-kurz.txt"),
    ]

    for i, doc in enumerate(documents):
        j = i + 1
        for doc2 in documents[j:]:
            print(f"{i} <-> {j}: {doc.compare(doc2) * 100:.2f}% similar")
            j += 1
p
# spits out a markdown ascii table for nice rendering
def make_md_table():
    doc = Document.from_file("files/tanja-maljartschuk.txt")

    # console output
    table = list(zip(
        ["topical words", *doc.best_words(10, topical=True)],
        ["topical phrases", *doc.best_phrases(10, topical=True)],
        ["unique words", *doc.best_words(10, topical=False)],
        ["unique phrases", *doc.best_phrases(10, topical=False)],
    ))

    print(*table[0], sep = ' | ')
    print(*(['---'] * 4), sep = ' | ')

    for row in table[1:]:
        strs = []
:
                strs.append(item.stringified)

        print(*strs, sep = ' | ')

# spits out a static single html file as a demo for web applications
def make_html():
    doc = Document.from_file("files/tanja-maljartschuk.txt")
    html = TEMPLATE

    # console output
    words = doc.best_words(10, topical=True)
    phrases = doc.best_phrases(10, topical=True)

    print("\n--- unique words ---")

    for word in words:
        print(f"{word.word:70}{word.uniqueness():10.2f}")

    print("\n--- unique phrases ---")

    for phrase in phrases:
        print(f"{str(phrase):70}{phrase.uniqueness():10.2f}")

    # construct html body
    body = f"<h1>{doc.title}</h1>"

    for paragraph in doc.text.splitlines():
        if len(paragraph):
            body += f"<p>{paragraph}</p>"

    html = html.replace("%DOCUMENT%", body)

    # construct wortliste
    vocab = "<h2>words</h2>"

    for word in words[:10]:
        vocab += f"<p>{word.word}</p>"

    vocab += "<h2>phrases</h2>"

    for phrase in phrases[:10]:
        vocab += f"<p>{str(phrase)}</p>"

    html = html.replace("%VOCAB%", vocab)

    with open("demo.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    init()
    main()
