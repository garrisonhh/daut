# Graphs with Graphemes: Exploring Methods for German Document Analysis

Garrison Hinson-Hasty

## Introduction

Deutsch Analysator mit umgekehrten Tries (DAUT) is a tool that analyzes a German text and picks out key words and phrases. It is able to discern words and phrases that are the most relevant to the topic of the text, as well as those which are likely to be domain-specific language. Using this data, my project can determine associativity between different German texts. The goal of DAUT is to use methods that are simple, efficient, and acceptably accurate to perform these tasks.

## Context

My project is firmly in the field of Natural Language Processing, commonly known as NLP. NLP is the study of techniques to analyze and process large amounts of natural language data. Programs employing NLP use various metrics to extract tons of useful information from just simple text or audio. Some applications of NLP that many people encounter in their daily lives are with machine translation tools, customer service phone and chat bots, and AI assistants like Alexa or Siri.

Whether you agree with it or not, the capacity for understanding and generating natural language has often been stated to be a strong indicator of, or even equivalent to, intelligence. Alan Turing's 1950 paper, *Computing Machinery and Intelligence*, introduced the measurement of a machine's language capabilities, in terms of how human it appears, as the de facto standard for testing a machine's ability to "exhibit intelligent behavior" \[1\]. This test is now famously known as the Turing Test. Though it has remained controversial since its initial publishing, the cultural influence of the Turing test is undeniable -- it made waves in the study of artificial intelligence and has cemented a place for itself in pop culture.

The most important developments in NLP fall under the umbrella of the development of the ability to semantically analyze language. NLP can be considered to be a specialized application of AI, so AI techniques for modeling information have proven to be incredibly useful in constructing an understanding of language. Two considerable challenges with language are the number of irregularities and sheer amount of possible variation in construction that languages tend to encompass. Due to this, it is generally infeasible to encode every possible irregularity of a given language, so programs must be smart in the way they internally represent data. By using specialized data structures and algorithms, and admitting that perfection is not an achievable goal, computers can settle for "pretty good".

Some common examples of everyday, useful programs that do approximating language analysis are handwriting recognizers and spell checkers, which DAUT inherits much of its ideas from. One such project written in 1961 and published in 1962, whose author believes to be the first of its kind, was a handwriting recognizer with a built-in spell checking feature \[2\]. Since the program was imperfect in its recognization of letters, it would search a limited list of words in order to attempt to correct itself. More sophisticated spell checkers later on would use basic statistical analysis of frequency and approximate word matching to perform their task \[3\]. DAUT uses methods extremely similar to these, though in slightly different ways.

In the past few decades, deep learning has become the fancy, buzzwordy way of creating convincing "pretty good" representations of language. The only difference between deep learning and traditional AI is that programs use opaque mathematical techniques to create and modify an understanding of the world where the programmer only has indirect control rather than directly implementing algorithms themselves. While neural networks are often fantastic at approximation problems, they are not without downsides. One downside is the inability to analyze or understand internal neural net functionality; they are often referred to colloquially as "black boxes". Another is the heavy computational load and relatively slow performance of complex deep learning applications. A large amount of time and energy is spent on the logistics alone of training large neural nets, such as Google Translate \[4\]. DAUT is able to sidestep these downsides by simply avoiding deep learning altogether.

## Methods

My project uses an approximate string matching technique coupled with analysis of word length, part of speech, and frequency to extract information from German documents. Instead of using the prevailing heavier and slower machine learning method, it uses a custom data structure and traditional machine learning on corpora to make probabilistic judgements of words. Though this method is simple, its accuracy is on par with deep learning methods: in part-of-speech identification on a previously tagged corpus, DAUT was able to achieve 70% accuracy, with spaCy, a state-of-the-art NLP library, achieving 71% \[5\].

DAUT's methodology is based on incredibly simple hypotheses, the first being that more common words in any text tend to be more relevant to the topic than less common words, the second being that longer words tend to be more specific and relevant to the domain or subject matter of the text, and the third being that different linguistic constructions are more important to the meaning of a sentence than others. By performing basic analysis of word frequency, length, and sentence structure, the program could then identify topical or domain specific words and phrases.

