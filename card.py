class Card:
    HEART = 0
    DIAMOND = 1
    SPADE = 2
    CLUB = 3
    SUITES = [HEART, DIAMOND, SPADE, CLUB]

    def __init__(self, suite, value):
        self.suite = suite
        self.value = value

    def __str__(self):
        return self.printableSuite()+self.printableValue()

    def printableSuite(self):
        if self.suite == Card.HEART:
            return "♥"
        elif self.suite == Card.DIAMOND:
            return "♦"
        elif self.suite == Card.CLUB:
            return "♣"
        else:
            return "♠"

    def printableValue(self):
        if self.value < 11:
            return str(self.value)

        if self.value == 11:
            return "J"
        elif self.value == 12:
            return "Q"
        elif self.value == 13:
            return "K"
        else:
            return "A"