import pygame
from block import Block
import rotation
pygame.init()


class Piece:
    def __init__(self, col, row):
        # Indexing note: Col and Row start at 1, ONLY THE board.py WILL USE 0 INDEXING
        # Col: 1-10 left to right Row: 1-22 bottom to top
        # Note: x_diff means col_diff and y_diff means row_diff, I like to think of the grid as a coordinate plane
        # defined in subclasses, all spawn points are based on https://tetris.fandom.com/wiki/SRS
        # col and row are the upper left corner of the 3x3 square the piece is in (black squares in link above)
        # or the 4x4 square the I piece is in
        # for the O piece, col and row is the upper left corner of the piece itself
        self.down = False  # is the down button currently held?
        self.state = 0  # rotation state, starts at 0, CW: +1 CC: -1 Double: +/- 2, everything %4
        self.col = col  # the current column of piece based on upper left corner of the grid
        self.row = row  # the current column of piece based on upper left corner of the grid
        self.color = None  # the color of the piece
        # blocks added in subclasses
        self.blocks = []  # each piece has 4 blocks

    # moves the piece by x_diff and y_diff, returns True if the move was successful, False otherwise
    def move(self, x_diff, y_diff, board):
        if not self.can_move(x_diff, y_diff, board):
            return False
        for bl in self.blocks:
            bl.set_col(bl.get_col() + x_diff)
            bl.set_row(bl.get_row() + y_diff)
        self.col = self.col + x_diff
        self.row = self.row + y_diff
        return True

    # used for when you don't actually want to move the piece but want to see if it can move
    # returns True if the piece can move x_diff and y_diff, False otherwise
    def can_move(self, x_diff, y_diff, board):
        for bl in self.blocks:
            if not board.avail(bl.get_col() + x_diff, bl.get_row() + y_diff):
                return False
        return True

    # default CW function, returns True if the rotation was successful, False otherwise
    def cw(self, board):
        if rotation.reg_cw(self, board):
            self.state += 1
            self.state = self.state % 4
            return True
        return False

    # default CC function, returns True if the rotation was successful, False otherwise
    def cc(self, board):
        if rotation.reg_cc(self, board):
            self.state += 3
            self.state = self.state % 4
            return True
        return False

    # default Double Rotate function, returns True if the rotation was successful, False otherwise
    def double_rotate(self, board):
        if rotation.double_rotate(self, board):
            self.state += 2
            self.state = self.state % 4
            return True
        return False

    # update the piece based on key presses (note left and right arrow keys handled in main for DAS)
    def update(self, event, board):
        if event.type == pygame.KEYDOWN:
            # if left pressed, move left ONCE
            if event.key == pygame.K_LEFT:
                self.move(-1, 0, board)
                return True, False
            # if right pressed, move right ONCE
            if event.key == pygame.K_RIGHT:
                self.move(1, 0, board)
                return True, False
            # if up pressed, CW rotate ONCE
            if event.key == pygame.K_UP:
                self.cw(board)
                return True, False
            # if z pressed, CC rotate ONCE
            if event.key == pygame.K_z:
                self.cc(board)
                return True, False
            # if x pressed, double rotate ONCE
            if event.key == pygame.K_x:
                self.double_rotate(board)
                return True, False
            # if down pressed, start soft-drop, set down to true
            if event.key == pygame.K_DOWN:
                self.down = True
                return False, False
            # if space pressed, hard drop the piece
            if event.key == pygame.K_SPACE:
                self.quick_move(0, -1, board)
                return True, True
        # if the down arrow key is released, stop soft dropping
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.down = False
        return False, False

    # get the gray shadow of the piece
    def get_ghost(self, board):
        stop = False
        counter = 0
        while not stop:
            for bl in self.blocks:
                if not board.avail(bl.get_col(), bl.get_row() - counter):
                    stop = True
                    break;
            if not stop:
                counter += 1
        return counter - 1

    # instantly moves piece as far as it can in designated direction
    def quick_move(self, x_diff, y_diff, board):
        while self.move(x_diff, y_diff, board):
            pass

    # move the piece down ONCE
    # soft drop happens because this is called 300 times per second, if you want to soft drop
    # you move down about once every .015 seconds.
    def soft_drop(self, board):
        if self.down:
            if not self.move(0, -1, board):
                return False
        pygame.time.delay(10)
        return self.down

    # render the piece, called by graphics method
    def draw(self, screen, col_diff, row_diff):
        for bl in self.blocks:
            bl.draw(screen, col_diff, row_diff)

    # get the current piece's column
    def get_col(self):
        return self.col

    # get the current piece's row
    def get_row(self):
        return self.row

    # get the current piece's blocks
    def get_blocks(self):
        return self.blocks

    # get the current piece's state
    def get_state(self):
        return self.state

    # set the current piece's block to something else
    def set_blocks(self, blocks):
        self.blocks = blocks

    # set the col of the piece
    def set_col(self, col):
        self.col = col

    # set the row of the piece
    def set_row(self, row):
        self.row = row


