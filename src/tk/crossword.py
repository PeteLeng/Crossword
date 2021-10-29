# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 11:41:30 2021

@author: Pete
"""
import numpy as np
from .word import Word


class Crossword(object):
    def __init__(self):
        self._words = []
        self.all_locs = {}
        self.joint_locs = {}
        self.open_locs = {}
        self.x_range = ()
        self.y_range = ()

    @property
    def words(self):
        return self._words

    @property
    def all_locs(self):
        return self._all_locs

    @all_locs.setter
    def all_locs(self, all_dict):
        self._all_locs = all_dict

    @property
    def joint_locs(self):
        return self._joint_locs

    @joint_locs.setter
    def joint_locs(self, joint_dict):
        self._joint_locs = joint_dict

    @property
    def open_locs(self):
        return self._open_locs

    @open_locs.setter
    def open_locs(self, open_dict):
        self._open_locs = open_dict

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

    def update_opens(self, loc):
        """
        Given a location tuple (of a jointLocation),
        update the openLocs dict,
        excluding all openLocations that are 1 unit away from the given location

        Parameters
        ----------
        loc : Tuple, location tuple of a jointLocation.

        Returns
        -------
        None, update the openLocs dictionary inplace

        """
        self.open_locs = {open_loc:cha for open_loc, cha in self.open_locs.items()
                          if abs(open_loc[0]-loc[0]) + abs(open_loc[1]-loc[1]) > 1}

    def update_locs(self, word):
        """
        Given a word that fits in the crossword,
        update locations of the word in the jointLocs, allLocs, openLocs dictionary,
        Go through all jointLocations, update the openLocs inplace.

        Parameters
        ----------
        word : Word, a word object that fits the crossword

        Returns
        -------
        None. updates all locs diction inplace.

        """
        for w_loc in word.locations.keys():
            if w_loc in self.all_locs:
                self.joint_locs[w_loc] = word.get_cha_at_loc(w_loc)
            else:
                self.all_locs[w_loc] = word.get_cha_at_loc(w_loc)
                self.open_locs[w_loc] = word.get_cha_at_loc(w_loc)
        for c_loc in self.joint_locs:
            self.update_opens(c_loc)

    def update_range(self, word):
        w_x_range = word.x_range
        w_y_range = word.y_range
        if not self.x_range or not self.y_range:
            self.x_range = w_x_range
            self.y_range = w_y_range
        else:
            x_high = max(self.x_range[1], w_x_range[1])
            x_low = min(self.x_range[0], w_x_range[0])
            y_high = max(self.y_range[1], w_y_range[1])
            y_low = min(self.y_range[0], w_y_range[0])
            self.x_range = (x_low, x_high)
            self.y_range = (y_low, y_high)

    def add(self, word):
        self.words.append(word)
        self.update_locs(word)
        self.update_range(word)

    def refresh_locs(self):
        self.all_locs = {}
        self.joint_locs = {}
        self.open_locs = {}
        for word in self.words:
            for loc in word.locations:
                if loc in self.all_locs:
                    self.joint_locs[loc] = word.get_cha_at_loc(loc)
                else:
                    self.all_locs[loc] = word.get_cha_at_loc(loc)
        for c_loc in self.joint_locs:
            self.update_opens(c_loc)
    
    def refresh_range(self):
        self.x_range = ()
        self.y_range = ()
        for word in self.words:
            w_x_range = word.x_range
            w_y_range = word.y_range
            if not self.x_range or not self.y_range:
                self.x_range = w_x_range
                self.y_range = w_y_range
            else:
                x_high = max(self.x_range[1], w_x_range[1])
                x_low = min(self.x_range[0], w_x_range[0])
                y_high = max(self.y_range[1], w_y_range[1])
                y_low = min(self.y_range[0], w_y_range[0])
                self.x_range = (x_low, x_high)
                self.y_range = (y_low, y_high)
        
    def transform(self, del_xy):
        [word.transform(del_xy) for word in self.words]
        self.refresh_locs()
        self.refresh_range()

    def get_word_strings(self):
        """
        Return a list of word strings in the crossword.

        Returns
        -------
        list, a list of strings

        """
        return [word.word for word in self.words]
    
    def get_word_by_string(self, word_string):
        for w in self.words:
            if w.get_word_by_string() == word_string:
                return w

    def get_dimension(self):
        return [int((self.x_range[1]+self.x_range[0])/2), int((self.y_range[1]+self.y_range[0])/2)]

    def word_dir_at_loc(self, loc):
        """
        Given a location tuple, return the direction of the word on the location.
        The given location has to be an open location.

        Parameters
        ----------
        loc : Tuple, the location tuple of an open location.

        Returns
        -------
        Boolean, 1 for vertical, 0 for horizontal

        """
        return 1 if tuple(np.array(loc) + np.array((0, 1))) in self.all_locs or \
                    tuple(np.array(loc) + np.array((0, -1))) in self.all_locs else 0

    def check_fit(self, word):
        """
        Given an word object of a particular placement,
        check if the placement fits the crossword.

        Parameters
        ----------
        word : Word

        Returns
        -------
        Boolean, True if no collision, False otherwise

        """
        # Check collision
        idx_list = []
        for i in range(len(word.word)):
            loc = word.get_loc_of_idx(i)
            if loc in self.all_locs:
                if word.get_cha_at_loc(loc) != self.all_locs[loc]:
                    return False
            else:
                idx_list.append(i)

        # Check connectivity
        neighbor_locs = word.get_neighbors(idx_list)
        for neighbor_loc in neighbor_locs:
            if neighbor_loc in self.all_locs:
                return False

        return True

    def get_loc_str(self):
        return {f"{k[0]},{k[1]}":v for k, v in self.all_locs.items()}

    def get_words_str(self):
        res = {}
        for w in self.words:
            loc = w.get_loc_of_idx(0)
            res[f'{loc[0]},{loc[1]}'] = w.word
        return res

    def __str__(self):
        if not self.words:
            return 'This is an empty crossword!'
        res = ''
        for word in self.words:
            res += 'Location of {}: \n'.format(word.word) + str(word) + '\n'
        return res[:-1]
    
    def __contains__(self, word_or_loc):
        if isinstance(word_or_loc, Word):
            return word_or_loc.word in self.get_word_strings()
        elif isinstance(word_or_loc, tuple):
            return word_or_loc in self.all_locs
        else:
            return "Incomprehensible type"
    
    def __eq__(self, other):
        if len(self.words) != len(other.words):
            return False
        for word in self.words:
            if word not in other:
                print("They don't have the same words!")
                return False
            if word != other.get_word_by_string(word.word):
                # print("They are not in the same location!")
                return False
        return True

def main():
    # wordList = ['CHRISTMAS', 'CHRISTMASEVE', 'COAT', 'LETTER', 'CROSS',
    #             'TREE', 'DECORATIONS', 'PRESENTS', 'FATHER', 'CHAIR']
    wordList = ['KING', 'XENOMORGPH', 'SIT']
    word1 = Word(wordList[0])
    word2 = Word(wordList[1])
    cw = Crossword()
    cw.add(word1)

    # Test add
    # for w in wordList:
    #     word = Word(w)
    #     cw.add(word)
    # print(cw.get_word_strings())
    # print(cw.joint_locs)
    # print(cw.all_locs)

    # Test __str__, get_dimension
    # print(cw)
    # print("Dimension of {}: {}".format(cw.get_word_strings(), cw.get_dimension()))

    # Test refresh
    # cw.refresh_locs()
    # print('Refreshed', cw)
    # print('Refreshed dimension {}: {}'.format(cw.get_word_strings(), cw.get_dimension()))

    # Test transform
    # cw.transform((5, 5))
    # cw.refresh_locs()
    # print('Transformed', cw)
    # print(cw.all_locs)
    # print('Transformed dimension', cw.get_dimension())

    # Test contain
    # print(word1 in cw)
    # print(word2 in cw)
    # for loc in word1.locations.keys():
    #     print(loc in cw)

    # Test get_loc_str, get_words_str,
    # transform dictionary key from tuple to string type,
    # such that json could serialized it
    print(cw.all_locs)
    print(cw.get_loc_str())
    print(cw.get_words_str())


if __name__ == '__main__':
    main()