One of the main challenges in implementing DAUT for a language like German is the non-analytic nature of the grammar. German is full of conjugation and declension, which means that a program counting word frequency and identifying parts of speech needs to be able to handle this variation intelligently.

Another challenge when identifying th
       Remove files matching pathspec from the index, or from the working tree and the index. git rm will not remove a file from just your working directory. (There
       is no option to remove a file only from the working tree and yet keep it in the index; use /bin/rm if you want to do that.) The files being removed have to be
       identical to the tip of the branch, and no updates to their contents can be staged in the index, though that default behavior can be overridden with the -f
       option. When --cached is given, the staged content has to match either the tip of the branch or the file on disk, allowing the file to be removed from just
       the index. When sparse-checkouts are in use (see git-sparse-checkout(1)), git rm will only remove paths within the sparse-checkout patterns.


DAUT has answers for each of these challenges. Using approximate matching techniques in the same lineage as spell checkers, DAUT is often able to find forms of words that are close enough to the original word. This is used both in guessing parts of speech and counting the frequency of words in a document. DAUT uses a reversed Trie data structure, a type of tree data structure that branches on letters, to naturally group words with similar forms together in order to make decent guesses at what part of speech they are. The reversed Trie and approximate matching in conjunction are able to tackle the challenges of German's conjugation and declension as well as storing only a portion of the German lexicon.

After figuring out the parts of speech of words, DAUT uses that data to identify noun and verb phrases. Noun phrases are the group of an article and any adjectives with a noun, such as 'the red dog', and verb phrases in DAUT are noun phrases alongside verbs, such as 'the red dog runs'. This example could be picked out of a larger sentence, such as 'the red dog runs alongside the car for two miles.' DAUT then will heuristically rate the words or phrases picked out of a document by two metrics, 'topicality' and 'uniqueness'. 'Topicality' refers to the relevancy of a given word or phrase to the topic of the document, and is identified by the most common and longest words and phrases. 'Uniqueness' refers to words and phrases which are uncommon, but long. 'Unique' is analogous to how specific the words are to the field, or domain, of a document. Nouns and verbs, the centers of noun and verb phrases and the objects of discussion, are also given slightly more weight than helper parts of speech like adjectives or adverbs.

## Discussion

Using an article from the German Newspaper *Deutsche Welle* \[6\], I used DAUT to extract the top ten topical and unique words and phrases:

topical words | topical phrases | unique words | unique phrases
--- | --- | --- | ---
Maljartschuk | literaturtage stehen | zusammenschließen | Journalistin arbeitete
Ukraine | veröffentlichten Roman zeichnen | Militärexpertin | spricht engagiert
Literaturpreis | erhält die schriftstellerin den usedomer Literaturpreis | Journalistin | veröffentlichten Roman zeichnen
russische | Journalistin arbeitete | repräsentieren | literaturtage stehen
Literaturtage | zeichnen die usedomer literaturtage | rechtfertigen | stärke zeigte
Deutsche | Putin schürt | Euromaidan | auch kunstschaffende einblicke geben
schreibt | Putins krieg nach der einnahme der ukraine aufhören | entschuldigt | zählt die jahreszahlen
Ukrainisch | ein gegenschlag russlands vermieden | unterstützen | ein gegenschlag russlands vermieden
gefragt | Literaturpreis habe sie ein paar wochen vor der russischen invasion erfahren | fortzusetzen | zu verpassen droht
sagt | spricht engagiert | Jahreszahlen | Putin schürt

As the topical words and phrases imply, this article is about a Ukrainian journalist named Tanja Maljartschuk who won a literature prize. Given the present context of the war between Russia and Ukraine, Putin and the war are also topics discussed throughout the article.

DAUT is quite successful in identifying topical words. The keywords that the Deutsche Welle manually identified for the article were "Tanja Maljartschuk," "Ukraine," and "Literatur," which are extremely close to the most highly rated topical words from DAUT. Many of the most unique words are also quite useful, "Militärexpertin," "Journalistin," and "Euromaidan" are words that are domain-specific to the topics of the article, and words like "zusammenschließen" and "rechtfertigen" are compound and relatively uncommon German verbs that would be likely to trip up a non-native German speaker.

