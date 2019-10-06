from deck import Deck
from utils import clearScreen
import firebaseutils
from player import Player
from stream import Stream
from dealer import Dealer

class Engine:
    def __init__(self):
        self.localPlayer = None
        self.roomKey = None

    def setup(self):
        print("______________________________")
        print("            CHEAT             ")
        print("       by Anmol Parande       ")
        print("______________________________")

        name = self.enterName()
        self.localPlayer = Player(name)
        clearScreen()
        print(f"Welcome {name} What would you like to do?")
        print("1. Join Room")
        print("2. Create Room")

        choice = self.handleEntrance()
        if choice == 1:
            self.joinRoom()
        else:
            self.createRoom()

        self.waitForOthers()

    def waitForOthers(self):
        players = [self.localPlayer.name]
        recentlyJoined = True
        def putFunc(data):
            nonlocal recentlyJoined, players
            for p in data:
                if p not in players:
                    if recentlyJoined:
                        print(f"{p} is already the room")
                    else:
                        print(f"{p} joined the room")
                    players.append(p)

            recentlyJoined = False
        
        playerStream = Stream(putFunc)
        firebaseutils.listenToPlayers(playerStream, self.roomKey)

        def shouldStartGame(isOpen):
            if not isOpen:
                print("The host has started the game.")
                startStream.close()
                playerStream.close()
                exit(1)

        startStream = Stream(shouldStartGame)
        firebaseutils.listenForStart(startStream, self.roomKey)

        if self.localPlayer.isHost:
            shouldExit = input("Press a key when you are ready to start the game: ")
            dealer = Dealer()
            hands = dealer.deal(players)
            print(hands)
            firebaseutils.startGame(self.roomKey, hands)

    def handleEntrance(self):
        choice = input()
        while choice != "1" and choice != "2":
            choice = input("Please enter either 1 or 2: ")
        
        clearScreen()
        return int(choice)

    def joinRoom(self):
        success = False
        while not success:
            self.roomKey = input("Please enter your room key: ")
            success = False
            success, message = firebaseutils.joinRoom(self.roomKey, self.localPlayer.name)
            if not success:
                print(f"Error: Could not join room because {message}")

        print(message)
        print("Waiting on other players")

    def createRoom(self):
        success, message, data = firebaseutils.createRoom(self.localPlayer.name)
        if not success:
            print("Could not create room key. Please try again")
            exit(1)
        print(message)
        self.roomKey = data['roomKey']
        self.localPlayer.isHost = True

    def enterName(self):
        name = input("Please enter your name: ")
        return name
        
    def startGame(self):
        while not self.gameOver():
            self.players[self.currentPlayer].takeTurn()
            self.clearScreen()
            self.currentPlayer = self.currentPlayer % len(self.players)

    def loadPlayers(self, playerCount):
        while (len(self.players) != playerCount):
            name, password = self.requestPlayer()
            self.players.append(Player(name, password))

    def requestPlayer(self):
        name = input("Please enter your name")
        password = input("Please enter a password")

        return name, password

    def dealCards(self):
        while not self.deck.isEmpty():
            for player in self.players:
                topCard = self.deck.takeTop()
                if topCard != None:
                    player.addCardToHand(topCard)