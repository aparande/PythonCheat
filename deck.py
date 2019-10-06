import random
from cardgroup import CardGroup
from card import Card

class Deck(CardGroup):
    def __init__(self):
        self.cards = []
        self.generate()

    def generate(self):
        for suite in Card.SUITES:
            for i in range(2, 14):
                self.cards.append(Card(suite, i))

    def shuffle(self):
        random.shuffle(self.cards)

    def takeTop(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

    def isEmpty(self):
        return len(self.cards) == 0
