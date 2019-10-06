import random
from card import *
class CardGroup:
    def __init__(self):
        self.cards = [None for i in range(52)]
        self.ordering = []

    def addCard(self, card):
        self.cards[card.hash()] = card
        self.ordering.append(card.hash())

    def distributeTo(self, players):
        i = 0
        while len(self.ordering) != 0:
            for player in players:
                card = self.takeTop()
                if card == None:
                    break

                player.addCardToHand(card)


    def takeTop(self):
        if len(self.ordering) == 0:
            return None
            
        hashVal = self.ordering.pop()
        card = self.cards[hashVal]
        self.cards[hashVal] = None
        return card

    def fill(self):
        for suite in Card.SUITES.values():
            for i in range(2, 15):
                self.addCard(Card(suite, i))

    def shuffle(self):
        random.shuffle(self.ordering)

    def getCards(self):
        return [card for card in self.cards if card is not None]

    def removeCard(self, removedCard):
        if self.cards[removedCard.hash()] is None:
            return None

        self.cards[removedCard.hash()] = None
        self.ordering.pop(self.ordering.index(removedCard.hash()))
        return removedCard
        
    def containsCard(self, card):
        return self.cards[card.hash()] is not None

    def isEmpty(self):
        return len(self.ordering) == 0

    def __str__(self):
        return " ".join([str(card) for card in self.cards if card is not None])