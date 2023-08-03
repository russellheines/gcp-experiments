import ast
import chess
import chess.engine
import chess.pgn
import io
import random

from google.cloud import firestore

db = firestore.Client()

engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")

def pgn_to_board(pgn_string):
    pgn = io.StringIO(pgn_string)
    game = chess.pgn.read_game(pgn)

    if game:
        board = game.end().board()
    else:
        board = chess.Board()

    #print(board)

    return board

def board_to_pgn(board):
    exporter = chess.pgn.StringExporter(headers=False, variations=False, comments=False)
    game = chess.pgn.Game.from_board(board)
    pgn_string = game.accept(exporter)

    #print(pgn_string)

    return pgn_string

def get_pgn(game_id):
    game_ref = db.collection("lets-play-chess").document(game_id)  # TODO: query
    pgn_string = game_ref.get().to_dict()['pgn']

    #print(pgn_string)

    return pgn_string

def set_pgn(game_id, pgn_string):
    game_ref = db.collection("lets-play-chess").document(game_id)  # TODO: query
    game_ref.update({"pgn": pgn_string})

    #print(pgn_string)

def play_randomly(message):
    print("Let's play randomly!")
    request = ast.literal_eval(message.data.decode())
    game_id = request["gameId"]
    pgn_string = get_pgn(game_id)
    print(pgn_string)
    board = pgn_to_board(pgn_string)
    #print(board)

    i = random.randint(0, board.legal_moves.count()-1)
    move = list(board.legal_moves)[i]
    if not move:
        return
    board.push(move)
    #print(board)

    pgn_string = board_to_pgn(board)
    print(pgn_string)
    set_pgn(game_id, pgn_string)

def play_stockfish(message):
    print("Let's play Stockfish!")
    request = ast.literal_eval(message.data.decode())
    game_id = request["gameId"]
    pgn_string = get_pgn(game_id)
    print(pgn_string)
    board = pgn_to_board(pgn_string)
    #print(board)

    result = engine.play(board, chess.engine.Limit(time=0.1))
    if not result.move:
        return
    board.push(result.move)
    #print(board)

    pgn_string = board_to_pgn(board)
    print(pgn_string)
    set_pgn(game_id, pgn_string)