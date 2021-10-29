# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 20:02:12 2021

@author: Pete
"""
import numpy as np


class Word(object):
    def __init__(self, word):
        self.word = word
        self.letters = [cha for cha in word]
        self.locations = None
        self.direction = None
        self.x_range = None
        self.y_range = None
        self.default()
        
    def place(self, index, toLoc, direction):
        self.direction = direction
        unit = np.array((0, 1)) if self.direction else np.array((1, 0))
        self.locations = {tuple(np.array(toLoc)+unit*(i-index)):i
                          for i in range(len(self.letters))}
        self.x_range = (toLoc[0], toLoc[0]) if self.direction \
            else (toLoc[0]-index, toLoc[0]-index+len(self.word)-1)
        self.y_range = (toLoc[1], toLoc[1]) if not self.direction \
            else (toLoc[1]-index, toLoc[1]-index+len(self.word)-1)
        
    def transform(self, del_xy):
        self.locations = {tuple(np.array(loc)+np.array(del_xy)):idx
                          for loc,idx in self.locations.items()}
        del_x, del_y = del_xy
        self.x_range = tuple(np.array(self.x_range) + np.array([del_x, del_x]))
        self.y_range = tuple(np.array(self.y_range) + np.array([del_y, del_y]))

    def default(self):
        self.place(0, (0, 0), 0)

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, word):
        self._word = word

    @property
    def letters(self):
        return self._letters

    @letters.setter
    def letters(self, c_list):
        self._letters = c_list

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        """
        Enter 1 for vertical, 0 for horizontal
        """
        self._direction = direction

    @property
    def locations(self):
        return self._locations

    @locations.setter
    def locations(self, loc_dict):
        self._locations = loc_dict

    @property
    def x_range(self):
        return self._x_range

    @x_range.setter
    def x_range(self, x_tuple):
        self._x_range = x_tuple

    @property
    def y_range(self):
        return self._y_range

    @y_range.setter
    def y_range(self, y_tuple):
        self._y_range = y_tuple

    def get_cha_at_loc(self, loc):
        return self.word[self.locations[loc]]

    def get_loc_of_idx(self, idx):
        return list(self.locations.keys())[list(self.locations.values()).index(idx)]

    def get_neighbors(self, idx_list):
        """
        Given a list of index, return a list of neighboring locations (tuples) 
        of characters in the index positions of the word.

        Parameters
        ----------
        idx_list : List
        A list of indices
        
        Returns
        -------
        neighbors : List
        A list of neighboring locations of chosen indices

        """
        neighbors = []
        if self.direction:
            for idx in idx_list:
                idx_loc = self.get_loc_of_idx(idx)
                if idx == 0:
                    neighbors.append((idx_loc[0], idx_loc[1]-1))
                if idx == len(self.word)-1:
                    neighbors.append((idx_loc[0], idx_loc[1]+1))
                neighbors.append((idx_loc[0]-1, idx_loc[1]))
                neighbors.append((idx_loc[0]+1, idx_loc[1]))
        else:
            for idx in idx_list:
                idx_loc = self.get_loc_of_idx(idx)
                if idx == 0:
                    neighbors.append((idx_loc[0]-1, idx_loc[1]))
                neighbors.append((idx_loc[0], idx_loc[1]-1))
                neighbors.append((idx_loc[0], idx_loc[1]+1))
                if idx == len(self.word)-1:
                    neighbors.append((idx_loc[0]+1, idx_loc[1]))
        return neighbors
    
    def __str__(self):
        # if self.locations is None:
        #     self.default()
        res = ''
        for loc in self.locations:
            res += '{}: {}'.format(self.get_cha_at_loc(loc), loc)+'\n'
        return res[:-1]
    
    def __eq__(self, other):
        if self.word != other.word:
            print('They are different words!')
            return False
        for loc in self.locations:
            if loc not in other.locations or other.get_cha_at_loc(loc) != self.get_cha_at_loc(loc):
                print("They are in different location!")
                return False
        return True

def main():
    apple = Word('APPLE')
    apple.direction = 0
    apple.place(0, (0, 1), 0)
    apple2 = Word('APPLE')

    # Test equality
    # print(apple == apple2)
    # print(apple.x_range)
    # print(apple.y_range)
    # print(apple2.x_range)

    # Test locations property
    # locs = apple.locations
    # print(locs)
    # print((6, 10) in locs)

    # Test trasform
    # apple.transform((2, 2))
    # print(apple.locations)
    # print(apple.get_loc_of_idx(3))

    # Test get_neighbors
    # print(apple.locations)
    # print(apple.get_neighbors(range(5)))

if __name__ == '__main__':
    main()
    