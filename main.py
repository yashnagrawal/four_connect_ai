#!/usr/bin/env python3
from FourConnect import *  # See the FourConnect.py file
import csv
import time

cutOffDepth = 3
recursiveMinimaxCalls = 0


class GameTreePlayer:

    def __init__(self):
        pass

    def MovePriority(self, action, currentState):
        """
        Calculate the priority of a move based on the Move Ordering Heuristic.

        Parameters:
        action (int): The action (column) for which to calculate the priority.
        currentState (list of lists): The current game state.

        Returns:
        priority (int): The priority value for the given action.

        Move Ordering Heuristic:
        - Winning Move: Prioritize actions that result in an immediate win.
        - Block Opponent's Winning Move: Prioritize blocking the opponent's winning move.
        - Center Column: Prioritize the center column (column 3, 0-based index).
        - Column Selection: Prioritize columns from the center outward (3, 2, 4, 1, 5, 0, 6).
        - Additional Heuristics: Implement other priorities based on your game understanding.

        Higher priority values indicate more desirable moves.
        """

        # Calculate the priority value for the action based on the heuristic rules.
        # Higher priority values indicate more desirable moves.
        priority = 0

        # Winning Move
        nextBoard = self.MakeMove(currentState, action, 2)
        if self.winner(nextBoard) == 2:
            priority += 1000

        # Block Opponent's Winning Move
        nextBoard = self.MakeMove(currentState, action, 1)
        if self.winner(nextBoard) == 1:
            priority += 500

        # Center Column
        if action == 3:
            priority += 100

        # Column Selection
        columnOrder = [3, 2, 4, 1, 5, 0, 6]
        priority += (6-columnOrder.index(action))

        return priority

    def MinimaxAlphaBeta(self, currentState, depth, alpha, beta, isMaximizingPlayer):
        global recursiveMinimaxCalls
        recursiveMinimaxCalls += 1

        if depth == 0 or self.IsGameFinished(currentState):
            return self.EvaluateBoard(currentState)

        if isMaximizingPlayer:
            maxEval = -float('inf')
            bestAction = None
            validActions = self.ValidActions(currentState)
            validActions.sort(key=lambda action: self.MovePriority(
                action, currentState), reverse=True)
            for action in validActions:
                # Player 2's move (Game Tree Player)
                nextBoard = self.MakeMove(currentState, action, 2)
                eval = self.MinimaxAlphaBeta(
                    nextBoard, depth - 1, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    bestAction = action
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if depth == cutOffDepth:  # If we're at the root level, return the best action
                # check if bestAction is not None
                return bestAction
            return maxEval
        else:
            minEval = float('inf')
            validActions = self.ValidActions(currentState)
            validActions.sort(
                key=lambda action: self.MovePriority(action, currentState))
            for action in validActions:
                # Player 1's move (Myopic Player)
                nextBoard = self.MakeMove(currentState, action, 1)
                eval = self.MinimaxAlphaBeta(
                    nextBoard, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def ValidActions(self, currentState):
        # Returns a list of valid actions (columns to drop a coin into) for the given board state.
        validActions = []
        for action in range(7):
            if currentState[0][action] == 0:
                validActions.append(action)
        return validActions

    def winner(self, currentState):
        # check rows
        for row in range(6):
            for col in range(4):
                if currentState[row][col] != 0 and currentState[row][col] == currentState[row][col + 1] == currentState[row][col + 2] == currentState[row][col + 3]:
                    return currentState[row][col]

        # check columns
        for col in range(7):
            for row in range(3):
                if currentState[row][col] != 0 and currentState[row][col] == currentState[row + 1][col] == currentState[row + 2][col] == currentState[row + 3][col]:
                    return currentState[row][col]

        # check diagonals
        for row in range(3):
            for col in range(4):
                if currentState[row][col] != 0 and currentState[row][col] == currentState[row + 1][col + 1] == currentState[row + 2][col + 2] == currentState[row + 3][col + 3]:
                    return currentState[row][col]

        for row in range(3, 6):
            for col in range(4):
                if currentState[row][col] != 0 and currentState[row][col] == currentState[row - 1][col + 1] == currentState[row - 2][col + 2] == currentState[row - 3][col + 3]:
                    return currentState[row][col]

        return None

    def IsGameFinished(self, currentState):
        # check if any player has won
        if self.winner(currentState) != None:
            return True

        # check if board is full
        for col in range(7):
            if currentState[0][col] == 0:
                return False

        return True

    def heuristicFunction1(self, currentState):
        # find number of 3-in-a-row for each player
        player1 = 0
        player2 = 0

        # check rows
        for row in range(6):
            for col in range(5):
                if currentState[row][col] != 0 and currentState[row][col] == currentState[row][col + 1] == currentState[row][col + 2]:
                    if currentState[row][col] == 1:
                        player1 += 1
                    else:
                        player2 += 1

        # check columns
        for col in range(7):
            for row in range(4):
                if currentState[row][col] != 0 and currentState[row][col] == currentState[row + 1][col] == currentState[row + 2][col]:
                    if currentState[row][col] == 1:
                        player1 += 1
                    else:
                        player2 += 1

        # check diagonals
        for row in range(4):
            for col in range(5):
                if currentState[row][col] != 0 and currentState[row][col] == currentState[row + 1][col + 1] == currentState[row + 2][col + 2]:
                    if currentState[row][col] == 1:
                        player1 += 1
                    else:
                        player2 += 1

        for row in range(2, 6):
            for col in range(5):
                if currentState[row][col] != 0 and currentState[row][col] == currentState[row - 1][col + 1] == currentState[row - 2][col + 2]:
                    if currentState[row][col] == 1:
                        player1 += 1
                    else:
                        player2 += 1

        return player2 - player1

    def findNumberOfOpportunities1(self, currentState, player):
        opportunities = 0
        # find the number of rows of length 4 with 3 coins of the player and 1 empty space
        for row in range(6):
            for col in range(4):
                if currentState[row][col] == player and currentState[row][col + 1] == player and currentState[row][col + 2] == player and currentState[row][col + 3] == 0:
                    opportunities += 1
                elif currentState[row][col] == player and currentState[row][col + 1] == player and currentState[row][col + 2] == 0 and currentState[row][col + 3] == player:
                    opportunities += 1
                elif currentState[row][col] == player and currentState[row][col + 1] == 0 and currentState[row][col + 2] == player and currentState[row][col + 3] == player:
                    opportunities += 1
                elif currentState[row][col] == 0 and currentState[row][col + 1] == player and currentState[row][col + 2] == player and currentState[row][col + 3] == player:
                    opportunities += 1

        # find the number of columns of length 4 with 3 coins of the player and 1 empty space
        for col in range(7):
            for row in range(3):
                if currentState[row][col] == player and currentState[row + 1][col] == player and currentState[row + 2][col] == player and currentState[row + 3][col] == 0:
                    opportunities += 1
                elif currentState[row][col] == player and currentState[row + 1][col] == player and currentState[row + 2][col] == 0 and currentState[row + 3][col] == player:
                    opportunities += 1
                elif currentState[row][col] == player and currentState[row + 1][col] == 0 and currentState[row + 2][col] == player and currentState[row + 3][col] == player:
                    opportunities += 1
                elif currentState[row][col] == 0 and currentState[row + 1][col] == player and currentState[row + 2][col] == player and currentState[row + 3][col] == player:
                    opportunities += 1

        # find the number of diagonals of length 4 with 3 coins of the player and 1 empty space
        for row in range(3):
            for col in range(4):
                if currentState[row][col] == player and currentState[row + 1][col + 1] == player and currentState[row + 2][col + 2] == player and currentState[row + 3][col + 3] == 0:
                    opportunities += 1
                elif currentState[row][col] == player and currentState[row + 1][col + 1] == player and currentState[row + 2][col + 2] == 0 and currentState[row + 3][col + 3] == player:
                    opportunities += 1
                elif currentState[row][col] == player and currentState[row + 1][col + 1] == 0 and currentState[row + 2][col + 2] == player and currentState[row + 3][col + 3] == player:
                    opportunities += 1
                elif currentState[row][col] == 0 and currentState[row + 1][col + 1] == player and currentState[row + 2][col + 2] == player and currentState[row + 3][col + 3] == player:
                    opportunities += 1

        for row in range(2, 6):
            for col in range(4):
                if currentState[row][col] == player and currentState[row - 1][col + 1] == player and currentState[row - 2][col + 2] == player and currentState[row - 3][col + 3] == 0:
                    opportunities += 1
                elif currentState[row][col] == player and currentState[row - 1][col + 1] == player and currentState[row - 2][col + 2] == 0 and currentState[row - 3][col + 3] == player:
                    opportunities += 1
                elif currentState[row][col] == player and currentState[row - 1][col + 1] == 0 and currentState[row - 2][col + 2] == player and currentState[row - 3][col + 3] == player:
                    opportunities += 1
                elif currentState[row][col] == 0 and currentState[row - 1][col + 1] == player and currentState[row - 2][col + 2] == player and currentState[row - 3][col + 3] == player:
                    opportunities += 1

        return opportunities

    def findNumberOfOpportunities2(self, currentState):

        opportunityOfPlayer1_3 = 0
        opportunityOfPlayer1_2 = 0
        opportunityOfPlayer1_1 = 0

        opportunityOfPlayer2_3 = 0
        opportunityOfPlayer2_2 = 0
        opportunityOfPlayer2_1 = 0

        for row in range(6):
            for col in range(4):
                # find the number of of coins of player 1, 2 and empty spaces
                player1 = 0
                player2 = 0
                empty = 0
                for i in range(4):
                    if currentState[row][col + i] == 1:
                        player1 += 1
                    elif currentState[row][col + i] == 2:
                        player2 += 1
                    else:
                        empty += 1

                if player1 == 3 and empty == 1:
                    opportunityOfPlayer1_3 += 1
                elif player1 == 2 and empty == 2:
                    opportunityOfPlayer1_2 += 1
                elif player1 == 1 and empty == 3:
                    opportunityOfPlayer1_1 += 1
                elif player2 == 3 and empty == 1:
                    opportunityOfPlayer2_3 += 1
                elif player2 == 2 and empty == 2:
                    opportunityOfPlayer2_2 += 1
                elif player2 == 1 and empty == 3:
                    opportunityOfPlayer2_1 += 1

        for col in range(7):
            for row in range(3):
                # find the number of of coins of player 1, 2 and empty spaces
                player1 = 0
                player2 = 0
                empty = 0
                for i in range(4):
                    if currentState[row + i][col] == 1:
                        player1 += 1
                    elif currentState[row + i][col] == 2:
                        player2 += 1
                    else:
                        empty += 1

                if player1 == 3 and empty == 1:
                    opportunityOfPlayer1_3 += 1
                elif player1 == 2 and empty == 2:
                    opportunityOfPlayer1_2 += 1
                elif player1 == 1 and empty == 3:
                    opportunityOfPlayer1_1 += 1
                elif player2 == 3 and empty == 1:
                    opportunityOfPlayer2_3 += 1
                elif player2 == 2 and empty == 2:
                    opportunityOfPlayer2_2 += 1
                elif player2 == 1 and empty == 3:
                    opportunityOfPlayer2_1 += 1

        for row in range(3):
            for col in range(4):
                # find the number of of coins of player 1, 2 and empty spaces
                player1 = 0
                player2 = 0
                empty = 0
                for i in range(4):
                    if currentState[row + i][col + i] == 1:
                        player1 += 1
                    elif currentState[row + i][col + i] == 2:
                        player2 += 1
                    else:
                        empty += 1

                if player1 == 3 and empty == 1:
                    opportunityOfPlayer1_3 += 1
                elif player1 == 2 and empty == 2:
                    opportunityOfPlayer1_2 += 1
                elif player1 == 1 and empty == 3:
                    opportunityOfPlayer1_1 += 1
                elif player2 == 3 and empty == 1:
                    opportunityOfPlayer2_3 += 1
                elif player2 == 2 and empty == 2:
                    opportunityOfPlayer2_2 += 1
                elif player2 == 1 and empty == 3:
                    opportunityOfPlayer2_1 += 1

        for row in range(2, 6):
            for col in range(4):
                # find the number of of coins of player 1, 2 and empty spaces
                player1 = 0
                player2 = 0
                empty = 0
                for i in range(4):
                    if currentState[row - i][col + i] == 1:
                        player1 += 1
                    elif currentState[row - i][col + i] == 2:
                        player2 += 1
                    else:
                        empty += 1

                if player1 == 3 and empty == 1:
                    opportunityOfPlayer1_3 += 1
                elif player1 == 2 and empty == 2:
                    opportunityOfPlayer1_2 += 1
                elif player1 == 1 and empty == 3:
                    opportunityOfPlayer1_1 += 1
                elif player2 == 3 and empty == 1:
                    opportunityOfPlayer2_3 += 1
                elif player2 == 2 and empty == 2:
                    opportunityOfPlayer2_2 += 1
                elif player2 == 1 and empty == 3:
                    opportunityOfPlayer2_1 += 1

        return opportunityOfPlayer2_3, opportunityOfPlayer2_2, opportunityOfPlayer2_1, opportunityOfPlayer1_3, opportunityOfPlayer1_2, opportunityOfPlayer1_1

    def heuristicFunction2(self, currentState):

        # find the opportunities for each player
        player1 = self.findNumberOfOpportunities1(currentState, 1)
        player2 = self.findNumberOfOpportunities1(currentState, 2)

        return (player2 - player1)*100

    def heuristicFunction3(self, currentState):

        # find the opportunities for each player
        player2_3, player2_2, player2_1, player1_3, player1_2, player1_1 = self.findNumberOfOpportunities2(
            currentState)

        opp2 = player2_3*1000 + player2_2*100 + player2_1*10
        opp1 = player1_3*1000 + player1_2*100 + player1_1*10

        return opp2 - opp1

    def EvaluateBoard(self, currentState):
        # Evaluate the given board state based on an evaluation function.
        # You need to implement this function to provide a heuristic evaluation.
        # This function should return a numerical value indicating the desirability of the board state.

        # find winner if any
        winner = self.winner(currentState)
        if winner == 2:
            # return 1000
            return 100000
        elif winner == 1:
            # return -1000
            return -100000
        return self.heuristicFunction3(currentState)

    def _CoinRowAfterAction(self, action, currentState):
        cRow = -1
        c = action
        for r in range(5, -1, -1):
            if currentState[r][c] == 0:
                cRow = r
                break
        return cRow

    def MakeMove(self, currentState, action, player):
        # Apply the given action (drop a coin into a column) for the specified player.
        # Return the resulting board state.

        # find the row in which the coin will be placed
        row = self._CoinRowAfterAction(action, currentState)

        # create a copy of the current state
        newState = copy.deepcopy(currentState)

        # place the coin
        newState[row][action] = player

        return newState

    def FindBestAction(self, currentState):
        """
        Modify this function to search the GameTree instead of getting input from the keyboard.
        The currentState of the game is passed to the function.
        currentState[0][0] refers to the top-left corner position.
        currentState[5][6] refers to the bottom-right corner position.
        Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
        Action 0 is refers to the left-most column and action 6 refers to the right-most column.
        """

        bestAction = self.MinimaxAlphaBeta(
            currentState, cutOffDepth, -float('inf'), float('inf'), True)
        # print("Best Action : {0}".format(bestAction))
        return bestAction


def LoadTestcaseStateFromCSVfile():
    testcaseState = list()

    with open('./testcases/testcase_easy1.csv', 'r') as read_obj:
        csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
        return testcaseState


def PlayGame():
    fourConnect = FourConnect()
    # fourConnect.PrintGameState()
    gameTree = GameTreePlayer()

    move = 0
    while move < 42:  # At most 42 moves are possible
        if move % 2 == 0:  # Myopic player always moves first
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner != None:
            break

    """
    You can add your code here to count the number of wins average number of moves etc.
    You can modify the PlayGame() function to play multiple games if required.
    # """
    if fourConnect.winner == None:
        print("Game is drawn.")
    else:
        print("Winner : Player {0}\n".format(fourConnect.winner))
    print("Moves : {0}".format(move))

    return fourConnect.winner, move


def RunTestCase():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """

    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move = 0
    while move < 5:  # Player 2 must win in 5 moves
        if move % 2 == 1:
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner != None:
            break

    if fourConnect.winner == 2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))


def PlayGameRandom():
    global cutOffDepth, recursiveMinimaxCalls

    for i in range(3):
        # play 100 games and count the number of wins for each player
        loss = 0
        wins = 0
        draws = 0

        avgMovesToWin = 0
        avgMovesToLose = 0
        avgMovesToDraw = 0
        avgRecursiveMinimaxCalls = 0
        avgDurationOfGame = 0

        for i in range(100):
            print("Game {0}".format(i + 1))
            startTime = time.time()
            winner, moves = PlayGame()
            endTime = time.time()
            durationOfGame = endTime - startTime
            avgDurationOfGame += durationOfGame

            if winner == 1:
                loss += 1
                avgMovesToLose += moves
            elif winner == 2:
                wins += 1
                avgMovesToWin += moves
            else:
                draws += 1
                avgMovesToDraw += moves

        if wins != 0:
            avgMovesToWin /= wins
        if loss != 0:
            avgMovesToLose /= loss
        if draws != 0:
            avgMovesToDraw /= draws

        avgRecursiveMinimaxCalls = recursiveMinimaxCalls / 100
        avgDurationOfGame /= 100

        # save the results in a text file for this cutoff depth
        with open('func3_results.txt', 'a') as f:
            f.write("With move ordering heuristic\n")
            f.write("Cutoff depth : {0}\n".format(cutOffDepth))
            f.write("Wins : {0}\n".format(wins))
            f.write("Loss : {0}\n".format(loss))
            f.write("Draws : {0}\n".format(draws))
            f.write("Average moves to win : {0}\n".format(avgMovesToWin))
            f.write("Average moves to lose : {0}\n".format(avgMovesToLose))
            f.write("Average moves to draw : {0}\n".format(avgMovesToDraw))
            f.write("Average recursive minimax calls : {0}\n".format(
                avgRecursiveMinimaxCalls))
            f.write("Average duration of game : {0}\n".format(
                avgDurationOfGame))
            f.write("\n")

        print("Cutoff depth : {0}".format(cutOffDepth))

        cutOffDepth += 1


def main():

    PlayGame()

    # PlayGameRandom()

    # RunTestCase()


if __name__ == '__main__':
    main()
