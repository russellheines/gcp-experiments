import ast
import base64
import chess
import random
import sys

from cloudevents.http import CloudEvent
import functions_framework

import utils

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
        
        #print('evaluated ' + board.san(move) + ' => ' + str(score))

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
        
        #print('evaluated ' + board.san(move) + ' => ' + str(score))

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

def process(request):
    if "gameId" not in request:
        print("Missing gameId")
        return

    if "color" not in request:
        print("Missing color")
        return

    game_id = request["gameId"]
    try:
        board = utils.pgn_to_board(utils.get_pgn(game_id))
    except:
        print("Error getting pgn for " + game_id)
        return
    
    print("Processing gameId: " + request["gameId"] + ", color: " + str(request["color"]))

    if (request["color"] == 0 and board.turn == chess.BLACK) or (request["color"] == 1 and board.turn == chess.WHITE):
        print("Wrong color")
        return

    if board.legal_moves.count() == 0:
        print("No legal moves")
        return

    if (board.turn == chess.WHITE):
        color = 1
    else:
        color = -1

    moves, _ = alphabeta_root(3, board, color)
    i = random.randint(0, len(moves)-1)
    move = moves[i]

    # e2e4
    uci = chess.square_name(move.from_square) + chess.square_name(move.to_square)
    board.push(chess.Move.from_uci(uci))

    try:
        utils.set_pgn(game_id, utils.board_to_pgn(board))
    except:
        print("Error setting pgn for " + game_id)
    
@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    data = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    request = ast.literal_eval(data)
    process(request)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        request = ast.literal_eval(sys.argv[1])
        process(request)
    else:
        print("Missing inputs")