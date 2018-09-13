# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 23:24:50 2018

@author: HP PC
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test.py

import sys
import pytest

import picross

class TestCouple:
	def test_valid_couple(self):
		assert picross.couple([True] , [False]) == [True]
		assert picross.couple([False], [True] ) == [False]
		assert picross.couple([False], [False]) == [None]
	
	def test_length_mismatch(self):
		with pytest.raises(ValueError):
			picross.couple([True], [False, False])
	
	def test_conflicting_sequences(self):
		with pytest.raises(ValueError):
			picross.couple([True], [True])

def test_decouple():
	assert picross.decouple([True]) == ([True], [False])
	assert picross.decouple([False]) == ([False], [True])
	assert picross.decouple([None]) == ([False], [False])


class TestLinePermutations:
	def test_valid_data(self):
		assert picross.line_permutations([1], 1) == [[True]]
		assert picross.line_permutations([], 1) == [[False]]
	
	def test_invalid_data(self):
		with pytest.raises(ValueError):
			picross.line_permutations([0], 1)
	
	def test_hard_cases(self):
		assert picross.line_permutations([1, 2, 1], 6) == \
				[[True, False, True, True, False, True]]
		assert picross.line_permutations([1, 2], 5, [True] + [None] * 4) == \
				[[True, False, True, True, False],
				 [True, False, False, True, True]]

class TestFindConstraint:
	def test_valid_permutations(self):
		assert picross.find_constraint([[True] , [True] ]) == [True]
		assert picross.find_constraint([[True] , [False]]) == [None]
		assert picross.find_constraint([[False], [False]]) == [False]
	
	def test_many_permutations(self):
		assert picross.find_constraint([[True], [True], [False]]) == [None]
		assert picross.find_constraint([[True, False], 
		                                [False, True]]) == [None, None]
		
	
	def test_empty_permutations(self):
		assert picross.find_constraint([[]]) == []
		assert picross.find_constraint([[], [], []]) == []


if __name__ == "__main__":
	sys.exit(pytest.main(__file__))