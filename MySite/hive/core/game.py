'''
Created on 13 Jul 2017

@author: Richard

Useful links:
Common algorithms and representations of hex grids:
- http://www.redblobgames.com/grids/hexagons/
hexjson format:
- https://odileeds.org/projects/hexmaps/hexjson.html
'''

import logging, json, os, time
from hive.core.pieces import *
from hive.core.exceptions import *

class Game(object):
    
    def __init__(self):
        self.board = Board(self)
        self.player1 = Player('Player1', self.board)
        self.player2 = Player('Player2', self.board)
        self.active_player = self.player1
        self.turn = 0
        self.actions = []
        
        self.logger = logging.getLogger('Game_logger')
        self.logger.setLevel(logging.WARNING)
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        self.logger.addHandler(ch)
    
    def start(self):
        while not self.game_finished():
            self.logger.info('Turn %d' % (self.turn))
            action = input('Turn %s \n%s please enter your action: ' % 
                           (self.turn, self.active_player))
            # Check if it is a legal action
            self.logger.info('Acion: %s' % action)
            self.end_turn()
            
    def handle_action(self, action):
        ''' Takes an action and executes it '''
        self.actions.append(action)
        self.active_player = self.player1 if self.turn%2 else self.player2
        self.turn += 1

    def end_turn(self):
        ''' Ends the turn of the current active player '''
        if self.active_player is self.player1:
            self.active_player = self.player2
        else:
            self.active_player = self.player1
        self.turn += 1
    
    def game_finished(self):
        ''' Returns if the game is finished '''
        return self.player1.bee.is_surrounded() \
            or self.player2.bee.is_surrounded()


class Board(object):
    '''
    Board represents the dynamic board on which Hive will be played.
    Pieces positions are stored in a dictionary using an axial coordinate 
    system (a.k.a. trapezoidal). The three coordinates are constrained under the 
    following function: x + y + z = 0
    Therefore only two coordinates need to be stored (q, r). From these two
    coordinates we can infer the third coordinate if needed. More information
    about the coordinate system see http://www.redblobgames.com/grids/hexagons/#coordinates
    '''
    
    DIRECTIONS = [(1, 0), (1, -1), (0, -1), \
                  (-1, 0), (-1, 1), (0, 1)]
    
    def __init__(self, game):
        self.board = {}
        self.game = game
    
#     def place_piece(self, q, r, piece):
#         ''' Adds a piece on the given coordinates
#         
#         Throws an InvalidPlaceError if there already exists a piece on the 
#         coordinates
#         '''
#         if (piece.q is not None) or (piece.r is not None):
#             raise InvalidPlace('Invalid coordinates')
#         
#         if self.board.get((q, r)) is None:
#             self.board[(q, r)] = piece
#             piece.set_coordinates(q, r, self)
#         else:
#             raise InvalidPlace('Position already taken')
    
    def get(self, q, r):
        ''' Return piece on board if it exists '''
        return self.board.get((q, r))
    
    def get_piece(self, q, r):
        ''' Return piece on board if it exists '''
        return self.board.get((q, r))
    
#     def move_piece(self, q, r, x, y):
#         ''' Moves piece from (q, r) to (x, y) '''
#         p = self.remove_piece(q, r)
#         self.place_piece(x, y, p)
    
    def remove_piece(self, q, r):
        piece = self.board.pop((q, r))
        piece.q = None
        piece.r = None
        return piece
    
    def get_neighbour(self, q, r, direction):
        ''' Returns the neighbour of a piece in a specified direction '''
        return self.board.get((q + direction[0], r + direction[1]))
    
    def get_neighbours(self, q, r):
        ''' Returns neighbours in all 6 directions as a list of pieces. 
        If a neighbour does not exists returns None '''
        return [self.board.get((q+1, r)), self.board.get((q+1, r-1)), \
                self.board.get((q+0, r-1)), self.board.get((q-1, r+0)), \
                self.board.get((q-1, r+1)), self.board.get((q+0, r+1))]
    
    def get_neighbours_coords(self, q, r):
        ''' Returns a list coordinates of existing neighbours '''
        n = self.get_neighbours(q, r)
        n = list(filter(None, n))
        return list(map(lambda x: (x.q, x.r), n))
        

    def get_distance(self, q1, r1, q2, r2):
        ''' Returns the distance between two points '''
        pass
    
    def connected_graph(self, start=None):
        ''' Checks if the board forms a complete graph 
        
        Returns True is the board is empty '''
        pieces = list(self.board.values())
        if len(pieces) == 0:
            return True
        if start is None:
            start = pieces[0]
        visited = set()
        queue = [start]
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                neighbours = vertex.get_neighbours()
                neighbours = list(filter(None, neighbours))
                unvisited = set(neighbours) - (set(visited).union(set(queue)))
                queue += list(unvisited)
        return len(visited) == len(pieces)
        
    def breaks_hive(self, q, r):
        ''' Returns whether moving the specified piece will break the hive 
        
        Throws KeyError if there is no piece on given position '''
        # Temporarily remove the piece and see if the hive is still connected
        temp = self.remove_piece(q, r)
        connected = self.connected_graph()
        temp.place(q, r)
        return not connected
    
    def can_shift(self, q, r, d):
        ''' Return whether a piece can shift in the given direction without
        being blocked. 
        
        Does not check whether moving this piece breaks the hive '''
