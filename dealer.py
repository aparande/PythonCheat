from deck import Deck

class Dealer:
    def __init__(self):
        self.deck = Deck()

    def deal(self, playerNames):
        hands = {p: [] for p in playerNames}
        i = 0
        while not self.deck.isEmpty():
            hands[playerNames[i]].append(str(self.deck.takeTop()))
            i = (i + 1) % len(playerNames)

        return hands