from deck import Deck
import firebaseutils
import random
from player import Player
from stream import Stream
from card import *

class Engine:
    def __init__(self, localPlayer):
        self.localPlayer = localPlayer
        self.playerIndex = -1
        self.players = {localPlayer.name: localPlayer}
        self.playerList = []
        self.currentRank = -1
    
    def startGame(self):
        deck = Deck()
        deck.shuffle()
        while not deck.isEmpty():
            for player in self.players.values():
                topCard = deck.takeTop()
                if topCard == None:
                    break
                
                player.addCardToHand(topCard)

    def takeTurn(self, cardPlayed):
        if cardPlayed is not None:
            self.currentPlayer().madeMove(cardPlayed)

        self.playerIndex = (self.playerIndex + 1) % len(self.playerList)
        self.currentRank = (self.currentRank + 1) % 13

        if self.currentPlayer().name == self.localPlayer.name:
            card = self.localPlayer.chooseCard(self.currentRank + 2)
            self.localPlayer.madeMove(card.hash())

            return {"isGameOver": self.localPlayer.hand.isEmpty(), "lastPlayedCard": card.hash()}

    def listHands(self):
        return {p.name: [card.hash() for card in p.hand.cards] for p in self.players.values()}

    def orderPlayers(self):
        self.playerList = list(self.players.values())
        random.shuffle(self.playerList)

    def addPlayer(self, playerName):
        if playerName in self.players:
            return False
        
        self.players[playerName] = Player(playerName)
        return True

    def currentPlayer(self):
        return self.playerList[self.playerIndex]

    def previousPlayer(self):
        return self.playerList[(self.playerIndex - 1) % len(self.playerList)]

    def setGameState(self, hands, turnList):
        for name in turnList:
            self.playerList.append(self.players[name])
        
        for playerName in hands:
            for cardHash in hands[playerName]:
                self.players[playerName].addCardToHand(cardFromHash(cardHash))