#         if self.breaks_hive(q, r):
#             return False
        if self.get_neighbour(q, r, d) is not None:
            return False
        pieces = set(self.board.values())
        board = self.board
        if d[0]==1 and d[1]==0:
            return len(pieces & set([board.get((q+1, r-1)), board.get((q+0, r+1))])) == 1
        elif d[0]==1 and d[1]==-1:
            return len(pieces & set([board.get((q+0, r-1)), board.get((q+1, r+0))])) == 1
        elif d[0]==0 and d[1]==-1:
            return len(pieces & set([board.get((q+1, r-1)), board.get((q-1, r+0))])) == 1
        elif d[0]==-1 and d[1]==0:
            return len(pieces & set([board.get((q+0, r-1)), board.get((q-1, r+1))])) == 1
        elif d[0]==-1 and d[1]==1:
            return len(pieces & set([board.get((q-1, r-0)), board.get((q+0, r+1))])) == 1
        elif d[0]==0 and d[1]==1:
            return len(pieces & set([board.get((q-1, r+1)), board.get((q+1, r+0))])) == 1
        else:
            raise InvalidDirection('Invalid direction')
        
    def pos_shifts(self, q, r):
        ''' Returns a list of coordinates from which the specified piece can 
        shift without being blocked '''
        moves = []
        for d in self.DIRECTIONS:
            if self.can_shift(q, r, d):
                moves.append( (q + d[0], r+d[1]) )
        return moves
        
    def get_empty_space_line(self, q, r, d):
        ''' Return the next empty space in the given direction, in a straight line 
        
        Args:
            q (int): first coordinate
            r (int): second coordinate
            d (tuple(int, int)): direction to search for
        '''
        i = 1
        while (q+d[0]*i, r+d[1]*i) in self.board.keys():
            i += 1
        return (q+d[0]*i, r+d[1]*i)
    
    def axial_to_cube(self, q, r):
        ''' Converts the given axial coordinates to cube coordinates '''
        s = - q - r
        return q, r, s
    
    def axial_to_offset(self, q, r, offset='odd-r'):
        ''' Converts axial coordinate system to offset coordinate system of the
        specified type
        
        Args:
            offset (str): the type of offset system layout, must be one of the following:
                - odd-r
                - even-r
                - odd-q
                - even-q
        '''
        col, row = None, None
        if offset == 'even-r':
            col = int( (q + (r - ( (r)&1) ) / 2) )
            row = r
        elif offset == 'odd-r':
            col = int( (q + (r + (r&1) ) / 2) )
            row = r
        elif offset == 'odd-q':
            col = q
            row = int( (r + (q - (q&1) ) / 2) )
        elif offset == 'even-q':
            col = q
            row = int( (r + (q + (q&1) ) / 2) )
        else:
            return InvalidCoordSystem('Invalid offset system, use one of the \
            following: odd-r, even-r, odd-q or even-q')
        return col, row  
    
    def output_board_hexjson(self, layout='odd-r', indent=4, file=None):
        ''' Returns a hexjson representation of the board in the given layout
        
        Args: 
            layout (str): defines the layout of the coordinate system, see
            http://www.redblobgames.com/grids/hexagons/#coordinates
            Should be one of the following:
                - axial
                - odd-r
                - even-r
                - odd-q
                - even-q
            indent (int): indent level for pretty printing
            file (file-like object): (default None) if specified output will 
            also be written to the file-like object.
        
        See https://odileeds.org/projects/hexmaps/hexjson.html for more 
        information about the hexjson format.
        '''
        if layout not in ['axial', 'odd-r', 'even-r', 'odd-q', 'even-q']:
            return InvalidCoordSystem('Invalid coordinate system; choose one \
            of the following: axial, odd-r, even-r, odd-q or even-q.')
        
        board_hexjson = {}
        board_hexjson['layout'] = layout
        hexes = {}
        for key, value in self.board.items():
            q, r = key[0], key[1]
            if layout is not 'axial':
                # need to convert axial system to specified coordinate system
                q, r =  self.axial_to_offset(key[0], key[1], layout)
            name_hex = 'Q%dR%d' % (q, r)
            value_hex = {'q': q, 'r': r, \
                         'type': type(value).__name__, 'player': value.player.name}
            hexes[name_hex] = value_hex
        board_hexjson['hexes'] = hexes
        
        if file is not None:
            json.dump(board_hexjson, file, indent=indent)
        return json.dumps(board_hexjson, indent=indent)
    
    def save_board(self, file='board.hexjson'):
        dir_loc = os.path.relpath('..\\static\\hive')
        cur_dir = os.path.dirname(__file__)
        file_loc = os.path.join(cur_dir, dir_loc, file)
        with open(file_loc, 'w') as out_file:
            self.output_board_hexjson('odd-r', indent=4, file=out_file)

