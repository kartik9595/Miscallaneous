# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 23:32:32 2018

@author: HP PC
"""



class Unsolvable(Exception):
    """Thrown when there is no solution (or we get stuck)"""
    pass

def elements_normalize(elements):
    """Filters zeroes from elements list"""
    return [e for e in elements if e > 0]

def element_to_list(element):
    """Converts an element to a list of True blocks"""
    return [True] * element

def elements_exact_row(elements):
    """For the given elements, return the most compact representation."""
    result = []
    for e in elements:
        if not e:
            continue
        if len(result):
            result.append(False)
        result.extend(element_to_list(e))

    return result

def pad(padlen):
    """Returns false padding for the given `padlen`gth"""
    return [False] * padlen

def elements_combinations(elements, size):
    """Returns all combinations of `elements` that can fit in 1d size"""
    elements = elements_normalize(elements)
    if len(elements) == 0:
        return [[False] * size]

    min_size = sum(elements) + len(elements) - 1

    if min_size > size:
        raise Unsolvable()

    if min_size == size:
        return [elements_exact_row(elements)]


    results = []
    for padlen in xrange(size - min_size + 1):
        first = elements[0]
        firstl = element_to_list(first)
        remaining = elements[1:]

        rpad = size - padlen - first - 1
        for result in elements_combinations(remaining, rpad):
            if rpad >= 0:
                results.append(pad(padlen) + firstl + [False] + result)
            else:
                results.append(pad(padlen) + firstl + result)

    return results 

def row_check_conflict(row1, row2):
    """Returns False if row1 and row2 have any conflicts.
    
    A conflict is where one position in a row is True while the other is False."""
    assert len(row1) == len(row2)
    for i, v1 in enumerate(row1):
        v2 = row2[i]
        # The solution can't conflict if either row is "None" (unknown).
        if v1 is None or v2 is None:
            continue

        if v1 != v2:
            return False

    # No conflicts in the entire row.  We must be good.
    return True

def find_commonalities(results):
    """Merges a merged row, with None in conflicting positions and True/False where consistent."""
    common = results[0]
    for result in results[1:]:
        for i, v in enumerate(result):
            if common[i] != v:
                common[i] = None
    return common

import copy

class Board(object):
    """Class for managing board state"""
    def __init__(self, width, height):
        """Constructor takes width, height as args"""
        self.width = width
        self.height = height
        self.rows = []

        # Init with None (Unknown state)
        for i in xrange(height):
            self.rows.append([None] * width)

        # Don't forget to overwrite these fields before trying to solve!
        self.col_elements = [[]] * width
        self.row_elements = [[]] * height

    def row(self, i):
        """Returns a copy of row i"""
        return self.rows[i][:]

    def col(self, j):
        """Returns a copy of row j"""
        result = []
        for i in xrange(self.height):
            result.append(self.rows[i][j])
        return result

    def set_row(self, i, row):
        """Updates `row` i"""
        self.rows[i] = row[:]
        print self.render()
        print '---'

    def set_col(self, j, col):
        """Updates `col` j"""
        for i, v in enumerate(col):
            self.set_cell(i, j, v)
        print self.render()
        print '---'

    def set_cell(self, i, j, value):
        """Sets cell at row i at col j"""
        self.rows[i][j] = value

    def solve(self):
        """Try to solve.  Returns if we finish or get stuck"""
        while True:
            oldrows = copy.deepcopy(self.rows)
            self.solve1()
            if self.rows == oldrows:
                return

    def solve1(self):
        """A single pass/iteration of our solve algorithm"""
        for i in xrange(self.height):
            row = self.row(i)

            # If the row is already solved, skip it.
            if None not in row:
                continue

            # Find all combinations of the set of elements within the puzzle width.
            possibilities = elements_combinations(self.row_elements[i], self.width)

            # Filter possibilities that conflict with the current board state
            possibilities = [
                possibility for possibility
                in possibilities
                if row_check_conflict(row, possibility)
            ]

            # Oops!  Something went wrong...
            if len(possibilities) == 0:
                raise Unsolvable()

            # There's only one possibility.  SET IT.
            elif len(possibilities) == 1:
                self.set_row(i, possibilities[0])
            else:

                # Multiple possibilties.  Find any patterns, and update the
                # row accordingly.
                commonalities = find_commonalities(possibilities)
                if commonalities != row:
                    self.set_row(i, commonalities)

        # Same as the above, but for every column instead of every row.
        for j in xrange(self.width):
            col = self.col(j)
            if None not in col:
                continue
            possibilities = [
                possibility for possibility
                in elements_combinations(self.col_elements[j], self.height)
                if row_check_conflict(col, possibility)
            ]

            if len(possibilities) == 0:
                raise Unsolvable()
            elif len(possibilities) == 1:
                self.set_col(j, possibilities[0])
            else:
                commonalities = find_commonalities(possibilities)
                if commonalities != col:
                    self.set_col(j, commonalities)

    def render(self):
        """Returns a unicode representation of the board.
        whitespace is used for unknown values (None)
        dark shade is used for True values
        light shade is used for False values
        """
        result = ''
        for row in self.rows:
            for v in row:
                if v is True:
                    result += 2*u'\u2593'
                elif v is False:
                    result += 2*u'\u2591'
                elif v is None:
                    result += '  '
            result += '\n'
        return result.rstrip('\n')