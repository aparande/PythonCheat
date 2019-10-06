from engine import Engine
from player import Player
from utils import clearScreen
from stream import Stream
from card import strFromValue
import firebaseutils
import random
import time

class CheatGame:
    def __init__(self):
        self.engine = None
        self.roomKey = None
        self.localPlayer = None

    def printHeader(self):
        clearScreen()
        print("______________________________")
        print("            CHEAT             ")
        print("       by Anmol Parande       ")
        print("______________________________")

    def printWelcome(self, name):
        clearScreen()
        print(f"Welcome {name}. What would you like to do?")
        print("1. Join Room")
        print("2. Create Room")
        
    def setup(self):
        self.printHeader()

        name = self.enterName()
        self.localPlayer = Player(name)
        
        self.printWelcome(name)
        choice = self.handleEntrance()

        if choice == 1:
            success = False
            while not success:
                self.roomKey = input("Please enter your room key: ")
                success = self.joinRoom()
        else:
            self.localPlayer.isHost = True
            self.roomKey = self.createRoom()

        self.engine = Engine(self.localPlayer)
        self.waitForOthers()

    def enterName(self):
        name = input("Please enter your name: ")
        return name

    def joinRoom(self):
        success, message = firebaseutils.joinRoom(self.roomKey, self.localPlayer.name)
        if not success:
            print(f"Error: Could not join room because {message}")
        return success

    def createRoom(self):
        success, message, data = firebaseutils.createRoom(self.localPlayer.name)
        if not success:
            print("Could not create room key. Please try again")
            exit(1)
        print(message)
        return data['roomKey']

    def waitForOthers(self):
        recentlyJoined = True
        def putFunc(data):
            nonlocal recentlyJoined
            for p in data:
                success = self.engine.addPlayer(p)
                if recentlyJoined and success:
                    print(f"{p} is already the room")
                elif success:
                    print(f"{p} joined the room")

            recentlyJoined = False
        
        playerStream = Stream(putFunc)
        firebaseutils.listenToPlayers(playerStream, self.roomKey)

        if self.localPlayer.isHost:
            shouldExit = input("Press a key when you are ready to start the game: ")
            playerStream.close()

            self.engine.startGame()
            self.startGame()
        else:
            def shouldStartGame(stillWaiting):
                if not stillWaiting:
                    print("The host has started the game.")
                    startStream.close()
                    playerStream.close()
                    self.loadGame()
                    
            startStream = Stream(shouldStartGame)
            firebaseutils.listenForStart(startStream, self.roomKey)

    def handleEntrance(self):
        choice = input()
        while choice != "1" and choice != "2":
            choice = input("Please enter either 1 or 2: ")
        
        return int(choice)

    def startGame(self):
        hands = self.engine.listHands()
        self.engine.orderPlayers()
        firebaseutils.startGame(self.roomKey, hands, self.engine.playerList)
        print(f"It is {self.engine.playerList[0].name}'s turn")

        turnStream = Stream(self.turnListener)
        firebaseutils.listenForTurn(turnStream, self.roomKey)

    def turnListener(self, data):
        if data != None:
            actual = data.get("lastPlayedCard", None)

            if actual is not None and self.engine.currentPlayer().name != self.localPlayer.name:
                print(f"{self.engine.currentPlayer().name} played a {strFromValue(self.engine.currentRank + 2)}")
            
            gameOver = data.get('isGameOver', False)
        else:
            actual = None
            gameOver = False

        if gameOver:
            self.endGame()
            return

        data = self.engine.takeTurn(actual)
        if data != None:
            firebaseutils.logTurn(self.roomKey, data)

    def loadGame(self):
        time.sleep(0.1)
        hands, turnList = firebaseutils.loadGameData(self.roomKey)
        self.engine.setGameState(hands, turnList)

        turnStream = Stream(self.turnListener)
        firebaseutils.listenForTurn(turnStream, self.roomKey)

    def endGame(self):
        print(f"Game Over: {self.engine.currentPlayer().name} won")
        exit(0)

def main():
    game = CheatGame()
    game.setup()

if __name__ == "__main__":
    main()