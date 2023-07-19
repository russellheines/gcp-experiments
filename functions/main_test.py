import chess

from main import * 

def test_generateMove():
    board = chess.Board()
    move = generateMove(board)

    assert move is not None
    assert move in board.legal_moves

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
    assert 'Nxe5' != board.san(moves[0]) # check all 18

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
    assert 1 == score
    assert 1 == len(moves)
    assert 'Nxe5' == board.san(moves[0])
    moves, score = alphabeta_root(2, board, 1)
    assert 0 == score
    assert 18 == len(moves)
    assert 'Nxe5' != board.san(moves[0]) # check all 18

def test_generateMove():
    # initial position, all 20 possible moves are equal
    board = chess.Board()
    assert generateMove(board) is not None

    # white can capture a hanging pawn
    board.set_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    assert 'dxe5' == board.san(generateMove(board))

    # white can capture a pawn, but would lose a knight
    board.set_fen("rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1")
    assert 'Nxe5' != board.san(generateMove(board))
