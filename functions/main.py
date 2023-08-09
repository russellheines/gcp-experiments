import ast
import base64
import chess
import random
import sys
import time

from cloudevents.http import CloudEvent
import functions_framework

import utils

'''
Simplest possible evaluation function.  Just counts up the value of the pieces on the board.
'''
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

'''
Quiescence search with no optimizations.  Very slow!
'''
def quiesce_slow(board, color, alpha, beta, quiesce_counter=0):
    quiesce_counter += 1

    stand_pat = evaluate(board, color)
    if stand_pat >= beta:
        return beta, quiesce_counter
    if  alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            neg_score, quiesce_counter = quiesce_slow(board, -color, -beta, -alpha, quiesce_counter)
            score = -neg_score
            board.pop()

            if score >= beta:
                return beta, quiesce_counter
            if score > alpha:
                alpha = score
  
    return alpha, quiesce_counter

def value_of(board, square):
    match board.piece_type_at(square):
        case chess.PAWN:
            return 1
        case chess.KNIGHT:
            return 3
        case chess.BISHOP:
            return 3
        case chess.ROOK:
            return 5
        case chess.QUEEN:
            return 9
        case _:
            return 18

'''
Quiescence search with capture ordering.
'''
def quiesce_ordered(board, color, alpha, beta, quiesce_counter=0):
    quiesce_counter += 1
    
    stand_pat = evaluate(board, color)
    if stand_pat >= beta:
        return beta, quiesce_counter
    if  alpha < stand_pat:
        alpha = stand_pat

    capture_moves = []
    for move in board.legal_moves:
        if board.is_capture(move):
            capture_moves.append(move)

    ordered_capture_moves = sorted(capture_moves, key=lambda move: value_of(board, move.to_square) - value_of(board, move.from_square), reverse = True)

    for move in ordered_capture_moves:
        board.push(move)
        neg_score, quiesce_counter = quiesce_ordered(board, -color, -beta, -alpha, quiesce_counter)
        score = -neg_score
        board.pop()

        if score >= beta:
            return beta, quiesce_counter
        if score > alpha:
            alpha = score
  
    return alpha, quiesce_counter
    
'''
Quiescence search with capture ordering and a depth limit.
'''
def quiesce(depth, board, color, alpha, beta, quiesce_counter=0):
    quiesce_counter += 1
    
    stand_pat = evaluate(board, color)

    if depth == 0:
        return stand_pat, quiesce_counter

    if stand_pat >= beta:
        return beta, quiesce_counter
    if  alpha < stand_pat:
        alpha = stand_pat

    capture_moves = []
    for move in board.legal_moves:
        if board.is_capture(move):
            capture_moves.append(move)

    ordered_capture_moves = sorted(capture_moves, key=lambda move: value_of(board, move.to_square) - value_of(board, move.from_square), reverse = True)

    for move in ordered_capture_moves:
        board.push(move)
        neg_score, quiesce_counter = quiesce(depth-1, board, -color, -beta, -alpha, quiesce_counter)
        score = -neg_score
        board.pop()

        if score >= beta:
            return beta, quiesce_counter
        if score > alpha:
            alpha = score
  
    return alpha, quiesce_counter

'''
Minimax search.
'''
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

'''
Alphabeta search, which keeps track of how many positions have been searched (to troubleshoot search explosion).
'''
def alphabeta_root(depth, board, color):
    if depth == 0:
        return [], evaluate(board, color)

    alphabeta_counter_total = 0
    quiesce_counter_total = 0
    
    bestscore = -999
    moves = []
    for move in board.legal_moves:
        board.push(move)
        neg_score, alphabeta_counter, quiesce_counter = alphabeta(depth-1, board, -color, -999, 999)
        score = -neg_score
        board.pop()
        
        print('evaluated ' + board.san(move) + ' => ' + str(score))
        print("alphabeta_counter: " + str(alphabeta_counter))
        print("quiesce_counter: " + str(quiesce_counter))

        alphabeta_counter_total += alphabeta_counter
        quiesce_counter_total += quiesce_counter

        if score > bestscore:
            moves = []
            moves.append(move)
            bestscore = score
        elif score == bestscore:
            moves.append(move)

    print("alphabeta_counter_total: " + str(alphabeta_counter_total))
    print("quiesce_counter_total: " + str(quiesce_counter_total))

    return moves, bestscore

def alphabeta(depth, board, color, alpha, beta, alphabeta_counter=0, quiesce_counter=0):
    alphabeta_counter += 1

    if depth == 0:
        q, quiesce_counter = quiesce(2, board, color, alpha, beta, quiesce_counter)
        return q, alphabeta_counter, quiesce_counter
    
    for move in board.legal_moves:
        board.push(move)
        neg_score, alphabeta_counter, quiesce_counter = alphabeta(depth-1, board, -color, -beta, -alpha, alphabeta_counter, quiesce_counter)
        score = -neg_score
        board.pop()
        if score >= beta:
            return beta, alphabeta_counter, quiesce_counter
        if score > alpha:
            alpha = score

    return alpha, alphabeta_counter, quiesce_counter

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

    moves, _ = alphabeta_root(2, board, color)
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

        # This is a good example for performance testing.  Findig the best move requires a depth of 4 and was taking
        # ~42 seconds before adding some optimziations to the quiescence search (capture ordering and depth limit).
        # Now it takes ~9 seconds and still find the best move (below).

        start = time.perf_counter()
        board = chess.Board()
        board.set_fen("6k1/5r1p/p2N4/nppP2q1/2P5/1P2N3/PQ5P/7K w KQkq - 0 1")
        print(board)
        moves, score = alphabeta_root(4, board, 1)
        stop = time.perf_counter()

        print(len(moves)) # 1
        print(board.san(moves[0])) # Qh8+
        print(score) # 3
        print(stop - start) # ~9.18
