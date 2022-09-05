import numpy as np
import pygame as p
from ChessEndgames import RetrogradeAnalysis

BOARD_WIDTH = BOARD_HEIGHT = SCREEN_HEIGHT = 600
SCREEN_WIDTH = 200
ROWS = 8
SQUARE_SIZE = BOARD_HEIGHT // ROWS
FPS = 15
IMAGES = {}


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def main():
    p.init()
    background = p.display.set_mode((BOARD_WIDTH + SCREEN_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    background.fill(p.Color("white"))
    logFont = p.font.SysFont("Arial", 14, False, False)
    game = RetrogradeAnalysis.EndgameTable()
    moveMade = False
    loadImages()
    running = True
    squareSelected = ()
    playerClicks = []

    playerOne = True  # True = human
    playerTwo = False  # False = AI
    pieceTypes = ["bK", "wK", "wQ"]  # select the piece types you wish to use
    pieceTypes = sortPieces(pieceTypes)
    initialTable = np.load("KQvKComplete.npy")  # load the relevant game type
    piecePositions = [0, 2, 38]  # select the positions of the pieces
    ppCopy = piecePositions[:]
    game.bKLocation = game.toRowCol(piecePositions[0])
    game.wKLocation = game.toRowCol(piecePositions[1])
    if game.wKLocation != (7, 4):
        game.whiteKingsideCastle = False
        game.whiteQueensideCastle = False
    if game.bKLocation != (0, 4):
        game.blackKingsideCastle = False
        game.blackQueensideCastle = False
    game.pieces = []
    for i in range(len(pieceTypes)):
        game.addPiece(piecePositions[i], pieceTypes[i])
    game.createBoard(game.pieces)
    print("White to move")
    print(game.board)
    validMoves = game.validMoves()
    game.printGameTypeMessage(pieceTypes, initialTable, sameColour=False)
    game.printMessage(piecePositions, initialTable)
    game.castlingPossible(game.wKLocation[0], game.wKLocation[1], validMoves)
    gameOver = game.initialGame(piecePositions, initialTable)

    while running:
        human = (game.whiteToMove and playerOne) or (not game.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and human:
                    location = p.mouse.get_pos()
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if squareSelected == (row, col) or col >= 8:
                        squareSelected = ()
                        playerClicks = []
                    else:
                        squareSelected = (row, col)
                        playerClicks.append(squareSelected)
                    if len(playerClicks) == 2:
                        move = RetrogradeAnalysis.Move(playerClicks[0], playerClicks[1], game.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                game.makeMove(validMoves[i])
                                startpos = game.toPosition(validMoves[i].startRow, validMoves[i].startCol)
                                endpos = game.toPosition(validMoves[i].newRow, validMoves[i].newCol)
                                for j in range(len(piecePositions)):
                                    if piecePositions[j] == startpos:
                                        piecePositions[j] = endpos
                                print(game.board)
                                code = game.code
                                game.printMessage(piecePositions, initialTable, initial=False)
                                if game.code >= code and len(validMoves) > 1:
                                    print("User mistake. A better move was possible.")
                                moveMade = True
                                if game.sinceCapture >= 100 and game.sincePawnMoved >= 100:
                                    game.draw = True
                                squareSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [squareSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    if not game.undone:
                        game.undoMove()
                        moveMade = True
                        gameOver = False
                        if len(game.moveLog) == 0 and piecePositions == ppCopy:
                            game.moveLog = []
                            game.moveLogNotation = []
                        else:
                            game.moveLog.remove(game.moveLog[len(game.moveLog) - 1])
                            game.moveLogNotation.remove(game.moveLogNotation[len(game.moveLogNotation) - 1])
                        drawMoveLog(background, game, logFont)
                        game.undone = True
                if e.key == p.K_r:
                    print("\n\n\n*****Game Reset*****\n\n\n:")
                    game = RetrogradeAnalysis.EndgameTable()
                    piecePositions = ppCopy
                    squareSelected = ()
                    playerClicks = []
                    moveMade = True
                    game.bKLocation = game.toRowCol(piecePositions[0])
                    game.wKLocation = game.toRowCol(piecePositions[1])
                    if game.wKLocation != (7, 4):
                        game.whiteKingsideCastle = False
                        game.whiteQueensideCastle = False
                    if game.bKLocation != (0, 4):
                        game.blackKingsideCastle = False
                        game.blackQueensideCastle = False
                    for i in range(len(pieceTypes)):
                        game.addPiece(piecePositions[i], pieceTypes[i])
                    game.createBoard(game.pieces)
                    validMoves = game.validMoves()
                    game.printGameTypeMessage(pieceTypes, initialTable, sameColour=False)
                    game.printMessage(piecePositions, initialTable)
                    game.castlingPossible(game.wKLocation[0], game.wKLocation[1], validMoves)
                    gameOver = game.initialGame(piecePositions, initialTable)

        if not gameOver and not human:
            AIMove = game.findBestMove(piecePositions, validMoves, initialTable)
            if AIMove is None:
                AIMove = game.randomMove(validMoves)
            for i in range(len(validMoves)):
                if AIMove == validMoves[i]:
                    game.makeMove(AIMove)
                    startpos = game.toPosition(validMoves[i].startRow, validMoves[i].startCol)
                    endpos = game.toPosition(validMoves[i].newRow, validMoves[i].newCol)
                    for j in range(len(piecePositions)):
                        if piecePositions[j] == startpos:
                            piecePositions[j] = endpos
                    print(game.board)
                    game.printMessage(piecePositions, initialTable, initial=False) \
                        if game.whiteToMove else game.printMessage(piecePositions, initialTable, initial=False)
                    moveMade = True

        if moveMade:
            validMoves = game.validMoves()
            moveMade = False

        visualise(background, game, validMoves, squareSelected, logFont)

        if game.checkmate:
            gameOver = True
            endgameText(background, "Black wins - Checkmate!" if game.whiteToMove else "White wins - Checkmate!")
        elif game.stalemate:
            endgameText(background, "Stalemate")
        elif game.draw:
            gameOver = True
            endgameText(background, "Draw")
        elif game.invalid:
            endgameText(background, "Invalid position")

        clock.tick(FPS)
        p.display.flip()


def highlightSquares(background, game, validMoves, squareSelected):
    if squareSelected != ():
        r, c = squareSelected
        if game.board[r][c][0] == ("w" if game.whiteToMove else "b"):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            background.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    if game.board[r][c][0] == "w" and game.board[move.newRow][move.newCol][0] == "b":
                        s.fill(p.Color("red"))
                        background.blit(s, (move.newCol * SQUARE_SIZE, move.newRow * SQUARE_SIZE))
                    elif game.board[r][c][0] == "b" and game.board[move.newRow][move.newCol][0] == "w":
                        s.fill(p.Color("red"))
                        background.blit(s, (move.newCol * SQUARE_SIZE, move.newRow * SQUARE_SIZE))
                    elif move.enPassant:
                        s.fill(p.Color("red"))
                        background.blit(s, (move.newCol * SQUARE_SIZE, move.newRow * SQUARE_SIZE))
                    else:
                        s.fill(p.Color("yellow"))
                        background.blit(s, (move.newCol * SQUARE_SIZE, move.newRow * SQUARE_SIZE))


def visualise(background, game, validMoves, squareSelected, logFont):
    drawBoard(background)
    highlightSquares(background, game, validMoves, squareSelected)
    drawPieces(background, game.board)
    drawMoveLog(background, game, logFont)


def drawBoard(background):
    colours = [p.Color("white"), p.Color("slate gray")]
    for row in range(ROWS):
        for col in range(ROWS):
            square = colours[((row + col) % 2)]
            p.draw.rect(background, square, p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(background, board):
    for row in range(ROWS):
        for col in range(ROWS):
            piece = board[row][col]
            if piece != "--":
                background.blit(IMAGES[piece],
                                p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawMoveLog(background, game, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    p.draw.rect(background, p.Color("black"), moveLogRect)
    moveLogNotation = game.moveLogNotation
    moveTexts = []
    for i in range(0, len(moveLogNotation), 2):
        moveString = str(i // 2 + 1) + ". " + str(moveLogNotation[i]) + " "
        if i + 1 < len(moveLogNotation):
            moveString += str(moveLogNotation[i + 1]) + " "
        moveTexts.append(moveString)
    padding = 5
    movesPerRow = 1
    textY = padding
    lineSpacing = 5
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]
        textObject = font.render(text, True, p.Color("Gray"))
        textLocation = moveLogRect.move(padding, textY)
        background.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


def endgameText(background, text):
    font = p.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, True, p.Color("Gray"))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    background.blit(textObject, textLocation)
    textObject = font.render(text, True, p.Color("Black"))
    background.blit(textObject, textLocation.move(2, 2))


def sortPieces(pieceTypes):
    whiteBishops, blackBishops = 0, 0
    for i in range(len(pieceTypes)):
        if pieceTypes[i] == "wB":
            whiteBishops += 1
        elif pieceTypes[i] == "bB":
            blackBishops += 1
    if whiteBishops < 2 and blackBishops < 2:
        pieceOrder = {"bK": 0, "wK": 1, "wQ": 2, "wR": 3, "wN": 4, "wB": 5,
                      "wp": 6, "bQ": 7, "bR": 8, "bN": 9, "bB": 10, "bp": 11}
    elif whiteBishops >= 2 and blackBishops < 2:
        pieceOrder = {"bK": 0, "wK": 1, "wB": 2, "wQ": 3, "wR": 4, "wN": 5,
                      "wp": 6, "bQ": 7, "bR": 8, "bN": 9, "bB": 10, "bp": 11}
    else:
        pieceOrder = {"bK": 0, "wK": 1, "bB": 2, "wQ": 3, "wR": 4, "wN": 5,
                      "wB": 6, "wp": 7, "bQ": 8, "bR": 9, "bN": 10, "bp": 11}
    pieces = []
    for i in range(len(pieceTypes)):
        for j in pieceOrder:
            if pieceTypes[i] == j:
                pieces.append((j, pieceOrder[j]))
    pieces = sorted(pieces, key=lambda x: x[1])
    pieceTypes = []
    for i in range(len(pieces)):
        pieceTypes.append(pieces[i][0])
    return pieceTypes


if __name__ == "__main__":
    main()
