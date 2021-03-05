# -*- coding: utf-8 -*-
from typing import Optional
from spacy.tokens import Token, Doc
from spacy.language import Language
import pyphen


@Language.factory(
    "syllables",
    assigns=["token._.syllables", "token._.syllables_count"],
    default_config={"lang": None},
    requires=["token.text"],
)
def make_spacysyllables(nlp: Language, name: str, lang: Optional[str]):
    return SpacySyllables(nlp, name, lang=lang)


class SpacySyllables:
    def __init__(
        self, nlp: Language, name: str = "syllables", lang: Optional[str] = None
    ):

        """
        nlp: an instance of spacy
        name: defaults to "syllables".
        lang: Optional, can be any format like : ["en", "en-us", "en_us", "en-US", ...]
              By default, it uses the language code of the model loaded.
        usage:
            nlp = spacy.load("en_core_web_sm")
            nlp.add_pipe("syllables", after="tagger", config={"lang": "en_US"})
        """
        self.name = name
        lang = lang or nlp.lang
        lang, *country_code = lang.lower().replace("-", "_").split("_")
        if country_code:
            country_code = country_code[0].upper()
            lang = f"{lang}_{country_code}"
        elif lang == "en":
            lang = "en_US"
        elif lang == "de":
            lang = "de_DE"
        elif lang == "pt":
            lang = "pt_PT"

        try:
            self.syllable_dic = pyphen.Pyphen(lang=lang)
        except KeyError:
            raise NotImplementedError(
                f"SpacySyllables has no support for language: {lang}"
            )

        Token.set_extension("syllables", default=None, force=True)
        Token.set_extension("syllables_count", default=None, force=True)

    def syllables(self, word: str):
        if word.isalpha():
            return self.syllable_dic.inserted(word.lower()).split("-")
        return None

    def __call__(self, doc: Doc):
        for token in doc:
            syllables = self.syllables(token.text)
            if syllables:
                token._.set("syllables", syllables)
                token._.set("syllables_count", len(syllables))
        return doc
