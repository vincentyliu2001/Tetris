from pieces import *
from board import *

# HOW ROTATIONS IN MODERN TETRIS WORK:
"""
There are three types of rotations in Tetris: clockwise, counter-clockwise, and double-rotate (implemented now in most
on line versions). All of this info can be found in more detail on https://tetris.wiki/Super_Rotation_System. Each piece
has 4 states as shown in the link previously, a CW rotation increases state by 1, CC rotation decreases by 1, and
Double Rotation decreases/increases by 2 depending on how you want to look at it. Each rotation has a kick table
which "kicks" the piece around until a valid rotation is found (where the rotated piece does not occupy any square that 
are already filled). If the kick table cannot find a valid rotation, then the rotation fails and nothing happens.
Otherwise, the piece is kicked by the first valid rotation found in the kick table. This rotation.py file handles all
of this, and is the heart of the rotation system the AI and the regular game use.
Design notes:
oPiece does not call rotations since it doesn't rotate
iPiece calls i_cw, i_cc and i double_rotate since it uses a 4x4 block, implementation is easier if this is just kept as
a separate module
"""


# regular clockwise rotation, for all pieces except for iPiece and oPiece

def reg_cw(piece, board):
    # this first block of code is to treat each piece as a 3x3 matrix see https://tetris.wiki/Super_Rotation_System
    # it then rotates clockwise the matrix with typical algo
    curr_col = piece.get_col()
    curr_row = piece.get_row() - 2
    new_blocks = []
    for block in piece.get_blocks():
        temp_col = block.get_col() - curr_col
        temp_row = block.get_row() - curr_row
        new_col = temp_row + curr_col
        new_row = abs(temp_col - 2) % 3 + curr_row
        new_blocks.append(Block(new_col, new_row, block.get_color()))

    # get the handling of kicktables which does the rest
    # parameters: (piece, new_blocks, piece_type, board, rotate_num, is_180)
    # piece_type = 1 which means it is not an iPiece
    # rotate_num = 1 which means it is CW rotate
    # is_180 = False because it is not a Double rotate
    return handle_kicktable(piece, new_blocks, 1, board, 1, False)


def reg_cc(piece, board):
    # this first block of code is to treat each piece as a 3x3 matrix see https://tetris.wiki/Super_Rotation_System
    # it then rotates counterclockwise the matrix with typical algo
    curr_col = piece.get_col()
    curr_row = piece.get_row() - 2
    new_blocks = []
    for block in piece.get_blocks():
        temp_col = block.get_col() - curr_col
        temp_row = block.get_row() - curr_row
        new_col = abs(temp_row - 2) % 3 + curr_col
        new_row = temp_col + curr_row
        new_blocks.append(Block(new_col, new_row, block.get_color()))
    # get the handling of kicktables which does the rest
    # parameters: (piece, new_blocks, piece_type, board, rotate_num, is_180)
    # piece_type = 1 which means it is not an iPiece
    # rotate_num = -1 which means it is CC rotate
    # is_180 = False because it is not a Double rotate
    return handle_kicktable(piece, new_blocks, 1, board, -1, False)


def double_rotate(piece, board):
    # this first block of code is to treat each piece as a 3x3 matrix see https://tetris.wiki/Super_Rotation_System
    # it then rotates counterclockwise the matrix twice with typical algo
    curr_col = piece.get_col()
    curr_row = piece.get_row() - 2
    new_blocks = []
    for block in piece.get_blocks():
        temp_col1 = block.get_col() - curr_col
        temp_row1 = block.get_row() - curr_row
        temp_col2 = abs(temp_row1 - 2) % 3
        temp_row2 = temp_col1
        new_col = abs(temp_row2 - 2) % 3 + curr_col
        new_row = temp_col2 + curr_row

        new_blocks.append(Block(new_col, new_row, block.get_color()))
    # get the handling of kicktables which does the rest
    # parameters: (piece, new_blocks, piece_type, board, rotate_num, is_180)
    # piece_type = 1 which means it is not an iPiece
    # rotate_num = 0 which means it not CC rotate
    # is_180 = True because it is a Double rotate
    return handle_kicktable(piece, new_blocks, 0, board, 2, True)


# everything is the same except we have 4x4 matrices now
# piece_type = 0 for handle_kicktable method because we are dealing with an iPiece now
def i_cw(piece, board):
    curr_col = piece.get_col()
    curr_row = piece.get_row() - 3
    new_blocks = []
    for block in piece.get_blocks():
        temp_col = block.get_col() - curr_col
        temp_row = block.get_row() - curr_row
        new_col = temp_row + curr_col
        new_row = abs(temp_col - 3) % 4 + curr_row
        new_blocks.append(Block(new_col, new_row, block.get_color()))

    return handle_kicktable(piece, new_blocks, 0, board, 1, False)


# everything is the same except we have 4x4 matrices now
# piece_type = 0 for handle_kicktable method because we are dealing with an iPiece now
def i_cc(piece, board):
    curr_col = piece.get_col()
    curr_row = piece.get_row() - 3
    new_blocks = []
    for block in piece.get_blocks():
        temp_col = block.get_col() - curr_col
        temp_row = block.get_row() - curr_row
        new_col = abs(temp_row - 3) % 4 + curr_col
        new_row = temp_col + curr_row
        new_blocks.append(Block(new_col, new_row, block.get_color()))

    return handle_kicktable(piece, new_blocks, 0, board, -1, False)


