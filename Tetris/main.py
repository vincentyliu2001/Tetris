import graphics
import random
import pieces
import time
from board import Board
from pieces import *
import AI_helper


pygame.init()


# makes the bag to get pieces from
def initialize_bag(piece_bag, piece_bag2):
    piece_bag.clear()
    piece_bag2.clear()
    for i in range(7):
        piece_bag2.append(i)
    for i in range(7):
        temp_id = random.choice(piece_bag2)
        piece_bag2.remove(temp_id)
        piece_bag.append(temp_id)
    for i in range(7):
        piece_bag2.append(i)


# returns a piece from the bag
# bag randomized: as explained below
# pieces are randomized, but for every 7 pieces, each piece must appear once
def extract_piece(piece_bag, piece_bag2):
    temp_num = piece_bag[0]
    piece_bag.remove(temp_num)
    piece_new = random.choice(piece_bag2)
    piece_bag.append(piece_new)
    piece_bag2.remove(piece_new)
    if len(piece_bag2) == 0:
        for j in range(7):
            piece_bag2.append(j)
    return pieces.get_piece(temp_num, 0, 0)


# moves pieces to the left or right instantly
def auto_repeat(piece, game_board, right):
    if right:
        piece.quick_move(1, 0, game_board)
    else:
        piece.quick_move(-1, 0, game_board)


# turns all filled blocks gray
def end_game(board):
    for i in range(22):
        for j in range(10):
            if board.get_board()[j][i] != (0, 0, 0):
                board.get_board()[j][i] = (120, 120, 120)

# ***TRIPLE T-SPIN TEST***
"""
    for i in range(5):
        for j in range(10):
            board.get_board()[j][i] = (255, 255, 255)

    board.get_board()[9][3] = (0, 0, 0)
    board.get_board()[9][4] = (0, 0, 0)
    board.get_board()[8][3] = (0, 0, 0)
    board.get_board()[8][4] = (0, 0, 0)
    board.get_board()[7][3] = (0, 0, 0)
    board.get_board()[7][2] = (0, 0, 0)
    board.get_board()[7][1] = (0, 0, 0)
    board.get_board()[7][0] = (0, 0, 0)
    board.get_board()[8][1] = (0, 0, 0)

    board.get_board()[0][3] = (0, 0, 0)
    board.get_board()[0][4] = (0, 0, 0)
    board.get_board()[1][3] = (0, 0, 0)
    board.get_board()[1][4] = (0, 0, 0)
    board.get_board()[2][3] = (0, 0, 0)
    board.get_board()[2][2] = (0, 0, 0)
    board.get_board()[2][1] = (0, 0, 0)
    board.get_board()[2][0] = (0, 0, 0)
    board.get_board()[1][1] = (0, 0, 0)
"""


