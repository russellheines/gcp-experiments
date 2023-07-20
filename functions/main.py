import base64

from cloudevents.http import CloudEvent
import functions_framework

import chess
import random
import ast
import sys

from google.cloud import firestore

db = firestore.Client()

WHITE = 1
BLACK = -1

def move_randomly(board):
    i = random.randint(0, board.legal_moves.count()-1)
    move = list(board.legal_moves)[i]

    return move

def evaluate(board, color):
    value = 0

    fen = board.fen()
    for i in range (len(fen)):
        x = fen[i:i+1]
        if x == 'p':
            value -= 1
        elif x == 'n':
            value -= 3
        elif x == 'b':
            value -= 3
        elif x == 'r':
            value -= 5
        elif x == 'q':
            value -= 9
        elif x == 'P':
            value += 1
        elif x == 'N':
            value += 3
        elif x == 'B':
            value += 3
        elif x == 'R':
            value += 5
        elif x == 'Q':
            value += 9
        elif x == ' ':
            break

    return value * color

def quiesce(board, color, alpha, beta):
    stand_pat = evaluate(board, color)
    if stand_pat >= beta:
        return beta
    if  alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(board, -color, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
  
    return alpha

def minimax_root(depth, board, color):
    if depth == 0:
        return [], evaluate(board, color)

    bestscore = -999
    moves = []
    for move in board.legal_moves:
        board.push(move)
        score = -minimax(depth-1, board, -color)
        board.pop()
        
        print('evaluated ' + board.san(move) + ' => ' + str(score))

        if score > bestscore:
            moves = []
            moves.append(move)
            bestscore = score
        elif score == bestscore:
            moves.append(move)

    return moves, bestscore

def minimax(depth, board, color):
    if depth == 0:
        return evaluate(board, color)

    max = -999
    for move in board.legal_moves:
        board.push(move)
        score = -minimax(depth-1, board, -color)
        board.pop()

        if score > max:
            max = score

    return max

def alphabeta_root(depth, board, color):
    if depth == 0:
        return [], evaluate(board, color)

    bestscore = -999
    moves = []
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(depth-1, board, -color, -999, 999)
        board.pop()
        
        print('evaluated ' + board.san(move) + ' => ' + str(score))

        if score > bestscore:
            moves = []
            moves.append(move)
            bestscore = score
        elif score == bestscore:
            moves.append(move)

    return moves, bestscore

def alphabeta(depth, board, color, alpha, beta):
    if depth == 0:
        #return quiesce(board, color, alpha, beta)
        return evaluate(board, color)
        
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(depth-1, board, -color, -beta, -alpha)
        board.pop()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha

def generateMove(board):    

    return move

def handle_request(request):
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

    if board.legal_moves.count() == 0:
        print("No legal moves")
        return

    if (board.turn == chess.WHITE):
        color = 1
    else:
        color = -1
    moves, _ = alphabeta_root(2, board, color)
    i = random.randint(0, len(moves)-1)
    move = moves[i]

    print(move)

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
    response = handle_request(request)

    if response:
        position = {"gameId": request["gameId"], "timestamp": firestore.SERVER_TIMESTAMP, "fen": response["fen"], "lastMove": response["lastMove"]}
        db.collection("lets-play-positions").add(position)    

if __name__ == "__main__":

    board = chess.Board()

    # white can capture a pawn, but would lose a knight

    board.set_fen("rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1")
    print(board)
    print("start: " + str(evaluate(board, WHITE)))
    moves, score = minimax_root(1, board, WHITE)
    print(len(moves))
    print(moves)
    
    board.set_fen("rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1")
    print(board)
    print("start: " + str(evaluate(board, WHITE)))
    moves, score = alphabeta_root(1, board, WHITE)
    print(len(moves))
    print(moves)
    
    board.set_fen("rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1")
    print(move_randomly(board))

'''
    if (len(sys.argv) > 1):
        request = ast.literal_eval(sys.argv[1])
        response = handle_request(request)
        if response:
            print (response)
    else:
        print ("Missing inputs")
'''