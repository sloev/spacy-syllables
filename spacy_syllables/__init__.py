# -*- coding: utf-8 -*-

from spacy.tokens import Token
import pyphen


class SpacySyllables:
    name = "syllables"

    def __init__(self, nlp, lang=None):
        """
        nlp: an instance of spacy
        lang: can be any format like : ["en", "en-us", "en_us", "en-US", ...]
        usage:
            nlp = spacy.load("en_core_web_sm")
            syllables = SpacySyllables(nlp)
            nlp.add_pipe(syllables, after="tagger")
        """
        lang = lang or nlp.lang
        lang, *country_code = lang.lower().replace("-", "_").split("_")

        if country_code:
            country_code = country_code[0].upper()
            lang = f"{lang}_{country_code}"
        try:
            self.syllable_dic = pyphen.Pyphen(lang=lang)
        except KeyError:
            raise NotImplementedError(
                f"SpacySyllables has no support for language: {lang}"
            )

        Token.set_extension("syllables", default=None, force=True)
        Token.set_extension("syllables_count", default=None, force=True)

    def syllables(self, word):
        if word.isalpha():
            return self.syllable_dic.inserted(word.lower()).split("-")
        return None

    def __call__(self, doc):
        for token in doc:
            syllables = self.syllables(token.text)
            if syllables:
                token._.set("syllables", syllables)
                token._.set("syllables_count", len(syllables))
        return doc
