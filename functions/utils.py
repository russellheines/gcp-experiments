import chess
import chess.pgn
import io

from google.cloud import firestore

db = firestore.Client()

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

