# Responsible for storing all the information for the current state. Also for dertiming the move and move log
#TODO : ADVANCED ALGO WAS BUGGY, SO I USED NAIVE ALGO INSTEAD

class GameState():
    def __init__(self):
        '''
        The board is an 8-8 2 dimensional list
        the first character represents the color of the piece 'b' or 'w'
        the second character represents the piece itself (k,q,r,b,n,p)
        '--' reprersents an empty space or square
        '''
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'], 
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]

        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q":self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4) 
        self.checkMate = False
        self.staleMate = False
        #**Advanced algo**
        # self.kingInCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () #cooridnates of the square where en passant is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]


    # def removePiece(self, r, c):
    #     self.board[r][c] = "--" 

    '''
    Takes a move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    '''
    def makeMove(self, move):
        
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move for reference or for undo
        self.whiteToMove = not self.whiteToMove # swap players
        #update king's position
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        # print()
        #enpassant move
        if move.isEnPassant:
            #print("Pawn en passant made")
            self.board[move.endRow][move.endCol] = "--" #capturing pawn

        #update enpassant variable
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        #castling move
        if move.isCastle == True:
            if move.endCol - move.startCol == 2: #kingside castle move
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves the rook
                print("Castle rook moved")
                self.board[move.endRow][move.endCol+1] = "--" #removes the old rook
            else: #queenside castle move
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #moves the rook
                print("Castle rook moved")
                self.board[move.endRow][move.endCol-2] = "--" #removes the old rook
        if move.isEnPassant:
            print("En Passant")

        self.enpassantPossibleLog.append(self.enpassantPossible)


        #update castling rights - whenever its a rook or a king's move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))

        
        


    '''
    Undo the last move
    '''
    def undoMove(self):
        if len(self.moveLog) !=0 :
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            #update king's position
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo enpassant move
            if move.isEnPassant:
                self.board[move.endRow][move.endCol] = "--" #leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                # self.enpassantPossible = (move.endRow, move.endCol)
            
            #undo a 2 square pawn advance
            # if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            #     self.enpassantPossible = ()

            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            #undo castling rights
            self.castleRightsLog.pop() #get rid of new castling rights from the move we are undoing
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(newRights.wks,newRights.bks,newRights.wqs, newRights.bqs )

            #undo castle move
            if move.isCastle:
                if move.endCol - move.startCol == 2: #kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else: #queenside
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"


            self.checkMate = False
            self.staleMate = False

                 
 
    '''
    Update the castle rights given the move
    '''

    def updateCastleRights(self, move):
        # print(self.currentCastlingRights.wks, self.currentCastlingRights.wqs, self.currentCastlingRights.bks, self.currentCastlingRights.bqs)
        if move.pieceMoved == 'wK' :
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRights.bks = False

        if move.pieceCaptured == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRights.wks = False

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        tempEnPassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs) #copy the current castling rights
        # #*********** NAIVE ALOGRITHM TO SEE CHECKS (EASY AND SIMPLE BUT INEFFICIENT) *********
        #1) generate all possible moves

        moves = self.getAllPossibleMoves()
        


        #2)for each move, make the move
        
        for i in range(len(moves)-1, -1, -1): # ** WHEN REMOVING FORM A LIST, GO BACKWARDS THROUGH THAT LIST **
            self.makeMove(moves[i])
        
            #3)generate all opponent's moves
            #4) for each of your opponent's moves, see if they attack your king
                
            self.whiteToMove = not self.whiteToMove #switch it back
            if self.inCheck():
                #5) if they do attack your king, not a valid move
                moves.remove(moves[i]) 
            self.whiteToMove = not self.whiteToMove #switch it back
            self.undoMove()
        


        # return moves

        # moves = []
        # self.kingInCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        # kingRow = self.whiteKingLocation[0] if self.whiteToMove else self.blackKingLocation[0]
        # kingCol = self.whiteKingLocation[1] if self.whiteToMove else self.blackKingLocation[1]
        # if self.kingInCheck:
        #     if len(self.checks) == 1: #only 1 check, block or move king
        #         moves = self.getAllPossibleMoves()
        #         #to block a check you must move a piece into one of the square between the enemy piece and king
        #         check = self.checks[0] # check information
        #         checkRow = check[0]
        #         checkCol = check[1]
        #         pieceChecking = self.board[checkRow][checkCol] # enemy piece causing the check
        #         validSquares = [] # squares that pieces can move to
        #         #if knight, must capture knight or move king, other pices can be blocked
        #         if pieceChecking[1] == "N":
        #             validSquares = [(checkRow,checkCol)]
        #         else:
        #             for i in range(1,8):
        #                 validSquare = (kingRow + check[2] * i, kingCol +check[3] * i) #check[2] and check[3] are the check directions
        #                 validSquares.append(validSquare)
        #                 if validSquare[0] == checkRow and validSquare[1] == checkCol: #once you get to piece end checks
        #                     break
        #         #get rid of all moves that don't block check or move king
        #         for i in range(len(moves)-1,-1,-1): # go through backwards when you are removing from list as iterating
        #             if moves[i].pieceMoved[1] != "K": #move doesn't move the ing so it must block or capture
        #                 if not (moves[i].endRow, moves[i].endCol) in validSquares: # move doesn't block check or capture piece
        #                     moves.remove(moves[i])
        #     else: #double check, king has to muve
        #         self.getKingMoves(kingRow,kingCol,moves)
        # else: #not in check so all moves are fine
        #     moves = self.getAllPossibleMoves()
        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
                print("Checkmate") 
                # quit(0)
            else:
                self.staleMate = True
                print("Stalemate")
                # quit(0)
        
            
        else:
            self.staleMate = False
            self.checkMate = False

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1], moves)

        self.enpassantPossible = tempEnPassantPossible
        self.currentCastlingRights = tempCastleRights
        return moves

    '''
    Determine if the current player is in check
    '''
    # ** NAIVE ALGORITHM **
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])

    '''
    Returns if the player is in check, a list of pins, and a list of checks
    '''
    #ADVANCED ALGO
    # def checkForPinsAndChecks(self):
    #     pins = [] #square where the allied pinned piece is and direction pinned from
    #     checks = [] #squares where enemy is applying a check
    #     kingInCheck = False
    #     enemyColor = "b" if self.whiteToMove else "w"
    #     allyColor = "w" if self.whiteToMove else "b"
    #     startRow = self.whiteKingLocation[0] if self.whiteToMove else self.blackKingLocation[0]
    #     startCol = self.whiteKingLocation[1] if self.whiteToMove else self.blackKingLocation[1]

    #     #check outwards from king for checks, keep track of pins
    #     directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
    #     for j in range(len(directions)):
    #         d = directions[j]
    #         possiblePin = () #reset
    #         for i in range(1,8):
    #             endRow = startRow + d[0] * i
    #             endCol = startCol + d[1] * i
    #             if 0 <= endRow < 8 and 0 <= endCol < 8:
    #                 endPiece = self.board[endRow][endCol]
    #                 if endPiece[0] == allyColor and endPiece != "K":
    #                     if possiblePin == (): #1st allied piece could be pinned
    #                         possiblePin = (endRow, endCol, d[0], d[1])
    #                     else: #2nd allied piece, so no pin or check possible in this direction
    #                         break
    #                 elif endPiece == enemyColor:
    #                     type = endPiece[1]
    #                     #5 possiblities here in this complex conditional
    #                     #1) Orthogonally away from king and piece is a rook
    #                     #2) diagonally away from king and piece is a bishop
    #                     #3) 1 square away diagonally from king and piece is a pawn
    #                     #4) any direction and piece is a queen
    #                     #5) any direction 1 square away and piece is a king (this is necessary to prevent a king to move to a square contorlled by another king)
    #                     if (0 <= j <=3 and type == 'R') or \
    #                         (4 <= j <= 7 and type == "B") or \
    #                         (i == 1 and type == "p" and ((enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or \
    #                         (type == "Q") or (i == 1 and type == 'K'):
    #                         if possiblePin == (): #no piece blocking so check
    #                             kingInCheck = True
    #                             checks.append((endRow,endCol,d[0],d[1]))
    #                             break
    #                         else: #piece blocking so pin
    #                             pins.append(possiblePin)
    #                             break
    #                 else: #enemy piece not applying check
    #                     break
    #             else: # off board
    #                 break
    #     #check for knight checks
    #     knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
    #     for m in knightMoves:
    #         endRow = startRow + m[0]
    #         endCol = startCol + m[1]
    #         if 0 <= endRow < 8 and 0 <= endCol < 8:
    #             endPiece = self.board[endRow][endCol]
    #             if endPiece[0] == enemyColor and endPiece[1] == 'N': #enemy knight attacking king
    #                 kingInCheck = True
    #                 checks.append((endRow,endCol,m[0],m[1]))
    #     return kingInCheck, pins, checks
            


    '''
    Determine if the enemy can attack the square r,c
    '''
    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's move
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                return True
        return False

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self,r,c,moves):

        #advanced algo
        # piecePinned = False
        # pinDirection = ()
        # for i in range(len(self.pins)-1,-1,-1):
        #     if self.pins[i][0] == r and self.pins[i][1] == c:
        #         piecePinned = True
        #         pinDirection = (self.pins[i][2],self.pins[i][3])
        #         self.pins.remove(self.pins[i])
        #         break
        #advanced algo
            
        if self.whiteToMove: #white pawn move
            if self.board[r-1][c] == "--": #1 square pawn advance
                # if not piecePinned or pinDirection == (-1,0):
                moves.append(Move((r,c), (r-1,c), self.board))
                if  r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c),(r-2,c),self.board))
            #captures
            if c-1 >= 0: #captures to left
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    # if not piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((r, c),(r-1, c-1), self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                        moves.append(Move((r, c),(r-1, c-1), self.board,isEnPassant=True))
            if c+1 <= 7: # captures to right
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture
                    # if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((r, c),(r-1, c+1), self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                        moves.append(Move((r, c),(r-1, c+1), self.board,isEnPassant=True))
        else: #black pawn moves
            if self.board[r+1][c] == "--": #1 square pawn advance
                # if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r,c), (r+1,c), self.board))
                    if  r == 1 and self.board[r+2][c] == "--": #2 square pawn advance
                        moves.append(Move((r,c),(r+2,c),self.board))
            #captures
            if c-1 >= 0: #captures to left
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture
                    # if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r, c),(r+1, c-1), self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                        moves.append(Move((r, c),(r+1, c-1), self.board,isEnPassant=True))
            if c+1 <= 7: # captures to right
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture
                    # if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((r, c),(r+1, c+1), self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                        moves.append(Move((r, c),(r+1, c+1), self.board,isEnPassant=True))


    '''
    Get all the rook moves for the rook located at row, col and add these moves to the list
    '''
    def getRookMoves(self,r,c,moves):
        #advanced algo
        # piecePinned = False
        # pinDirection = ()
        # for i in range(len(self.pins)-1,-1,-1):
        #     if self.pins[i][0] == r and self.pins[i][1] == c:
        #         piecePinned = True
        #         pinDirection = (self.pins[i][2],self.pins[i][3])
        #         if self.board[r][c][1] != 'Q': #can't remove queen form pin on rook moves, only remove it on bishop moves
        #             self.pins.remove(self.pins[i])
        #         break
        #advanced algo
        directions = ((-1,0),(0,-1),(1,0),(0,1)) # up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    # if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #empty space valid
                            moves.append(Move((r,c),(endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #enemy piece valid
                            moves.append(Move((r,c),(endRow, endCol), self.board))
                            break
                        else: #friendly invalid
                            break 
                else: break # invalid

    '''
    Get all the bishop moves for the rook located at row, col and add these moves to the list
    '''
    def getBishopMoves(self,r,c,moves):

        #advanced algo
        # piecePinned = False
        # pinDirection = ()
        # for i in range(len(self.pins)-1,-1,-1):
        #     if self.pins[i][0] == r and self.pins[i][1] == c:
        #         piecePinned = True
        #         pinDirection = (self.pins[i][2],self.pins[i][3])
        #         self.pins.remove(self.pins[i])
        #         break
        #advanced algo
            
        directions = ((-1,-1),(-1,1),(1,-1),(1,1)) #4 diagonals
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    # if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #empty space valid
                            moves.append(Move((r,c),(endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #enemy piece valid
                            moves.append(Move((r,c),(endRow, endCol), self.board))
                            break
                        else: #friendly invalid
                            break 
                else: break # invalid

    '''
    Get all the knight moves for the rook located at row, col and add these moves to the list
    '''
    def getKnightMoves(self,r,c,moves):

        #advanced algo
        # piecePinned = False
        # pinDirection = ()
        # for i in range(len(self.pins)-1,-1,-1):
        #     if self.pins[i][0] == r and self.pins[i][1] == c:
        #         piecePinned = True
        #         pinDirection = (self.pins[i][2],self.pins[i][3])
        #         self.pins.remove(self.pins[i])
        #         break
        #advanced algo
            
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                # if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #not an ally piece(empty or enemy piece)
                        moves.append(Move((r,c),(endRow, endCol), self.board))

    '''
    Get all the queen moves for the rook located at row, col and add these moves to the list
    '''
    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)

    '''
    Get all the king moves for the rook located at row, col and add these moves to the list
    '''
    def getKingMoves(self,r,c,moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece(empty or enemy piece)
                    #place king on end square and check for checks
                    # if allyColor == "w":
                    #     self.whiteKingLocation = (endRow,endCol)
                    # else:
                    #     self.blackKingLocation = (endRow,endCol)
                    # inCheck, pins, checks = self.checkForPinsAndChecks()
                    # if not self.inCheck():
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    #place king on original location
                        # if allyColor == "w":
                        #     self.whiteKingLocation = (r,c)
                        # else:
                        #     self.blackKingLocation = (r,c)

        # self.getCastleMoves(r,c,moves,allyColor)

    '''
    Generate all valid castle moves for the king at (r,c) and add them to the list of moves 
    '''
    ### THE ACTUAL ONE
    # def getCastleMoves(self, r, c, moves):
    #     if self.squareUnderAttack(r,c):
    #         return #can't castle while we are in check
    #     if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
    #         self.getKingSideCastleMoves(r,c,moves)
    #         # if self.currentCastlingRights.wks:
    #         #     print("white king castle")
    #         # elif self.currentCastlingRights.bks:
    #         #     print("black king castle")
    #     if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
    #         self.getQueenSideCastleMoves(r,c,moves)
    #         # if self.currentCastlingRights.wqs:
    #         #     print("white queen castle")
    #         # elif self.currentCastlingRights.bqs:
    #         #     print("black queen castle")
        
    # def getKingSideCastleMoves(self, r, c, moves):
    #     if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
    #         if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
    #             moves.append(Move((r,c),(r,c+2),self.board, isCastle=True)) 
    #             print("castle true")


    # def getQueenSideCastleMoves(self, r, c, moves): 
    #     if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
    #         if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2) and not self.squareUnderAttack(r,c-3):
    #             moves.append(Move((r,c),(r,c-2),self.board, isCastle=True)) 
    #             print("castle true")


    #THE PROPOSED ONE
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r,c):
            return #can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(r,c,moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r,c,moves)

    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board, isCastle=True)) 

    def getQueenSideCastleMoves(self, r, c, moves): 
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2) and not self.squareUnderAttack(r,c-3):
                moves.append(Move((r,c),(r,c-2),self.board, isCastle=True)) 

class CastleRights():
     def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():
    #maps keys to values
    #key:value
    ranksToRows = {"1":7, "2":6,"3":5, "4":4,"5":3, "6":2,"7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1,"c":2, "d":3,"e":4, "f":5,"g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassant = False, isCastle = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # Pawn promotion
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7) 
        # En passant
       
        self.isEnPassant = isEnPassant
        if self.isEnPassant:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"
        # self.epPawnRow = self.pieceCaptured[0]
        # self.epPawnCol = self.pieceCaptured[1]
        #castle move
        self.isCastle = isCastle
        # print(isCastle)
        self.isCapture = self.pieceCaptured != "--"
        self.moveId = self.startRow * 1000 +self.startCol * 100 + self.endRow * 10 + self.endCol
        # print(self.moveId)

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    '''
    Overriding the str() function
    '''
    def __str__(self):
        #castle move
        if self.isCastle:
            print("Castle display")
            # "O-O" for kingside castling
            # "O-O-O" for queenside castling
            return "O-O" if self.endCol == 6 else "O-O-O"
        endSquare = self.getRankFile(self.endRow, self.endCol)
        #pawn moves
        if self.pieceMoved[1] == "p":
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" +endSquare
            else:
                return endSquare
        
        #piece moves
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString+='x'
        return moveString + endSquare
