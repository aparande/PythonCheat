# Cheat

A UNIX console based implementation of the card game Cheat built in Python3 using Firebase as a backend.

## Playing the Game
### Setup
The only requirements for play are a UNIX system with Python3 installed. Upon cloning/downloading the repository, please run install all the necessary packages with pip.
```
pip3 install -r requirements.txt
```
### Playing the Game
```
python3 cheat.py
```

## Game Rules
The objective of Cheat is very simple: to get rid of all your cards. It is best played with 3 to 5 people. 

First, the deck of cards is divided as evenly as possible among all of the players.

The first round begins with the card of rank `2`. The first player places down a card and declares its rank to be `2`. If they have a card of rank `2`, they may play it, but they may also lie. All other players then have an opportunity to either call them on their bluff or let gameplay continue. If players call the bluff, if the initial player was indeed bluffing, they take the entire middle pile. If they were not bluffing, then all players who were wrong divide the pile in the middle among themselves. 

The next player commences the subsequent round with a card of rank `3`. Gameplay continues until someone runs out of cards. When the round's designated rank reaches `A`, the next round will wrap around back to rank `2`.

## Architecture Design
### Tech Stack
- Game Logic - Python3
- Database/Server - Google's Firebase

### Why have a database?
In Cheat, it is imperative that other players have absolutely no knowledge about the other players' cards. To enforce this requirement, each user plays the game on a different computer. The program coordinates the gameplay between different computers through Firebase's Realtime Database. This provides a layer of separation between players and removes the complex, unintuitive gameplay experience which workarounds such as passwords would necessitate. 

### Why Firebase?

I chose Firebase Realtime Database in particular because it is NoSQL, so it is much easier to store the unstructured data required to manage Game State than with a relational database. Moreover, because it is real-time, the game can be played in real-time with constant updates. Firebase also has well designed APIs to interact with the database as if it was a regular REST API.

### Why Python
As a scripting language, Python is incredily versatile in the programs it can create. Because I was using Firebase, I needed a language which made it easy to handle concurrency issues and act on events triggered in Real-time. Python has the capabilities readily available and it still has the object-oriented aspects of it which allow for clean but complex functionality.

## Code Structure
### Classes
- `Card`: A model class to represent cards
- `CardGroup`: A group of cards which can model a deck, a hand, or the center pile. Uses a HashMap like implementation to provide O(1) retrieval operations
- `CheatGame`: The game client which coordinates between the `Engine` and Firebase to show information and take input from the user.
- `Engine`: The game engine which each user runs. It manages game rules and controls game flow
- `Player`: A model object which represents a Player
- `Stream`: A listener class which listens to updates from Firebase
### Utilities
- `firebaseutils.py`: Firebase utility functions to abstract away the Database implementation
- `utils.py`: Minor utility functions

By structuring this code in this way, I reduced the amount of data I needed to store in Firebase and made it easier to handle concurrency. Since each client maintains its own game state through the `Engine`, I do not need to store the entire game (each player and their hands, the pile, etc) in Firebase. Instead I can just update the last card played and have every client update its internal state accordingly.

The `Stream` class also makes it easier to handle concurrency because I can pass it a method which gets called every time an update is made to Firebase. This allows the program to be asynchronous and update in real time.

I chose to create `Player`, `Card`, and `CardGroup` model classes because having these abstractions which reflect real objects makes the code easier to read and the logic easier to understand. It also groups together related functionality, reducing repetition.

I chose to make `CardGroup` a modified HashMap because the O(1) lookup times make it easy to use when checking if a player is making a valid move. Adding an `ordering` to the HashMap also enables easy distribution of the cards in the group to different players via the `distributeTo` function because each removal is also `O(1)` and allows for the `CardGroup` to double as a deck.

### Edge Cases
- If two people with the same name try to enter a room, the second one is barred from entering
- People cannot enter a room once the game has begun
- A game can't start with fewer than 2 people, and more than 6 people can't enter a room

## External Libraries
- Pyrebase: A Firebase API wrapper [[link]](https://github.com/thisbejim/Pyrebase)