
var board_width = 4, board_height = 4;
var score_to_win = 3;

// .copy() doesnt work for jagged
function jl_copy(t_list) {
    var new_list = [];
    for (var a = 0; a < t_list.length; a++) {
        var sub = [];
        for (var b = 0; b < t_list[a].length; b++) {
            sub.push(t_list[a][b]);
        }
        new_list.push(sub);
    }
    return new_list;
}

function bound_check(to_check, max_x, max_y) {
    if (to_check[0] < 0 || to_check[1] < 0 || to_check[0] > max_x || to_check[1] > max_y) {
        return false;
    }
    return true;
}

function win_check(board_w, board_h, t_board, updated_square, required_score) {
    var start = performance.now();
    var test_board = jl_copy(t_board);
    var looking_for = test_board[updated_square[1]][updated_square[0]];
    var neighbors = [];
    // get a list of neighbors of starting square
    for (var xs = -1; xs <= 1; xs++) {
        for (var ys = -1; ys <= 1; ys++) {
            if (xs === 0 && ys === 0) {
                continue;
            } else {
                if (updated_square[1] - 1 < 0 && ys === -1) { // vertical 0 edge
                    continue;
                } else if (updated_square[1] + 1 > board_h - 1 && ys === 1) { // high edge
                    continue;
                }
                if (updated_square[0] - 1 < 0 && xs === -1) { // horizontal 0 edge
                    continue;
                } else if (updated_square[0] + 1 > board_w - 1 && xs === 1) { // horizontal limit edge
                    continue;
                }
                // otherwise add the square to neighbours[] if matches
                var try_x = updated_square[0] + xs, try_y = updated_square[1] + ys;
                if (test_board[try_y][try_x] === looking_for) {
                    neighbors.push([try_x, try_y]);
                }
            }
        }
    }

    for (var i = 0; i < neighbors.length; i++) {
        var neighbor = neighbors[i];
        var vector = [neighbor[0] - updated_square[0], neighbor[1] - updated_square[1]]; // ex [1,0], [-1,-1]
        var squares = [updated_square];
        var current_score = 1; // the updated square is 1
        // keep checking next square in that direction until win
        var reversing = false;
        var j = 0;
        while (j < required_score * 2) {
            if (current_score >= required_score) {
                return [true, looking_for, performance.now() - start]; // did someone win? if so, who? how long?
            } else {
                if (!reversing) {
                    var x = updated_square[0] + (j + 1) * vector[0];
                    var y = updated_square[1] + (j + 1) * vector[1];
                    var sam = [x, y];
                } else {
                    var x = updated_square[0] + (j + 1) * -vector[0];
                    var y = updated_square[1] + (j + 1) * -vector[1];
                    var sam = [x, y];
                }

                if (!bound_check(sam, board_width - 1, board_height - 1) || test_board[sam[1]][sam[0]] !== looking_for) {
                    if (!reversing) {
                        reversing = true;
                        j = j * 0 - 1; // looping back up adds 1
                    } else {
                        break;
                    }
                } else {
                    current_score += 1;
                    squares.push(sam);
                }
            }
            j += 1;
        }
    }

    // if the code has advanced to here, then there was no win
    return [false, looking_for, performance.now() - start];
}

function display_board(to_display) {
    for (var i = 0; i < to_display.length; i++) {
        console.log(to_display[i]);
    }
}

