board_width, board_height = 3, 3
line_length = 3
board = [[0]*board_width]*board_height


def win_check (test_board, updated_square, required_score):
    check_x, check_y = updated_square


def square_check (board_w, board_h, test_board, updated_square, required_score, current_score, vector, parts):

    neighbors = []
    if vector is None:
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
    else:
        if vector == (1, 0) or vector == (-1, 0):
            neighbors.append((updated_square[1] + 1, updated_square[0]))
            neighbors.append((updated_square[1] - 1, updated_square[0]))
        elif vector == (0, 1) or vector == (0, 1):
            neighbors.append((updated_square[1], updated_square[0] - 1))
            neighbors.append((updated_square[1], updated_square[0] + 1))
        elif vector == (1, 1) or vector == (-1, -1):
            neighbors.append((updated_square[1] - 1, updated_square[0] - 1))
            neighbors.append((updated_square[1] + 1, updated_square[0] + 1))
        elif vector == (1, -1) or vector == (-1, 1):
            neighbors.append((updated_square[1] + 1, updated_square[0] - 1))
            neighbors.append((updated_square[1] - 1, updated_square[0] + 1))

    updated_square_value = test_board[updated_square[1]][updated_square[0]]
    #  go through each neighbor to see if they are the same as current
    current_score = len(parts)
    for neighbor in neighbors:
        #
        if test_board[neighbor[1]][neighbor[0]] == updated_square_value:
            if current_score+1 == required_score:  # if the length has been reached
                return True, updated_square  # win for this value
            else:
                #  check the ones in line of the vector (front and behind)




