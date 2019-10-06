from deck import Deck
import firebaseutils
import random
from player import Player
from stream import Stream
from card import *
from cardgroup import CardGroup

class Engine:
    def __init__(self, localPlayer):
        self.localPlayer = localPlayer
        self.playerIndex = -1
        self.players = {localPlayer.name: localPlayer}
        self.playerList = []
        self.currentRank = -1
        self.currentCalls = {}
        self.lastPlayedCard = None
        self.isReadyForNextPlayer = True
        self.pile = CardGroup()
    
    def startGame(self):
        deck = Deck()
        deck.shuffle()
        while not deck.isEmpty():
            for player in self.players.values():
                topCard = deck.takeTop()
                if topCard == None:
                    break
                
                player.addCardToHand(topCard)

    def registerTurn(self):
        if self.lastPlayedCard is not None:
            card = self.currentPlayer().madeMove(self.lastPlayedCard)
            self.pile.addCard(card)

        self.playerIndex = (self.playerIndex + 1) % len(self.playerList)
        self.currentRank = (self.currentRank + 1) % 13

    def takeTurn(self):
        if self.currentPlayer().name == self.localPlayer.name:
            card = self.localPlayer.chooseCard(self.currentRank + 2)
            self.localPlayer.madeMove(card.hash())

            return {"isGameOver": self.localPlayer.hand.isEmpty(), "lastPlayedCard": card.hash()}

    def logCalls(self, callDict):
        for name in callDict:
            self.currentCalls[name] = callDict[name]

        if len(self.currentCalls) == len(self.playerList) - 1:
            result = self.executeCalls()
            self.isReadyForNextPlayer = True
            return result
        else:
            self.isReadyForNextPlayer = False
            return 0

    def executeCalls(self):
        if not any(self.currentCalls.values()):
            self.currentCalls = {}
            return 0

        requiredVal = (self.currentRank - 1) % 13
        if requiredVal + 2 != self.lastPlayedCard: #Last person bluffed
            for i in range(len(self.pile.cards)):
                self.previousPlayer().addCardToHand(self.pile.cards.pop())

            self.currentCalls = {}
            return -1
        else:
            wrongPlayers = [self.players[name] for name in self.currentCalls if self.currentCalls[name] == True]
            for i in range(len(self.pile.cards)):
                wrongPlayers[i % len(wrongPlayers)].addCardToHand(self.pile.cards.pop())

            self.currentCalls = {}
            return 1
        
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