function bot(foresight, board_w, board_h, board, team, enemy, required_score, level) {
    // literally simulate a game in its head
    // find all empties, simulate what happens.
    var start_time = performance.now();
    var empties = [];
    var scores = []; // scores will be assigned to each empty
    for (var row = 0; row < board.length; row++) {
        for (var column = 0; column < board[row].length; column++) {
            if (board[row][column] === 0) {
                empties.push([column, row]); // lists go (y, x)
                scores.push(0);
            }
        }
    }

    while (true) {
        var finish = false;

        // pass 1 (can bot win this turn?)
        for (var i = 0; i < empties.length; i++) {
            var empty = empties[i];
            var b = jl_copy(board);
            b[empty[1]][empty[0]] = team;
            if (win_check(board_w, board_h, b, empty, required_score)[0]) {
                scores[i] += 100 / level; // things are more important the sooner they are
                finish = true;
            }
        }

        if (finish) {
            break;
        }

        // pass 2 (can enemy win this turn? if so stop it)
        for (var i = 0; i < empties.length; i++) {
            var empty = empties[i];
            var b = jl_copy(board);
            b[empty[1]][empty[0]] = enemy;
            if (win_check(board_w, board_h, b, empty, required_score)[0]) {
                // negative score to everything except the blocker
                for (var j = 0; j < empties.length; j++) {
                    if (j !== i) {
                        scores[j] = -100 / level; // choosing this would result in defeat
                    } else {
                        scores[j] = 0; // gain nothing, but don't lose
                    }
                }
                finish = true;
            }
        }

        if (finish) {
            break;
        }

        // pass 3 how valuable is this move?
        if (level < foresight) {
            for (var i = 0; i < empties.length; i++) {
                var empty = empties[i];
                var b = jl_copy(board);
                b[empty[1]][empty[0]] = team;
                // consider the enemy action
                var ns = 0;
                for (var j = 0; j < empties.length; j++) {
                    var r_empty = empties[j];
                    // play
                    var bb = jl_copy(b);
                    bb[r_empty[1]][r_empty[0]] = enemy;
                    ns += sum(bot(foresight, board_w, board_h, bb, team, enemy, required_score, level + 1));
                }
                scores[i] = ns / empties.length;
            }
        }
        break;
    }

    if (level === 1) { // level starts at 1 to avoid divide by 0
        var highest = -999999;
        var pick = empties[Math.floor(Math.random() * empties.length)];
        for (var i = 0; i < scores.length; i++) {
            if (scores[i] > highest) {
                pick = empties[i];
                highest = scores[i];
            }
        }
        console.log((performance.now() - start_time) / 1000000 + "ms");
        return pick;
    } else { // sub-level, return scores
        return scores;
    }
}

function play() {
    while (true) {
        var board = [];
        for (var a = 0; a < board_height; a++) {
            var sub = [];
            for (var b = 0; b < board_width; b++) {
                sub.push(0);
            }
            board.push(sub);
        }
        console.log("START");
        display_board(board);
        var played_squares = [];
        // as many turns as there are squares
        var first_player = Math.floor(Math.random() * 2); // if 0, the human goes first
        var winner = 0;
        for (var turns = 0; turns < board_width * board_height * 2; turns++) {
            if (turns % 2 === first_player) {
                // human plays
                console.log("HUMAN PLAYS");
                while (true) {
                    var new_square = [parseInt(prompt("x:")), parseInt(prompt("y:"))];
                    if (played_squares.includes(new_square)) {
                        console.log("invalid, retry");
                    } else {
                        played_squares.push(new_square); // wont repeat again
                        board[new_square[1]][new_square[0]] = 1; // player is 1, bot is 2
                        if (win_check(board_width, board_height, board, new_square, score_to_win)[0]) {
                            console.log("FINISHED");
                            winner = 1;
                        }
                        display_board(board);
                        break;
                    }
                }
            } else {
                // bot plays
                console.log("BOT PLAYS");
                var new_square = bot(2, board_width, board_height, board, 2, 1, score_to_win, 1);
                played_squares.push(new_square); // wont repeat again
                board[new_square[1]][new_square[0]] = 2; // player is 1, bot is 2
                console.log(new_square);
                if (win_check(board_width, board_height, board, new_square, score_to_win)[0]) {
                    console.log("***FINISHED***");
                    winner = 2;
                }
                display_board(board);
            }

            if (winner !== 0) {
                if (winner === 1) {
                    console.log("**PLAYER WON**");
                } else {
                    console.log("**BOT WON**");
                }
                break;
            }
        }
    }
}

play();
