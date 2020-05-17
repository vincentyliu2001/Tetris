
class Board:
    def __init__(self):
        self.combo = 0  # counter for how many lines cleared in a row
        self.b2b = False  # has the last line-cleared been a Tetris or T-Spin?
        self.board = [[(0, 0, 0) for i in range(22)] for j in range(10)]  # initially the entire board is Black
        self.game_over = False  # is the game over?
        self.soft_drop = 0  # how many soft-drops has this piece done to reach it's final position?
        self.curr_row = 0  # what was the last row the piece was at when check_new_event last happened?
        self.score = 0  # what is the total score of this game?
        self.need_next = False  # do we need another piece?
        self.can_hold = True  # have we already held? we can only hold once per piece
        self.holes = 0  # how many holes are in the board?

    # is this block in the grid available
    def avail(self, col, row):
        # since we always used 1 indexing for our coordinate plane
        # we we adjust to 0 indexing
        board_col = col - 1
        board_row = row - 1
        if board_col < 0 or board_col > 9 or board_row < 0 or board_row > 21:
            return False
        return self.board[board_col][board_row] == (0, 0, 0)

    # add a block to the board
    def add(self, col, row, color):
        board_col = col - 1
        board_row = row - 1
        self.board[board_col][board_row] = color

    # clear line, if a line is full, remove it from the board and move everything else down
    def clear_line(self, active, t_piece, i_piece):
        t_spin = 0  # case for t-spins
        level = 1  # in case levels are ever implemented, makes for easy score conversions
        message1 = ""  # the first message to display
        message2 = ""  # the second message to display
        score = 0  # the total score accrued by that dropped piece
        corner_count = 0  # to help detect t-spins
        # loop below checks if the highest row is full, if it is, then the user has lost the game
        for i in range(10):
            if self.board[i][21] != (0, 0, 0):
                self.game_over = True
                return int(score), "Game Over", "Restart: F4", True, 0, 0
        # check if a t-spin has been performed
        if t_piece:
            if not self.avail(active.get_col(), active.get_row()):
                corner_count += 1
            if not self.avail(active.get_col() + 2, active.get_row()):
                corner_count += 1
            if not self.avail(active.get_col(), active.get_row() - 2):
                corner_count += 1
            if not self.avail(active.get_col() + 2, active.get_row() - 2):
                corner_count += 1
        clear_count = 0
        i = 0
        # clears the lines, incrementing clear_count for every line that was filled
        while i < 22:
            filled = True
            for j in range(10):
                if self.board[j][i] == (0, 0, 0):
                    filled = False
                    break;
            if filled:
                clear_count += 1
                for k in range(i, 21):
                    for j in range(10):
                        self.board[j][k] = self.board[j][k + 1]
                for k in range(10):
                    self.board[k][21] = (0, 0, 0)
                i -= 1
            i += 1
        empty_count = 0
        # case checks for T-spins
        if (corner_count == 3 and (active.get_state() == 0 or active.get_state() == 2)) or corner_count == 4:
            if self.avail(active.get_col() + 1, active.get_row()):
                empty_count += 1
            if self.avail(active.get_col(), active.get_row() - 1):
                empty_count += 1
            if self.avail(active.get_col() + 2, active.get_row() - 1):
                empty_count += 1
            if self.avail(active.get_col() + 1, active.get_row() - 2):
                empty_count += 1
            if empty_count >= 1:
                if clear_count == 0:
                    score += 400
                    message1 = "T-Spin!"
                    t_spin = 1
                elif clear_count == 1:
                    score += 800
                    message1 = "T-Spin Single!"
                    t_spin = 2
                elif clear_count == 2:
                    score += 1200
                    message1 = "T-Spin Double!"
                    t_spin = 3
                elif clear_count == 3:
                    score += 1600
                    message1 = "T-Spin Triple!"
                    t_spin = 4
        # check if a tetris happened
        if clear_count == 4:
            score += 800
            message1 = "Tetris!"
        # if b2b is true, then bonus points
        if self.b2b and clear_count != 0:
            score *= 3/ 2
            message1 = "Back to Back " + message1
        # if the piece dropped cleared something but it wasn't a tetris or t-spin, b2b is now false
        if score == 0 and clear_count != 0:
            self.b2b = False
            if clear_count == 1:
                score += 100
                message1 = "Single"
            elif clear_count == 2:
                score += 300
                message1 = "Double"
            elif clear_count == 3:
                score += 500
                message1 = "Triple"
        # otherwise, if a t-spin or tetris was performed, b2b is true
        elif score != 0 and clear_count != 0:
            self.b2b = True
        # account for combos
        if score != 0:
            score += 50 * self.combo
            if self.combo > 0:
                message2 = "Combo " + str(self.combo) + "!"
            self.combo += 1
        # otherwise if nothing was cleared, then the combo is broken, reset it to 0
        else:
            self.combo = 0
        score *= level
        # account for points based on soft drops and hard drops
        score += self.soft_drop
        # an i Piece spawns one grid below all the other pieces, so it has it's own case
        if i_piece:
            score += (21 - active.get_row() - self.soft_drop) * 2
        else:
            score += (22 - active.get_row() - self.soft_drop) * 2
        # reset soft_drop
        self.soft_drop = 0
        # add the score gained by that one piece to the total score
        self.score += score
        # return all useful info
        return int(score), message1, message2, False, clear_count, t_spin

    # returns the board
    def get_board(self):
        return self.board
