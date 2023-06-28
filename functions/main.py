import base64

from cloudevents.http import CloudEvent
import functions_framework

import chess
import random
import ast
import sys

from google.cloud import firestore

db = firestore.Client()

def generateMove(board):
    i = random.randint(0, board.legal_moves.count()-1)
    move = list(board.legal_moves)[i]

    return move

def handleRequest(request):
    if "gameId" not in request:
        print("Missing gameId")
        return

    if "fen" not in request:
        print("Missing fen")
        return

    board = chess.Board()
    try:
        board.set_fen(request["fen"])
    except:
        print("Invalid fen: " + request["fen"])
        return

    move = generateMove(board)

    response = {}
    response["lastMove"] = {}
    response["lastMove"]["from"] = chess.square_name(move.from_square)
    response["lastMove"]["to"] = chess.square_name(move.to_square)
    response["lastMove"]["san"] = board.san(move)

    board.push(move)

    response["fen"] = board.fen()

    return response

@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    data = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    request = ast.literal_eval(data)
    response = handleRequest(request)

    if response:
        position = {"gameId": request["gameId"], "timestamp": firestore.SERVER_TIMESTAMP, "fen": response["fen"], "lastMove": response["lastMove"]}
        db.collection("one-player-positions").add(position)    

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        request = ast.literal_eval(sys.argv[1])
        response = handleRequest(request)
        if response:
            print (response)
    else:
        print ("Missing inputs")