def game():
    clock = pygame.time.Clock()
    # Screen dimensions
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 500
    # Create screen obj
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    piece_bag = []
    piece_bag2 = []
    hold_piece = None
    initialize_bag(piece_bag, piece_bag2)
    can_hold = True
    board = Board()

    active = extract_piece(piece_bag, piece_bag2)
    # Run until the user asks to quit
    running = True
    ticks = 0
    auto_drop_event = pygame.USEREVENT + 1  # Even to auto drop piece once every second
    check_new_event = pygame.USEREVENT + 2  # Checks to see if the piece hasn't changed height and get's new piece
    auto_drop_freq = 1000
    check_new_freq = 500
    pygame.time.set_timer(auto_drop_event, auto_drop_freq)  # set the event
    pygame.time.set_timer(check_new_event, check_new_freq)  # set the event
    das = 0.070  # Delayed auto shift see: https://harddrop.com/wiki/DAS
    # Note ARR in this iteration of the game is always 0 see: https://harddrop.com/wiki/DAS
    # below are variables to handle DAS
    right_timer = None
    left_timer = None
    left_pressed = False
    right_pressed = False
    left_first = False
    right_first = False
    curr_row = 0  # curr_row, used by check_new_event
    score = 0  # the user's score
    print_message_1 = ""  # print's singles, doubles, t-spins etc. if the user performs them
    print_message_2 = ""  # print's combo 1, combo 2 etc if the user performs them
    game_over = False  # checker to see if the game is over
    need_next = False  # checker to see if we need another piece
    ticker = 0  # ticks every time the game loop runs
    while running:
        changed = False  # nothing has changed from the last game loop
        if game_over:
            end_game(board)  # turn all active blocks gray
            # draw this newly grayed board
            graphics.draw(screen, active, board, hold_piece, piece_bag, score, print_message_1, print_message_2)
        # soft_drop counting for scoring purposes
        if active.soft_drop(board):
            changed = True
            board.soft_drop += 1
        for event in pygame.event.get():
            if not game_over:
                # auto drops piece every second
                if event.type == auto_drop_event:
                    changed = active.move(0, -1, board)
                    board.soft_drop += 1
                # if the piece has not moved down for the event period, then get the next piece
                if event.type == check_new_event:
                    if active.get_row() == curr_row and not active.can_move(0, -1, board):
                        need_next = True
                    # this is to prevent stalling, if a piece hasn't been plaed in 50 seconds, the next one auto appears
                    elif ticker > 100:
                        need_next = True
                        active.quick_move(0, -1, board)
                    else:
                        ticker += 1
                        curr_row = active.get_row()
            # Did the user click the window close button?
            if event.type == pygame.QUIT:
                running = False
            # If not then handle everything else
            else:
                if event.type == pygame.KEYDOWN:
                    # F4 is the reset button
                    if event.key == pygame.K_F4:
                        # essentially resetting every relevant var, see above for var descriptions
                        board = Board()
                        hold_piece = None
                        score = 0
                        right_timer = None
                        left_timer = None
                        left_pressed = False
                        right_pressed = False
                        left_first = False
                        right_first = False
                        board.soft_drop = 0
                        print_message_1 = ""
                        print_message_2 = ""
                        can_hold = True
                        initialize_bag(piece_bag, piece_bag2)
                        active = extract_piece(piece_bag, piece_bag2)
                        game_over = False
                        graphics.draw(screen, active, board, hold_piece, piece_bag, score, print_message_1, print_message_2)
                    # we don't want our user to keep playing if they've already lost
                    if not game_over:
                        # holding handling
                        if event.key == pygame.K_LSHIFT:
                            changed = True
                            if can_hold:
                                temp_piece = hold_piece
                                if isinstance(active, oPiece):
                                    hold_piece = type(active)(5, 22)
                                else:
                                    hold_piece = type(active)(4, 22)
                                active = temp_piece
                                if active is None:
                                    active = extract_piece(piece_bag, piece_bag2)
                                can_hold = False
                            board.soft_drop = 0
                        # handling pressing the right key, this is handled in the main
                        # because key presses should transfer over to next pieces
                        # ie if I hold the right key, and place a key, continue holding right, the next key should
                        # almost instantly move to the right as well
                        if event.key == pygame.K_RIGHT:
                            right_timer = time.time()
                            right_first = True
                            left_first = False
                            right_pressed = True
                        # handling pressing the left key
                        # handled in main for same reasons above, not unique to each piece
                        if event.key == pygame.K_LEFT:
                            left_timer = time.time()
                            left_first = True
                            right_first = False
                            left_pressed = True
            # reset variables if the left or right arrow key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right_pressed = False
                    right_first = False
                if event.key == pygame.K_LEFT:
                    left_pressed = False
                    left_first = False
            # update piece based on event
            if game_over:
                continue
            # returns if anything happened, if not nothing changed
            booleans = active.update(event, board)
            if booleans[0]:
                changed = booleans[0]
            if not need_next:
                need_next = booleans[1]
            # if we need another piece, set the piece into the game board
            # then get the next piece from the piece_bag
            if need_next:
                can_hold = True
                for block in active.get_blocks():
                    board.add(block.get_col(), block.get_row(), block.get_color())
                results = board.clear_line(active, isinstance(active, tPiece), isinstance(active, iPiece))
                # updating print messages and score
                score += results[0]
                print_message_1 = results[1]
                print_message_2 = results[2]
                game_over = results[3]
                active = extract_piece(piece_bag, piece_bag2)
                curr_row = 0
                need_next = False
                ticker = 0
        # DAS handling
        temp_time = time.time()
        if left_pressed and (not right_pressed):
            if (temp_time - left_timer) > das:
                auto_repeat(active, board, False)
                changed = True
        elif right_pressed and (not left_pressed):
            if (temp_time - right_timer) > das:
                auto_repeat(active, board, True)
                changed = True
        elif right_pressed and left_pressed:
            if left_first:
                if (temp_time - left_timer) > das:
                    auto_repeat(active, board, False)
                    changed = True
            elif right_first:
                if (temp_time - right_timer) > das:
                    auto_repeat(active, board, True)
                    changed = True
        # Draw everything if something changed or if first frame
        pygame.display.flip()
        if changed or ticks == 0:
            graphics.draw(screen, active, board, hold_piece, piece_bag, score, print_message_1, print_message_2)
        # Flip the display
        test = AI_helper.get__hrt_advanced(board)

        # Limit 1000 fps note rendering only occurs when something changes so this is not cpu heavy at all
        # for most ticks, nothing even happens since no events are even pressed, very cpu light
        # for accurate DAS and ARR recommended tick at least 1000
        clock.tick(300)
        # print fps
        if ticks == 300:
            print("fps: " + str(clock.get_fps()))
            ticks = 0
        ticks += 1
    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    # run the game!
    game()
