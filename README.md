![spacy syllables](https://raw.githubusercontent.com/sloev/spacy-syllables/master/header.jpg)

# Spacy Syllables

[![Build Status](https://travis-ci.com/sloev/spacy-syllables.svg?branch=master)](https://travis-ci.com/sloev/spacy-syllables) [![Latest Version](https://img.shields.io/pypi/v/spacy-syllables.svg)](https://pypi.python.org/pypi/spacy-syllables) [![Python Support](https://img.shields.io/pypi/pyversions/spacy-syllables.svg)](https://pypi.python.org/pypi/spacy-syllables)

<a href="https://www.buymeacoffee.com/sloev" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-pink.png" alt="Buy Me A Coffee" height="51px" width="217px"></a>

A [spacy 2+ pipeline component](https://spacy.io/universe/category/pipeline) for adding multilingual syllable annotation to tokens. 

* Uses well established [pyphen](https://github.com/Kozea/Pyphen) for the syllables.
* Supports [a ton of languages](https://github.com/Kozea/Pyphen/tree/master/pyphen/dictionaries)
* Ease of use thx to the awesome pipeline framework in spacy

## Install

```bash
$ pip install spacy_syllables
```

which also installs the following dependencies:

* spacy = "^2.2.3"
* pyphen = "^0.9.5"

## Usage

The [`SpacySyllables`](spacy_syllables/__init__.py) class autodetects language from the given spacy nlp instance, but you can also override the detected language by specifying the `lang` parameter during instantiation, see how [here](tests/test_all.py).

### Normal usecase

```python

import spacy
from spacy_syllables import SpacySyllables

nlp = spacy.load("en_core_web_sm")

nlp.add_pipe("syllables", after="tagger")

assert nlp.pipe_names == ["tok2vec", "tagger", "syllables", "parser", "ner", "attribute_ruler", "lemmatizer"]

doc = nlp("terribly long")

data = [(token.text, token._.syllables, token._.syllables_count) for token in doc]

assert data == [("terribly", ["ter", "ri", "bly"], 3), ("long", ["long"], 1)]

```

more examples in [tests](tests/test_all.py)

## Migrating from spacy 2.x to 3.0

In spacy 2.x, spacy_syllables was originally added to the pipeline by instantiating a [`SpacySyllables`](spacy_syllables/__init__.py) object with the desired options and adding it to the pipeline: 

```python
from spacy_syllables import SpacySyllables

syllables = SpacySyllables(nlp, "en_US")

nlp.add_pipe(syllables, after="tagger")
```

In spacy 3.0, you now add the component to the pipeline simply by adding it by name, setting custom configuration information in the `add_pipe()` parameters:
```python
from spacy_syllables import SpacySyllables

nlp.add_pipe("syllables", after="tagger", config={"lang": "en_US"})
```



In addition, the default pipeline components have changed between 2.x and 3.0; please make sure to update any asserts you have that check for these.
e.g.:

spacy 2.x:
```python
assert nlp.pipe_names == ["tagger", "syllables", "parser", "ner"]
```

spacy 3.0:
```python
assert nlp.pipe_names == ["tok2vec", "tagger", "syllables", "parser", "ner", "attribute_ruler", "lemmatizer"]
```

## Dev setup / testing

we are using
* [poetry](https://python-poetry.org/) for the package
* [nox](https://github.com/theacodes/nox) for the tests
* [pyenv](https://github.com/pyenv/pyenv) for specifying python versions for nox tests

### install

* [install pyenv](https://github.com/pyenv/pyenv#installation)
* [install poetry](https://python-poetry.org/docs/#installation)

then install the dev package and pyenv versions

```bash
$ poetry install
$ poetry run nox --session install_pyenv_versions
```

### run tests

```bash
$ poetry run nox
```
