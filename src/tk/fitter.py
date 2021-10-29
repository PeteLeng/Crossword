# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 12:50:36 2021

@author: Pete
"""
import copy
from .crossword import Crossword
from .word import Word


def find_matches(word, crossword):
    """
    Given a word and a crossword,
    find all combinations of matching letters between the word and the crossword,
    return the index, loc tuples of all matches.

    Parameters
    ----------
    word : Word
    crossword : Crossword

    Returns
    -------
    List, a list of 2-tuples.
    First element is the index of the match in the word,
    second element is the key of the match in the crossword openLocs dictionary.

    """
    return [(i,loc) for i in range(len(word.letters))
            for loc in crossword.open_locs
            if word.letters[i] == crossword.open_locs[loc]]


def gen_fits(word, crossword):
    """
    Given a word and crossword, 
    return a generator that generate all possible fits.

    Parameters
    ----------
    word : Word
    
    crossword : Crossword

    Yields
    ------
    Crossword.

    """
    if not crossword.get_word_strings():
        fit = copy.deepcopy(crossword)
        fit.add(copy.deepcopy(word))
        yield fit
    if word not in crossword:
        matches = find_matches(word, crossword)
        while matches:
            w_idx, cw_loc = matches.pop(0)
            w_dir = not crossword.word_dir_at_loc(cw_loc)
            word.place(w_idx, cw_loc, w_dir)
            if crossword.check_fit(word):
                fit = copy.deepcopy(crossword)
                fit.add(copy.deepcopy(word))
                yield fit
    else:
        print('Word already exists in Crossword')
        yield crossword
    

def gen_crosswords(w_list, cw_list=[Crossword()]):
    if not w_list:
        for cw in cw_list:
            yield cw
    else:
        word = Word(w_list[0])
        exists_fit = False
        for crossword in cw_list:
            fits = [cw for cw in gen_fits(word, crossword)]
            if fits:
                yield from gen_crosswords(w_list[1:], fits)
                exists_fit = True
        if not exists_fit:
            for crossword in cw_list:
                yield crossword


def printCrosswords(cwList):
    res = ''
    for cw in cwList:
        wordsText = ''
        for word in cw.get_word_strings():
            wordsText += word + ', '
        res += 'The crossword is made up of <{}>\n'.format(wordsText[:-2])
        res += str(cw) + '\n'
    print (res[:-1])


def main():
    w1 = Word('APPLE')
    w2 = Word('PINEAPPLE')
    w3 = Word('WATERMELLON')
    cw1 = Crossword()
    cw3 = Crossword()
    cw1.add(w1)
    cw3.add(w3)

    # Test find_matches
    # matches = find_matches(w2, cw1)
    # print(matches)

    # Test genFits
    # fits = gen_fits(w2, cw1)
    # print(next(fits))
    # for fit in fits:
    #     print(fit, '\n')

    # Test generator
    # genCWs = genCrosswords(['APPLE', 'PEACH', 'ROBOT'], [Crossword()])
    # try:
    #     print(next(genCWs))
    # except StopIteration:
    #     print('No crossword made!')
    # count = 0
    # for cw in genCWs:
    #     # print(cw.xRange)
    #     # print(cw.yRange)
    #     print("Dimension of {}: {}".format(cw.getWords(), cw.getDimension()))
    #     print(cw, '\n')
    #     count += 1
    # print(count)


if __name__ == '__main__':
    main()
