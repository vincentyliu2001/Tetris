import pygame

pygame.init()

# These are the building blocks of the game, everything in Tetris is a block in one form or another
# Each piece has four blocks
# The game board does not use blocks as it only cares about colors


class Block:
    def __init__(self, col, row, color):
        self.color = color  # color of the block
        self.row = row  # position by row of the block, 1 indexing because only Pieces use blocks
        self.col = col  # position by col of the block, 1 indexing because only Pieces use blocks

    # draws the block in appropriate location on screen given col and row
    def draw(self, screen, col_diff, row_diff):
        pygame.draw.rect(screen, self.color, (((self.col + col_diff) * 20 + 130), ((20 - self.row + row_diff) * 20 + 50),
                                              20, 20))

    # set the row
    def set_row(self, row):
        self.row = row

    # set the column
    def set_col(self, col):
        self.col = col

    # get the row
    def get_row(self):
        return self.row

    # get the column
    def get_col(self):
        return self.col

    # get the color
    def get_color(self):
        return self.color
