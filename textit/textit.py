import typing

import aiohttp

from .api import make_request
from .types import exceptions
from .types.base import APIMethod
from .types.numeral import *
from .types.speller import *
from .types.word import *
from .utils import generate_payload, choose_response


class TextIT:
    def __init__(self, session: aiohttp.ClientSession = None):
        self._session = session

    @property
    def session(self) -> typing.Optional[aiohttp.ClientSession]:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def correct(self, word: str) -> typing.List[WordObject]:
        """
        Displays possible options for correcting an error when entering a word

        :param word: misspelled word (e.g. очепатка)
        :type word: str
        :return: variants of the correct word (e.g., опечатка)
        :rtype: typing.List[WordObject]
        :raises ALotOfWords: if more than one word was specified
        """
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        payload = generate_payload(func=APIMethod.CORRECT, pars={"word": word})
        response = await make_request(self.session, payload)
        return [WordObject(**resp) for resp in response]

    async def hint(self, text: str) -> typing.List[WordObject]:
        """
        Suggests the next word for the previously entered text

        :param text: up to 30 of the last entered text characters (e.g. я иду д)
        :type text: str
        :return: list of hint-words (e.g. домой)
        :rtype: typing.List[WordObject]
        :raises ToLongText: if the text is longer than 30 characters
        """
        if len(text) > 30:
            raise exceptions.ToLongText("Maximum length of text is 30 characters")
        payload = generate_payload(func=APIMethod.HINT, pars={"text": text})
        response = await make_request(self.session, payload)
        return [WordObject(**word) for word in response]

    async def numeral(
        self,
        number: int,
        word: str,
        case: WordCase = WordCase.NOMINATIVE,
        direct: NumeralType = NumeralType.COUNT,
        reduce: bool = False,
        format: NumeralFormat = NumeralFormat.STRING,
    ) -> NumeralObject:
        """
        Generates a text representation of a number

        :param number: a number to convert to a string (e.g. 1234)
        :type number: int
        :param word: object name (e.g. рубль)
        :type word: str
        :param case: case of a word. Default - WordCase.NOMINATIVE
        :type case: WordCase
        :param direct: number type (count, order, union). Default - NumeralType.COUNT
        :type direct: NumeralType
        :param reduce: sign: reduce orders (e.g., тыс., млн so on). Default - False
        :type reduce: bool
        :param format: format of a word (Number, Number-string, string). Default - NumeralFormat.STRING
        :type format: NumeralFormat
        :return: numeral object with number and text (e.g., одна тысяча двести тридцать четыре рубля)
        :rtype: NumeralObject
        :raises NegativeNumber: if the number is negative
        :raises ALotOfWords: if more than one word was specified
        """

        if number < 0:
            raise exceptions.NegativeNumber("Negative number aren't allowed")
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        payload = generate_payload(
            func=APIMethod.NUMERAL,
            pars={
                "number": number,
                "word": word,
                "case": case,
                "direct": direct,
                "reduce": reduce,
                "format": format,
            },
        )
        response = await make_request(self.session, payload)
        probable_response = choose_response(response)
        return NumeralObject(**probable_response)

    async def speller(self, text: str, add_correct: bool = False) -> SpellerObject:
        """
        Checks the text for errors

        :param text: up to 10,000 text characters for check (e.g. Пример тектса)
        :type text: str
        :param add_correct: add word correction suggestions. Default - False
        :type add_correct: bool
        :return: speller object with founded and error and position in text (e.g. тектса and 8)
        :rtype: SpellerObject
        :raises ToLongText: if the text is longer than 10000 characters
        """
        if len(text) > 10000:
            raise exceptions.ToLongText("Maximum length of text is 10000 characters")
        payload = generate_payload(func=APIMethod.SPELLER, pars={"text": text})
        response = await make_request(self.session, payload)
        if add_correct:
            response["correct"] = await self.correct(response["word"])
        return SpellerObject(**response)

    async def word_info(self, word: str) -> WordObject:
        """
        Method original name - "word".
        Returns parts of a word (root, prefix, etc.) and morphological features (part, number, gender, case, etc.).
        Also returns the lemma (normal form) of the word.

        :param word: one word about which we want to get information
        :type word: str
        :return: word object with information
        :rtype: WordObject
        :raises ALotOfWords: if more than one word was specified
        """
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        payload = generate_payload(func=APIMethod.WORD, pars={"word": word})
        response = await make_request(self.session, payload)
        probable_response = choose_response(response)
        return WordObject(**probable_response)

    async def set_form(
        self,
        word: str,
        part: typing.Optional[WordPart] = None,
        number: typing.Optional[WordNumber] = None,
        gender: typing.Optional[WordGender] = None,
        case: typing.Optional[WordCase] = None,
        tense: typing.Optional[WordTense] = None,
        person: typing.Optional[WordPerson] = None,
        form: typing.Optional[WordForm] = None,
        kind: typing.Optional[WordKind] = None,
        add_info: bool = False,
    ) -> WordObject:
        """
        Returns the original word in the desired word form (number, gender, case, etc.)

        :param word: one word which form we want to set
        :type word: str
        :param part: required part of speech
        :type part: typing.Optional[WordPart]
        :param number: word number
        :type number: typing.Optional[WordNumber]
        :param gender: word gender
        :type gender: typing.Optional[WordGender]
        :param case: word case
        :type case: typing.Optional[WordCase]
        :param tense: word tense (verb)
        :type tense: typing.Optional[WordTense]
        :param person: word person (verb)
        :type person: typing.Optional[WordPerson]
        :param form: word form
        :type form: typing.Optional[WordForm]
        :param kind: word kind (verb)
        :type kind: typing.Optional[WordKind]
        :param add_info: add info about this word. Default - false
        :type add_info: bool
        :return: word object in required form
        :rtype: WordObject
        :raises ALotOfWords: if more than one word was specified
        """
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        payload = generate_payload(
            func=APIMethod.SET_FORM,
            pars={
                "word": word,
                "part": part,
                "number": number,
                "gender": gender,
                "case": case,
                "tense": tense,
                "person": person,
                "form": form,
                "kind": kind,
            },
        )
        response = await make_request(self.session, payload)
        probable_response = choose_response(response)
        if add_info:
            info = await self.word_info(probable_response["word"])
            probable_response.update(**info.__dict__)
        return WordObject(**probable_response)

    async def cognate(self, word: str) -> typing.List[WordObject]:
        """
        Returns a list of words of the same root

        :param str word: one word for which we want to get the same root words (e.g. делать)
        :type word: str
        :return: list of words with the same root (word and its part of speech) (e.g. дело and WordPart.NOUN)
        :rtype: typing.List[WordObject]
        :raises ALotOfWords: if more than one word was specified
        """
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        payload = generate_payload(func=APIMethod.COGNATE, pars={"word": word})
        response = await make_request(self.session, payload)
        return [WordObject(**resp) for resp in response]

    async def synonym(self, word: str) -> typing.List[WordObject]:
        """
        Returns a list of synonyms

        :param str word: one word for which we want to get synonyms (e.g. ёмкость)
        :type word: str
        :return: list of synonyms (word and its part of speech) (e.g. сосуд and WordPart.NOUN)
        :rtype: typing.List[WordObject]
        :raises ALotOfWords: if more than one word was specified
        """
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        payload = generate_payload(func=APIMethod.SYNONYM, pars={"word": word})
        response = await make_request(self.session, payload)
        return [WordObject(**resp) for resp in response]

    async def lat_to_cyr(self, text: str) -> str:
        """
        Returns the Cyrillic text converted from the text typed in the Latin keyboard layout

        :param text: up to 10,000 text characters for convert (e.g. Ghbvth ntrcnf)
        :type text: str
        :return Cyrillic text (e.g. Пример текста)
        :rtype: str
        :raises ToLongText: if the text is longer than 10000 characters
        """

        if len(text) > 10000:
            raise exceptions.ToLongText("Maximum length of text is 10000 characters")
        payload = generate_payload(func=APIMethod.LAT_TO_CYR, pars={"text": text})
        response = (await make_request(self.session, payload))[0]
        return response.get("text")