# iPiece inherits Piece
class iPiece(Piece):
    def __init__(self, col, row):
        # call super
        super(iPiece, self).__init__(col, row)
        # i piece is conventionally cyan
        self.color = (0, 255, 255)
        # add blocks to array of blocks
        self.blocks.append(Block(col, row - 1, self.color))
        self.blocks.append(Block(col + 1, row - 1, self.color))
        self.blocks.append(Block(col + 2, row - 1, self.color))
        self.blocks.append(Block(col + 3, row - 1, self.color))

    # i piece rotations have their own kicktable so overrides the Piece's rotate method
    def cw(self, board):
        if rotation.i_cw(self, board):
            self.state += 1
            self.state = self.state % 4
            return True
        return False

    def cc(self, board):
        if rotation.i_cc(self, board):
            self.state += 3
            self.state = self.state % 4
            return True
        return False

    def double_rotate(self, board):
        if rotation.i_double_rotate(self, board):
            self.state += 2
            self.state = self.state % 4
            return True
        return False


# just initializes the piece, J Piece is a regular piece
class jPiece(Piece):
    def __init__(self, col, row):
        # call super
        super(jPiece, self).__init__(col, row)
        # j piece is conventionally blue
        self.color = (0, 0, 255)
        # add blocks to array of blocks
        self.blocks.append(Block(col, row, self.color))
        self.blocks.append(Block(col, row - 1, self.color))
        self.blocks.append(Block(col + 1, row - 1, self.color))
        self.blocks.append(Block(col + 2, row - 1, self.color))


# just initializes the piece, L Piece is a regular piece
class lPiece(Piece):
    def __init__(self, col, row):
        # call super
        super(lPiece, self).__init__(col, row)
        # l piece is conventionally orange
        self.color = (255, 165, 0)
        # add blocks to array of blocks
        self.blocks.append(Block(col, row - 1, self.color))
        self.blocks.append(Block(col + 1, row - 1, self.color))
        self.blocks.append(Block(col + 2, row - 1, self.color))
        self.blocks.append(Block(col + 2, row, self.color))


# initializes the piece, O Piece does not rotate so it overrides Piece's rotate methods with filler methods
class oPiece(Piece):
    def __init__(self, col, row):
        # call super
        super(oPiece, self).__init__(col, row)
        # o piece is conventionally yellow
        self.color = (255, 255, 0)
        # add blocks to array of blocks
        self.blocks.append(Block(col, row, self.color))
        self.blocks.append(Block(col, row - 1, self.color))
        self.blocks.append(Block(col + 1, row, self.color))
        self.blocks.append(Block(col + 1, row - 1, self.color))

    # note the O piece does not rotate, so we override the rotation methods, it always returns False
    def cw(self, board):
        return False

    def cc(self, board):
        return False

    def double_rotate(self, board):
        return False


# just initializes the piece, S Piece is a regular piece
class sPiece(Piece):
    def __init__(self, col, row):
        # call super
        super(sPiece, self).__init__(col, row)
        # s piece is conventionally green
        self.color = (0, 255, 0)
        # add blocks to array of blocks
        self.blocks.append(Block(col + 1, row, self.color))
        self.blocks.append(Block(col + 2, row, self.color))
        self.blocks.append(Block(col, row - 1, self.color))
        self.blocks.append(Block(col + 1, row - 1, self.color))


# just initializes the piece, T Piece is a regular piece
class tPiece(Piece):
    def __init__(self, col, row):
        # call super
        super(tPiece, self).__init__(col, row)
        # t piece is conventionally magenta
        self.color = (255, 0, 255)
        # add blocks to array of blocks
        self.blocks.append(Block(col + 1, row, self.color))
        self.blocks.append(Block(col, row - 1, self.color))
        self.blocks.append(Block(col + 1, row - 1, self.color))
        self.blocks.append(Block(col + 2, row - 1, self.color))


# just initializes the piece, Z Piece is a regular piece
class zPiece(Piece):
    def __init__(self, col, row):
        # call super
        super(zPiece, self).__init__(col, row)
        # z piece is conventionally red
        self.color = (255, 0, 0)
        # add blocks to array of blocks
        self.blocks.append(Block(col, row, self.color))
        self.blocks.append(Block(col + 1, row, self.color))
        self.blocks.append(Block(col + 1, row - 1, self.color))
        self.blocks.append(Block(col + 2, row - 1, self.color))


# get's piece based on number, useful for retrieving from bag
"""
0: iPiece
1: jPiece
2: lPiece
3: oPiece
4: sPiece
5: tPiece
6: zPiece
"""


def get_piece(piece_id, col_diff, row_diff):
    if piece_id == 0:
        return iPiece(4 + col_diff, 22 + row_diff)
    if piece_id == 1:
        return jPiece(4 + col_diff, 22 + row_diff)
    if piece_id == 2:
        return lPiece(4 + col_diff, 22 + row_diff)
    if piece_id == 3:
        return oPiece(5 + col_diff, 22 + row_diff)
    if piece_id == 4:
        return sPiece(4 + col_diff, 22 + row_diff)
    if piece_id == 5:
        return tPiece(4 + col_diff, 22 + row_diff)
    if piece_id == 6:
        return zPiece(4 + col_diff, 22 + row_diff)
    return None


# given a piece, returns a number, the reverse of get_piece method, same number_codes as above
def get_num(piece):
    if isinstance(piece, iPiece):
        return 0
    if isinstance(piece, jPiece):
        return 1
    if isinstance(piece, lPiece):
        return 2
    if isinstance(piece, oPiece):
        return 3
    if isinstance(piece, sPiece):
        return 4
    if isinstance(piece, tPiece):
        return 5
    if isinstance(piece, zPiece):
        return 6
    return 7
