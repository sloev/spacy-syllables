import pytest
import spacy
from spacy_syllables import SpacySyllables


def test_simple_english():
    nlp = spacy.load("en_core_web_sm")
    syllables = SpacySyllables(nlp)
    nlp.add_pipe(syllables, after="tagger")

    doc = nlp("This is a terribly long sentence. And i dont care")

    print(nlp.pipe_names)
    assert nlp.pipe_names == ["tagger", "syllables", "parser", "ner"]

    data = [(token.text, token._.syllables, token._.syllables_count) for token in doc]
    print(data)

    assert data == [
        ("This", ["this"], 1),
        ("is", ["is"], 1),
        ("a", ["a"], 1),
        ("terribly", ["ter", "ri", "bly"], 3),
        ("long", ["long"], 1),
        ("sentence", ["sen", "tence"], 2),
        (".", None, None),
        ("And", ["and"], 1),
        ("i", ["i"], 1),
        ("do", ["do"], 1),
        ("nt", ["nt"], 1),
        ("care", ["care"], 1),
    ]


def test_english_with_language_code_formats():
    nlp = spacy.load("en_core_web_sm")
    syllables = SpacySyllables(nlp, lang="en")

    nlp = spacy.load("en_core_web_sm")
    syllables = SpacySyllables(nlp, lang="en_us")

    nlp = spacy.load("en_core_web_sm")
    syllables = SpacySyllables(nlp, lang="en-us")

    nlp = spacy.load("en_core_web_sm")
    syllables = SpacySyllables(nlp, lang="en_US")

    nlp = spacy.load("en_core_web_sm")
    syllables = SpacySyllables(nlp, lang="en-US")

    nlp = spacy.load("en_core_web_sm")
    syllables = SpacySyllables(nlp, lang="en_Us")

    nlp = spacy.load("en_core_web_sm")
    syllables = SpacySyllables(nlp, lang="eN_Us")


def test_english_with_unsupported_country_code_fails():
    with pytest.raises(NotImplementedError):
        nlp = spacy.load("en_core_web_sm")
        syllables = SpacySyllables(nlp, lang="lol-cat")
