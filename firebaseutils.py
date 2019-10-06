import pyrebase
from utils import randomString

class FirebaseError(Exception):
    pass

config = {
  "apiKey": "AIzaSyCzEusI6pfHwO5I6rmu-uwsthK2UsTIHA0",
  "databaseURL": "https://kpcgcheat.firebaseio.com/",
  "authDomain": "kpcgcheat.firebaseapp.com",
  "storageBucket": ""
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def joinRoom(roomKey, name):
    #TODO: Make sure no duplicate names
    room = db.child("rooms").child(roomKey).get()
    if not room.val():
        return False, "room key does not exist."

    if not room.val()["open"]:
        return False, "a game is in progress"

    playerData = room.val()["players"]
    if len(playerData) >= 6:
        return False, " only 6 people can play at once."

    playerData.append(name)
    db.child("rooms").child(roomKey).update({"players": playerData})
    return True, "Successfully joined room"

def createRoom(hostName):
    key = randomString(stringLength=4)
    result = db.child("rooms").child(key).set({"roomKey": key, "players": [hostName], "open": True})

    if len(result) != 0:
        return True, f"Successfully created room. Your room key is {key}. Please share it with your friends", \
            {"roomKey": key}
    else:
        return False, "Could not create room. Please try again", {}

def startGame(roomKey, hands, playerList):
    db.child("rooms").child(roomKey).update({"open": False})
    db.child("rooms").child(roomKey).child("hands").set(hands)
    db.child("rooms").child(roomKey).child("turnList").set([p.name for p in playerList])

def logTurn(roomKey, cardHash):
    db.child("rooms").child(roomKey).child("turnData").child("gameState").set({"lastPlayedCard": cardHash})

def logCall(roomKey, playerName, decision):
    db.child("rooms").child(roomKey).child("turnData").child("bluffs").child(playerName).set(decision)

def clearCalls(roomKey):
    db.child("rooms").child(roomKey).child("turnData").child("bluffs").remove()

def loadGameData(roomKey, retries = 3):
    if retries == 0:
        raise FirebaseError()
    hands = db.child("rooms").child(roomKey).child("hands").get()
    turnList = db.child("rooms").child(roomKey).child("turnList").get()
    if turnList == None:
        return loadGameData(roomKey, retries= retries - 1)

    return hands.val(), turnList.val()

def listenToPlayers(listener, roomKey):
    def stream_handler(message):
        if message['event'] == "put":
            listener.respondToPut(message['data'])
        else:
            print(f"Received {message['event']} with data {message['data']}")

    listener.stream = db.child("rooms").child(roomKey).child("players").stream(stream_handler)

def listenForStart(listener, roomKey):
    def stream_handler(message):
        if message['event'] == 'put':
            listener.respondToPut(message["data"])
        else:
            print(f"Received {message['event']} with data {message['data']}")

    listener.stream = db.child("rooms").child(roomKey).child("open").stream(stream_handler)

def listenForTurn(listener, roomKey):
    def stream_handler(message):
        if message['event'] == 'put':
            listener.respondToPut(message["data"])
        else:
            print(f"Received {message['event']} with data {message['data']}")

    listener.stream = db.child("rooms").child(roomKey).child("turnData").child("gameState").stream(stream_handler)

def listenForCall(listener, roomKey):
    def stream_handler(message):
        if message['event'] == 'put':
            path = message["path"].replace("/", '')
            if path == '':
                listener.respondToPut(message["data"])
            else:
                listener.respondToPut({path: message["data"]})
        else:
            print(f"Received {message['event']} with data {message['data']}")

    listener.stream = db.child("rooms").child(roomKey).child("turnData").child("bluffs").stream(stream_handler)
