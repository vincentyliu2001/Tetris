
import pieces
from pieces import *


# draws everything
def draw(screen, piece, board, hold_piece, pieces_bag, score, print_message_1, print_message_2):
    screen.fill((0, 0, 0))  # fill the screen with black
    draw_board(screen, board)  # draw the colors in the board
    draw_ghost(screen, board, piece)  # draw the shadow of the piece
    draw_pieces(screen, piece)  # draw the piece itself
    draw_grids(screen)  # draws the gray grid lines on the screen
    draw_queue(screen, pieces_bag)  # draws the 5-piece queue on the side
    font = pygame.font.Font('freesansbold.ttf', 24)  # set the font
    message_display("Score: " + str(score), screen, 0, font)  # displays the score
    message_display(print_message_1, screen, 25, font)  # displays first message, single, double, tetris etc
    message_display(print_message_2, screen, 50, font)  # displays second message, combo 1, combo 2 etc
    # if the hold_piece exists (it wouldn't exist before the first time the user uses hold)
    if hold_piece is not None:
        draw_hold(screen, hold_piece)  # draw the hold piece)


# draw grids
def draw_grids(screen):
    # grid color is gray
    gray = (100, 100, 100)
    for i in range(11):
        pygame.draw.line(screen, gray, (i * 20 + 150, 50), (i * 20 + 150, 450), 1)
    for i in range(21):
        pygame.draw.line(screen, gray, (150, i * 20 + 50), (350, i * 20 + 50), 1)


# draws pieces
def draw_pieces(screen, piece):
    piece.draw(screen, 0, 0)


# draw the board
def draw_board(screen, board):
    for i in range(10):
        for j in range(20):
            # create a block so we can draw it
            temp = Block(i + 1, j + 1, board.get_board()[i][j])
            temp.draw(screen, 0, 0)


# get the ghost with piece.get_ghost and draw it by making blocks and drawing them
def draw_ghost(screen, board, piece):
    diff = piece.get_ghost(board)
    for block in piece.get_blocks():
        gray = (110, 110, 110)
        temp = Block(block.get_col(), block.get_row() - diff, gray)
        temp.draw(screen, 0, 0)


# get the type of piece and make one that is in column -4, which would be to the upper left of the board
def draw_hold(screen, hold_piece):
    hold_draw = type(hold_piece)(-4, 20)
    for block in hold_draw.get_blocks():
        block.draw(screen, 0, 0)


# for every piece in the queue, get a piece that is translated appropriately and draw that piece
def draw_queue(screen, pieces_bag):
    counter = 0
    for i in range(5):
        pieces.get_piece(pieces_bag[i], 8, -counter * 3 - 2).draw(screen, 0, 0)
        counter += 1


# given text and font, draw the message
def text_objects(text, font):
    white = (255, 255, 255)
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


# draw the message accounting for y_diff
def message_display(text, screen, y_diff, large_text):
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.left = 375
    text_rect.bottom = 375 + y_diff
    screen.blit(text_surf, text_rect)


