'''
Created on 21 Jul 2017

@author: Richard
'''
import unittest
from hive.core.game import Board, Game, Player
from hive.core.pieces import Piece
from hive.core.exceptions import InvalidPlaceError


# class TestGame(unittest.TestCase):
#     
#     def setUp(self):
#         self.game = Game()
#     
#     def test_game(self):
#         self.game.start()


class TestBoard(unittest.TestCase):

    def setUp(self):
        # Create simple board
        self.p1 = Player('p1')
        self.p2 = Player('p2')
        
        self.board = Board()
        self.a = Piece(self.p1)
        self.b = Piece(self.p2)
        self.c = Piece(self.p1)
        self.d = Piece(self.p2)
        self.e = Piece(self.p1)
        self.f = Piece(self.p2)
        self.g = Piece(self.p1)
        self.board.place_piece(2, -2, self.a)
        self.board.place_piece(3, -2, self.b)
        self.board.place_piece(3, -3, self.c)
        self.board.place_piece(2, -3, self.d)
        self.board.place_piece(1, -2, self.e)
        self.board.place_piece(1, -1, self.f)
        self.board.place_piece(2, -1, self.g)
        # Create invalid board
        self.board_unconnected = Board()
        self.board_unconnected.place_piece(0, 0, Piece())
        self.board_unconnected.place_piece(1, 1, Piece())
        
        self.board2 = Board()
        self.a2 = Piece()
        self.b2 = Piece()
        self.c2 = Piece()
        self.d2 = Piece()
        self.e2 = Piece()
        self.f2 = Piece()
        self.g2 = Piece()
        self.h2 = Piece()
        self.board2.place_piece(1, 1, self.a2)
        self.board2.place_piece(2, 1, self.b2)
        self.board2.place_piece(2, 0, self.c2)
        self.board2.place_piece(1, 0, self.d2)
        self.board2.place_piece(0, 1, self.e2)
        self.board2.place_piece(0, 2, self.f2)
        self.board2.place_piece(1, 2, self.g2)
        self.board2.place_piece(3, 0, self.h2)

    def tearDown(self):
        pass

    def test_adding_pieces(self):
        ''' Test for adding and retrieving pieces from the board '''
        self.assertEqual(self.board.get_piece(2, -2), self.a)
        self.assertEqual(self.board.get_piece(3, -2), self.b)
        self.assertEqual(self.board.get_piece(3, -3), self.c)
        self.assertEqual(self.board.get_piece(4, 5), None)
        # Try to place on already existing place:
        h = Piece()
        self.assertRaises(InvalidPlaceError, self.board.place_piece, 2, -2, h)
        # Try to place the same piece twice:
        self.assertRaises(InvalidPlaceError, self.board.place_piece, 2, -4, self.a)
    
    def test_get_neighbours(self):
        ''' Retrieving neighbours on the board '''
        neighbours = self.board.get_neighbours(2, -2)
        self.assertEqual(neighbours, [self.b, self.c, self.d, self.e, self.f, self.g])
        neighbours = self.board.get_neighbours(3, -2)
        self.assertEqual(neighbours, [None, None, self.c, self.a, self.g, None])
        neighbours = self.board.get_neighbours(-5, -5)
        self.assertEqual(neighbours, [None, None, None, None, None, None])
        n = self.board.get_neighbour(2, -2, (1, 0))
        self.assertEqual(n, self.b)
        n = self.board.get_neighbour(2, -2, (0, 1))
        self.assertEqual(n, self.g)
        n = self.board.get_neighbour(2, -2, (-1, 0))
        self.assertEqual(n, self.e)
        n = self.board.get_neighbour(3, -2, (1, -1))
        self.assertEqual(n, None)
    
    def test_complete_graph(self):
        self.assertTrue(self.board.connected_graph())
        self.assertFalse(self.board_unconnected.connected_graph())
        self.board.board.pop((2, -2))
        self.assertTrue(self.board.connected_graph())
        self.board.board.pop((2, -3))
        self.assertTrue(self.board.connected_graph())
        self.board.board.pop((2, -1))
        self.assertFalse(self.board.connected_graph())
    
    def test_breaks_hive(self):
        self.assertFalse(self.board.breaks_hive(2, -2))
        del self.board.board[(2, -2)]
        self.assertFalse(self.board.breaks_hive(3, -3))
        del self.board.board[(3, -3)]
        self.assertTrue(self.board.breaks_hive(1, -1))
        self.assertRaises(KeyError, self.board.breaks_hive, 2, -2)
        self.assertFalse(self.board_unconnected.breaks_hive(0, 0))
        del self.board_unconnected.board[(0, 0)]
        self.assertFalse(self.board_unconnected.breaks_hive(1, 1))
        
    def test_get_empty_space_line(self):
        e = self.board.get_empty_space_line(2, -2, (1, -1))
        self.assertEqual(e, (4, -4))
        e = self.board.get_empty_space_line(4, -2, (-1, 0))
        self.assertEqual(e, (0, -2))
        e = self.board.get_empty_space_line(0, 0, (0, -1))
        self.assertEqual(e, (0, -1))
        del self.board.board[(2, -2)]
        e = self.board.get_empty_space_line(0, -2, (1, 0))
        self.assertEqual(e, (2, -2))
        e = self.board.get_empty_space_line(4, -3, (-1, 1))
        self.assertEqual(e, (1, 0))
        
    def test_can_shift(self):
        self.assertFalse(self.board.can_shift(2, -2, (1, 0)))
        self.assertFalse(self.board.can_shift(2, -2, (1, -1)))
        self.assertFalse(self.board.can_shift(2, -2, (0, -1)))
        self.assertFalse(self.board.can_shift(2, -2, (-1, 0)))
        self.assertFalse(self.board.can_shift(2, -2, (-1, 1)))
        self.assertFalse(self.board.can_shift(2, -2, (0, 1)))
        
        self.assertTrue(self.board.can_shift(3, -2, (0, 1)))
        self.assertTrue(self.board.can_shift(3, -2, (1, -1)))
        self.assertFalse(self.board.can_shift(3, -2, (1, 0)))
        self.assertFalse(self.board.can_shift(3, -2, (0, -1)))
        self.assertFalse(self.board.can_shift(3, -2, (-1, 0)))
        
        del self.board.board[(3, -3)]
        self.assertFalse(self.board.can_shift(2, -2, (1, -1)))
        
    def test_axial_to_cube(self):
        self.assertEqual(self.board.axial_to_cube(2, -2), (2, -2, 0))
        self.assertEqual(self.board.axial_to_cube(0, 0), (0, 0, 0))
        self.assertEqual(self.board.axial_to_cube(1, 1), (1, 1, -2))
        
    def test_axial_to_offset(self):
        self.assertEqual(self.board.axial_to_offset(2, -2, 'odd-r'), (1, -2))
        self.assertEqual(self.board.axial_to_offset(1, -2, 'odd-r'), (0, -2))
        self.assertEqual(self.board.axial_to_offset(2, -2, 'even-r'), (1, -2))
        self.assertEqual(self.board.axial_to_offset(1, -2, 'even-r'), (0, -2))
        self.assertEqual(self.board.axial_to_offset(2, -2, 'odd-q'), (2, -1))
        self.assertEqual(self.board.axial_to_offset(1, -2, 'odd-q'), (1, -2))
        self.assertEqual(self.board.axial_to_offset(2, -2, 'even-q'), (2, -1))
        self.assertEqual(self.board.axial_to_offset(1, -2, 'even-q'), (1, -1))
              
    def test_output_board_hexjson(self):
        self.board.output_board_hexjson('odd-r', indent=4, file='board.hexjson')
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
