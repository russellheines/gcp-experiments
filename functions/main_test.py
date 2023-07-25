import chess

from main import * 

def test_evaluate():
    # initial position, value is 0
    board = chess.Board()
    assert 0 == evaluate(board, 1)

    # white captured a pawn, value is 1 or -1
    board.set_fen("rnbqkbnr/pppp1ppp/8/4P3/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1")
    assert 1 == evaluate(board, 1)
    assert -1 == evaluate(board, -1)

def test_minimax():
    # initial position, all 20 possible moves are equal
    board = chess.Board()
    moves, score = minimax_root(1, board, 1)
    assert 0 == score
    assert 20 == len(moves)
    moves, score = minimax_root(2, board, 1)
    assert 0 == score
    assert 20 == len(moves)

    # white can capture a hanging pawn
    board.set_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    moves, score = minimax_root(1, board, 1)
    assert 1 == score
    assert 1 == len(moves)
    assert 'dxe5' == board.san(moves[0])
    moves, score = minimax_root(2, board, 1)
    assert 1 == score
    assert 1 == len(moves)
    assert 'dxe5' == board.san(moves[0])

    # white can capture a pawn, but would lose a knight
    board.set_fen("rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1")
    moves, score = minimax_root(1, board, 1)
    assert 1 == score
    assert 1 == len(moves)
    assert 'Nxe5' == board.san(moves[0])
    moves, score = minimax_root(2, board, 1)
    assert 0 == score
    assert 18 == len(moves)
    assert 'Nxe5' != board.san(moves[0]) # need to check all 18

    # lichess - absolute pin #1
    board.set_fen("7k/8/8/4n3/4P3/8/8/6BK w KQkq - 0 1")
    moves, score = minimax_root(3, board, 1)
    assert 4 == score
    assert 1 == len(moves)
    assert 'Bd4' == board.san(moves[0]) # only if depth >= 3

    # lichess - absolute pin #2
    board.set_fen("5k2/p1p2pp1/7p/2r5/8/1P3P2/PBP3PP/1K6 w KQkq - 0 1")
    moves, score = minimax_root(3, board, 1)
    assert 4 == score
    assert 1 == len(moves)
    assert 'Ba3' == board.san(moves[0]) # only if depth >= 3

    # lichess - knight fork #1
    board.set_fen("2q3k1/8/8/5N2/6P1/7K/8/8 w KQkq - 0 1")
    moves, score = minimax_root(3, board, 1)
    assert 4 == score
    assert 1 == len(moves)
    assert 'Ne7+' == board.san(moves[0]) # only if depth >= 3

    # lichess - knight fork #2 is TOO SLOW!

def test_alphabeta():
    # initial position, all 20 possible moves are equal
    board = chess.Board()
    moves, score = alphabeta_root(1, board, 1)
    assert 0 == score
    assert 20 == len(moves)
    moves, score = alphabeta_root(2, board, 1)
    assert 0 == score
    assert 20 == len(moves)

    # white can capture a hanging pawn
    board.set_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    moves, score = alphabeta_root(1, board, 1)
    assert 1 == score
    assert 1 == len(moves)
    assert 'dxe5' == board.san(moves[0])
    moves, score = alphabeta_root(2, board, 1)
    assert 1 == score
    assert 1 == len(moves)
    assert 'dxe5' == board.san(moves[0])

    # white can capture a pawn, but would lose a knight
    board.set_fen("rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1")
    moves, score = alphabeta_root(1, board, 1)
    # w/o quiesce search
    assert 1 == score
    assert 1 == len(moves)
    assert 'Nxe5' == board.san(moves[0])
    # w/ quiesce search
    #assert 0 == score
    #assert 21 == len(moves)
    #assert 'Nxe5' != board.san(moves[0]) # need to check all 18
    moves, score = alphabeta_root(2, board, 1)
    # w/o quiesce search
    assert 0 == score
    assert 18 == len(moves)
    assert 'Nxe5' != board.san(moves[0]) # need to check all 18
    # w/ quiesce search
    #assert 0 == score
    #assert 21 == len(moves) # not 18?
    #assert 'Nxe5' != board.san(moves[0]) # need to check all 18

    # lichess - absolute pin #1
    board.set_fen("7k/8/8/4n3/4P3/8/8/6BK w KQkq - 0 1")
    moves, score = alphabeta_root(3, board, 1)
    assert 4 == score
    assert 1 == len(moves)
    assert 'Bd4' == board.san(moves[0]) # only if depth >= 3

    # lichess - absolute pin #2
    board.set_fen("5k2/p1p2pp1/7p/2r5/8/1P3P2/PBP3PP/1K6 w KQkq - 0 1")
    moves, score = alphabeta_root(3, board, 1)
    assert 4 == score
    assert 1 == len(moves)
    assert 'Ba3' == board.san(moves[0]) # only if depth >= 3

    # lichess - knight fork #1
    board.set_fen("2q3k1/8/8/5N2/6P1/7K/8/8 w KQkq - 0 1")
    moves, score = alphabeta_root(3, board, 1)
    assert 4 == score
    assert 1 == len(moves)
    assert 'Ne7+' == board.san(moves[0]) # only if depth >= 3

    # lichess - knight fork #2
    board.set_fen("6k1/5r1p/p2N4/nppP2q1/2P5/1P2N3/PQ5P/7K w KQkq - 0 1")
    moves, score = alphabeta_root(4, board, 1)
    # depth = 4 w/o quiesce search
    assert 0 == score
    assert 'Nxf7' == board.san(moves[0])
    # depth = 4 w/ quiesce search
    #assert 1 == len(moves)
    #assert 'Qh8+' == board.san(moves[0])