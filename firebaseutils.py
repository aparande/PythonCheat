import pyrebase
from utils import randomString

"""
<!-- The core Firebase JS SDK is always required and must be listed first -->
<script src="https://www.gstatic.com/firebasejs/7.1.0/firebase-app.js"></script>

<!-- TODO: Add SDKs for Firebase products that you want to use
     https://firebase.google.com/docs/web/setup#available-libraries -->

<script>
  // Your web app's Firebase configuration
  var firebaseConfig = {
    apiKey: "AIzaSyCzEusI6pfHwO5I6rmu-uwsthK2UsTIHA0",
    authDomain: "kpcgcheat.firebaseapp.com",
    databaseURL: "https://kpcgcheat.firebaseio.com",
    projectId: "kpcgcheat",
    storageBucket: "",
    messagingSenderId: "668356097878",
    appId: "1:668356097878:web:5b79963ee98fdfeb97c8f7"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
</script>
"""
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

def startGame(roomKey, hands):
    db.child("rooms").child(roomKey).update({"open": False})
    db.child("rooms").child(roomKey).child("hands").set(hands)

def listenToPlayers(stream, roomKey):
    def stream_handler(message):
        if message['event'] == "put":
            stream.respondToPut(message['data'])
        else:
            print(f"Received {message['event']} with data {message['data']}")

    stream.stream = db.child("rooms").child(roomKey).child("players").stream(stream_handler)

def listenForStart(stream, roomKey):
    def stream_handler(message):
        if message['event'] == 'put':
            stream.respondToPut(message["data"])
        else:
            print(f"Received {message['event']} with data {message['data']}")

    stream.stream = db.child("rooms").child(roomKey).child("open").stream(stream_handler)