class Player(object):
    
    def __init__(self, name, board):
        self.name = name
        self.ant = [Ant(self, board), Ant(self, board), Ant(self, board)]
        self.beetle = [Beetle(self, board), Beetle(self, board)]
        self.grasshopper = [Grasshopper(self, board), Grasshopper(self, board),
                            Grasshopper(self, board)]
        self.bee = [Bee(self, board)]
        self.spider = [Spider(self, board), Spider(self, board)]
        self.ladybug = [Ladybug(self, board)]
        self.mosquito = [Mosquito(self, board)]
        
    def __repr__(self, *args, **kwargs):
        return self.name


class Action(object):
    ''' All actions done by players are represented as a subclass of Action.
    Once a action is created it is immediately executed
    '''
    
    def __init__(self, piece, q, r):
        self.piece = piece
        self.player = self.piece.player
        self.game = self.piece.board.game
        self.old_q = None
        self.old_r = None
        self.q = q
        self.r = r
        self.execute()
        
    def execute(self):
#         if self.player is not self.piece.player:
#             raise InvalidAction('Cannot do actions on opponent\'s pieces')
        
        self.executed = True
        self.timestamp = time.time()
        self.game.handle_action(self)
    
    def undo(self):
        assert self.executed
        self.executed = False
    

class ActionPlacePiece(Action):
    
    def __init__(self, piece, q, r):
        super().__init__(piece, q, r)
    
    def execute(self):
        if self.player is not self.game.active_player:
            raise InvalidAction('It is %s his/her turn' % self.game.active_player)
        if self.piece.q is not  None or self.piece.r is not None:
            raise InvalidPlace('%s is already on the board' % self.piece)
        if (self.q is None) or (self.r is None):
            raise InvalidPlace('Invalid coordinates')
        if self.game.board.get(self.q, self.r) is not None:
            raise InvalidPlace('Must place piece on empty space')
        if self.game.turn >= 6 and len(self.player.bee) > 0:
            raise InvalidPlace('Must place bee within 4 turns')
        
        neighbours = self.game.board.get_neighbours(self.q, self.r)
        neighbours = list(filter(None, neighbours))
        if len(neighbours) == 0 and not self.game.turn == 0:
            raise InvalidPlace('Piece must be connected to the hive')
        for n in neighbours:
            if n.player is not self.player and not self.game.turn == 1:
                raise InvalidPlace('Piece cannot be placed against pieces of enemy')
        self.piece.place(self.q, self.r)
        super().execute()
        
    def undo(self):
        super()
        # TODO: add piece again to player
        self.game.board.remove_piece(self.q, self.r)
        pass
    

class ActionMovePiece(Action):
    
    def __init__(self, piece, q, r):
        self.old_q = q
        self.old_r = r
        super().__init__(piece, q, r)      
    
    def execute(self):
        if len(self.player.bee) > 0:
            raise InvalidMove('Must place bee before you can move pieces')
        pos_moves = self.piece.get_possible_moves()
        if ((self.q, self.r) not in pos_moves):
            raise InvalidMove('Move not possible')
        if (self.piece.player is not self.player):
            raise InvalidMove('Piece is not yours')
        self.piece.move(self.q, self.r)
        super().execute()

    def undo(self):
        super()
        self.piece.move(self.old_q, self.old_r)