# everything is the same except we have 4x4 matrices now
# piece_type = 0 for handle_kicktable method because we are dealing with an iPiece now
def i_double_rotate(piece, board):
    curr_col = piece.get_col()
    curr_row = piece.get_row() - 3
    new_blocks = []
    for block in piece.get_blocks():
        temp_col1 = block.get_col() - curr_col
        temp_row1 = block.get_row() - curr_row
        temp_col2 = abs(temp_row1 - 3) % 4
        temp_row2 = temp_col1
        new_col = abs(temp_row2 - 3) % 4 + curr_col
        new_row = temp_col2 + curr_row

        new_blocks.append(Block(new_col, new_row, block.get_color()))

    return handle_kicktable(piece, new_blocks, 1, board, 2, True)


# parameters explained above
def handle_kicktable(piece, new_blocks, piece_type, board, rotate_num, is_180):
    # there are only two tests if the rotation type is 180
    if is_180:
        test_num = 2
    # there are five tests otherwise
    else:
        test_num = 5
    # test up until the test limit
    for i in range(test_num):
        # get the appropriate kick from kicktable in the form of (col_diff, row_diff)
        kick = kicktable(piece.get_state(), (piece.get_state() + rotate_num) % 4, piece_type, i + 1, is_180)
        valid = True
        # for every block, check to see if that transformation is valid
        for bl in new_blocks:
            if not board.avail(bl.get_col() + kick[0], bl.get_row() + kick[1]):
                valid = False
                break
        # if all of them are valid, then the rotation succeeded
        if valid:
            # rotate and set the block now
            for block in new_blocks:
                block.set_col(block.get_col() + kick[0])
                block.set_row(block.get_row() + kick[1])
            piece.set_blocks(new_blocks)
            piece.set_col(piece.get_col() + kick[0])
            piece.set_row(piece.get_row() + kick[1])
            return True
    # if we get to this point, none of the tests worked, and the rotation has failed, return False
    return False


# wall kicks system, see https://tetris.fandom.com/wiki/SRS Wall Kicks section for CC and CCW kick tables
# 180 kick tables are based on jstris and much more simple:
"""
|states | Test 1 | Test 2 |
| 0 -> 2| 0, 0   | 0, 1   |
| 1 -> 3| 0, 0   | 1, 0   |
| 2 -> 0| 0, 0   | 0,-1   |
| 3 -> 1| 0, 0   |-1, 0   |
"""
# this is also how cool spins like the triple-t-spins happen
# this table returns the kick given initial state, final state, and piece type
# the if statements equate to the tables in the link above


def kicktable(state1, state2, piece_type, test, is_180):
    # piece_type will be 1 for all pieces except for i
    if is_180:
        # if statements to encode above 180 degree kicktable
        if test == 1:
            return 0, 0
        if test ==2:
            if state1 == 0:
                return 0, 1
            if state1 == 1:
                return 1, 0
            if state1 == 2:
                return 0, -1
            if state1 == 3:
                return -1, 0
    # this was really fun to code /s
    # if statements that encode all 80 possibilities from kick tables, I'm not going to comment this at all
    # from extensive play-testing, this if-statement-kick-table works, take my word for it
    else:
        if piece_type == 1:
            if test == 1:
                return 0, 0
            if test == 2:
                if state2 == 1 or state1 == 3:
                    return -1, 0
                else:
                    return 1, 0
            if test == 3:
                if state2 == 1:
                    return -1, 1
                if state1 == 3:
                    return -1, -1
                if state2 == 3:
                    return 1, 1
                if state1 == 1:
                    return 1, -1
            if test == 4:
                if state2 == 1 or state2 == 3:
                    return 0, -2
                else:
                    return 0, 2
            if test == 5:
                if state1 == 3:
                    return -1, 2
                if state2 == 1:
                    return -1, -2
                if state1 == 1:
                    return 1, 2
                if state2 == 3:
                    return 1, -2
        else:
            if test == 1:
                return 0, 0
            if test == 2:
                if (state1 == 0 and state2 == 1) or (state1 == 3 and state2 == 2):
                    return -2, 0
                if (state1 == 1 and state2 == 0) or (state1 == 2 and state2 == 3):
                    return 2, 0
                if (state1 == 1 and state2 == 2) or (state1 == 0 and state2 == 3):
                    return -1, 0
                if (state1 == 2 and state2 == 1) or (state1 == 3 and state2 == 0):
                    return 1, 0
            if test == 3:
                if (state1 == 0 and state2 == 1) or (state1 == 3 and state2 == 2):
                    return 1, 0
                if (state1 == 1 and state2 == 0) or (state1 == 2 and state2 == 3):
                    return -1, 0
                if (state1 == 1 and state2 == 2) or (state1 == 0 and state2 == 3):
                    return 2, 0
                if (state1 == 2 and state2 == 1) or (state1 == 3 and state2 == 0):
                    return -2, 0
            if test == 4:
                if (state1 == 0 and state2 == 1) or (state1 == 3 and state2 == 2):
                    return -2, 1
                if (state1 == 1 and state2 == 0) or (state1 == 2 and state2 == 3):
                    return 2, 1
                if (state1 == 1 and state2 == 2) or (state1 == 0 and state2 == 3):
                    return -1, 2
                if (state1 == 2 and state2 == 1) or (state1 == 3 and state2 == 0):
                    return 1, -2
            if test == 5:
                if (state1 == 0 and state2 == 1) or (state1 == 3 and state2 == 2):
                    return 1, 2
                if (state1 == 1 and state2 == 0) or (state1 == 2 and state2 == 3):
                    return -1, -2
                if (state1 == 1 and state2 == 2) or (state1 == 0 and state2 == 3):
                    return 2, -1
                if (state1 == 2 and state2 == 1) or (state1 == 3 and state2 == 0):
                    return -2, 1
