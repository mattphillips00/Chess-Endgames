import numpy as np


class EndgameTable:
    def __init__(self):
        self.board = np.full((8, 8), "--")
        self.endgameTable3 = np.full((64, 64, 64, 2), -1)
        self.endgameTable4 = np.full((64, 64, 64, 64, 2), -1)
        self.endgameTable5 = np.full((64, 64, 64, 64, 64, 2), -1)
        self.getPieceMoves = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.wKLocation = (7, 4)
        self.bKLocation = (0, 4)
        self.distanceToCheckmate = 0
        self.pieces = []
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
        self.checkmates = []
        self.stalemate = False
        self.draw = False
        self.invalid = False
        self.undone = False
        self.pins = []
        self.checks = []
        self.sincePawnMoved = 0
        self.sinceCapture = 0
        self.code = 0
        self.moveLog = []
        self.moveLogNotation = []

    def initialPositions3(self, pieceTypes):

        """ Removing any positions in which pieces are on the same square """
        for i in range(0, 64):
            self.bKLocation = self.toRowCol(i)
            for j in range(0, 64):
                self.wKLocation = self.toRowCol(j)
                invalid = False

                if i == j:
                    self.endgameTable3[i][j] = -2
                    invalid = True
                elif i % 8 == 0:
                    if i - 8 == j or i - 7 == j or i + 1 == j or i + 8 == j or i + 9 == j:
                        self.endgameTable3[i][j] = -2
                        invalid = True
                elif i % 8 == 7:
                    if i - 9 == j or i - 8 == j or i - 1 == j or i + 7 == j or i + 8 == j:
                        self.endgameTable3[i][j] = -2
                        invalid = True
                else:
                    if i - 9 == j or i - 8 == j or i - 7 == j or i - 1 == j or i + 1 == j or i + 7 == j or i + 8 == j or i + 9 == j:
                        self.endgameTable3[i][j] = -2
                        invalid = True

                if not invalid:
                    for k in range(0, 64):

                        if i == k or j == k:
                            self.endgameTable3[i][j][k] = -2
                        else:
                            self.whiteToMove = True
                            self.pieces = []
                            self.addPiece(i, pieceTypes[0])
                            self.addPiece(j, pieceTypes[1])
                            self.addPiece(k, pieceTypes[2])
                            self.createBoard(self.pieces)
                            if self.pieces[2][2] == "wp" and self.pieces[2][0] == 0:
                                self.endgameTable3[i][j][k] = -2
                                invalid = True
                            elif self.pieces[2][2] == "bp" and self.pieces[2][0] == 7:
                                self.endgameTable3[i][j][k] = -2
                                invalid = True
                            if not invalid:
                                for m in range(0, 2):
                                    if m == 0 and self.whiteToMove:
                                        self.whiteToMove = False
                                        inCheck, pins, checks = self.pinsAndChecks()
                                        self.whiteToMove = True
                                        if inCheck:
                                            self.endgameTable3[i][j][k][m] = -2
                                    elif m == 1:
                                        self.bKLocation = self.toRowCol(i)
                                        moves = []
                                        self.whiteToMove = False
                                        inCheck, pins, checks = self.pinsAndChecks()
                                        self.bKLocation = self.toRowCol(i)
                                        if inCheck:
                                            self.getKingMoves(self.bKLocation[0], self.bKLocation[1], moves)
                                            if len(moves) == 0:
                                                self.endgameTable3[i][j][k][m] = 0
        return self.endgameTable3

    def initialPositions4(self, pieceTypes, sameColour):

        """ Removing any positions in which pieces are on the same square """
        for i in range(0, 64):
            self.bKLocation = self.toRowCol(i)
            for j in range(0, 64):
                self.wKLocation = self.toRowCol(j)
                invalid = False

                if i == j:
                    self.endgameTable4[i][j] = -2
                    invalid = True
                elif i % 8 == 0:
                    if i - 8 == j or i - 7 == j or i + 1 == j or i + 8 == j or i + 9 == j:
                        self.endgameTable4[i][j] = -2
                        invalid = True
                elif i % 8 == 7:
                    if i - 9 == j or i - 8 == j or i - 1 == j or i + 7 == j or i + 8 == j:
                        self.endgameTable4[i][j] = -2
                        invalid = True
                else:
                    if i - 9 == j or i - 8 == j or i - 7 == j or i - 1 == j or i + 1 == j or i + 7 == j or i + 8 == j or i + 9 == j:
                        self.endgameTable4[i][j] = -2
                        invalid = True

                if not invalid:
                    for k in range(0, 64):

                        if i == k or j == k:
                            self.endgameTable4[i][j][k] = -2
                        else:
                            for l in range(0, 64):

                                if i == l or j == l or k == l:
                                    self.endgameTable4[i][j][k][l] = -2
                                else:
                                    self.whiteToMove = True
                                    self.pieces = []
                                    self.addPiece(i, pieceTypes[0])
                                    self.addPiece(j, pieceTypes[1])
                                    self.addPiece(k, pieceTypes[2])
                                    self.addPiece(l, pieceTypes[3])
                                    self.createBoard(self.pieces)
                                    for p in range(2, 3):
                                        if self.pieces[p][2] == "wp" and self.pieces[p][0] == 0:
                                            self.endgameTable4[i][j][k][l] = -2
                                            invalid = True
                                        elif self.pieces[p][2] == "bp" and self.pieces[p][0] == 7:
                                            self.endgameTable4[i][j][k][l] = -2
                                            invalid = True
                                    if not invalid:
                                        for m in range(0, 2):
                                            self.whiteToMove = True
                                            inCheck, pins, checks = self.pinsAndChecks()
                                            whiteInCheck = True if inCheck else False
                                            self.whiteToMove = False
                                            inCheck, pins, checks = self.pinsAndChecks()
                                            blackInCheck = True if inCheck else False
                                            if whiteInCheck and blackInCheck:
                                                self.endgameTable4[i][j][k][l] = -2
                                            elif whiteInCheck and m == 1:
                                                self.endgameTable4[i][j][k][l][m] = -2
                                            elif blackInCheck and m == 0:
                                                self.endgameTable4[i][j][k][l][m] = -2
                                            elif whiteInCheck and not blackInCheck:
                                                self.whiteToMove = True
                                                self.wKLocation = self.toRowCol(j)
                                                moves = self.validMoves()
                                                if len(moves) == 0:
                                                    self.endgameTable4[i][j][k][l][0] = 0
                                            elif blackInCheck and not whiteInCheck:
                                                self.whiteToMove = False
                                                self.bKLocation = self.toRowCol(i)
                                                moves = self.validMoves()
                                                if len(moves) == 0:
                                                    self.endgameTable4[i][j][k][l][1] = 0

        if pieceTypes[2] == "wB" and pieceTypes[3] == "wB":
            for i in range(0, 64):
                for j in range(0, 64):
                    for k in range(0, 64):
                        for l in range(0, 64):
                            rowk, colk = self.toRowCol(k)
                            rowl, coll = self.toRowCol(l)
                            if not sameColour:
                                if (rowk % 2 == 0 and colk % 2 == 0) or (rowk % 2 != 0 and colk % 2 != 0):
                                    if (rowl % 2 == 0 and coll % 2 == 0) or (rowl % 2 != 0 and coll % 2 != 0):
                                        self.endgameTable4[i][j][k][l] = -2
                                elif (rowk % 2 == 0 and colk % 2 != 0) or (rowk % 2 != 0 and colk % 2 == 0):
                                    if (rowl % 2 == 0 and coll % 2 != 0) or (rowl % 2 != 0 and coll % 2 == 0):
                                        self.endgameTable4[i][j][k][l] = -2
                            else:
                                if (rowk % 2 == 0 and colk % 2 == 0) or (
                                        rowk % 2 != 0 and colk % 2 != 0):
                                    if (rowl % 2 == 0 and coll % 2 != 0) or (
                                            rowl % 2 != 0 and coll % 2 == 0):
                                        self.endgameTable4[i][j][k][l] = -2
                                elif (rowl % 2 == 0 and coll % 2 == 0) or (
                                        rowl % 2 != 0 and coll % 2 != 0):
                                    if (rowk % 2 == 0 and colk % 2 != 0) or (
                                            rowk % 2 != 0 and colk % 2 == 0):
                                        self.endgameTable4[i][j][k][l] = -2
        return self.endgameTable4

    def initialPositions5(self, pieceTypes, sameColour):

        """ Removing any positions in which pieces are on the same square """
        for i in range(0, 64):
            self.bKLocation = self.toRowCol(i)
            for j in range(0, 64):
                self.wKLocation = self.toRowCol(j)
                invalid = False

                if i == j:
                    self.endgameTable5[i][j] = -2
                    invalid = True
                elif i % 8 == 0:
                    if i - 8 == j or i - 7 == j or i + 1 == j or i + 8 == j or i + 9 == j:
                        self.endgameTable5[i][j] = -2
                        invalid = True
                elif i % 8 == 7:
                    if i - 9 == j or i - 8 == j or i - 1 == j or i + 7 == j or i + 8 == j:
                        self.endgameTable5[i][j] = -2
                        invalid = True
                else:
                    if i - 9 == j or i - 8 == j or i - 7 == j or i - 1 == j or i + 1 == j or i + 7 == j or i + 8 == j or i + 9 == j:
                        self.endgameTable5[i][j] = -2
                        invalid = True

                if not invalid:
                    for k in range(0, 64):

                        if i == k or j == k:
                            self.endgameTable5[i][j][k] = -2
                        else:
                            for l in range(0, 64):

                                if i == l or j == l or k == l:
                                    self.endgameTable5[i][j][k][l] = -2
                                else:
                                    for m in range(0, 64):

                                        if m == l or j == l or k == l:
                                            self.endgameTable5[i][j][k][l] = -2
                                        else:
                                            self.whiteToMove = True
                                            self.pieces = []
                                            self.addPiece(i, pieceTypes[0])
                                            self.addPiece(j, pieceTypes[1])
                                            self.addPiece(k, pieceTypes[2])
                                            self.addPiece(l, pieceTypes[3])
                                            self.addPiece(m, pieceTypes[4])
                                            self.createBoard(
                                                self.pieces)
                                            for p in range(2,
                                                           4):
                                                if self.pieces[p][2] == "wp" and self.pieces[p][0] == 0:
                                                    self.endgameTable5[i][j][k][l] = -2
                                                    invalid = True
                                                elif self.pieces[p][2] == "bp" and self.pieces[p][0] == 7:
                                                    self.endgameTable5[i][j][k][l] = -2
                                                    invalid = True
                                            if not invalid:
                                                for n in range(0, 2):
                                                    if n == 0 and self.whiteToMove:
                                                        self.whiteToMove = False
                                                        inCheck, pins, checks = self.pinsAndChecks()
                                                        self.whiteToMove = True
                                                        if inCheck:
                                                            self.endgameTable5[i][j][k][l][n] = -2
                                                    elif n == 1:
                                                        self.bKLocation = self.toRowCol(
                                                            i)
                                                        moves = []
                                                        self.whiteToMove = False
                                                        inCheck, pins, checks = self.pinsAndChecks()
                                                        self.bKLocation = self.toRowCol(
                                                            i)
                                                        if inCheck:
                                                            self.getKingMoves(self.bKLocation[0], self.bKLocation[1],
                                                                              moves)
                                                            if len(moves) == 0:
                                                                self.endgameTable5[i][j][k][l][n] = 0

        if pieceTypes[2] == "wB" and pieceTypes[3] == "wB":
            for i in range(0, 64):
                for j in range(0, 64):
                    for k in range(0, 64):
                        for l in range(0, 64):
                            for m in range(0, 64):
                                rowk, colk = self.toRowCol(k)
                                rowl, coll = self.toRowCol(l)
                                if not sameColour:
                                    if (rowk % 2 == 0 and colk % 2 == 0) or (rowk % 2 != 0 and colk % 2 != 0):
                                        if (rowl % 2 == 0 and coll % 2 == 0) or (rowl % 2 != 0 and coll % 2 != 0):
                                            self.endgameTable4[i][j][k][l] = -2
                                    elif (rowk % 2 == 0 and colk % 2 != 0) or (rowk % 2 != 0 and colk % 2 == 0):
                                        if (rowl % 2 == 0 and coll % 2 != 0) or (rowl % 2 != 0 and coll % 2 == 0):
                                            self.endgameTable4[i][j][k][l] = -2
                                else:
                                    if (rowk % 2 == 0 and colk % 2 == 0) or (rowk % 2 != 0 and colk % 2 != 0):
                                        if (rowl % 2 == 0 and coll % 2 != 0) or (rowl % 2 != 0 and coll % 2 == 0):
                                            self.endgameTable4[i][j][k][l][m] = -2
                                    elif (rowl % 2 == 0 and coll % 2 == 0) or (rowl % 2 != 0 and coll % 2 != 0):
                                        if (rowk % 2 == 0 and colk % 2 != 0) or (rowk % 2 != 0 and colk % 2 == 0):
                                            self.endgameTable4[i][j][k][l][m] = -2
        return self.endgameTable5

    def getInitialPositions(self, pieceTypes, sameColour=False):
        if len(pieceTypes) == 3:
            initialTable = self.initialPositions3(pieceTypes)
        elif len(pieceTypes) == 4:
            initialTable = self.initialPositions4(pieceTypes, sameColour)
        else:
            initialTable = self.initialPositions5(pieceTypes, sameColour)
        return initialTable

    def mainLoop3(self, pieceTypes, initialTable):
        self.endgameTable3 = initialTable
        self.distanceToCheckmate = 0
        done = False

        while not done:
            changed = False
            self.distanceToCheckmate += 1
            for i in range(0, 64):
                for j in range(0, 64):
                    for k in range(0, 64):
                        if self.endgameTable3[i][j][k][1] == self.distanceToCheckmate - 1:
                            self.pieces = []
                            self.addPiece(i, pieceTypes[0])
                            self.addPiece(j, pieceTypes[1])
                            self.addPiece(k, pieceTypes[2])
                            self.createBoard(self.pieces)
                            self.whiteToMove = True
                            moves = self.validMoves()
                            if len(moves) != 0:
                                for move in range(len(moves)):
                                    pieceMoved = self.toPosition(moves[move].startRow, moves[move].startCol)
                                    newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                                    if j == pieceMoved:
                                        if self.endgameTable3[i][newPosition][k][0] == -1 and newPosition != i:
                                            self.endgameTable3[i][newPosition][k][0] = self.distanceToCheckmate
                                            changed = True
                                    elif k == pieceMoved:
                                        if self.endgameTable3[i][j][newPosition][0] == -1 and newPosition != i:
                                            self.endgameTable3[i][j][newPosition][0] = self.distanceToCheckmate
                                            changed = True
            self.distanceToCheckmate += 1
            for i in range(0, 64):
                for j in range(0, 64):
                    for k in range(0, 64):
                        if self.endgameTable3[i][j][k][0] == self.distanceToCheckmate - 1:
                            self.pieces = []
                            self.addPiece(i, pieceTypes[0])
                            self.addPiece(j, pieceTypes[1])
                            self.addPiece(k, pieceTypes[2])
                            self.createBoard(self.pieces)
                            self.whiteToMove = False
                            moves = []
                            row, col = self.toRowCol(i)
                            self.getKingMovesNoCheck(row, col, moves)
                            if len(moves) != 0:
                                for move in range(len(moves)):
                                    newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                                    if self.endgameTable3[newPosition][j][k][1] == -1:
                                        self.pieces = []
                                        self.addPiece(newPosition, pieceTypes[0])
                                        self.addPiece(j, pieceTypes[1])
                                        self.addPiece(k, pieceTypes[2])
                                        self.createBoard(self.pieces)
                                        self.whiteToMove = False
                                        newMoves = []
                                        newRow, newCol = self.toRowCol(newPosition)
                                        self.getKingMoves(newRow, newCol, newMoves)
                                        valid = True
                                        previousMove = False
                                        if len(newMoves) != 0:
                                            for newMove in range(len(newMoves)):
                                                thirdPosition = self.toPosition(newMoves[newMove].newRow, newMoves[newMove].newCol)
                                                if newMoves[newMove].capture:
                                                    self.endgameTable3[newPosition][j][k][1] = -3
                                                    valid = False
                                                if self.endgameTable3[thirdPosition][j][k][0] == self.distanceToCheckmate - 1:
                                                    previousMove = True
                                                if self.endgameTable3[thirdPosition][j][k][0] > self.distanceToCheckmate - 1 or \
                                                        self.endgameTable3[thirdPosition][j][k][0] == -1:
                                                    valid = False
                                            if valid and previousMove:
                                                self.endgameTable3[newPosition][j][k][1] = self.distanceToCheckmate
                                                changed = True

            if not changed:
                done = True

        for i in range(0, 64):
            for j in range(0, 64):
                for k in range(0, 64):
                    for m in range(0, 2):
                        if self.endgameTable3[i][j][k][m] == -1:
                            self.endgameTable3[i][j][k][m] = -3

    def mainLoop4(self, pieceTypes, initialTable, table2, table3):
        self.endgameTable4 = initialTable
        self.distanceToCheckmate = 0
        done = False

        while not done:
            changed = False
            self.distanceToCheckmate += 1
            checkmates = np.where(initialTable == self.distanceToCheckmate - 1)
            positions = np.array(list(zip(checkmates[0], checkmates[1], checkmates[2], checkmates[3], checkmates[4])))
            for p in positions:
                if p[4] == 1:
                    self.pieces = []
                    self.addPiece(p[0], pieceTypes[0])
                    self.addPiece(p[1], pieceTypes[1])
                    self.addPiece(p[2], pieceTypes[2])
                    self.addPiece(p[3], pieceTypes[3])
                    self.createBoard(self.pieces)
                    self.whiteToMove = True
                    moves = self.validMoves()
                    if len(moves) != 0:
                        for move in range(len(moves)):
                            pieceMoved = self.toPosition(moves[move].startRow, moves[move].startCol)
                            newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                            if p[1] == pieceMoved:
                                if self.endgameTable4[p[0]][newPosition][p[2]][p[3]][0] == -1 and newPosition != p[0]:
                                    self.endgameTable4[p[0]][newPosition][p[2]][p[3]][0] = self.distanceToCheckmate
                                    changed = True
                            elif p[2] == pieceMoved:
                                if self.endgameTable4[p[0]][p[1]][newPosition][p[3]][0] == -1 and newPosition != p[0]:
                                    self.endgameTable4[p[0]][p[1]][newPosition][p[3]][0] = self.distanceToCheckmate
                                    changed = True
                            elif p[3] == pieceMoved:
                                if self.endgameTable4[p[0]][p[1]][p[2]][newPosition][0] == -1 and newPosition != p[0]:
                                    self.endgameTable4[p[0]][p[1]][p[2]][newPosition][0] = self.distanceToCheckmate
                                    changed = True
                elif p[4] == 0:
                    self.pieces = []
                    self.addPiece(p[0], pieceTypes[0])
                    self.addPiece(p[1], pieceTypes[1])
                    self.addPiece(p[2], pieceTypes[2])
                    self.addPiece(p[3], pieceTypes[3])
                    self.createBoard(self.pieces)
                    self.whiteToMove = False
                    moves = self.validMoves()
                    if len(moves) != 0:
                        for move in range(len(moves)):
                            pieceMoved = self.toPosition(moves[move].startRow, moves[move].startCol)
                            newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                            if p[0] == pieceMoved:
                                if self.endgameTable4[newPosition][p[1]][p[2]][p[3]][1] == -1 and newPosition != p[1]:
                                    self.endgameTable4[newPosition][p[1]][p[2]][p[3]][1] = self.distanceToCheckmate
                                    changed = True
                            elif p[2] == pieceMoved:
                                if self.endgameTable4[p[0]][p[1]][newPosition][p[3]][1] == -1 and newPosition != p[1]:
                                    self.endgameTable4[p[0]][p[1]][newPosition][p[3]][1] = self.distanceToCheckmate
                                    changed = True
                            elif p[3] == pieceMoved:
                                if self.endgameTable4[p[0]][p[1]][p[2]][newPosition][1] == -1 and newPosition != p[1]:
                                    self.endgameTable4[p[0]][p[1]][p[2]][newPosition][1] = self.distanceToCheckmate
                                    changed = True

            checkmates = np.where(table2 == self.distanceToCheckmate - 1)
            positions = np.array(list(zip(checkmates[0], checkmates[1], checkmates[2], checkmates[3])))
            for p in positions:
                self.pieces = []
                self.addPiece(p[0], pieceTypes[0])
                self.addPiece(p[1], pieceTypes[1])
                self.addPiece(p[2], pieceTypes[2])
                self.createBoard(self.pieces)
                self.whiteToMove = True
                moves = self.validMoves()
                if len(moves) != 0:
                    for move in range(len(moves)):
                        pieceMoved = self.toPosition(moves[move].startRow, moves[move].startCol)
                        newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                        if p[1] == pieceMoved:
                            if self.endgameTable4[p[0]][newPosition][p[2]][p[1]][0] == -1:
                                self.endgameTable4[p[0]][newPosition][p[2]][p[1]][0] = self.distanceToCheckmate
                        elif p[2] == pieceMoved:
                            if self.endgameTable4[p[0]][p[1]][newPosition][p[2]][0] == -1:
                                self.endgameTable4[p[0]][p[1]][newPosition][p[2]][0] = self.distanceToCheckmate

            checkmates = np.where(table3 == self.distanceToCheckmate - 1)
            positions = np.array(list(zip(checkmates[1], checkmates[0], checkmates[2], checkmates[3])))
            for p in positions:
                self.pieces = []
                self.addPiece(p[0], pieceTypes[0])
                self.addPiece(p[1], pieceTypes[1])
                self.addPiece(p[2], pieceTypes[3])
                self.createBoard(self.pieces)
                self.whiteToMove = False
                moves = self.validMoves()
                if len(moves) != 0:
                    for move in range(len(moves)):
                        pieceMoved = self.toPosition(moves[move].startRow, moves[move].startCol)
                        newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                        if p[0] == pieceMoved:
                            if self.endgameTable4[newPosition][p[1]][p[0]][p[2]][1] == -1:
                                self.endgameTable4[newPosition][p[1]][p[0]][p[2]][1] = self.distanceToCheckmate
                        elif p[2] == pieceMoved:
                            if self.endgameTable4[p[0]][p[1]][p[2]][newPosition][1] == -1:
                                self.endgameTable4[p[0]][p[1]][p[2]][newPosition][1] = self.distanceToCheckmate

            self.distanceToCheckmate += 1
            checkmates = np.where(initialTable == self.distanceToCheckmate - 1)
            positions = np.array(list(zip(checkmates[0], checkmates[1], checkmates[2], checkmates[3], checkmates[4])))
            for p in positions:
                if p[4] == 0:
                    self.pieces = []
                    self.addPiece(p[0], pieceTypes[0])
                    self.addPiece(p[1], pieceTypes[1])
                    self.addPiece(p[2], pieceTypes[2])
                    self.addPiece(p[3], pieceTypes[3])
                    self.createBoard(self.pieces)
                    self.whiteToMove = False
                    moves = []
                    row, col = self.toRowCol(p[0])
                    self.getKingMovesNoCheck(row, col, moves)
                    if len(moves) != 0:
                        for move in range(len(moves)):
                            newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                            if self.endgameTable4[newPosition][p[1]][p[2]][p[3]][1] == -1:
                                self.pieces = []
                                self.addPiece(newPosition, pieceTypes[0])
                                self.addPiece(p[1], pieceTypes[1])
                                self.addPiece(p[2], pieceTypes[2])
                                self.addPiece(p[3], pieceTypes[3])
                                self.createBoard(self.pieces)
                                self.whiteToMove = False
                                self.bKLocation = self.toRowCol(newPosition)
                                newMoves = self.validMoves()
                                valid = True
                                capture = False
                                if len(newMoves) != 0:
                                    for newMove in range(len(newMoves)):
                                        pieceMoved = self.toPosition(newMoves[newMove].startRow,
                                                                     newMoves[newMove].startCol)
                                        thirdPosition = self.toPosition(newMoves[newMove].newRow,
                                                                        newMoves[newMove].newCol)
                                        if newPosition == pieceMoved:
                                            if self.endgameTable4[thirdPosition][p[1]][p[2]][p[3]][0] == -1:
                                                valid = False
                                        elif p[2] == pieceMoved:
                                            if self.endgameTable4[p[0]][p[1]][thirdPosition][p[3]][0] == -1:
                                                valid = False
                                        elif p[3] == pieceMoved:
                                            if self.endgameTable4[p[0]][p[1]][p[2]][thirdPosition][0] == -1:
                                                valid = False
                                        if newMoves[newMove].capture:
                                            capture = True
                                    if valid and not capture:
                                        self.endgameTable4[newPosition][p[1]][p[2]][p[3]][1] = self.distanceToCheckmate
                                        changed = True
                    if pieceTypes[2][0] == "b":
                        self.pieces = []
                        self.addPiece(p[2], pieceTypes[2])
                        self.createBoard(self.pieces)
                        self.whiteToMove = False
                        moves = self.validMoves()
                        if len(moves) != 0:
                            for move in range(len(moves)):
                                newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                                if self.endgameTable4[p[0]][p[1]][newPosition][p[3]][1] == -1:
                                    self.pieces = []
                                    self.addPiece(p[0], pieceTypes[0])
                                    self.addPiece(p[1], pieceTypes[1])
                                    self.addPiece(newPosition, pieceTypes[2])
                                    self.addPiece(p[3], pieceTypes[3])
                                    self.createBoard(self.pieces)
                                    self.whiteToMove = False
                                    self.bKLocation = self.toRowCol(p[0])
                                    newMoves = self.validMoves()
                                    valid = True
                                    capture = False
                                    if len(newMoves) != 0:
                                        for newMove in range(len(newMoves)):
                                            pieceMoved = self.toPosition(newMoves[newMove].startRow,
                                                                         newMoves[newMove].startCol)
                                            thirdPosition = self.toPosition(newMoves[newMove].newRow,
                                                                            newMoves[newMove].newCol)
                                            if newPosition == pieceMoved:
                                                if self.endgameTable4[p[0]][p[1]][thirdPosition][p[3]][0] == -1:
                                                    valid = False
                                            elif p[0] == pieceMoved:
                                                if self.endgameTable4[thirdPosition][p[1]][newPosition][p[3]][0] == -1:
                                                    valid = False
                                            elif p[3] == pieceMoved:
                                                if self.endgameTable4[p[0]][p[1]][newPosition][thirdPosition][0] == -1:
                                                    valid = False
                                            if newMoves[newMove].capture:
                                                capture = True
                                        if valid and not capture:
                                            self.endgameTable4[p[0]][p[1]][newPosition][p[3]][
                                                1] = self.distanceToCheckmate
                                            changed = True
                    elif pieceTypes[3][0] == "b":
                        self.pieces = []
                        self.addPiece(p[3], pieceTypes[3])
                        self.createBoard(self.pieces)
                        self.whiteToMove = False
                        moves = self.validMoves()
                        if len(moves) != 0:
                            for move in range(len(moves)):
                                newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                                if self.endgameTable4[p[0]][p[1]][p[2]][newPosition][1] == -1:
                                    self.pieces = []
                                    self.addPiece(p[0], pieceTypes[0])
                                    self.addPiece(p[1], pieceTypes[1])
                                    self.addPiece(p[2], pieceTypes[2])
                                    self.addPiece(newPosition, pieceTypes[3])
                                    self.createBoard(self.pieces)
                                    self.whiteToMove = False
                                    self.bKLocation = self.toRowCol(p[0])
                                    newMoves = self.validMoves()
                                    valid = True
                                    capture = False
                                    if len(newMoves) != 0:
                                        for newMove in range(len(newMoves)):
                                            pieceMoved = self.toPosition(newMoves[newMove].startRow,
                                                                         newMoves[newMove].startCol)
                                            thirdPosition = self.toPosition(newMoves[newMove].newRow,
                                                                            newMoves[newMove].newCol)
                                            if newPosition == pieceMoved:
                                                if self.endgameTable4[p[0]][p[1]][p[2]][thirdPosition][0] == -1:
                                                    valid = False
                                            elif p[0] == pieceMoved:
                                                if self.endgameTable4[thirdPosition][p[1]][p[2]][newPosition][0] == -1:
                                                    valid = False
                                            elif p[2] == pieceMoved:
                                                if self.endgameTable4[p[0]][p[1]][thirdPosition][newPosition][0] == -1:
                                                    valid = False
                                            if newMoves[newMove].capture:
                                                capture = True
                                        if valid and not capture:
                                            self.endgameTable4[p[0]][p[1]][p[2]][newPosition][
                                                1] = self.distanceToCheckmate
                                            changed = True
                elif p[4] == 1:
                    self.pieces = []
                    self.addPiece(p[0], pieceTypes[0])
                    self.addPiece(p[1], pieceTypes[1])
                    self.addPiece(p[2], pieceTypes[2])
                    self.addPiece(p[3], pieceTypes[3])
                    self.createBoard(self.pieces)
                    self.whiteToMove = True
                    moves = []
                    row, col = self.toRowCol(p[1])
                    self.getKingMovesNoCheck(row, col, moves)
                    if len(moves) != 0:
                        for move in range(len(moves)):
                            newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                            if self.endgameTable4[p[0]][newPosition][p[2]][p[3]][0] == -1:
                                self.pieces = []
                                self.addPiece(p[0], pieceTypes[0])
                                self.addPiece(newPosition, pieceTypes[1])
                                self.addPiece(p[2], pieceTypes[2])
                                self.addPiece(p[3], pieceTypes[3])
                                self.createBoard(self.pieces)
                                self.whiteToMove = True
                                self.wKLocation = self.toRowCol(newPosition)
                                newMoves = self.validMoves()
                                valid = True
                                capture = False
                                if len(newMoves) != 0:
                                    for newMove in range(len(newMoves)):
                                        pieceMoved = self.toPosition(newMoves[newMove].startRow,
                                                                     newMoves[newMove].startCol)
                                        thirdPosition = self.toPosition(newMoves[newMove].newRow,
                                                                        newMoves[newMove].newCol)
                                        if newPosition == pieceMoved:
                                            if self.endgameTable4[p[0]][thirdPosition][p[2]][p[3]][1] == -1:
                                                valid = False
                                        elif p[2] == pieceMoved:
                                            if self.endgameTable4[p[0]][p[1]][thirdPosition][p[3]][1] == -1:
                                                valid = False
                                        elif p[3] == pieceMoved:
                                            if self.endgameTable4[p[0]][p[1]][p[2]][thirdPosition][1] == -1:
                                                valid = False
                                        if newMoves[newMove].capture:
                                            capture = True
                                    if valid and not capture:
                                        self.endgameTable4[p[0]][newPosition][p[2]][p[3]][0] = self.distanceToCheckmate
                                        changed = True
                    if pieceTypes[2][0] == "w":
                        self.pieces = []
                        self.addPiece(p[2], pieceTypes[2])
                        self.createBoard(self.pieces)
                        self.whiteToMove = True
                        moves = self.validMoves()
                        if len(moves) != 0:
                            for move in range(len(moves)):
                                newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                                if self.endgameTable4[p[0]][p[1]][newPosition][p[3]][0] == -1:
                                    self.pieces = []
                                    self.addPiece(p[0], pieceTypes[0])
                                    self.addPiece(p[1], pieceTypes[1])
                                    self.addPiece(newPosition, pieceTypes[2])
                                    self.addPiece(p[3], pieceTypes[3])
                                    self.createBoard(self.pieces)
                                    self.whiteToMove = True
                                    self.wKLocation = self.toRowCol(p[1])
                                    newMoves = self.validMoves()
                                    valid = True
                                    capture = False
                                    if len(newMoves) != 0:
                                        for newMove in range(len(newMoves)):
                                            pieceMoved = self.toPosition(newMoves[newMove].startRow,
                                                                         newMoves[newMove].startCol)
                                            thirdPosition = self.toPosition(newMoves[newMove].newRow,
                                                                            newMoves[newMove].newCol)
                                            if newPosition == pieceMoved:
                                                if self.endgameTable4[p[0]][p[1]][thirdPosition][p[3]][1] == -1:
                                                    valid = False
                                            elif p[0] == pieceMoved:
                                                if self.endgameTable4[thirdPosition][p[1]][p[2]][p[3]][1] == -1:
                                                    valid = False
                                            elif p[3] == pieceMoved:
                                                if self.endgameTable4[p[0]][p[1]][p[2]][thirdPosition][1] == -1:
                                                    valid = False
                                            if newMoves[newMove].capture:
                                                capture = True
                                        if valid and not capture:
                                            self.endgameTable4[p[0]][p[1]][newPosition][p[3]][
                                                0] = self.distanceToCheckmate
                                            changed = True
                    elif pieceTypes[3][0] == "w":
                        self.pieces = []
                        self.addPiece(p[3], pieceTypes[3])
                        self.createBoard(self.pieces)
                        self.whiteToMove = True
                        moves = self.validMoves()
                        if len(moves) != 0:
                            for move in range(len(moves)):
                                newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                                if self.endgameTable4[p[0]][p[1]][p[2]][newPosition][0] == -1:
                                    self.pieces = []
                                    self.addPiece(p[0], pieceTypes[0])
                                    self.addPiece(p[1], pieceTypes[1])
                                    self.addPiece(p[2], pieceTypes[2])
                                    self.addPiece(newPosition, pieceTypes[3])
                                    self.createBoard(self.pieces)
                                    self.whiteToMove = True
                                    self.wKLocation = self.toRowCol(p[1])
                                    newMoves = self.validMoves()
                                    valid = True
                                    capture = False
                                    if len(newMoves) != 0:
                                        for newMove in range(len(newMoves)):
                                            pieceMoved = self.toPosition(newMoves[newMove].startRow,
                                                                         newMoves[newMove].startCol)
                                            thirdPosition = self.toPosition(newMoves[newMove].newRow,
                                                                            newMoves[newMove].newCol)
                                            if newPosition == pieceMoved:
                                                if self.endgameTable4[p[0]][p[1]][p[2]][thirdPosition][1] == -1:
                                                    valid = False
                                            elif p[0] == pieceMoved:
                                                if self.endgameTable4[thirdPosition][p[1]][p[2]][p[3]][1] == -1:
                                                    valid = False
                                            elif p[2] == pieceMoved:
                                                if self.endgameTable4[p[0]][p[1]][thirdPosition][p[3]][1] == -1:
                                                    valid = False
                                            if newMoves[newMove].capture:
                                                capture = True
                                        if valid and not capture:
                                            self.endgameTable4[p[0]][p[1]][p[2]][newPosition][
                                                0] = self.distanceToCheckmate
                                            changed = True
            if not changed:
                done = True

        self.endgameTable4 = np.where(initialTable == -1, -3, initialTable)

    def mainLoop5(self, pieceTypes, initialTable):
        self.endgameTable5 = initialTable
        self.distanceToCheckmate = 0
        done = False

        while not done:
            changed = False
            self.distanceToCheckmate += 1
            for i in range(0, 64):
                for j in range(0, 64):
                    for k in range(0, 64):
                        for l in range(0, 64):
                            for m in range(0, 64):
                                if self.endgameTable5[i][j][k][l][m][1] == self.distanceToCheckmate - 1:
                                    self.pieces = []
                                    self.addPiece(i, pieceTypes[0])
                                    self.addPiece(j, pieceTypes[1])
                                    self.addPiece(k, pieceTypes[2])
                                    self.addPiece(l, pieceTypes[3])
                                    self.addPiece(m, pieceTypes[4])
                                    self.createBoard(self.pieces)
                                    self.whiteToMove = True
                                    moves = self.validMoves()
                                    if len(moves) != 0:
                                        for move in range(len(moves)):
                                            pieceMoved = self.toPosition(moves[move].startRow, moves[move].startCol)
                                            newPosition = self.toPosition(moves[move].newRow, moves[move].newCol)
                                            if j == pieceMoved:
                                                if self.endgameTable5[i][newPosition][k][l][m][0] == -1 and newPosition != i:
                                                    self.endgameTable5[i][newPosition][k][l][m][
                                                        0] = self.distanceToCheckmate
                                                    changed = True
                                            elif k == pieceMoved:
                                                if self.endgameTable5[i][j][newPosition][l][m][0] == -1 and newPosition != i:
                                                    self.endgameTable5[i][j][newPosition][l][m][0] = self.distanceToCheckmate
                                                    changed = True
                                            elif l == pieceMoved:
                                                if self.endgameTable5[i][j][k][newPosition][m][0] == -1 and newPosition != i:
                                                    self.endgameTable5[i][j][k][newPosition][m][
                                                        0] = self.distanceToCheckmate
                                                    changed = True
                                            elif m == pieceMoved:
                                                if self.endgameTable5[i][j][k][l][newPosition][0] == -1 and newPosition != i:
                                                    self.endgameTable5[i][j][k][l][newPosition][
                                                        0] = self.distanceToCheckmate
                                                    changed = True
            self.distanceToCheckmate += 1
            for i in range(0, 64):
                for j in range(0, 64):
                    for k in range(0, 64):
                        for l in range(0, 64):
                            for m in range(0, 64):
                                if self.endgameTable5[i][j][k][l][m][0] == self.distanceToCheckmate - 1:
                                    self.pieces = []
                                    self.addPiece(i, pieceTypes[0])
                                    self.addPiece(j, pieceTypes[1])
                                    self.addPiece(k, pieceTypes[2])
                                    self.addPiece(l, pieceTypes[3])
                                    self.addPiece(m, pieceTypes[4])
                                    self.createBoard(self.pieces)
                                    self.whiteToMove = False
                                    moves = []
                                    row, col = self.toRowCol(i)
                                    self.getKingMovesNoCheck(row, col, moves)
                                    if len(moves) != 0:
                                        for move in range(len(moves)):
                                            newPosition = self.toPosition(moves[move].newRow, moves[
                                                move].newCol)
                                            if self.endgameTable5[newPosition][j][k][l][m][1] == -1:
                                                self.pieces = []
                                                self.addPiece(newPosition, pieceTypes[0])
                                                self.addPiece(j, pieceTypes[1])
                                                self.addPiece(k, pieceTypes[2])
                                                self.addPiece(l, pieceTypes[3])
                                                self.addPiece(m, pieceTypes[4])
                                                self.createBoard(self.pieces)
                                                self.whiteToMove = False
                                                newMoves = []
                                                newRow, newCol = self.toRowCol(newPosition)
                                                self.getKingMoves(newRow, newCol, newMoves)
                                                valid = True
                                                previousMove = False
                                                if len(newMoves) != 0:
                                                    for newMove in range(len(newMoves)):
                                                        thirdPosition = self.toPosition(newMoves[newMove].newRow,
                                                                                        newMoves[newMove].newCol)
                                                        if newMoves[newMove].capture:
                                                            self.endgameTable5[newPosition][j][k][l][m][1] = -3
                                                            valid = False
                                                        if self.endgameTable5[thirdPosition][j][k][l][m][0] == self.distanceToCheckmate - 1:
                                                            previousMove = True
                                                        if self.endgameTable5[thirdPosition][j][k][l][m][0] > self.distanceToCheckmate - 1 or \
                                                                self.endgameTable5[thirdPosition][j][k][l][m][0] == -1:
                                                            valid = False
                                                    if valid and previousMove:
                                                        self.endgameTable5[newPosition][j][k][l][m][1] = self.distanceToCheckmate
                                                        changed = True
            if not changed:
                done = True

        for i in range(0, 64):
            for j in range(0, 64):
                for k in range(0, 64):
                    for l in range(0, 64):
                        for m in range(0, 64):
                            for n in range(0, 2):
                                if self.endgameTable5[i][j][k][l][m][n] == -1:
                                    self.endgameTable5[i][j][k][l][m][n] = -3

    def createEndgameTable(self, pieceTypes, initialTable, table2, table3):
        if len(pieceTypes) == 3:
            self.mainLoop3(pieceTypes, initialTable)
        elif len(pieceTypes) == 4:
            self.mainLoop4(pieceTypes, initialTable, table2, table3)
        else:
            self.mainLoop5(pieceTypes, initialTable)

    @staticmethod
    def toRowCol(position):
        row = position // 8
        col = position % 8
        return row, col

    @staticmethod
    def toPosition(row, col):
        return (row * 8) + col

    def printMessage(self, piecePositions, initialTable, initial=True):

        if len(piecePositions) == 3:
            if self.whiteToMove:
                code = initialTable[piecePositions[0]][piecePositions[1]][piecePositions[2]][0]
            else:
                code = initialTable[piecePositions[0]][piecePositions[1]][piecePositions[2]][1]
        elif len(piecePositions) == 4:
            if self.whiteToMove:
                code = initialTable[piecePositions[0]][piecePositions[1]][piecePositions[2]][piecePositions[3]][0]
            else:
                code = initialTable[piecePositions[0]][piecePositions[1]][piecePositions[2]][piecePositions[3]][1]
        else:
            if self.whiteToMove:
                code = initialTable[piecePositions[0]][piecePositions[1]][piecePositions[2]][piecePositions[3]][
                    piecePositions[4]][0]
            else:
                code = initialTable[piecePositions[0]][piecePositions[1]][piecePositions[2]][piecePositions[3]][
                    piecePositions[4]][1]

        if code == -3 and initial:
            print("The initial position is a draw.")
        elif code == -3 and not initial:
            print("Draw.")
        elif code == -2 and initial:
            print("The initial position is invalid, please pick a new position.")
            self.invalid = True
        elif code == 0 and initial:
            print("The initial position is checkmate.")
        elif code == 0 and not initial:
            print("Checkmate.")
        elif code == 1:
            print("White wins in", code, "move")
        elif code > 1:
            print("White wins in", code, "moves")

        self.code = code

    def printGameTypeMessage(self, pieceTypes, endgameTable, sameColour):
        if len(pieceTypes) == 3:
            if pieceTypes[2] == "wB" or pieceTypes[2] == "wN":
                print("Checkmate cannot be forced by white due to insufficient material")
            else:
                self.printWinningPositions(pieceTypes, endgameTable)
        elif len(pieceTypes) == 4:
            if pieceTypes[2] == "wB" and pieceTypes[3] == "wB" and sameColour:
                print("Checkmate cannot be forced by white due to insufficient material")
            elif pieceTypes[2] == "wN" and pieceTypes[3] == "wN":
                print("Checkmate cannot be forced by white due to insufficient material")
            else:
                self.printWinningPositions(pieceTypes, endgameTable)
        elif len(pieceTypes) == 5:
            if pieceTypes[2] == "wB" and pieceTypes[3] == "wB" and pieceTypes[4] == "wB" and sameColour:
                print("Checkmate cannot be forced by white due to insufficient material")
            else:
                self.printWinningPositions(pieceTypes, endgameTable)

    @staticmethod
    def initialGame(piecePositions, initialTable):
        if len(piecePositions) == 3:
            if initialTable[piecePositions[0]][piecePositions[1]][piecePositions[2]][0] <= 0:
                return True
        elif len(piecePositions) == 4:
            if initialTable[piecePositions[0]][piecePositions[1]][piecePositions[2]][piecePositions[3]][0] <= 0:
                return True
        elif len(piecePositions) == 5:
            if \
                    initialTable[piecePositions[0]][piecePositions[1]][piecePositions[2]][piecePositions[3]][piecePositions[4]][
                        0] <= 0:
                return True
        else:
            return False

    @staticmethod
    def printWinningPositions(pieceTypes, endgameTable):
        winningPositions = 0
        drawPositions = 0
        if len(pieceTypes) == 3:
            for i in range(0, 64):
                for j in range(0, 64):
                    for k in range(0, 64):
                        if endgameTable[i][j][k][1] == -3:
                            drawPositions += 1
                        if endgameTable[i][j][k][1] > -1:
                            winningPositions += 1
        elif len(pieceTypes) == 4:
            for i in range(0, 64):
                for j in range(0, 64):
                    for k in range(0, 64):
                        for l in range(0, 64):
                            if endgameTable[i][j][k][l][1] == -3:
                                drawPositions += 1
                            if endgameTable[i][j][k][l][1] > -1:
                                winningPositions += 1
        elif len(pieceTypes) == 5:
            for i in range(0, 64):
                for j in range(0, 64):
                    for k in range(0, 64):
                        for l in range(0, 64):
                            for m in range(0, 64):
                                if endgameTable[i][j][k][l][m][1] == -3:
                                    drawPositions += 1
                                if endgameTable[i][j][k][l][m][1] > -1:
                                    winningPositions += 1
        totalPositions = drawPositions + winningPositions
        if len(pieceTypes) == 3:
            print("K" + pieceTypes[2][1] + "vK Endgame:")
        print("The percentage of winning positions for white is: ",
              "{0:.3}%".format((winningPositions / totalPositions) * 100))

    def createBoard(self, pieces):
        self.board[:] = "--"
        for piece in pieces:
            self.board[piece[0], piece[1]] = piece[2]

    def addPiece(self, position, type):
        row = self.toRowCol(position)[0]
        col = self.toRowCol(position)[1]
        self.pieces.append((row, col, type))

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
                        if self.board[row + 2 * moveDirection][col - 1][0] == enemy or \
                                self.board[row + 2 * moveDirection][col + 1][0] == enemy:
                            moves.append(
                                Move((row, col), (row + 2 * moveDirection, col), self.board, doublePawnMove=True))
                            if self.board[row + 2 * moveDirection][col - 1][0] == enemy and \
                                    self.board[row + 2 * moveDirection][col + 1][0] == enemy:
                                self.doubleEnPassant = True
                        else:
                            moves.append(Move((row, col), (row + 2 * moveDirection, col), self.board))
                    elif col == 0:
                        if self.board[row + 2 * moveDirection][col + 1][0] == enemy:
                            moves.append(
                                Move((row, col), (row + 2 * moveDirection, col), self.board, doublePawnMove=True))
                            self.pawnMoved = (row + 2 * moveDirection, col)
                        else:
                            moves.append(Move((row, col), (row + 2 * moveDirection, col), self.board))
                    elif col == 7:
                        if self.board[row + 2 * moveDirection][col - 1][0] == enemy:
                            moves.append(
                                Move((row, col), (row + 2 * moveDirection, col), self.board, doublePawnMove=True))
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
            moves.append(Move((row, col), (self.pawnMoved[0] - 1, self.pawnMoved[1]), self.board, enPassant=True))
        else:
            moves.append(Move((row, col), (self.pawnMoved[0] + 1, self.pawnMoved[1]), self.board, enPassant=True))
        if self.doubleEnPassant:
            self.enPassantPossible = True
            self.doubleEnPassant = False
        else:
            self.enPassantPossible = False

    def getKnightMoves(self, row, col, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
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
                    if ally == "w":
                        self.wKLocation = (newRow, newCol)
                    else:
                        self.bKLocation = (newRow, newCol)
                    inCheck, pins, checks = self.pinsAndChecks()
                    if not inCheck:
                        moves.append(Move((row, col), (newRow, newCol), self.board))
                    if ally == "w":
                        self.wKLocation = (row, col)
                    else:
                        self.bKLocation = (row, col)

        if not self.inCheck:
            self.kingsideCastle(row, col, moves)
            self.queensideCastle(row, col, moves)

    def getKingMovesNoCheck(self, row, col, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally = "w" if self.whiteToMove else "b"
        for k in kingMoves:
            newRow = row + k[0]
            newCol = col + k[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                newPiece = self.board[newRow][newCol]
                if newPiece[0] != ally:
                    if ally == "w":
                        self.wKLocation = (newRow, newCol)
                    else:
                        self.bKLocation = (newRow, newCol)
                    if not Move((row, col), (newRow, newCol), self.board) in moves:
                        moves.append(Move((row, col), (newRow, newCol), self.board))
                    if ally == "w":
                        self.wKLocation = (row, col)
                    else:
                        self.bKLocation = (row, col)

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

    def castlingPossible(self, row, col, moves):
        m = len(moves)
        self.kingsideCastle(row, col, moves)
        self.queensideCastle(row, col, moves)
        if len(moves) > m:
            print("Castling might be possible for white based on the initial position.")
        else:
            print("Castling is impossible for white based on the initial position.")

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
        self.whiteToMove = not self.whiteToMove
        self.undone = False
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
            # promotedPiece = input("Q, B, R or N?")
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
        self.validMoves()
        self.moveLogNotation.append(self.getChessNotation(move))
        self.moveLog.append(move)
        print("White to move") if self.whiteToMove else print("Black to move")

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.newRow][move.newCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.wKLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.bKLocation = (move.startRow, move.startCol)
            if move.enPassant:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            if move.castle:
                if move.newCol - move.startCol == 2:
                    self.board[move.newRow][move.newCol + 1] = self.board[move.newRow][move.newCol - 1]
                    self.board[move.newRow][move.newCol - 1] = "--"
                else:
                    self.board[move.newRow][move.newCol - 2] = self.board[move.newRow][move.newCol + 1]
                    self.board[move.newRow][move.newCol + 1] = "--"
            self.checkmate = False
            self.stalemate = False
            self.draw = False
            self.invalid = False

    @staticmethod
    def randomMove(moves):
        if len(moves) != 0:
            return moves[0]

    def findBestMove(self, piecePositions, moves, endgameTable):
        if len(moves) == 1:
            return moves[0]
        else:
            if len(piecePositions) == 3:
                AIMove = self.findBestMove3(piecePositions[0], piecePositions[1], piecePositions[2], moves,
                                            endgameTable)
            elif len(piecePositions) == 4:
                AIMove = self.findBestMove4(piecePositions[0], piecePositions[1], piecePositions[2], piecePositions[3],
                                            moves, endgameTable)
            else:
                AIMove = self.findBestMove5(piecePositions[0], piecePositions[1], piecePositions[2], piecePositions[3],
                                            piecePositions[4], moves, endgameTable)
        return AIMove

    def findBestMove3(self, a, b, c, moves, endgameTable):
        highestDTM = -1000
        bestMove = ()
        if self.whiteToMove:
            for i in range(len(moves)):
                pieceMoved = self.toPosition(moves[i].startRow,
                                             moves[i].startCol)
                newPosition = self.toPosition(moves[i].newRow, moves[i].newCol)
                if b == pieceMoved:
                    if endgameTable[a][b][c][0] > endgameTable[a][newPosition][c][1] >= 0:
                        return Move((moves[i].startRow, moves[i].startCol), (moves[i].newRow, moves[i].newCol),
                                    self.board)
                elif c == pieceMoved:
                    if endgameTable[a][b][c][0] > endgameTable[a][b][newPosition][1] >= 0:
                        return Move((moves[i].startRow, moves[i].startCol), (moves[i].newRow, moves[i].newCol),
                                    self.board)
        else:
            for i in range(len(moves)):
                newPosition = self.toPosition(moves[i].newRow, moves[i].newCol)
                if moves[i].capture:
                    print("Blunder! White made an error and gave up a piece.")
                    return Move((self.toRowCol(a)[0], self.toRowCol(a)[1]), (moves[i].newRow, moves[i].newCol),
                                self.board)
                elif endgameTable[newPosition][b][c][0] == -3:
                    return Move((self.toRowCol(a)[0], self.toRowCol(a)[1]), (moves[i].newRow, moves[i].newCol),
                                self.board)
                elif endgameTable[newPosition][b][c][0] > highestDTM:
                    highestDTM = endgameTable[newPosition][b][c][0]
                    bestMove = (moves[i].newRow, moves[i].newCol)
                if i == len(moves) - 1:
                    return Move((self.toRowCol(a)[0], self.toRowCol(a)[1]), (bestMove[0], bestMove[1]), self.board)

    def findBestMove4(self, a, b, c, d, moves, endgameTable):
        highestDTM = -1000
        bestMove = ()
        if self.whiteToMove:
            for i in range(len(moves)):
                pieceMoved = self.toPosition(moves[i].startRow, moves[i].startCol)
                newPosition = self.toPosition(moves[i].newRow, moves[i].newCol)
                if b == pieceMoved:
                    if endgameTable[a][b][c][d][0] > endgameTable[a][newPosition][c][d][1] >= 0:
                        return Move((moves[i].startRow, moves[i].startCol), (moves[i].newRow, moves[i].newCol),
                                    self.board)
                elif c == pieceMoved:
                    if endgameTable[a][b][c][d][0] > endgameTable[a][b][newPosition][d][1] >= 0:
                        return Move((moves[i].startRow, moves[i].startCol), (moves[i].newRow, moves[i].newCol),
                                    self.board)
                elif d == pieceMoved:
                    if endgameTable[a][b][c][d][0] > endgameTable[a][b][c][newPosition][1] >= 0:
                        return Move((moves[i].startRow, moves[i].startCol), (moves[i].newRow, moves[i].newCol),
                                    self.board)
        else:
            for i in range(len(moves)):
                newPosition = self.toPosition(moves[i].newRow, moves[i].newCol)
                if moves[i].capture:
                    print("Blunder! White made an error and gave up a piece.")
                    return Move((self.toRowCol(a)[0], self.toRowCol(a)[1]), (moves[i].newRow, moves[i].newCol),
                                self.board)
                elif endgameTable[newPosition][b][c][d][0] == -3:
                    return Move((self.toRowCol(a)[0], self.toRowCol(a)[1]), (moves[i].newRow, moves[i].newCol),
                                self.board)
                elif endgameTable[newPosition][b][c][d][0] > highestDTM:
                    highestDTM = endgameTable[newPosition][b][c][d][0]
                    bestMove = (moves[i].newRow, moves[i].newCol)
                if i == len(moves) - 1:
                    return Move((self.toRowCol(a)[0], self.toRowCol(a)[1]), (bestMove[0], bestMove[1]), self.board)

    def findBestMove5(self, a, b, c, d, e, moves, endgameTable):
        highestDTM = -1000
        bestMove = ()
        if self.whiteToMove:
            for i in range(len(moves)):
                pieceMoved = self.toPosition(moves[i].startRow, moves[i].startCol)
                newPosition = self.toPosition(moves[i].newRow, moves[i].newCol)
                if b == pieceMoved:
                    if endgameTable[a][b][c][d][e][0] > endgameTable[a][newPosition][c][d][e][1] >= 0:
                        return Move((moves[i].startRow, moves[i].startCol), (moves[i].newRow, moves[i].newCol),
                                    self.board)
                elif c == pieceMoved:
                    if endgameTable[a][b][c][d][e][0] > endgameTable[a][b][newPosition][d][e][1] >= 0:
                        return Move((moves[i].startRow, moves[i].startCol), (moves[i].newRow, moves[i].newCol),
                                    self.board)
                elif d == pieceMoved:
                    if endgameTable[a][b][c][d][e][0] > endgameTable[a][b][c][newPosition][e][1] >= 0:
                        return Move((moves[i].startRow, moves[i].startCol), (moves[i].newRow, moves[i].newCol),
                                    self.board)
                elif e == pieceMoved:
                    if endgameTable[a][b][c][d][e][0] > endgameTable[a][b][c][d][newPosition][1] >= 0:
                        return Move((moves[i].startRow, moves[i].startCol), (moves[i].newRow, moves[i].newCol),
                                    self.board)
        else:
            for i in range(len(moves)):
                newPosition = self.toPosition(moves[i].newRow, moves[i].newCol)
                if moves[i].capture:
                    print("Blunder! White made an error and gave up a piece.")
                    return Move((self.toRowCol(a)[0], self.toRowCol(a)[1]), (moves[i].newRow, moves[i].newCol),
                                self.board)
                elif endgameTable[newPosition][b][c][d][e][0] == -3:
                    return Move((self.toRowCol(a)[0], self.toRowCol(a)[1]), (moves[i].newRow, moves[i].newCol),
                                self.board)
                elif endgameTable[newPosition][b][c][d][e][0] > highestDTM:
                    highestDTM = endgameTable[newPosition][b][c][d][e][0]
                    bestMove = (moves[i].newRow, moves[i].newCol)
                if i == len(moves) - 1:
                    return Move((self.toRowCol(a)[0], self.toRowCol(a)[1]), (bestMove[0], bestMove[1]), self.board)

    def getChessNotation(self, move):
        notation = move.__str__()
        if move.pawnPromotion:
            notation += "=Q"
        if self.checkmate:
            notation += "#"
        elif self.inCheck:
            notation += "+"
        print(notation)
        return notation


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSquare, newSquare, board, pawnPromotion=False, enPassant=False, doublePawnMove=False,
                 castle=False):
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

    def __str__(self):
        if self.castle:
            return "O-O" if self.newCol == 6 else "O-O-O"

        endSquare = self.toFileRank(self.newRow, self.newCol)
        if self.pieceMoved[1] == "p":
            if self.capture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

        moveString = self.pieceMoved[1]
        if self.capture:
            moveString += "x"
        return moveString + endSquare


def main():
    game = EndgameTable()
    pieceTypes = ["bK", "wK", "wQ", "wB", "bN"]
    # initpos = game.getInitialPositions(pieceTypes)
    # np.save("KQBvKN.npy", initpos)
    # initialTable = np.load("KQvKR.npy")
    # table2 = np.load("KQvKComplete.npy")
    # table3 = np.load("KRvKComplete.npy")
    # game.createEndgameTable(pieceTypes, initialTable, table2, table3)
    # np.save("KQvKRComplete.npy", game.endgameTable4)
    # table = np.load("KQvKComplete.npy")
    # game.endgameTable3 = table
    # checkmates = np.where(game.endgameTable3 == 0)
    # positions = np.array(list(zip(checkmates[0], checkmates[1], checkmates[2], checkmates[3])))
    # for p in positions:
    #     if p[4] == 0:
    #         print(p[0], p[1], p[2], p[3], p[4])
    # table = np.load("KQvKComplete.npy")
    # print("Invalid Position at [0][2][1][0], expected value = -2, real value =", table[0][2][1][0])
    # print("Draw Position at [63][61][55][1], expected value = -3, real value =", table[63][61][55][1])
    # print("Stalemate Position at [7][5][22][1], expected value = -3, real value =", table[7][5][22][1])
    # print("Checkmate Position at [0][2][1][1], expected value = 0, real value =", table[0][2][1][1])
    # print("DTM 1 Position at [24][26][43][0], expected value = 1, real value =", table[24][26][43][0])
    # print("DTM 2 Position at [32][26][43][1], expected value = 2, real value =", table[32][26][43][1])
    # print("DTM 3 Position at [32][17][43][0], expected value = 3, real value =", table[32][17][43][0])
    # print("DTM 4 Position at [33][17][43][1], expected value = 4, real value =", table[33][17][43][1])
    # print("DTM 5 Position at [33][10][43][0], expected value = 5, real value =", table[33][10][43][0])
    # print("Longest DTM Position at [36][56][49][1], expected value = 20, real value =", table[36][56][49][1])
    # table = np.load("KNBvKComplete.npy")
    # print("Invalid Position at [57][41][40][58][0], expected value = -2, real value =", table[57][41][40][58][0])
    # print("Draw Position at [57][41][40][58][1], expected value = -3, real value =", table[57][41][40][58][1])
    # print("Stalemate Position at [56][41][50][58][1], expected value = -3, real value =", table[56][41][50][58][1])
    # print("Checkmate Position at [0][2][10][26][1], expected value = 0, real value =", table[0][2][10][26][1])
    # print("DTM 1 Position at [56][41][40][51][0], expected value = 1, real value =", table[56][41][40][51][0])
    # print("DTM 2 Position at [57][41][40][51][1], expected value = 2, real value =", table[57][41][40][51][1])
    # print("DTM 3 Position at [57][41][50][51][0], expected value = 3, real value =", table[57][41][50][51][0])
    # print("DTM 4 Position at [56][41][50][51][1], expected value = 4, real value =", table[56][41][50][51][1])
    # print("DTM 5 Position at [56][41][44][51][0], expected value = 5, real value =", table[56][41][44][51][0])
    # print("Longest DTM Position at [52][57][63][30][1], expected value = 66, real value =", table[52][57][63][30][1])
    # table = np.load("KBBvKsameComplete.npy")
    # print("Invalid Position at [0][2][18][27][0], expected value = -2, real value =", table[0][2][18][27][0])
    # print("Invalid Position at [0][2][39][40][1], expected value = -2, real value =", table[0][2][39][40][1])
    # print("Draw Position at [0][2][8][28][1], expected value = -3, real value =", table[0][2][8][28][1])
    # print("Draw Position at [0][2][42][28][0], expected value = -3, real value =", table[0][2][42][28][0])
    # print("Stalemate Position at [0][2][40][35][1], expected value = -3, real value =", table[0][2][40][35][1])
    table = np.load("KQvKRComplete.npy")
    print("Invalid Position at [5][7][46][31][1], expected value = -2, real value =", table[5][7][46][31][1])
    print("Draw Position at [0][2][16][8][0], expected value = -3, real value =", table[0][2][16][8][0])
    print("Checkmate Position for white at [0][2][1][24][1], expected value = 0, real value =", table[0][2][1][24][1])
    print("Checkmate Position for black at [5][7][46][31][0], expected value = 0, real value =", table[5][7][46][31][0])
    print("DTM 3 Position at [8][18][43][25][0], expected value = 3, real value =", table[8][18][43][25][0])
    print("DTM 4 Position at [16][18][43][25][1], expected value = 4, real value =", table[16][18][43][25][1])
    print("DTM 5 Position at [16][26][43][25][0], expected value = 5, real value =", table[16][26][43][25][0])

if __name__ == "__main__":
    main()
