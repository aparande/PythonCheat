class Card:
    HEART = 0
    DIAMOND = 1
    SPADE = 2
    CLUB = 3

    SUITES = {"S": SPADE, "C": CLUB, "D": DIAMOND, "H": HEART}
    FACES_TO_NUMS = {"J": 11, "Q": 12, "K": 13, "A": 14}
    NUMS_TO_FACES = {11: "J", 12:"Q", 13:"K", 14:"A"}

    def __init__(self, suite, value):
        self.suite = suite
        self.value = value

    def hash(self):
        return self.suite * 13 + (self.value - 2)

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

def cardFromTerminalString(terminalRepr):
    try:
        suite = terminalRepr[0]
        value = terminalRepr[1:]

        cardVal = value
        if value in Card.FACES_TO_NUMS:
            cardVal = Card.FACES_TO_NUMS[value]
        else:
            cardVal = int(cardVal)

        return Card(Card.SUITES[suite], cardVal)
    except:
        return None

def cardFromHash(hashVal):
    value = hashVal % 13 + 2
    suite = hashVal // 13
    return Card(suite, value)

def strFromValue(val):
    if val in Card.NUMS_TO_FACES:
        return Card.NUMS_TO_FACES[val]
    else:
        return val