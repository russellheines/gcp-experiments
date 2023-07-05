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

def test_negaMax():
    # initial position, no captures in the first two moves
    board = chess.Board()
    assert 0 == negaMax(0, board, 1)
    assert 0 == negaMax(1, board, 1)
    assert 0 == negaMax(2, board, 1)

    # white can capture a hanging pawn
    board.set_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    assert 1 == negaMax(1, board, 1)
    assert 1 == negaMax(2, board, 1)

    # white can capture a pawn, but would lose a knight
    board.set_fen("rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1")
    assert 0 == negaMax(0, board, 1)
    assert 1 == negaMax(1, board, 1)
    assert 0 == negaMax(2, board, 1)

def test_negaMaxRoot():
    # initial position, all 20 possible moves are equal
    board = chess.Board()
    assert 0 == len(negaMaxRoot(0, board, 1))
    assert 20 == len(negaMaxRoot(1, board, 1))
    assert 20 == len(negaMaxRoot(2, board, 1))

    # white can capture a hanging pawn
    board.set_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    assert 1 == len(negaMaxRoot(1, board, 1))
    #assert 'dxe5' in negaMaxRoot(1, board, 1)
    assert 1 == len(negaMaxRoot(2, board, 1))
    #assert 'dxe5' in negaMaxRoot(2, board, 1)

    # white can capture a pawn, but would lose a knight
    board.set_fen("rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1")
    assert 0 == len(negaMaxRoot(0, board, 1))
    assert 1 == len(negaMaxRoot(1, board, 1))
    #assert 'Nxe5' in negaMaxRoot(1, board, 1)
    assert 18 == len(negaMaxRoot(2, board, 1))
    #assert 'Nxe5' not in negaMaxRoot(2, board, 1)

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
