import random
import time
board_width, board_height = 4, 4
score_to_win = 3


# .copy() doesnt work for jagged
def jl_copy(t_list):
    new = []
    for a in range(len(t_list)):
        sub = []
        for b in range(len(t_list[a])):
            sub.append(t_list[a][b])
        new.append(sub)
    return new


def bound_check(to_check, max_x, max_y):
    if to_check[0] < 0 or to_check[1] < 0 or to_check[0] > max_x or to_check[1] > max_y:
        return False
    return True


def win_check(board_w, board_h, t_board, updated_square, required_score):
    start = time.time_ns()
    test_board = jl_copy(t_board)
    looking_for = test_board[updated_square[1]][updated_square[0]]
    neighbors = []
    # get a list of neighbors of starting square
    for xs in [-1, 0, 1]:
        for ys in [-1, 0, 1]:
            if xs == 0 and ys == 0:
                continue
            else:
                if updated_square[1]-1 < 0 and ys == -1:  # vertical 0 edge
                    continue
                elif updated_square[1]+1 > board_h-1 and ys == 1:  # high edge
                    continue
                if updated_square[0]-1 < 0 and xs == -1:  # horizontal 0 edge
                    continue
                elif updated_square[0]+1 > board_w-1 and xs == 1:  # horizontal limit edge
                    continue
                # otherwise add the square to neighbours[] if matches
                try_x, try_y = updated_square[0] + xs, updated_square[1] + ys
                if test_board[try_y][try_x] == looking_for:
                    neighbors.append((try_x, try_y))

    for neighbor in neighbors:
        vector = (neighbor[0]-updated_square[0], neighbor[1]-updated_square[1])  # ex (1,0), (-1,-1)
        squares = [updated_square]
        current_score = 1  # the updated square is 1
        # keep checking next square in that direction until win
        reversing = False
        i = 0
        while i < required_score*2:
            if current_score >= required_score:
                return True, looking_for, time.time_ns() - start  # did someone win? if so, who? how long?
            else:
                if not reversing:
                    x = updated_square[0] + (i+1) * vector[0]
                    y = updated_square[1] + (i+1) * vector[1]
                    sam = x, y

                else:
                    x = updated_square[0] + (i+1) * -vector[0]
                    y = updated_square[1] + (i+1) * -vector[1]
                    sam = x, y

                if not bound_check(sam, board_width-1, board_height-1) or test_board[sam[1]][sam[0]] != looking_for:
                    if not reversing:
                        reversing = True
                        i = i * 0 - 1  # looping back up adds 1
                    else:
                        break
                else:
                    current_score += 1
                    squares.append(sam)
            i += 1

    # if the code has advanced to here, then there was no win
    return False, looking_for, time.time_ns() - start


def display_board(to_display):
    for i in range(len(to_display)):
        print(to_display[i])


def bot(foresight, board_w, board_h, board, team, enemy, required_score, level):
    # literally simulate a game in its head
    # find all empties, simulate what happens.
    start_time = time.time_ns()
    empties = []
    scores = []  # scores will be assigned to each empty
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == 0:
                empties.append((int(column), int(row)))  # lists go (y, x)
                scores.append(0)

    #  I just wanna use break
    while True:
        finish = False

        # pass 1 (can bot win this turn?)
        for i, empty in enumerate(empties):
            b = jl_copy(board)
            b[empty[1]][empty[0]] = team
            if win_check(board_w, board_h, b, empty, required_score)[0]:
                scores[i] += 100/level  # things are more important the sooner they are
                finish = True

        if finish is True:
            break

        # pass 2 (can enemy win this turn? if so stop it)
        for i, empty in enumerate(empties):
            b = jl_copy(board)
            b[empty[1]][empty[0]] = enemy
            if win_check(board_w, board_h, b, empty, required_score)[0]:
                # negative score to everything except the blocker
                for j in range(len(empties)):
                    if j != i:
                        scores[j] = -100/level  # choosing this would result in defeat
                    else:
                        scores[j] = 0  # gain nothing, but don't lose
                finish = True

        if finish is True:
            break

        # pass 3 how valuable is this move?
        if level < foresight:
            for i, empty in enumerate(empties):
                b = jl_copy(board)
                b[empty[1]][empty[0]] = team
                # consider the enemy action
                ns = 0
                for j, r_empty in enumerate(empties):
                    # play
                    bb = jl_copy(b)
                    bb[r_empty[1]][r_empty[0]] = enemy
                    ns += sum(bot(foresight, board_w, board_h, bb, team, enemy, required_score, level+1))
                scores[i] = ns/(len(empties))
        break

    if level == 1:  # level starts at 1 to avoid divide by 0
        highest = -999999
        pick = random.choice(empties)
        for i, score in enumerate(scores):
            if score > highest:
                pick = empties[i]
                highest = score
        print(str((time.time_ns() - start_time)/1000000) + "ms")
        return pick
    else:  # sub-level, return scores
        return scores


