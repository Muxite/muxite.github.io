import random

board_width, board_height = 3, 3
score_to_win = 3
board = []


def win_check(board_w, board_h, test_board, updated_square, required_score):
    looking_for = test_board[updated_square[1]][updated_square[0]]
    neighbors = []
    # get a list of neighbors of starting square
    for xs in [-1, 0, 1]:
        for ys in [-1, 0, 1]:
            if (xs, ys) != (0, 0):
                if updated_square[0]-1 < 0 and ys == -1:  # vertical 0 edge
                    continue
                elif updated_square[0]+1 > board_h-1 and ys == 1:  # high edge
                    continue
                if updated_square[1]-1 < 0 and xs == -1:  # horizontal 0 edge
                    continue
                elif updated_square[1]+1 > board_w-1 and xs == 1:  # horizontal limit edge
                    continue
                # otherwise add the square to neighbours[]
                neighbors.append((updated_square[1] + xs, updated_square[0] + ys))
            else:
                continue

    for neighbor in neighbors:
        vector = (neighbor[0]-updated_square[0], neighbor[1]-updated_square[1])  # ex (1,0), (-1,-1)
        print(vector)
        current_score = 1  # the updated square is 1
        # keep checking next square in that direction until win
        for i in range(required_score):
            if current_score > required_score:
                print("WINNER" + str(looking_for))
                return True, looking_for  # did someone win? if so, who?
            else:
                # if the next square in the vector is same as looking_for
                try:  # 2 is added to skip to after neighbor
                    print(test_board[updated_square[1]+(i+1)*vector[1]][updated_square[0]+(i+1)*vector[0]])
                    if test_board[updated_square[1]+(i+1)*vector[1]][updated_square[0]+(i+1)*vector[0]] == looking_for:
                        current_score += 1
                except IndexError:  # out of bounds
                    break  # now hit edge
        # now check reverse direction
        for i in range(required_score):
            if current_score > required_score:
                print("WINNER " + str(looking_for))
                return True, looking_for  # did someone win? if so, who?
            else:
                # if the next square in the vector is same as looking_for
                try:  # add 1 to skip the starting block
                    if test_board[updated_square[1] + (i+1) * -vector[1]][
                     updated_square[0] + (i+1) * -vector[0]] == looking_for:
                        current_score += 1
                except IndexError:  # out of bounds
                    break  # now hit edge

    # if the code has advanced to here, then there was no win
    return False, looking_for


def display_board(to_display):
    for i in range(len(to_display)):
        print(to_display[i])


def play():
    global board
    board = []
    for a in range(board_height):
        sub = []
        for b in range(board_width):
            sub.append(0)
        board.append(sub)
    print(board)
    display_board(board)
    played_squares = []
    # as many turns as there are squares
    first_player = random.randint(0, 1)  # if 0, the human goes first
    for turns in range(board_width*board_height):
        if turns % 2 == first_player:
            # human plays
            while True:
                new_square = (int(input("x:")), int(input("y:")))
                if new_square in played_squares:
                    print("invalid, retry")
                else:
                    played_squares.append(new_square)  # wont repeat again
                    board[new_square[1]][new_square[0]] = 1  # player is 1, bot is 2
                    win_check(board_width, board_height, board, new_square, score_to_win)
                    display_board(board)
                    break

        else:
            # bot plays
            pass

play()

