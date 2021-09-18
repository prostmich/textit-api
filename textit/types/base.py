from .helper import Item


class APIMethod:
    CORRECT = Item()
    HINT = Item()
    NUMERAL = Item()
    SPELLER = Item()
    WORD = Item()
    SET_FORM = Item(value="setform")
    COGNATE = Item()
    SYNONYM = Item()
    LAT_TO_CYR = Item(value="lattocyr")