def play():
    while True:
        board = []
        for a in range(board_height):
            sub = []
            for b in range(board_width):
                sub.append(0)
            board.append(sub)
        print("START")
        display_board(board)
        played_squares = []
        # as many turns as there are squares
        first_player = random.randint(0, 1)  # if 0, the human goes first
        winner = 0
        for turns in range(board_width*board_height*2):
            if turns % 2 == first_player:
                # human plays
                print("HUMAN PLAYS")
                while True:
                    new_square = (int(input("x:")), int(input("y:")))
                    if new_square in played_squares:
                        print("invalid, retry")
                    else:
                        played_squares.append(new_square)  # wont repeat again
                        board[new_square[1]][new_square[0]] = 1  # player is 1, bot is 2
                        if win_check(board_width, board_height, board, new_square, score_to_win)[0]:
                            print("FINISHED")
                            winner = 1
                        display_board(board)
                        break
            else:
                # bot plays
                print("BOT PLAYS")
                new_square = bot(2, board_width, board_height, board, 2, 1, score_to_win, 1)
                played_squares.append(new_square)  # wont repeat again
                board[new_square[1]][new_square[0]] = 2  # player is 1, bot is 2
                print(new_square)
                if win_check(board_width, board_height, board, new_square, score_to_win)[0]:
                    print("***FINISHED***")
                    winner = 2
                display_board(board)

            if winner != 0:
                if winner == 1:
                    print("**PLAYER WON**")
                else:
                    print("**BOT WON**")
                break

    # for turns in range(board_width*board_height*2):
    #     # bot v bot
    #     if turns % 2 == first_player:
    #         print("BOT PLAYS")
    #         new_square = bot(2, board_width, board_height, board, 1, 2, score_to_win, 1)
    #         played_squares.append(new_square)  # wont repeat again
    #         board[new_square[1]][new_square[0]] = 1  # player is 1, bot is 2
    #         print(new_square)
    #         display_board(board)
    #         if win_check(board_width, board_height, board, new_square, score_to_win)[0]:
    #             print("***FINISHED***")
    #             break
    #
    #     else:
    #         # bot plays
    #         print("BOT PLAYS")
    #         new_square = bot(2, board_width, board_height, board, 2, 1, score_to_win, 1)
    #         played_squares.append(new_square)  # wont repeat again
    #         board[new_square[1]][new_square[0]] = 2  # player is 1, bot is 2
    #         print(new_square)
    #         display_board(board)
    #         if win_check(board_width, board_height, board, new_square, score_to_win)[0]:
    #             print("***FINISHED***")
    #             break


def benchmark_win_check(reps):  # roughly 0.01433ms
    board = [[0, 1, 1],
             [0, 1, 1],
             [1, 0, 1]]

    adder = 0
    for i in range(reps):
        adder += win_check(board_width, board_height, board, (1, 1), score_to_win)[2]  # times
    ave_time = adder/reps
    print(str(ave_time/1000000) + "ms")


# benchmark_win_check(100000)

play()
