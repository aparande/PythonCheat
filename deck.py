import random
from cardgroup import CardGroup
from card import Card

class Deck(CardGroup):
    def __init__(self):
        super().__init__()
        self.generate()

    def generate(self):
        for suite in Card.SUITES.values():
            for i in range(2, 15):
                self.cards.append(Card(suite, i))

    def shuffle(self):
        random.shuffle(self.cards)

    def takeTop(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()
