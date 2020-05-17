import pieces
from pieces import *
from board import Board
from copy import copy, deepcopy


# gets basic values to feed into the AI
def get__hrt(board):
    peaks = []  # array of the highest block in each column
    holes = 0  # number of holes (empty blocks with blocks that are occupied above)
    roughness = 0  # sum of the differences between columns
    total_height = 0  # sum of the highest blocks on all columns
    # below are the loops that accomplish the above
    for i in range(10):
        for j in range(22):
            if board.get_board()[i][21 - j] != (0, 0, 0):
                peaks.append(21 - j)
                total_height += 21 - j
                break
            if j == 21:
                peaks.append(0)
    for i in range(9):
        roughness += abs(peaks[i] - peaks[i + 1])
    for i in range(10):
        for j in range(peaks[i]):
            if board.get_board()[i][j] == (0, 0, 0):
                holes += 1
    return holes, roughness, total_height, max(peaks) ** 1.5, max(peaks) - min(peaks)


# an attempt at training a more advanced ai which accounts for t-shaped holes
def get__hrt_advanced(board):
    peaks = []  # same as above
    holes = []  # returns an array of (col, row) holes
    simple_holes = 0  # same as holes in above
    roughness = 0  # same as above
    total_height = 0  # same as above
    # similar loops
    for i in range(10):
        for j in range(22):
            if board.get_board()[i][21 - j] != (0, 0, 0):
                peaks.append(21 - j)
                total_height += 21 - j
                break
            if j == 21:
                peaks.append(0)
    for i in range(9):
        roughness += abs(peaks[i] - peaks[i + 1])
    for i in range(10):
        for j in range(peaks[i]):
            if board.get_board()[i][j] == (0, 0, 0):
                holes.append(((i + 1) * 13 + (j + 1) * 17, (i + 1, j + 1)))
                simple_holes += 1
    holes_dict = dict(holes)
    to_remove_dict = {}
    # this code essentially determines if a hole is part of a t-shape for potential t-spins
    # figuring this out is important because it differentiates regular holes from t-spin setups
    for key in list(holes_dict):
        to_remove = is_t(holes_dict[key][0], holes_dict[key][1], board)
        for i in range(len(to_remove)):
            curr_key = to_remove[i][0] * 13 + to_remove[i][1] * 17
            if curr_key in holes_dict:
                to_remove_dict[curr_key] = (to_remove[i][0], to_remove[i][1])
    for key in to_remove_dict:
        del holes_dict[key]
    for key in holes_dict:
        curr_pos = holes_dict[key]
        curr_key = curr_pos[0] * 13 + curr_pos[1] * 17
        potential = is_t(curr_pos[0] - 1, curr_pos[1], board)
        potential += is_t(curr_pos[0] + 1, curr_pos[1], board)
        if curr_pos in potential:
            to_remove_dict[curr_key] = (curr_pos[0], curr_pos[1])
    return len(to_remove_dict), roughness, total_height, max(peaks) ** 1.5, max(peaks) - min(peaks), \
           simple_holes


# given a hole of col, row, returns whether or not it is part of a t-shaped chunk
def is_t(col, row, board):
    up = row + 1
    down = row - 1
    left = col - 1
    right = col + 1
    empty_counter = 0
    parts = [(col, row)]
    case = 0
    # below if statements count number of adjacent empty blocks
    if board.avail(col, up):
        empty_counter += 1
        parts.append((col, up))
    else:
        case = 1
    if board.avail(col, down):
        empty_counter += 1
        parts.append((col, down))
    else:
        case = 2
    if board.avail(right, row):
        empty_counter += 1
        parts.append((right, row))
    else:
        case = 3
    if board.avail(left, row):
        empty_counter += 1
        parts.append((left, row))
    else:
        case = 4
    # if three adjacent blocks are not empty then the hole cannot be part of a t-shape
    if empty_counter < 3:
        return []
    filled_counter = 0
    # counts the number of filled corners relative to the hole
    if not board.avail(left, up):
        filled_counter += 1
    if not board.avail(right, up):
        filled_counter += 1
    if not board.avail(right, down):
        filled_counter += 1
    if not board.avail(left, down):
        filled_counter += 1
    # if there are 3 filled corners then it is a potential t-spin setup
    if filled_counter == 3:
        return parts
    # if there are 4 then this hole is inaccessible (barring triple t-spin setup)
    elif filled_counter == 4:
        return []
    # t spins can also happen if only two corners are filled, below is the if statement for that case:
    if case != 1:
        if (not board.avail(right, up) and not board.avail(left, down)) or (not board.avail(right, down) and not
        board.avail(left, up)):
            return parts
    return []


