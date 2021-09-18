class Item:
    """
    Helper item

    If a value is not provided,
    it will be automatically generated based on a variable's name
    """

    def __init__(self, value=None):
        self._value = value

    def __get__(self, instance, owner):
        return self._value

    def __set_name__(self, owner, name):
        if not name.isupper():
            raise NameError("Name for item must be in uppercase!")
        self._value = self._value or name.lower()
