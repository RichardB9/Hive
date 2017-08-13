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
        self.b = Piece()
        self.c = Piece()
        self.d = Piece()
        self.e = Piece()
        self.f = Piece()

        self.board.place_piece(3, -2, self.b)
        self.board.place_piece(3, -3, self.c)
        self.board.place_piece(2, -3, self.d)
        self.board.place_piece(1, -2, self.e)
        self.board.place_piece(1, -1, self.f)


    def tearDown(self):
        pass

    def test_ant(self):
        a = Ant()
        self.board.place_piece(0, -2, a)
        possible_moves = a.get_possible_moves()
        self.assertEqual(len(possible_moves), 12)
        a1 = Ant()
        self.board.place_piece(-1, -2, a1)
        possible_moves = a.get_possible_moves()
        self.assertCountEqual(possible_moves, [])
        
    def test_bee(self):
        b = Bee()
        self.board.place_piece(2, -2, b)
        possible_moves = b.get_possible_moves()
        self.assertCountEqual(possible_moves, [])
        self.assertFalse(b.is_surrounded())
        b2 = Bee()
        self.board.place_piece(0, -2, b2)
        possible_moves = b2.get_possible_moves()
        self.assertCountEqual(possible_moves, [(1, -3), (0, -1)])
        p = Piece()
        self.board.place_piece(2, -1, p)
        self.assertTrue(b.is_surrounded())
    
    def test_beetle(self):
        beetle = Beetle()
        self.board.place_piece(0, -2, beetle)
        possible_moves = beetle.get_possible_moves()
        self.assertCountEqual(possible_moves, [(1, -2), (1, -3), (0, -1)])
        
    def test_grasshopper(self):
        g = Grasshopper()
        self.board.place_piece(2, -2, g)
        possible_moves = g.get_possible_moves()
        self.assertCountEqual(possible_moves, [(4, -2), (4, -4), (2, -4), 
                                               (0, -2), (0, 0)])
        g2 = Grasshopper()
        g3 = Grasshopper()
        self.board.place_piece(4, -2, g2)
        self.board.place_piece(5, -2, g3)
        self.assertCountEqual(g2.get_possible_moves(), [])
        self.assertCountEqual(g3.get_possible_moves(), [(0, -2)])

    def test_spider(self):
        s = Spider()
        self.board.place_piece(0, -2, s)
        possible_moves = s.get_possible_moves()
        self.assertCountEqual(possible_moves, [(3, -4), (1, 0)])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

