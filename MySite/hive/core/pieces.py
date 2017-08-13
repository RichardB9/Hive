'''
Created on 21 Jul 2017

@author: Richard
'''

from hive.core.exceptions import InvalidMove

class Piece(object):
    
    def __init__(self, player=None, board=None, q=None, r=None):
        self.player = player
        self.board = board
        self.q = q
        self.r = r
        
    def get_possible_moves(self):
        ''' Returns a list of coordinates of possible moves for this piece '''
        if self.board.breaks_hive(self.q, self.r):
            return []
    
    def move(self, q, r):
        ''' Moves the piece to (q, r)
        
        Throws InvalidMove if the move is not possible '''
        possible_moves = self.get_possible_moves()
        if (q, r) in possible_moves:
            self.board.move_piece(self.q, self.r, q, r)
        else:
            raise InvalidMove('Invalid move')
    
    def place(self, board, q, r):
        ''' Places this piece from your hand into the board '''
        self.board = board
        self.q = q
        self.r = r
    
    def set_coordinates(self, q, r, board):
        self.q = q
        self.r = r
        self.board = board
    
    def get_neighbours(self):
        ''' Returns a list of all neighbours '''
        return self.board.get_neighbours(self.q, self.r)

    def __repr__(self, *args, **kwargs):
        if (self.q is not None) and (self.r is not None):
            return '<%s(%d,%d)>' % (type(self).__name__, self.q, self.r)
        else:
            return '<%s(None,None)>' % (type(self).__name__)


class Ant(Piece):
    
    def get_possible_moves(self):
        super()
        if self.board.breaks_hive(self.q, self.r):
            return []
        queue = []
        visited = set()
        q, r = self.q, self.r
        
        queue += self.board.pos_shifts(self.q, self.r)
        visited.add((self.q, self.r))
        # Temporarily remove this piece
        temp = self.board.remove_piece(self.q, self.r)
        while queue:
            vertex = queue.pop(0)
            visited.add(vertex)
            neighbours = self.board.pos_shifts(vertex[0], vertex[1])
            unvisited = set(neighbours) - (set(visited).union(set(queue)))
            queue += list(unvisited)
        # Return the piece
        self.board.place_piece(q, r, temp)
        return list(visited)


class Bee(Piece):
    
    def get_possible_moves(self):
        ''' Returns a list of coordinates of possible moves for this piece '''
        if self.board.breaks_hive(self.q, self.r):
            return []
        return self.board.pos_shifts(self.q, self.r)

    def is_surrounded(self):
        ''' Returns if the bee is completely surrounded '''
        if self.q is None or self.r is None:
            return False
        neighbours = self.board.get_neighbours_coords(self.q, self.r)
        return len(neighbours) == 6

class Beetle(Piece):
    
    def get_possible_moves(self):
        ''' Returns a list of coordinates of possible moves for this piece '''
        moves = []
        if self.board.breaks_hive(self.q, self.r):
            return moves
        moves += self.board.pos_shifts(self.q, self.r)
        moves += self.board.get_neighbours_coords(self.q, self.r)
        return moves 


class Grasshopper(Piece):
    
    def get_possible_moves(self):
        ''' Returns a list of coordinates of possible moves for this piece '''
        moves = []
        if self.board.breaks_hive(self.q, self.r):
            return moves
        for d in self.board.DIRECTIONS: 
            if (self.board.get(self.q + d[0], self.r + d[1])) is not None:
                moves.append(self.board.get_empty_space_line(self.q, self.r, d))
        return moves


class Ladybug(Piece):
    pass


class Mosquito(Piece):
    pass


class Spider(Piece):
    
    def get_possible_moves(self):
        ''' Returns a list of coordinates of possible moves for this piece '''
        if self.board.breaks_hive(self.q, self.r):
            return []
        moves, queue = [], []
        visited = set()
        q, r = self.q, self.r
        
        queue += self.board.pos_shifts(self.q, self.r)
        visited.add((self.q, self.r))
        # Temporarily remove this piece
        temp = self.board.remove_piece(self.q, self.r)
        for n1 in queue:
            queue2 = []
            queue2 += self.board.pos_shifts(n1[0], n1[1])
            queue2.remove((q, r))
            for n2 in queue2:
                moves += self.board.pos_shifts(n2[0], n2[1])
                moves.remove(n1)
        # Return the piece
        self.board.place_piece(q, r, temp)
        return moves
        
    


