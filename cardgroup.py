class CardGroup:
    def __init__(self):
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)

    def removeCard(self, removedCard):
        newHand = []
        popped = None
        for card in self.cards:
            if card.hash() != removedCard.hash():
                newHand.append(card)
            else:
                popped = card

        if popped == None:
            print("Couldn't find card to pop")
        self.cards = newHand
        return popped
        
    def containsCard(self, card):
        for groupCard in self.cards:
            if card.hash() == groupCard.hash():
                return True
        
        return False

    def isEmpty(self):
        return len(self.cards) == 0

    def __str__(self):
        return " ".join([str(card) for card in self.cards])