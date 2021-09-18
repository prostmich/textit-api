from .helper import Item


class NumeralType:
    COUNT = Item()
    ORDER = Item()
    UNION = Item()


class NumeralFormat:
    NUMBER = Item(value="Number")
    NUMBER_STRING = Item(value="Number-string")
    STRING = Item()


class NumeralObject:
    number: str = ""
    text: str = ""

    def __init__(self, number: str, text: str):
        self.number = number
        self.text = text

    @property
    def full_text(self):
        return f"{self.number} {self.text}"
