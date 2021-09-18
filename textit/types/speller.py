class SpellerObject:
    word: str = ""
    position: int = 0
    correct: list = None

    def __init__(self, word: str, position: int, correct: list = None):
        self.word = word
        self.position = position
        self.correct = correct
