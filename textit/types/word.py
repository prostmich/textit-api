import enum
from .helper import Item


class WordPart(enum.Enum):
    NOUN = 1
    ADJECTIVE = 2
    VERB = 3
    ADVERB = 4
    NUMERAL = 5
    PRONOUN = 6
    PREPOSITION = 7
    UNION = 8
    PARTICLE = 9
    INTERJECTION = 10
    PARTICIPLE = 11
    VERBAL_PARTICIPLE = 12
    COMPARATIVE = 13
    PREDICATIVE = 14


class WordCase(enum.Enum):
    NOMINATIVE = 1
    GENITIVE = 2
    DATIVE = 3
    ACCUSATIVE = 4
    INSTRUMENTAL = 5
    PREPOSITIONAL = 6


class WordForm(enum.Enum):
    UNDEFINED = 1
    PERSONAL = 2
    FULL = 3
    SHORT = 4


class WordGender(enum.Enum):
    MASCULINE = 1
    FEMININE = 2
    NEUTER = 3
    COMMON = 4


class WordKind(enum.Enum):
    IMPERFECT = 1
    PERFECT = 2


class WordAnimate(enum.Enum):
    ANIMATE = 1
    INANIMATE = 2


class WordNumber(enum.Enum):
    SINGULAR = 1
    PLURAL = 2


class WordPerson(enum.Enum):
    FIRST_PERSON = 1
    SECOND_PERSON = 2
    THIRD_PERSON = 3


class WordTense(enum.Enum):
    PRESENT = 1
    PAST = 2
    FUTURE = 3


class WordType:
    DICTIONARY = Item()
    NAMED = Item()
    UNKNOWN = Item()


class WordObject:
    word: str = ""
    part = WordPart
    case = WordCase
    form = WordForm
    gender = WordGender
    kind = WordKind
    animate = WordAnimate
    number = WordNumber
    person = WordPerson
    tense = WordTense
    prefix: str = ""
    base: str = ""
    interfix: str = ""
    suffix: str = ""
    ending: str = ""
    postfix: str = ""
    initial: str = ""
    lemma: str = ""
    type = WordType()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                attr = self.__getattribute__(key)
                if isinstance(attr, enum.EnumMeta):
                    self.__setattr__(key, attr(value))
                else:
                    self.__setattr__(key, value)
