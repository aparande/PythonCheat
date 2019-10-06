from engine import Engine
from player import Player
from utils import clearScreen
from stream import Stream
import firebaseutils

class CheatGame:
    def __init__(self):
        self.engine = None

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
        localPlayer = Player(name)
        
        self.printWelcome(name)
        choice = self.handleEntrance()

        roomKey = None
        if choice == 1:
            roomKey = input("Please enter your room key: ")
            self.joinRoom(roomKey, localPlayer.name)
        else:
            localPlayer.isHost = True
            roomKey = self.createRoom(localPlayer.name)

        self.engine = Engine(localPlayer, roomKey)
        self.waitForOthers()

    def enterName(self):
        name = input("Please enter your name: ")
        return name

    def joinRoom(self, roomKey, playerName):
        success = False
        while not success:
            success, message = firebaseutils.joinRoom(roomKey, playerName)
            if not success:
                print(f"Error: Could not join room because {message}")

        print(message)
        print("Waiting on other players")

    def createRoom(self, playerName):
        success, message, data = firebaseutils.createRoom(playerName)
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
        firebaseutils.listenToPlayers(playerStream, self.engine.roomKey)

        def shouldStartGame(isOpen):
            if not isOpen:
                print("The host has started the game.")
                startStream.close()
                playerStream.close()
                exit(1)

        startStream = Stream(shouldStartGame)
        firebaseutils.listenForStart(startStream, self.engine.roomKey)

        if self.engine.localPlayer.isHost:
            shouldExit = input("Press a key when you are ready to start the game: ")
            self.engine.startGame()

    def handleEntrance(self):
        choice = input()
        while choice != "1" and choice != "2":
            choice = input("Please enter either 1 or 2: ")
        
        return int(choice)

def main():
    game = CheatGame()
    game.setup()

if __name__ == "__main__":
    main()