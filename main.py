# Main file. Responsible for displying and handling user input

import pygame as p
import engine
import ai
from multiprocessing import Process, Queue

p.init()
WIDTH = HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = HEIGHT
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}
global colorLight 
global colorDark 



'''
Initialise a global dictionary, will be called once
to save memory and remove lag
'''

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ',
              'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("AI_Based_Projects/Chess_Engine/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))

    #we can access any image by calling the image at the position "piece name" like "IMAGES[wp]" 


green = ["white", "green"]
brown = ["white", "brown"]
blue = ["white", "blue"]
gray = ["white", "gray"]
pink = ["white", "pink"]


'''
The main driver of code the handle graphics and user input
'''

def main():
    screen = p.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH,HEIGHT))
    p.display.set_caption("Chess AI")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = engine.GameState()
    # print(gs.board)
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable
    animate = False
    moveLogFont = p.font.SysFont("Ariel", 24, False, False)
    loadImages() #only doing once
    running = True
    sqSelected = () #no square selected initially, keep track of the last user click (row, col)
    playerClicks = [] #keep trach of player clicks (two tuples)
    gameOver = False
    playerOne = False #if a human is white, then this will be true, if ai is playing, then false
    playerTwo = False #if a human is black, then this will be true, if ai is playing, then false
    AIThinking = False
    moveUndone = False
    moveFinderProcess = None
    print("Welcome to this CHESS AI!")

    print("Please select your theme:")
    print("1) Green")
    print("2) Brown")
    print("3) Blue")
    print("4) Gray")
    print("5) Pink")
    while True:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            global colorLight, colorDark
            colorLight, colorDark = green[0], green[1]
            break
        elif choice == 2:
            colorLight, colorDark = brown[0], brown[1]

            break
        elif choice == 3:
            colorLight, colorDark = blue[0], blue[1]

            break
        elif choice == 4:
            colorLight, colorDark = gray[0], gray[1]

            break
        elif choice == 5:
            colorLight, colorDark = pink[0], pink[1]

            break
        else:
            print("Invalid choice")

    print("Choose which AI you would like to use this time:")
    print("1) Random AI")
    print("2) Greedy AI (MiniMax Non-Recursive)")
    print("3) Minimax Algorithm(use it at your own risk, analysing moves is going to take forever)")
    print("4) Negamax Algorithm")
    print("5) Negamax Algorithm with Alpha Beta Pruning (Positional Play integrated) RECIEVES REGULAR UPGRADRES")
    print("6) Play Player vs Player Instead (not use other AIs, MAKE SURE TO CHOOSE PLAYER VS PLAYER IN NEXT MENU)")
    print("(more AI coming soon...)")
    while True:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            randomAI = True
            greedyAI = False
            miniMaxAI = False
            negaMaxAI = False
            break
        elif choice == 2:
            randomAI = False
            greedyAI = True
            miniMaxAI = False
            negaMaxAI = False
            alphaBetaAI = False
            break
        elif choice == 3:
            randomAI = False
            greedyAI = False
            miniMaxAI = True
            negaMaxAI = False
            alphaBetaAI = False
            # global depth
            # depth = int(input("Enter the depth: "))
            break
        elif choice == 4:
            randomAI = False
            greedyAI = False
            miniMaxAI = False
            negaMaxAI = True
            alphaBetaAI = False
            break
        elif choice == 5:
            randomAI = False
            greedyAI = False
            miniMaxAI = False
            negaMaxAI = False
            alphaBetaAI = True
            break
        elif choice == 6:
            randomAI = False
            greedyAI = False
            miniMaxAI = False
            negaMaxAI = False
            alphaBetaAI = False
            break
        else:
            print("Invalid choice, please try again")


    print("Choose your option:")
    print("1) AI vs AI")
    print("2) Player vs Player")
    print("3) AI vs Player (Player is White)")
    print("4) AI vs Player (Player is Black)")
    while True:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            playerOne = False
            playerTwo = False
            print("Switch over to the window now, thanks for your patience!")
            break
        elif choice == 2:
            playerOne = True
            playerTwo = True
            print("Switch over to the window now, thanks for your patience!")
            break
        elif choice == 3:
            playerOne = True
            playerTwo = False
            print("Switch over to the window now, thanks for your patience!")
            break
        elif choice == 4:
            playerOne = False
            playerTwo = True
            print("Switch over to the window now, thanks for your patience!")
            break
        else:
            print("Invalid choice")
        
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        # print(gs.board)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handling
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver: #not humanTurn
                    location = p.mouse.get_pos() #(x,y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8:
                        sqSelected = () # deselect
                        playerClicks = [] #deselect
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
                    if len(playerClicks) == 2 and humanTurn:
                        move = engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        # print(move.getChessNotation())
                        for i in range(len(validMoves)):

                            if move == validMoves[i]:
                        # if move in validMoves:
                                # print("Move made")
                                gs.makeMove(move)
                                moveMade = True
                                animate = True
                                sqSelected = () #reset
                                playerClicks = [] #reset
                        if not moveMade:
                        # else:
                            playerClicks = [sqSelected]
                    # if moveMade:
                    #     print(gs.board)

            #key handling
            elif e.type == p.KEYDOWN:
                if e.key == p.K_LEFT:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        # moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True  
                if e.key == p.K_r: #reset the board when 'r' is pressed
                    gs = engine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    moveUndone = True

        #AI move finder
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                print("Thnking....")
                returnQueue = Queue()#used to pass data between threads
                # moveFinderProcess = Process(target=ai.findBestMoveNegaMaxAlphaBeta, args=(gs, validMoves, returnQueue))
                # moveFinderProcess.start() #call that method
                if randomAI:
                    AIMove = ai.findRandomMove(validMoves)
                    # # returnQueue = Queue()#used to pass data between threads
                    # moveFinderProcess = Process(target=ai.findRandomMove, args=(validMoves, returnQueue))
                    # moveFinderProcess.start() #call that methodAIMove = ai.findRandomMove(validMoves) 
                    # if not moveFinderProcess.is_alive():
                    #     print("Done Thinking")
                    #     AIMove = returnQueue.get()
                    #     if AIMove is None:
                    #         AIMove = ai.findRandomMoveWhenNoMoveMade(validMoves)
                    #     gs.makeMove(AIMove)
                    #     moveMade = True
                    #     animate = True
                    #     AIThinking = False
                elif greedyAI:
                    AIMove = ai.findGreedyMove(gs, validMoves, returnQueue)

                    # returnQueue = Queue()#used to pass data between threads
                    # moveFinderProcess = Process(target=ai.findGreedyMove, args=(gs, validMoves, returnQueue))
                    # moveFinderProcess.start() #call that method 
                    # # if AIMove is None:
                    # #     AIMove = ai.findRandomMove(validMoves)
                    # if not moveFinderProcess.is_alive():
                    #     print("Done Thinking")
                    #     AIMove = returnQueue.get()
                    #     if AIMove is None:
                    #         AIMove = ai.findRandomMoveWhenNoMoveMade(validMoves)
                    #     gs.makeMove(AIMove)
                    #     moveMade = True
                    #     animate = True
                    #     AIThinking = False
                elif miniMaxAI:
                    AIMove = ai.findBestMoveMiniMax(gs, validMoves, returnQueue)
                    
                    # returnQueue = Queue()#used to pass data between threads
                    # moveFinderProcess = Process(target=ai.findBestMoveMiniMax, args=(gs, validMoves, returnQueue))
                    # moveFinderProcess.start() #call that method
                    # if not moveFinderProcess.is_alive():
                    #     print("Done Thinking")
                    #     AIMove = returnQueue.get()
                    #     if AIMove is None:
                    #         AIMove = ai.findRandomMoveWhenNoMoveMade(validMoves)
                    #     gs.makeMove(AIMove)
                    #     moveMade = True
                    #     animate = True
                    #     AIThinking = False
                elif negaMaxAI:
                    AIMove = ai.findBestMoveNegaMax(gs, validMoves, returnQueue)
                    # returnQueue = Queue()#used to pass data between threads
                    # moveFinderProcess = Process(target=ai.findBestMoveNegaMax, args=(gs, validMoves, returnQueue))
                    # moveFinderProcess.start() #call that method
                    # if not moveFinderProcess.is_alive():
                    #     print("Done Thinking")
                    #     AIMove = returnQueue.get()
                    #     if AIMove is None:
                    #         AIMove = ai.findRandomMoveWhenNoMoveMade(validMoves)
                    #     gs.makeMove(AIMove)
                    #     moveMade = True
                    #     animate = True
                    #     AIThinking = False
                elif alphaBetaAI:
                    AIMove = ai.findBestMoveNegaMaxAlphaBeta(gs, validMoves, returnQueue)
                    # returnQueue = Queue()#used to pass data between threads
                    # moveFinderProcess = Process(target=ai.findBestMoveNegaMaxAlphaBeta, args=(gs, validMoves, returnQueue))
                    # moveFinderProcess.start() #call that method
                    # if not moveFinderProcess.is_alive():
                    #     print("Done Thinking")
                    #     AIMove = returnQueue.get()
                    #     if AIMove is None:
                    #         AIMove = ai.findRandomMoveWhenNoMoveMade(validMoves)
                    #     gs.makeMove(AIMove)
                    #     moveMade = True
                    #     animate = True
                    #     AIThinking = False
                gs.makeMove(AIMove)
                moveMade = True
                animate = True
                AIThinking = False
                # AIMove = ai.findRandomMoveWhenNoMoveMade(validMoves)
                # gs.makeMove(AIMove)
                # if not moveFinderProcess.is_alive():
                #     print("Done Thinking")
                #     AIMove = returnQueue.get()
                #     if AIMove is None:
                #         AIMove = ai.findRandomMoveWhenNoMoveMade(validMoves)
                #     gs.makeMove(AIMove)
                #     moveMade = True
                #     animate = True
                #     AIThinking = False


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            moveUndone = False
            
        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkMate or gs.staleMate:
            gameOver = True
            # if gs.staleMate:
            text = "Stalemate" if gs.staleMate else ("White wins by checkmate!" if not gs.whiteToMove else "Blacks wins by checkmate!")
            drawEndGameText(screen, text)
        # elif gs.staleMate:
        #     gameOver = True
        #     drawEndGameText(screen, "Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Highlight square selected and moves for piece selected
'''
def highLightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transperancy -> 0 transparent; 255 opague
            s.fill(p.Color('red'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #hightlight moves from that square
            s.fill(p.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))




'''
responsible for the graphics in the game state
'''


def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen) # draw squares in the board
    highLightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)

def drawBoard(screen):
    global colors 
    colors = [p.Color(colorLight), p.Color(colorDark)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current gamestate board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draws the move log
'''
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range (0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i])+ ' ' 
        if i + 1 < len(moveLog): #make sure balck made a move
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)
    movesPerRow = 1

    padding = 5
    textY = padding
    lineSpacing = 2
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range (movesPerRow):
            if i+j<len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing
    # textObject = font.render(text,0,p.Color("Black"))
    # screen.blit(textObject, textLocation.move(2,2))



'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    coords = [] #list of coords that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r,c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        if move.pieceCaptured != "--":
            if move.isEnPassant:
                enPassantRow = (move.endRow + 1) if move.pieceCaptured == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol*SQ_SIZE, enPassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(120)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvitca", 48, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_width()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text,0,p.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))









    
# def getDepth():
#     returnDepth = depth
#     return returnDepth


if __name__ == "__main__":

    main()

