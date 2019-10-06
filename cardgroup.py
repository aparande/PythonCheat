class CardGroup:
    def __init__(self):
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)

    #TODO: Make this remove a card, not a hash
    def removeCard(self, cardHash):
        newHand = []
        popped = None
        for card in self.cards:
            if card.hash() != cardHash:
                newHand.append(card)
            else:
                popped = card

        self.cards = newHand
        return popped
        
    def containsCard(self, card):
        for groupCard in self.cards:
            if card.hash() == groupCard.hash():
                return True
        
        return False

    def isEmpty(self):
        return len(self.cards) == 0