# returns fresh piece from spawn, this is used a lot
def reset_piece(piece):
    if isinstance(piece, oPiece):
        piece_copy = type(piece)(5, 22)
    else:
        piece_copy = type(piece)(4, 22)
    return piece_copy


# given a piece, returns every possible move in this format:
"""
possible_moves = (piece_hashcode, (move_set, piece))
piece_hashcode: a unique hash to every possible position that differentiates one piece from another
move_set: an ordered list of numbers that represent moves on how to move a piece from spawn to final location
piece: the piece representing the final location the piece from spawn, the result of the move_set
"""


def get_possible_moves(board, piece):
    possible_moves = []
    test_piece = reset_piece(piece)
    move_set = [1]  # hard drop for basic moves is always the last one
    get_basic_moves(possible_moves, test_piece, piece, board, move_set)  # returns set of basic moves
    move_set = [1]
    test_piece = reset_piece(piece)
    # get basic moves for pieces that are CW rotated from spawn
    if test_piece.cw(board):
        move_set.insert(0, 3)
        get_basic_moves(possible_moves, test_piece, piece, board, move_set)
    move_set = [1]
    test_piece = reset_piece(piece)
    # get basic moves for pieces that are CC rotated from spawn
    if test_piece.cc(board):
        move_set.insert(0, 4)
        get_basic_moves(possible_moves, test_piece, piece, board, move_set)
    move_set = [1]
    test_piece = reset_piece(piece)
    # get basic moves fro pieces that are double rotated from spawn
    if test_piece.double_rotate(board):
        move_set.insert(0, 8)
        get_basic_moves(possible_moves, test_piece, piece, board, move_set)
    move_stack = deepcopy(possible_moves)
    check_moves = dict(possible_moves)
    # get's more advanced moves, ie tucking and various spins
    while not len(move_stack) == 0:
        curr_moves = move_stack.pop()
        # returns all possible moves from a final position
        new_moves = get_advanced_moves(curr_moves[1][0], curr_moves[1][1], board)
        # for every possible new move, compare the hashes of each move_set, if the hash isn't in the dict yet, add it
        # it is now a new move that we need to loop back and check if more unique moves are possible from that move
        for i in range(len(new_moves[1])):
            curr_hash = new_moves[0][i]
            if not curr_hash == 0:
                if curr_hash not in check_moves:
                    check_moves[curr_hash] = new_moves[1][i]
                    possible_moves.append((curr_hash, (new_moves[1][i], new_moves[2][i])))
                    move_stack.append((curr_hash, (new_moves[1][i], new_moves[2][i])))
    for i in range(len(possible_moves)):
        possible_moves[i][1][0].append(1)
    return possible_moves


