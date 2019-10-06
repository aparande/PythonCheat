from cardgroup import CardGroup
from card import cardFromTerminalString, strFromValue
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = CardGroup()
        self.isHost = False

    def addCardToHand(self, card):
        self.hand.addCard(card)

    def chooseCard(self, expectedCard):
        print("It is your turn")
        self.printHand()
        print("Please pick a card to play (e.g SJ -> Jack of Spades)")
        chosen = input(f"You are expected to play a {strFromValue(expectedCard)}, but you can always lie ;)\n")
        card = cardFromTerminalString(chosen)
        while card is None or not self.hand.containsCard(card):
            chosen = input("Please enter a valid card\n")
            card = cardFromTerminalString(chosen)

        self.hand.removeCard(card.hash())
            
        return card

    def madeMove(self, cardHash):
        return self.hand.removeCard(cardHash)

    def printHand(self):
        for card in self.hand.cards:
            print(card, end=" ")
        print()