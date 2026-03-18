import random
# from main import getDepth

pieceScore = {"K": 0, "Q": 9, "R": 5, "B":3, "N":3, "p":1}

knightScore = [ [1,1,1,1,1,1,1,1],
                [1,2,2,2,2,2,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,2,2,2,2,2,1],
                [1,1,1,1,1,1,1,1]]

bishopScore = [ [4,3,2,1,1,2,3,4],
                [3,4,3,2,2,3,4,3],
                [2,3,4,3,3,4,3,2],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [2,3,4,3,3,4,3,2],
                [3,4,3,2,2,3,4,3],
                [4,3,2,1,1,2,3,4]]


queenScore = [  [1,1,1,3,1,1,1,1],
                [1,2,3,3,3,1,1,1],
                [1,4,3,3,3,4,2,1],
                [1,2,3,3,3,2,2,1],
                [1,2,3,3,3,2,2,1],
                [1,4,3,3,3,4,2,1],
                [1,2,3,3,3,1,1,1],
                [1,1,1,3,1,1,1,1]]

rookScore = [   [4,3,4,4,4,4,3,4],
                [4,4,4,4,4,4,4,4],
                [1,1,2,3,3,2,1,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,1,2,3,3,2,1,1],
                [4,4,4,4,4,4,4,4],
                [4,3,4,4,4,4,3,4]]

whitePawnScore=[[8,8,8,8,8,8,8,8],
                [8,8,8,8,8,8,8,8],
                [5,6,6,7,7,6,6,5],
                [2,3,3,5,5,3,3,2],
                [1,2,3,4,4,3,2,1],
                [1,1,2,3,3,2,1,1],
                [1,1,1,0,0,1,1,1],
                [0,0,0,0,0,0,0,0]]

blackPawnScore=[
                [0,0,0,0,0,0,0,0],
                [1,1,1,0,0,1,1,1],
                [1,1,2,3,3,2,1,1],
                [1,2,3,4,4,3,2,1],
                [2,3,3,5,5,3,3,2],
                [5,6,6,7,7,6,6,5],
                [8,8,8,8,8,8,8,8],
                [8,8,8,8,8,8,8,8],]


piecePositionScores = {"N": knightScore, "Q": queenScore, "B": bishopScore, "R": rookScore, "bp": blackPawnScore, "wp": whitePawnScore}


CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

'''
Picks and returns a random move
'''

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]
    # returnQueue.put(validMoves[random.randint(0,len(validMoves)-1)])

def findRandomMoveWhenNoMoveMade(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

'''
Find the best move based on material alone
'''

def findGreedyMove(gs, validMoves, returnQueue):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.checkMate:
                score = -CHECKMATE
        elif gs.staleMate:
                score = STALEMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if(score > opponentMaxScore):
                    opponentMaxScore = score
                    # bestPlayerMove = playerMove
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore :
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    # returnQueue.put(bestPlayerMove)

    return bestPlayerMove

'''
Helper method to make the first recursive call
'''

def findBestMoveMiniMax(gs, validMoves, returnQueue):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveMiniMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # returnQueue.put(nextMove)
    return nextMove
    
def findMoveMiniMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMiniMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMiniMax(gs,nextMoves, depth - 1, True)    
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findBestMoveNegaMax(gs, validMoves, returnQueue):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    # returnQueue.put(nextMove)
    return nextMove

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def findBestMoveNegaMaxAlphaBeta(gs, validMoves, returnQueue):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    # returnQueue.put(nextMove)
    return nextMove

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    #move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha: #pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore





'''
A positive score is good for white, a negative score is good for black
'''
'''
A better "scoreMaterial" method
'''
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE # black wins
        else:
            return CHECKMATE # white wins
    elif gs.staleMate:
        return STALEMATE




    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                #score it 
                piecePositionScore = 0
                if square[1] != "K":
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                    

                if square[0] == "w":
                    score+=pieceScore[square[1]] + piecePositionScore * .1
                elif square[0] == "b":
                    score-=pieceScore[square[1]] + piecePositionScore * .1
    return score


'''
Score the board based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score+=pieceScore[square[1]]
            elif square[0] == "b":
                score-=pieceScore[square[1]]
    return score