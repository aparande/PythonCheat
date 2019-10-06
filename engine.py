from deck import Deck

import firebaseutils
from player import Player
from stream import Stream

class Engine:
    def __init__(self, localPlayer, roomKey):
        self.localPlayer = localPlayer
        self.roomKey = roomKey
        self.players = {localPlayer.name: localPlayer}
    
    def startGame(self):
        self.dealCards()
        hands = {p.name: [str(card) for card in p.hand.cards] for p in self.players.values()}
        firebaseutils.startGame(self.roomKey, hands)

        #while not self.gameOver():
        #    self.players[self.currentPlayer].takeTurn()
        #    self.clearScreen()
        #    self.currentPlayer = self.currentPlayer % len(self.players)

    def addPlayer(self, playerName):
        if playerName in self.players:
            return False
        
        self.players[playerName] = Player(playerName)
        return True

    def dealCards(self):
        deck = Deck()
        deck.shuffle()
        while not deck.isEmpty():
            for player in self.players.values():
                topCard = deck.takeTop()
                if topCard == None:
                    break
                
                player.addCardToHand(topCard)
                    