'''
Created on 21 Aug 2017

@author: Richard
'''
import unittest, os
from hive.core.game import Board, Game, Player, Action, ActionMovePiece, ActionPlacePiece
from hive.core.pieces import Ant
from hive.core.exceptions import InvalidPlace, InvalidMove

class TestAction(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.board = self.game.board
        self.p1 = self.game.player1
        self.p2 = self.game.player2

    def tearDown(self):
        pass
    
    def test_place_piece(self):
        ''' 
        First turn can place anywhere.
        Second turn must place next to the first piece.
        Third turn must place onto hive and not against enemy pieces.
        Must have piece available.
        Must place bee in 4 turns.
        '''
        # First turn:
        self.assertEqual(self.game.turn, 0)
        self.assertEqual(self.game.active_player, self.p1)
        self.assertEqual(len(self.p1.ant), 3)
        ActionPlacePiece(self.p1.ant.pop(), 0, 0)
        self.assertEqual(self.board.get(0, 0).player, self.p1)
        self.assertEqual(self.board.get(0, 0).q, 0)
        self.assertEqual(self.board.get(0, 0).r, 0)
        self.assertIsInstance(self.board.get(0, 0), Ant)
        self.assertEqual(len(self.p1.ant), 2)
        self.assertEqual(self.game.turn, 1)
        self.assertEqual(self.game.active_player, self.p2)
        
        # Second turn:
        ActionPlacePiece(self.p2.ant.pop(), 1, -1)
        self.assertEqual(self.game.turn, 2)
        self.assertEqual(self.game.active_player, self.p1)
        
        # Third turn:
        ActionPlacePiece(self.p1.ant.pop(), -1, 1)
        
        # Fourth turn:
        # First try some invalid actions:
        with self.assertRaises(InvalidPlace):
            # Try placing piece against enemies piece:
            ActionPlacePiece(self.p2.ant.pop(), 0, -1)
            # Try placing on top of another piece:
            ActionPlacePiece(self.p2.ant.pop(), 0, 0)
            # Try placing a piece disconnected from the hive
            ActionPlacePiece(self.p2.ant.pop(), 10, 10)
        
        with self.assertRaises(InvalidMove):
            # Move piece before placing bee
            ActionMovePiece(self.board.get(1, -1), 1, 0)
        ActionPlacePiece(self.p2.bee.pop(), 2, -1)
        
        # Fifth turn:
        ActionPlacePiece(self.p1.ant.pop(), 0, 1)
        
        # Sixth turn:
        self.assertEqual(self.game.turn, 5)
        with self.assertRaises(InvalidMove):
            ActionMovePiece(self.board.get(1, -1), 1, 0)
            ActionMovePiece(self.board.get(2, -1), -1, 0)
        ActionMovePiece(self.board.get(2, -1), 1, 0)
        # Seventh turn:
        with self.assertRaises(IndexError):
            ActionPlacePiece(self.p1.ant.pop(), 0, 1)
        
        self.board.save_board()
    
    def test_move_piece(self):
        ''' 
        Can only move your own pieces.
        
        '''
        pass

    def test_normal_game(self):
        pass
        # ActionPlacePiece('Ant', self.p1, self.game, 0, 0)
    
    def test_asdf(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()