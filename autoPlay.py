import neat
import os
from copy import copy, deepcopy
# Set up the drawing window
import AI_helper
import graphics
import random
import pieces
import time
from board import Board
from pieces import *
from block import Block

# this code is re-designed from "main.py" for use in python neat AI see comments there for more details
# documentation in this file focuses on the differences


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

# auto-repeat function missing: cpu does not use ARR as it can move to right or left fast enough one at a time


def end_game(board):
    for i in range(22):
        for j in range(10):
            if board.get_board()[j][i] != (0, 0, 0):
                board.get_board()[j][i] = (120, 120, 120)


# eval_genome is similar to "game" function in "main.py"


def eval_genome(genome, config):
    pygame.init()
    clock = pygame.time.Clock()
    ticks = 0
    running = True
    # Screen dimensions
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 500
    # Create screen obj
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    piece_bag = []
    piece_bag2 = []
    initialize_bag(piece_bag, piece_bag2)
    board = Board()
    active = extract_piece(piece_bag, piece_bag2)
    ge = genome
    tickers = 0
    piece_count = 0
    hold_piece = None
    print_message_1 = ""
    print_message_2 = ""
    # game loop very similar except every time the game loop runs, multiple games are played
    while running:
        # removes dead or stagnant genomes
        if board.game_over:
            board = Board()
            hold_piece = None
            score = 0
            board.soft_drop = 0
            print_message_1 = ""
            print_message_2 = ""
            can_hold = True
            initialize_bag(piece_bag, piece_bag2)
            active = extract_piece(piece_bag, piece_bag2)
            game_over = False
            graphics.draw(screen, active, board, hold_piece, piece_bag, score, print_message_1, print_message_2)
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # update piece based on genome
        # AI training main part:
        # gets all possible moves for current piece
        curr_possible_moves = AI_helper.get_possible_moves(board, active)
        # gets all possible moves for the piece if "hold" is used
        if hold_piece is None:
            curr_possible_moves_hold = AI_helper.get_possible_moves(board,
                                                                    pieces.get_piece(piece_bag[0], 0, 0))
        else:
            curr_possible_moves_hold = AI_helper.get_possible_moves(board, hold_piece)
        # best_move_ratings and best_possible_moves are not used in this iteration but are there for future use
        move_ratings = []
        total_possible_moves = []
        best_move_ratings = []
        best_possible_moves = []
        # for all possible moves, get the move_rating
        for i in range(len(curr_possible_moves)):
            # create a copy of the board
            temp_board = deepcopy(board)
            curr_piece = curr_possible_moves[i][1][1]
            # add the potential result of that move to the copy of the board
            for bl in curr_piece.get_blocks():
                temp_board.add(bl.get_col(), bl.get_row(), bl.get_color())
            # evaluate the board
            temp_nums = temp_board.clear_line(curr_piece, isinstance(curr_piece, tPiece),
                                              isinstance(curr_piece, iPiece))
            # evaluate the board
            nums = AI_helper.get__hrt_advanced(temp_board)
            # feed those numbers into the neural network to evaluate the state
            move_rating = net.activate((*nums, temp_nums[0], temp_nums[4], temp_nums[5]))[0]
            # add that evaluation to the list of all other evaluations
            move_ratings.append(move_rating)
            # add the possible move to the list of all other possible moves
            # move ratings and moves correspond (if not then nothing will work)
            total_possible_moves.append(curr_possible_moves[i])
            # this adds to best_possible_moves and best_move_ratings
            # note these are not actually used in this iteration, simply for future use
            if (nums[0] - board.holes) <= 0:
                best_possible_moves.append(curr_possible_moves[i])
                best_move_ratings.append(move_rating)
        # does the exact same thing as the above loop but for the piece you get if you used the "hold" command
        # adds results to the same list
        # differences are commented
        for i in range(len(curr_possible_moves_hold)):
            temp_board = deepcopy(board)
            curr_piece = curr_possible_moves_hold[i][1][1]
            for bl in curr_piece.get_blocks():
                temp_board.add(bl.get_col(), bl.get_row(), bl.get_color())
            temp_nums = temp_board.clear_line(curr_piece, isinstance(curr_piece, tPiece),
                                              isinstance(curr_piece, iPiece))
            nums = AI_helper.get__hrt_advanced(temp_board)
            move_rating = net.activate((*nums, temp_nums[0], temp_nums[4], temp_nums[5]))[0]
            move_ratings.append(move_rating)
            # because we have to hold first to access this piece, insert the corresponding number to move set
            # remember: 7 = hold
            curr_possible_moves_hold[i][1][0].insert(0, 7)
            total_possible_moves.append(curr_possible_moves_hold[i])
            if (nums[0] - board.holes) <= 0:
                best_possible_moves.append(curr_possible_moves_hold[i])
                best_move_ratings.append(move_rating)
        index = move_ratings.index(max(move_ratings))
        final_move_set = total_possible_moves[index][1][0]
        # only if 0 holes: diff AI version, code commented out:
        # index = best_move_ratings.index(max(best_move_ratings))
        # final_move_set = best_possible_moves[index][1][0]

        # given the best move: we loop through the move set and perform those moves to the piece
        # the moves should result in the board state that the neural network evaluated in the loops above
        for i in range(len(final_move_set)):
            if final_move_set[i] != 7:
                AI_helper.move_code(final_move_set[i], active, board)
            else:
                if hold_piece is not None:
                    temp_piece = active
                    active = hold_piece
                    hold_piece = temp_piece
                else:
                    hold_piece = active
                    active = extract_piece(piece_bag, piece_bag2)
            # every move_set hsa a 1 at the end because in regular tetris
            # hard dropping means you get the next piece instantly, if you soft drop, you have to wait a bit
            if final_move_set[i] == 1:
                board.need_next = True
            # draw the piece so we can see what's going on
            # this game loop pretty computationally heavy, the graphics will be really laggy
            # loop to get the next piece
        if board.need_next:
            # increment piece_count useful potentially in the future
            piece_count += 1
            board.can_hold = True
            # add it to that piece's game board
            for block in active.get_blocks():
                board.add(block.get_col(), block.get_row(), block.get_color())
            # clear the line
            messages = board.clear_line(active, isinstance(active, tPiece), isinstance(active, iPiece))
            print_message_1 = messages[1]
            print_message_2 = messages[2]
            # get the next piece
            active = extract_piece(piece_bag, piece_bag2)
            board.curr_row = 0
            # we don't need a next anymore
            board.need_next = False
            ticker = 0
        # Draw everything if something changed or if first frame
        # We only draw the first in each genome, rendering all of them would be too much
        # Flip the display
        pygame.display.flip()
        pps = 2
        # uncomment below line to limit pieces per second
        # clock.tick(pps)
        graphics.draw(screen, active, board, hold_piece, piece_bag, board.score, print_message_1, print_message_2)
        # Done! Time to quit.
        ticks += 1


pygame.quit()


def run(config_file):
    # import pickle so we can save checkpoints (each generation on my pc takes ~15 minutes)
    import pickle
    # config file from neat_configs
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    genome_file = open("tetris-ai", "rb")
    genome = pickle.load(genome_file)
    eval_genome(genome, config)


if __name__ == '__main__':
    # gets config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat_configs")
    run(config_path)
