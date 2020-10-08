from random import random, randrange
import numpy as np

from tictactoe import TicTacToe, GameState


ALPHA = 0.2
GAMMA = 0.5

class QLearning:
    """Q learning algorithm to play TicTacToe"""
    def __init__(self, exploration=0.2):
        nr_states = 3 ** 9
        nr_actions = 9
        self.q_table = np.zeros((nr_states, nr_actions))
        self.exploration=exploration

    def make_move(self, board, exploration=True):
        state = TicTacToe.encode_board(board)
        if exploration and random() <= exploration:
            move = randrange(0,9)
        else:
            move = np.argmax(self.q_table[state])
        return move

    def train_move(self, move, illegal=False, win=False, lose=False):
        old_board, new_board, action = move
        reward = 10 if win else 0
        reward = -100 if illegal else reward
        reward = -10 if lose else reward
        state = TicTacToe.encode_board(old_board)
        new_state = TicTacToe.encode_board(new_board)
        old_val = self.q_table[state, action]
        new_val = np.max(self.q_table[new_state])
        new_q = (1 - ALPHA) * old_val + ALPHA * (reward + GAMMA * new_val)
        self.q_table[state, action] = new_q

    def train(self, moves, winner=False, loser=False):
        self.train_move(moves[-1], win=winner, lose=loser)
        moves.reverse()
        for move in moves[1:]:
            self.train_move(move)