An area for DAUT to improve is the consistency in identifying phrases. In general, many of the phrases are still quite useful, "veröffentlichten Roman zeichnen" and "erhält die Schriftstellerin den usedomer Literaturpreis" in particular are coherent phrases that clearly have relevance to the themes of the article. However, "Literaturtage stehen" is not a particulary coherent verb phrase. German's free word order and sentences with many clauses is a challenge which makes it harder for DAUT to reliably identify noun-verb relationships. Noticeable false positives like this are, however, not a unique problem to programs like DAUT -- state-of-the-art deep learning models also struggle with this.

DAUT uses the TIGER corpus \[7\]to generate the reverse Trie used by its algorithm. The size, breadth, and content of the corpus thus affects the output. The TIGER corpus is taken from newspaper text, and it is possible that this biases DAUT's abilities towards analyzing newspapers.

## Conclusion and Future Work

The techniques used in this project have many potential applications. A common problem faced by a speaker of any language is acquiring the necessary vocabulary when reading about a new topic. Some common examples of this are reading papers written for experts in a field, or books from a century ago. Without knowledge of the specific vocabulary being used, the confused reader has to continuously stop, look up a dictionary definition, and find their place again. For language learners, this problem is not just restricted to old books and esoteric academic studies, it's everywhere. Being forced to stop and google constantly results in a much less fluid reading experience, making it much more challenging for readers to keep track of the context and narrative of a given text.

DAUT is able to solve this problem by augmenting translation and dictionary tools. For language speakers, it can pick out domain specific words and phrases and fetch definitions for them before they are needed. For language learners and educators, it can pick out the words and phrases that it thinks will be most likely to be a challenge, and provide definitions and translations.

Another useful application is the ability the program has to condense the information in a text document into a shorter set of the most important words and phrases. This list of keywords can be used as a sort of semantic summary of a document. This is extraordinarily useful for search engines in general, which can use the data to accurately categorize and find stored documents (such as webpages).

DAUT can also use its analysis to identify how related two documents are. Being able to automatically group related material together by topic is useful in any context where classification or providing accurate suggestions is useful. Some good examples would be academic journals, media sources, and website aggregators.

By creating user-facing applications, DAUT will also be able to benefit from accumulating feedback. The usefulness of the program is in its ability to serve human language speakers, so constructive criticism from end users would allow DAUT to grow in the right direction.

## Sources

1. Turing, Alan M. ‘Computing Machinery and Intelligence’. _Parsing the Turing Test: Philosophical and Methodological Issues in the Quest for the Thinking Computer_. Robert Epstein, Gary Roberts, Grace Beber. Dordrecht: Springer Netherlands, 2009. 23–65. Web.
2. Earnest, L. D.. “Machine Recognition of Cursive Writing.” _IFIP Congress_ (1962).
3. Li, Mu. ‘Exploring Distributional Similarity Based Models for Query Spelling Correction’. _Proceedings of the 21st International Conference on Computational Linguistics and the 44th Annual Meeting of the Association for Computational Linguistics_. USA: Association for Computational Linguistics, 2006. 1025–1032. Web. ACL-44.
4. Chen, Jiasi, Xukan Ran. ‘Deep Learning With Edge Computing: A Review’. _Proceedings of the IEEE_ 107.8 (2019): 1655–1674. Web.
5. Explosion. “spaCy: Industrial-Strength Natural Language Processing in Python.” _spaCy_, spacy.io. Accessed 30 Apr. 2022.
6. Deutsche Welle (www.dw.com). “Tanja Maljartschuk erhält Usedomer Literaturpreis.” _Deutsche Welle_, 2022, www.dw.com/de/tanja-maljartschuk-erh%C3%A4lt-usedomer-literaturpreis/a-61620775.
7. Brants, Sabine. ‘TIGER: Linguistic Interpretation of a German Corpus’. _Research on Language and Computation_ 2.4 (2004): 597–620. Web.