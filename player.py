from cardgroup import CardGroup
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = CardGroup()
        self.isHost = False

    def addCardToHand(self, card):
        self.hand.addCard(card)

    def takeTurn(self):
        self.printHand()
        chosen = input("Please pick a card to play (e.g SJ -> Jack of Spades)")
        while not self.hand.containsCard(chosen):
            chosen = input("Please enter a valid card")

        return chosen

    def printHand(self):
        for card in self.hand:
            print(card, sep=" ")
        print()