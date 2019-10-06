class CardGroup:
    def __init__(self):
        self.cards = []


    def addCard(self, card):
        self.cards.append(card)
        
    def containsCard(self, suite, spade):
        for card in self.cards:
            if self.suite == suite and self.spade == spade:
                return True
        
        return False