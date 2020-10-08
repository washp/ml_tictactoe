from copy import deepcopy

from tictactoe import TicTacToe, GameState
from myalgo import MyAlgo
from qlearning import QLearning


EPISODES = 1000000
EXPLORATION = 0.5


def main(algo):
    game = TicTacToe()
    player_wins = {1:0, 2:0}
    exp_step = EXPLORATION/(EPISODES*0.75)
    for i in range(EPISODES):
        algo.exploration -= exp_step
        if algo.exploration < 0:
            algo.exploration = 0
        player_moves = {1:[], 2:[]}
        winner = None
        if (i % 1000 == 0):
            print(f'Running episode {i}')
            print(f'Exploration: {round(algo.exploration,2)}')
            #print(f'Player1 wins: {player_wins[1]}\nPlayer2 wins: {player_wins[2]}')
            print(f'Total wins: {player_wins[1] + player_wins[2]}')
            player_wins = {1: 0, 2: 0}
        nr_of_moves = 0
        while game.get_gamestate() == GameState.ONGOING:
            for player in range(1,3):
                if player == 2:
                    board = game.get_inv_board()
                else:
                    board = game.board

                legal_move = False
                while not legal_move:
                    move = algo.make_move(board)
                    old_board = deepcopy(board)
                    legal_move = game.play(player, move)
                    if player == 2:
                        board = game.get_inv_board()
                    else:
                        board = game.board
                    if not legal_move:
                        algo.train_move((old_board, deepcopy(board), move), illegal=True)
                    else:
                        player_moves[player].append((old_board, deepcopy(board), move))

                if game.get_gamestate() == GameState.WON:
                    winner = player
                    player_wins[player] += 1
                    break
                nr_of_moves += 1
                if nr_of_moves >= 9:
                    break
        if game.get_gamestate() == GameState.WON:
            algo.train(player_moves[1], winner=(winner == 1), loser=(winner != 1))
            algo.train(player_moves[2], winner=(winner == 2), loser=(winner != 2))
        else:
            algo.train(player_moves[1])
            algo.train(player_moves[2])
        game.clear_board()

    nr_of_moves = 0
    while game.get_gamestate() == GameState.ONGOING:
        #Human player
        print(game)
        move = int(input('Move: '))-1
        game.play(1,move)
        if game.get_gamestate() == GameState.WON:
            winner = 1
            continue
        nr_of_moves += 1
        if nr_of_moves > 9:
            break
        #AI player
        move = algo.make_move(game.get_inv_board(), exploration=False)
        game.play(2, move)
        if game.get_gamestate() == GameState.WON:
            winner = 2
        nr_of_moves += 1
        if nr_of_moves > 9:
            break
    print(game)

if __name__ == '__main__':
    #main(MyAlgo())
    main(QLearning(exploration=0.2))
