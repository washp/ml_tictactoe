from random import random

import numpy as np
from sklearn.neural_network import MLPClassifier
import warnings
from sklearn.exceptions import ConvergenceWarning


warnings.filterwarnings("ignore", category=ConvergenceWarning)

HIDDEN_LAYER_SIZE = (25,2)
EXPLORATION = 0.1

class MyAlgo:
    """An experiment from my side, which doesn't work, this class is incompatible with new format"""
    def __init__(self):
        self.x_init = np.random.random_integers(0,2,(9,9))
        self.y_init = np.arange(9)
        self.x = None
        self.y = None
        self.clf = MLPClassifier(solver='lbfgs',
                            alpha=1e-5,
                            hidden_layer_sizes=HIDDEN_LAYER_SIZE,
                            random_state=1,
                            max_iter=10000)
        self.clf.fit(self.x_init, self.y_init)

    def _add_x(self, new_x):
        if self.x is None:
            self.x = new_x
        else:
            np.vstack((self.x,new_x))

    def _add_y(self, new_y):
        if self.y is None:
            self.y = new_y
        else:
            np.append(self.y, new_y)

    def make_move(self, game, board, player, exploration=True):
        if exploration and random() <= EXPLORATION:
            move = np.arange(9).flatten()
            np.random.shuffle(move)
            pass
        else:
            board = np.array(board).reshape(1,-1)
            probability = self.clf.predict_proba(board)
            move = np.argsort(probability).flatten()
            move = np.flip(move)
        legal_move = False
        for i in range(9):
            legal_move = game.play(player, move[i])
            if legal_move:
                break

        return move[i]

    def add_data(self, data):
        new_x = []
        new_y = []
        for tuple in data:
            new_x.append(tuple[0])
            new_y.append(tuple[1])
        self._add_x(np.array(new_x))
        self._add_y(np.array(new_y))

    def retrain(self):
        if self.y is not None:
            for i in range(9):
                if i in self.y:
                    index = np.argwhere(self.y_init == i)
                    self.x_init = np.delete(self.x_init, index, 0)
                    self.y_init = np.delete(self.y_init, index, 0)
        x = np.vstack((self.x_init, self.x))
        y = np.append(self.y_init, self.y)
        self.clf.fit(x, y)


