'''
Created on 21 Jul 2017

@author: Richard
'''
import unittest
from hive.core.pieces import Piece, Ant, Bee, Beetle, Grasshopper, Spider
from hive.core.game import Board


class PiecesTest(unittest.TestCase):


    def setUp(self):
        self.board = Board()
        self.b = Piece(None, self.board, 3, -2)
        self.c = Piece(None, self.board, 3, -3)
        self.d = Piece(None, self.board, 2, -3)
        self.e = Piece(None, self.board, 1, -2)
        self.f = Piece(None, self.board, 1, -1)


    def tearDown(self):
        pass

    def test_ant(self):
        a = Ant(None, self.board, 0, -2)
        possible_moves = a.get_possible_moves()
        self.assertEqual(len(possible_moves), 12)
        a1 = Ant(None, self.board, -1, -2)
        possible_moves = a.get_possible_moves()
        self.assertCountEqual(possible_moves, [])
        
    def test_bee(self):
        b = Bee(None, self.board, 2, -2)
        possible_moves = b.get_possible_moves()
        self.assertCountEqual(possible_moves, [])
        self.assertFalse(b.is_surrounded())
        b2 = Bee(None, self.board, 0, -2)
        possible_moves = b2.get_possible_moves()
        self.assertCountEqual(possible_moves, [(1, -3), (0, -1)])
        p = Piece(None, self.board, 2, -1)
        self.assertTrue(b.is_surrounded())
    
    def test_beetle(self):
        beetle = Beetle(None, self.board, 0, -2)
        possible_moves = beetle.get_possible_moves()
        self.assertCountEqual(possible_moves, [(1, -2), (1, -3), (0, -1)])
        
    def test_grasshopper(self):
        g = Grasshopper(None, self.board, 2, -2)
        possible_moves = g.get_possible_moves()
        self.assertCountEqual(possible_moves, [(4, -2), (4, -4), (2, -4), 
                                               (0, -2), (0, 0)])
        g2 = Grasshopper(None, self.board, 4, -2)
        g3 = Grasshopper(None, self.board, 5, -2)
        self.assertCountEqual(g2.get_possible_moves(), [])
        self.assertCountEqual(g3.get_possible_moves(), [(0, -2)])

    def test_spider(self):
        s = Spider(None, self.board, 0, -2)
        possible_moves = s.get_possible_moves()
        self.assertCountEqual(possible_moves, [(3, -4), (1, 0)])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

