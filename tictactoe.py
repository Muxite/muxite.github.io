board_width, board_height = 3, 3
line_length = 3
board = [[0]*board_width]*board_height


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
        vector = (updated_square[0]-neighbor[0],updated_square[1]-neighbor[1])  # ex (1,0), (-1,-1)
        current_score = 2  # the updated square is 1, the neighbor in this direction is 2
        # keep checking next square in that direction until win
        for i in range(required_score):
            if current_score > required_score:
                print("WINNER" + str(looking_for))
                return True, looking_for  # did someone win? if so, who?
            else:
                # if the next square in the vector is same as looking_for
                try:  # 2 is added to skip to after neighbor
                    if test_board[updated_square[1]+(i+2)*vector[1]][updated_square[0]+(i+2)*vector[0]] == looking_for:
                        current_score += 1
                except IndexError:  # out of bounds
                    break  # now
        # now check reverse direction
        for i in range(required_score):
            if current_score > required_score:
                print("WINNER" + str(looking_for))
                return True, looking_for  # did someone win? if so, who?
            else:
                # if the next square in the vector is same as looking_for
                try:  # add 1 to skip the starting block
                    if test_board[updated_square[1] + (i+1) * -vector[1]][
                     updated_square[0] + (i+1) * -vector[0]] == looking_for:
                        current_score += 1
                except IndexError:  # out of bounds
                    break  # now

    # if the code has advanced to here, then there was no win
    return False, looking_for