# for every move_set, try to move it right, left, CW rotate, CC rotate and double Rotate
# return those new moves for the main function to evaluate
def get_advanced_moves(move_set, piece, board):
    reference_piece = deepcopy(piece)
    hashes = []
    new_pieces = []
    new_move_sets = []
    for i in range(5):
        new_move_sets.append(copy(move_set))
        new_move_sets[i][-1] = 2
        hashes.append(0)
    test_piece = deepcopy(reference_piece)
    # left move
    if test_piece.move(-1, 0, board):
        test_piece.quick_move(0, -1, board)
        new_move_sets[0].append(6)
        hashes[0] = hash_piece(test_piece)
    new_pieces.append(deepcopy(test_piece))
    test_piece = deepcopy(reference_piece)
    # right move
    if test_piece.move(1, 0, board):
        test_piece.quick_move(0, -1, board)
        new_move_sets[1].append(5)
        hashes[1] = hash_piece(test_piece)
    new_pieces.append(deepcopy(test_piece))
    test_piece = deepcopy(reference_piece)
    # clockwise rotate
    if test_piece.cw(board):
        test_piece.quick_move(0, -1, board)
        new_move_sets[2].append(3)
        new_move_sets[2].append(2)
        hashes[2] = hash_piece(test_piece)
    new_pieces.append(deepcopy(test_piece))
    test_piece = deepcopy(reference_piece)
    # counterclockwise rotate
    if test_piece.cc(board):
        test_piece.quick_move(0, -1, board)
        new_move_sets[3].append(4)
        new_move_sets[3].append(2)
        hashes[3] = hash_piece(test_piece)
    new_pieces.append(deepcopy(test_piece))
    test_piece = deepcopy(reference_piece)
    # double-rotate
    if test_piece.double_rotate(board):
        test_piece.quick_move(0, -1, board)
        new_move_sets[4].append(8)
        new_move_sets[4].append(2)
        hashes[4] = hash_piece(test_piece)
    new_pieces.append(deepcopy(test_piece))
    return hashes, new_move_sets, new_pieces


# function that gets basic moves from a piece
def get_basic_moves(possible_moves, test_piece, piece, board, move_set):
    if len(move_set) == 2:
        insert_pos = 1
    else:
        insert_pos = 0
    test_piece.quick_move(0, -1, board)
    possible_moves.append((hash_piece(test_piece), (copy(move_set), deepcopy(test_piece))))
    test_piece = reset_piece(piece)
    move_set_copy = copy(move_set)
    move_count = 1
    # while the piece can move to the left, add it to the list of possible moves
    while test_piece.move(-move_count, 0, board):
        if insert_pos == 1:
            move_code(move_set[0], test_piece, board)
        test_piece.quick_move(0, -1, board)
        move_set_copy.insert(insert_pos, 6)
        possible_moves.append((hash_piece(test_piece), (copy(move_set_copy), deepcopy(test_piece))))
        test_piece = reset_piece(piece)
        move_count += 1

    move_count = 1
    # while the piece can move to the right, add it to the list of possible moves
    while test_piece.move(move_count, 0, board):
        if insert_pos == 1:
            move_code(move_set[0], test_piece, board)
        test_piece.quick_move(0, -1, board)
        move_set.insert(insert_pos, 5)
        possible_moves.append((hash_piece(test_piece), (copy(move_set), deepcopy(test_piece))))
        test_piece = reset_piece(piece)
        move_count += 1


"""
Move Code:
1: Hard Drop
2: Soft Drop
3. CW rotate
4: CC rotate
5: Move Right
6: Move Left
7: Hold
8: Double Rotate
"""


# see above move_code, given a piece and a move_number, this function moves the piece based on input number
# note that this function cannot handle hold, which must be handled in the original game loop
def move_code(move_num, piece, board):
    if move_num == 1:
        while piece.quick_move(0, -1, board):
            board.need_next = True
            pass
    if move_num == 2:
        while piece.move(0, -1, board):
            pass
    if move_num == 3:
        return piece.cw(board)
    if move_num == 4:
        return piece.cc(board)
    if move_num == 5:
        return piece.move(1, 0, board)
    if move_num == 6:
        return piece.move(-1, 0, board)
    if move_num == 7:
        pass
    if move_num == 8:
        return piece.double_rotate(board)
    return False


# hash function for each piece
# no two pieces in two different positions can have the same hash
def hash_piece(piece):
    hashcode = 13
    hashcode += piece.get_col() * 61
    hashcode += piece.get_row() * 59
    hashcode += piece.get_state() * 53
    hashcode += pieces.get_num(piece) * 79
    return hashcode
