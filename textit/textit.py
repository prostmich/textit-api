import typing

import aiohttp

from .api import make_request
from .types import exceptions
from .types.base import APIMethod
from .types.numeral import *
from .types.speller import *
from .types.word import *
from .utils import (
    generate_command,
    choose_response,
    generate_payload,
    get_func_list,
    sign_responses,
)


class TextIT:
    def __init__(self, session: aiohttp.ClientSession = None):
        self._session = session
        self.request = []

    @property
    def session(self) -> typing.Optional[aiohttp.ClientSession]:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def correct(
        self, word: str, immediately: bool = True
    ) -> typing.Optional[typing.List[WordObject]]:
        """
        Displays possible options for correcting an error when entering a word

        :param word: misspelled word (e.g. очепатка)
        :type word: str
        :param immediately: immediately send request
        :type immediately: bool
        :return: variants of the correct word (e.g., опечатка)
        :rtype: typing.Optional[typing.List[WordObject]]
        :raises ALotOfWords: if more than one word was specified
        """
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        command = generate_command(func=APIMethod.CORRECT, pars={"word": word})
        if not immediately:
            return self.request.append(command)
        response = await make_request(self.session, generate_payload(command))
        return [WordObject(**word) if word else None for word in response[0]]

    async def hint(
        self, text: str, immediately: bool = True
    ) -> typing.Optional[typing.List[WordObject]]:
        """
        Suggests the next word for the previously entered text

        :param text: up to 30 of the last entered text characters (e.g. я иду д)
        :type text: str
        :param immediately: immediately send request. Default - True
        :type immediately: bool
        :return: list of hint-words (e.g. домой)
        :rtype: typing.Optional[typing.List[WordObject]]
        :raises ToLongText: if the text is longer than 30 characters
        """
        if len(text) > 30:
            raise exceptions.ToLongText("Maximum length of text is 30 characters")
        command = generate_command(func=APIMethod.HINT, pars={"text": text})
        if not immediately:
            return self.request.append(command)
        response = await make_request(self.session, generate_payload(command))
        return [WordObject(**word) if word else None for word in response[0]]

    async def numeral(
        self,
        number: int,
        word: str,
        case: WordCase = WordCase.NOMINATIVE,
        direct: NumeralType = NumeralType.COUNT,
        reduce: bool = False,
        format: NumeralFormat = NumeralFormat.STRING,
        immediately: bool = True,
    ) -> typing.Optional[NumeralObject]:
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
        :param immediately: immediately send request. Default - True
        :type immediately: bool
        :return: numeral object with number and text (e.g., одна тысяча двести тридцать четыре рубля)
        :rtype: typing.Optional[NumeralObject]
        :raises NegativeNumber: if the number is negative
        :raises ALotOfWords: if more than one word was specified
        """

        if number < 0:
            raise exceptions.NegativeNumber("Negative number aren't allowed")
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        command = generate_command(
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
        if not immediately:
            return self.request.append(command)
        response = await make_request(self.session, generate_payload(command))
        probable_response = choose_response(response[0])
        return NumeralObject(**probable_response) if probable_response else None

    async def speller(
        self, text: str, immediately: bool = True
    ) -> typing.Optional[SpellerObject]:
        """
        Checks the text for errors

        :param text: up to 10,000 text characters for check (e.g. Пример тектса)
        :type text: str
        :param immediately: immediately send request. Default - True
        :type immediately: bool
        :return: speller object with founded and error and position in text (e.g. тектса and 8)
        :rtype: typing.Optional[SpellerObject]
        :raises ToLongText: if the text is longer than 10000 characters
        """
        if len(text) > 10000:
            raise exceptions.ToLongText("Maximum length of text is 10000 characters")
        command = generate_command(func=APIMethod.SPELLER, pars={"text": text})
        if not immediately:
            return self.request.append(command)
        response = await make_request(self.session, generate_payload(command))
        return SpellerObject(**response[0]) if response else None

    async def word_info(
        self, word: str, immediately: bool = True
    ) -> typing.Optional[WordObject]:
        """
        Method original name - "word".
        Returns parts of a word (root, prefix, etc.) and morphological features (part, number, gender, case, etc.).
        Also returns the lemma (normal form) of the word.

        :param word: one word about which we want to get information
        :type word: str
        :param immediately: immediately send request. Default - True
        :type immediately: bool
        :return: word object with information
        :rtype: typing.Optional[WordObject]
        :raises ALotOfWords: if more than one word was specified
        """
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        command = generate_command(func=APIMethod.WORD, pars={"word": word})
        if not immediately:
            return self.request.append(command)
        response = await make_request(self.session, generate_payload(command))
        probable_response = choose_response(response[0])
        return WordObject(**probable_response) if probable_response else None

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
        immediately: bool = True,
    ) -> typing.Optional[WordObject]:
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
        :param immediately: immediately send request. Default - True
        :type immediately: bool
        :return: word object in required form
        :rtype: typing.Optional[WordObject]
        :raises ALotOfWords: if more than one word was specified
        """
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        command = generate_command(
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
        if not immediately:
            return self.request.append(command)
        response = await make_request(self.session, generate_payload(command))
        probable_response = choose_response(response[0])
        return WordObject(**probable_response) if probable_response else None

    async def cognate(
        self, word: str, immediately: bool = True
    ) -> typing.Optional[typing.List[WordObject]]:
        """
        Returns a list of words of the same root

        :param str word: one word for which we want to get the same root words (e.g. делать)
        :type word: str
        :param immediately: immediately send request. Default - True
        :type immediately: bool
        :return: list of words with the same root (word and its part of speech) (e.g. дело and WordPart.NOUN)
        :rtype: typing.Optional[typing.List[WordObject]]
        :raises ALotOfWords: if more than one word was specified
        """
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        command = generate_command(func=APIMethod.COGNATE, pars={"word": word})
        if not immediately:
            return self.request.append(command)
        response = await make_request(self.session, generate_payload(command))
        return [WordObject(**word) if word else None for word in response[0]]

    async def synonym(
        self, word: str, immediately: bool = True
    ) -> typing.Optional[typing.List[WordObject]]:
        """
        Returns a list of synonyms

        :param str word: one word for which we want to get synonyms (e.g. ёмкость)
        :type word: str
        :param immediately: immediately send request. Default - True
        :type immediately: bool
        :return: list of synonyms (word and its part of speech) (e.g. сосуд and WordPart.NOUN)
        :rtype: typing.Optional[typing.List[WordObject]]
        :raises ALotOfWords: if more than one word was specified
        """
        if len(word.split(" ")) > 1:
            raise exceptions.ALotOfWords(
                "API doesn't support phrases of more than one word"
            )
        command = generate_command(func=APIMethod.SYNONYM, pars={"word": word})
        if not immediately:
            return self.request.append(command)
        response = await make_request(self.session, generate_payload(command))
        return [WordObject(**word) if word else None for word in response[0]]

    async def lat_to_cyr(
        self, text: str, immediately: bool = True
    ) -> typing.Optional[str]:
        """
        Returns the Cyrillic text converted from the text typed in the Latin keyboard layout

        :param text: up to 10,000 text characters for convert (e.g. Ghbvth ntrcnf)
        :type text: str
        :param immediately: immediately send request. Default - True
        :type immediately: bool
        :return Cyrillic text (e.g. Пример текста)
        :rtype: typing.Optional[str]
        :raises ToLongText: if the text is longer than 10000 characters
        """

        if len(text) > 10000:
            raise exceptions.ToLongText("Maximum length of text is 10000 characters")
        command = generate_command(func=APIMethod.LAT_TO_CYR, pars={"text": text})
        if not immediately:
            return self.request.append(command)
        response = await make_request(self.session, generate_payload(command))
        return response[0][0].get("text")

    async def send_request(self):
        """
        Sends a batch request to the API

        :return: list of responses
        :raises BatchProcessingError: if are not requests for sending
        """
        if not self.request:
            raise exceptions.BatchProcessingError(
                "Empty request list for batch processing"
            )
        func_list = get_func_list(self.request)
        payload = generate_payload(self.request)
        self.request = []
        responses = await make_request(self.session, payload)
        signed_responses = sign_responses(func_list, responses)
        return [
            _wrap_response(signed_response.get("func"), signed_response.get("response"))
            for signed_response in signed_responses
        ]


def _wrap_response(func_name: str, response: typing.Union[typing.Dict, typing.List]):
    """
    Local method to wrap API response by function name

    :param func_name: name of function to wrap
    :type func_name: str
    :param response: API response
    :type response: typing.Union[typing.Dict, typing.List]
    :return: API object
    """
    if func_name in (
        APIMethod.CORRECT,
        APIMethod.HINT,
        APIMethod.COGNATE,
        APIMethod.SYNONYM,
    ):
        return (
            [WordObject(**word) if word else None for word in response]
            if response
            else None
        )
    elif func_name in (APIMethod.WORD, APIMethod.SET_FORM):
        return WordObject(**choose_response(response)) if response else None
    elif func_name == APIMethod.NUMERAL:
        return NumeralObject(**choose_response(response)) if response else None
    elif func_name == APIMethod.SPELLER:
        return SpellerObject(**response) if response else None
    elif func_name == APIMethod.LAT_TO_CYR:
        return response[0].get("text") if response else None
