'''
Created on 21 Jul 2017

@author: Richard
'''

class InvalidPlaceError(Exception):
    ''' Exception raised when trying to place a piece on an invalid place.
    
    Examples include  placing a piece on top of another piece or a piece against
    an opponents' piece.
    
    Attributes:
        message (str): explanation of the error
    '''
    
    def __init__(self, message):
        self.message = message


class InvalidDirection(Exception):
    ''' Exception raised when supplying a invalid direction
    
    Attributes:
        message (str): explanation of the error '''
    
    def __init__(self, message):
        self.message = message
 
       
class InvalidMove(Exception):
    ''' Exception raised when trying to make an invalid move
    
    Attributes:
        message (str): explanation of the error '''
    
    def __init__(self, message):
        self.message = message

class InvalidCoordSystem(Exception):
    ''' Exception raised when specifying an invalid coordinate system.
    Valid coordinate systems normally are: axial, cube or offset. 
    Offset has the following systems: odd-r, even-r, odd-q, even-q.
    
    Attributes:
        message (str): explanation of the error '''
    
    def __init__(self, message):
        self.message = message          