import numpy as np


class Game:
    def __init__(self):
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])
        self.getPieceMoves = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.wKLocation = (7, 4)
        self.bKLocation = (0, 4)
        self.whiteKingsideCastle = True
        self.whiteQueensideCastle = True
        self.blackKingsideCastle = True
        self.blackQueensideCastle = True
        self.enPassantPossible = False
        self.doubleEnPassant = False
        self.pawnMoved = ()
        self.enPassantPawns = ()
        self.inCheck = False
        self.checkmate = False
        self.stalemate = False
        self.draw = False
        self.pins = []
        self.checks = []
        self.sincePawnMoved = 0
        self.sinceCapture = 0
        self.moveLog = []

    def getPawnMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            moveDirection = -1
            startRow = 6
            backRow = 0
            enemy = "b"
        else:
            moveDirection = 1
            startRow = 1
            backRow = 7
            enemy = "w"

        if self.enPassantPossible:
            for p in self.enPassantPawns:
                if p[0] == row and p[1] == col:
                    self.enPassant(row, col, moves)

        if self.board[row + moveDirection][col] == "--":
            if not piecePinned or pinDirection == (moveDirection, 0):
                if row + moveDirection == backRow:
                    moves.append(Move((row, col), (row + moveDirection, col), self.board, pawnPromotion=True))
                else:
                    moves.append(Move((row, col), (row + moveDirection, col), self.board))
                if row == startRow and self.board[row + 2 * moveDirection][col] == "--":
                    if 0 <= col - 1 < 8 and 0 <= col + 1 < 8:
                        if self.board[row + 2 * moveDirection][col - 1][0] == enemy or self.board[row + 2 * moveDirection][col + 1][0] == enemy:
                            moves.append(Move((row, col), (row + 2 * moveDirection, col), self.board, doublePawnMove=True))
                            if self.board[row + 2 * moveDirection][col - 1][0] == enemy and self.board[row + 2 * moveDirection][col + 1][0] == enemy:
                                self.doubleEnPassant = True
                        else:
                            moves.append(Move((row, col), (row + 2 * moveDirection, col), self.board))
                    elif col == 0:
                        if self.board[row + 2 * moveDirection][col + 1][0] == enemy:
                            moves.append(Move((row, col), (row + 2 * moveDirection, col), self.board, doublePawnMove=True))
                            self.pawnMoved = (row + 2 * moveDirection, col)
                        else:
                            moves.append(Move((row, col), (row + 2 * moveDirection, col), self.board))
                    elif col == 7:
                        if self.board[row + 2 * moveDirection][col - 1][0] == enemy:
                            moves.append(Move((row, col), (row + 2 * moveDirection, col), self.board, doublePawnMove=True))
                            self.pawnMoved = (row + 2 * moveDirection, col)
                        else:
                            moves.append(Move((row, col), (row + 2 * moveDirection, col), self.board))
        if col - 1 >= 0:
            if not piecePinned or pinDirection == (moveDirection, -1):
                if self.board[row + moveDirection][col - 1][0] == enemy:
                    if row + moveDirection == backRow:
                        moves.append(Move((row, col), (row + moveDirection, col - 1), self.board, pawnPromotion=True))
                    else:
                        moves.append(Move((row, col), (row + moveDirection, col - 1), self.board))
        if col + 1 <= 7:
            if not piecePinned or pinDirection == (moveDirection, 1):
                if self.board[row + moveDirection][col + 1][0] == enemy:
                    if row + moveDirection == backRow:
                        moves.append(Move((row, col), (row + moveDirection, col + 1), self.board, pawnPromotion=True))
                    else:
                        moves.append(Move((row, col), (row + moveDirection, col + 1), self.board))

    def enPassant(self, row, col, moves):
        if self.whiteToMove:
            moves.append(Move((row, col), (self.pawnMoved[0]-1, self.pawnMoved[1]), self.board, enPassant=True))
        else:
            moves.append(Move((row, col), (self.pawnMoved[0]+1, self.pawnMoved[1]), self.board, enPassant=True))
        if self.doubleEnPassant:
            self.enPassantPossible = True
            self.doubleEnPassant = False
        else:
            self.enPassantPossible = False

    def getKnightMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally = "w" if self.whiteToMove else "b"
        for k in knightMoves:
            newRow = row + k[0]
            newCol = col + k[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                if not piecePinned:
                    newPiece = self.board[newRow][newCol]
                    if newPiece[0] != ally:
                        moves.append(Move((row, col), (newRow, newCol), self.board))

    def getBishopMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        bishopMoves = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        ally = "w" if self.whiteToMove else "b"
        for b in bishopMoves:
            for i in range(1, 8):
                newRow = row + b[0] * i
                newCol = col + b[1] * i
                if 0 <= newRow < 8 and 0 <= newCol < 8:
                    if not piecePinned or pinDirection == b or pinDirection == (-b[0], -b[1]):
                        newPiece = self.board[newRow][newCol]
                        if newPiece == "--":
                            moves.append(Move((row, col), (newRow, newCol), self.board))
                        elif newPiece[0] != ally:
                            moves.append(Move((row, col), (newRow, newCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getRookMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != "Q":
                    self.pins.remove(self.pins[i])
                break
        rookMoves = ((-1, 0), (0, -1), (1, 0), (0, 1))
        ally = "w" if self.whiteToMove else "b"
        for r in rookMoves:
            for i in range(1, 8):
                newRow = row + r[0] * i
                newCol = col + r[1] * i
                if 0 <= newRow < 8 and 0 <= newCol < 8:
                    if not piecePinned or pinDirection == r or pinDirection == (-r[0], -r[1]):
                        newPiece = self.board[newRow][newCol]
                        if newPiece == "--":
                            moves.append(Move((row, col), (newRow, newCol), self.board))
                        elif newPiece[0] != ally:
                            moves.append(Move((row, col), (newRow, newCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self, row, col, moves):
        self.getRookMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally = "w" if self.whiteToMove else "b"
        for k in kingMoves:
            newRow = row + k[0]
            newCol = col + k[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                newPiece = self.board[newRow][newCol]
                if newPiece[0] != ally:
                    # Kings sent to their potential end locations to see if these positions would be valid
                    if ally == "w":
                        self.wKLocation = (newRow, newCol)
                    else:
                        self.bKLocation = (newRow, newCol)
                    inCheck, pins, checks = self.pinsAndChecks()
                    if not inCheck:
                        moves.append(Move((row, col), (newRow, newCol), self.board))
                    # If the move has not been appended to val3dMoves, the King locations are reset
                    # Otherwise they remain the same
                    if ally == "w":
                        self.wKLocation = (row, col)
                    else:
                        self.bKLocation = (row, col)

        if not self.inCheck:
            self.kingsideCastle(row, col, moves)
            self.queensideCastle(row, col, moves)

    def kingsideCastle(self, row, col, moves):
        oldKingLocation = self.wKLocation if self.whiteToMove else self.bKLocation
        if self.whiteToMove:
            if self.whiteKingsideCastle:
                if self.board[7][5] == "--" and self.board[7][6] == "--":
                    self.wKLocation = (7, 5)
                    inCheck, pins, checks = self.pinsAndChecks()
                    if not inCheck:
                        self.wKLocation = (7, 6)
                        inCheck, pins, checks = self.pinsAndChecks()
                        if not inCheck:
                            self.wKLocation = (7, 7)
                            inCheck, pins, checks = self.pinsAndChecks()
                            if not inCheck:
                                self.wKLocation = oldKingLocation
                                moves.append(Move((row, col), (7, 6), self.board, castle=True))
        else:
            if self.blackKingsideCastle:
                if self.board[0][5] == "--" and self.board[0][6] == "--":
                    self.bKLocation = (0, 5)
                    inCheck, pins, checks = self.pinsAndChecks()
                    if not inCheck:
                        self.bKLocation = (0, 6)
                        inCheck, pins, checks = self.pinsAndChecks()
                        if not inCheck:
                            self.bKLocation = (0, 7)
                            inCheck, pins, checks = self.pinsAndChecks()
                            if not inCheck:
                                self.bKLocation = oldKingLocation
                                moves.append(Move((row, col), (0, 6), self.board, castle=True))

    def queensideCastle(self, row, col, moves):
        oldKingLocation = self.wKLocation if self.whiteToMove else self.bKLocation
        if self.whiteToMove:
            if self.whiteQueensideCastle:
                if self.board[7][1] == "--" and self.board[7][2] == "--" and self.board[7][3] == "--":
                    self.wKLocation = (7, 0)
                    inCheck, pins, checks = self.pinsAndChecks()
                    if not inCheck:
                        self.wKLocation = (7, 1)
                        inCheck, pins, checks = self.pinsAndChecks()
                        if not inCheck:
                            self.wKLocation = (7, 2)
                            inCheck, pins, checks = self.pinsAndChecks()
                            if not inCheck:
                                self.wKLocation = (7, 3)
                                inCheck, pins, checks = self.pinsAndChecks()
                                if not inCheck:
                                    self.wKLocation = oldKingLocation
                                    moves.append(Move((row, col), (7, 2), self.board, castle=True))
        else:
            if self.blackQueensideCastle:
                if self.board[0][1] == "--" and self.board[0][2] == "--" and self.board[0][3] == "--":
                    self.bKLocation = (0, 0)
                    inCheck, pins, checks = self.pinsAndChecks()
                    if not inCheck:
                        self.bKLocation = (0, 1)
                        inCheck, pins, checks = self.pinsAndChecks()
                        if not inCheck:
                            self.bKLocation = (0, 2)
                            inCheck, pins, checks = self.pinsAndChecks()
                            if not inCheck:
                                self.bKLocation = (0, 3)
                                inCheck, pins, checks = self.pinsAndChecks()
                                if not inCheck:
                                    self.bKLocation = oldKingLocation
                                    moves.append(Move((row, col), (0, 2), self.board, castle=True))

    def inCheck(self):
        if self.whiteToMove:
            return self.underAttack(self.wKLocation[0], self.wKLocation[1])
        else:
            return self.underAttack(self.bKLocation[0], self.bKLocation[1])

    def underAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        allEnemyMoves = self.allMoves()
        self.whiteToMove = not self.whiteToMove
        for move in allEnemyMoves:
            if move.newRow == row and move.newCol == col:
                return True
        return False

    def allMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.getPieceMoves[piece](row, col, moves)
        return moves

    def validMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.pinsAndChecks()
        if self.whiteToMove:
            kingRow = self.wKLocation[0]
            kingCol = self.wKLocation[1]
        else:
            kingRow = self.bKLocation[0]
            kingCol = self.bKLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.allMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != "K":
                        if not (moves[i].newRow, moves[i].newCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.allMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def pinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemy = "b"
            ally = "w"
            startRow = self.wKLocation[0]
            startCol = self.wKLocation[1]
        else:
            enemy = "w"
            ally = "b"
            startRow = self.bKLocation[0]
            startCol = self.bKLocation[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                newRow = startRow + d[0] * i
                newCol = startCol + d[1] * i
                if 0 <= newRow < 8 and 0 <= newCol < 8:
                    newPiece = self.board[newRow][newCol]
                    if newPiece[0] == ally and newPiece[1] != "K":
                        if possiblePin == ():
                            possiblePin = (newRow, newCol, d[0], d[1])
                        else:
                            break
                    elif newPiece[0] == enemy:
                        type = newPiece[1]
                        if (0 <= j <= 3 and type == "R") or \
                                (4 <= j <= 7 and type == "B") or \
                                (i == 1 and type == "p" and ((enemy == "w" and 6 <= j <= 7) or (
                                        enemy == "b" and 4 <= j <= 5))) or \
                                (type == "Q") or (i == 1 and type == "K"):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((newRow, newCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for k in knightMoves:
            newRow = startRow + k[0]
            newCol = startCol + k[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                newPiece = self.board[newRow][newCol]
                if newPiece[0] == enemy and newPiece[1] == "N":
                    inCheck = True
                    checks.append((newRow, newCol, k[0], k[1]))
        return inCheck, pins, checks

    def makeMove(self, move):
        self.board[move.newRow][move.newCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.wKLocation = (move.newRow, move.newCol)
            self.whiteKingsideCastle = False
            self.whiteQueensideCastle = False
        elif move.pieceMoved == "bK":
            self.bKLocation = (move.newRow, move.newCol)
            self.blackKingsideCastle = False
            self.blackQueensideCastle = False
        if move.pieceMoved == "wR" and move.startCol == 0:
            self.whiteQueensideCastle = False
        elif move.pieceMoved == "wR" and move.startCol == 7:
            self.whiteKingsideCastle = False
        elif move.pieceMoved == "bR" and move.startCol == 0:
            self.blackQueensideCastle = False
        elif move.pieceMoved == "bR" and move.startCol == 7:
            self.blackKingsideCastle = False
        if move.pawnPromotion:
            promotedPiece = "Q"
            #promotedPiece = input("Q, B, R or N?")
            self.board[move.newRow][move.newCol] = move.pieceMoved[0] + promotedPiece
        if move.doublePawnMove:
            self.enPassantPossible = True
            self.pawnMoved = (move.newRow, move.newCol)
            self.enPassantPawns = ((move.newRow, move.newCol - 1), (move.newRow, move.newCol + 1))
        if move.enPassant:
            self.board[move.startRow][move.newCol] = "--"
        if move.castle:
            if not self.whiteToMove:
                if move.newRow == 7 and move.newCol == 6:
                    self.board[7][7] = "--"
                    self.board[7][5] = "wR"
                elif move.newRow == 7 and move.newCol == 2:
                    self.board[7][0] = "--"
                    self.board[7][3] = "wR"
            else:
                if move.newRow == 0 and move.newCol == 6:
                    self.board[0][7] = "--"
                    self.board[0][5] = "bR"
                elif move.newRow == 0 and move.newCol == 2:
                    self.board[0][0] = "--"
                    self.board[0][3] = "bR"
        if not move.capture:
            self.sinceCapture += 1
        else:
            self.sinceCapture = 0
        if not move.pieceMoved[1] == "p":
            self.sincePawnMoved += 1
        else:
            self.sincePawnMoved = 0

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.newRow][move.newCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.wKLocation = (move.startRow, move.startCol)
                self.whiteKingsideCastle = False
                self.whiteQueensideCastle = False
            elif move.pieceMoved == "bK":
                self.bKLocation = (move.startRow, move.startCol)
            if move.enPassant:
                self.board[move.newRow][move.newCol] = "--"
                self.board[move.startRow][move.newCol] = move.pieceCaptured
            if move.castle:
                if move.newCol - move.startCol == 2:
                    self.board[move.newRow][move.newCol + 1] = self.board[move.newRow][move.newCol - 1]
                    self.board[move.newRow][move.newCol - 1] = "--"
                else:
                    self.board[move.newRow][move.newCol - 2] = self.board[move.newRow][move.newCol + 1]
                    self.board[move.newRow][move.newCol + 1] = "--"
            self.checkmate = False
            self.stalemate = False


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSquare, newSquare, board, pawnPromotion=False, enPassant=False, doublePawnMove=False, castle=True):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.newRow = newSquare[0]
        self.newCol = newSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.newRow][self.newCol]
        self.capture = self.pieceCaptured != "--"
        self.pawnPromotion = pawnPromotion
        self.enPassant = enPassant
        if enPassant:
            self.pieceCaptured = "bp" if self.pieceMoved == "wp" else "wp"
        self.doublePawnMove = doublePawnMove
        self.castle = castle
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.newRow * 10 + self.newCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def toFileRank(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]

    def getChessNotation(self):
        return self.toFileRank(self.startRow, self.startCol) + self.toFileRank(self.newRow, self.newCol)
