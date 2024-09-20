//by Muk Chunpongtong. Initially made for python.
var board_width = 6;
var board_height = 6;
var score_to_win = 4;
var html_board = []; // a jagged array 
var container = document.querySelector('.ttt-container');
var width_input = document.getElementById('width');
var height_input = document.getElementById('height');
var length_input = document.getElementById('length');
var enter_button = document.getElementById('enter');
var shrink_button = document.getElementById('shrink');
var expand_button = document.getElementById('expand');
var win_text = document.querySelector('.win-text');
var player_color = '#000099';
var bot_color = '#990000';
var base_color = '#171717';
var gray_color = '#cdcdcd';
var player_selection;
var board = [];
var played_squares = [];
var winner = 0;
var started = false;



function contains_subarray(main_array, sub_array) {
    return main_array.some(arr =>
      Array.isArray(arr) && sub_array.every((subElem, index) => arr[index] === subElem)
    );
  }
  

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



function bot(foresight, board_w, board_h, board, team, enemy, required_score, level) {
    // literally simulate a game in its head
    // find all empties, simulate what happens.
    var start_time = performance.now();
    var empties = [];
    var scores = []; // scores will be assigned to each empty
    for (var row = 0; row < board.length; row++) {
        for (var column = 0; column < board[row].length; column++) {
            if (board[row][column] === 0) {
                empties.push([column, row]); // lists go (x, y)
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
                    ns += bot(foresight, board_w, board_h, bb, team, enemy, required_score, level + 1).reduce((a, b) => a + b, 0);
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

function play_start() {
    board = []; // jagged array
    for (var a = 0; a < board_height; a++) {
        var sub = [];
        for (var b = 0; b < board_width; b++) {
            sub.push(0);
        }
        board.push(sub);
    }
    display_board();
    
    var first_player = Math.floor(Math.random() * 2); // if 0, the human goes first
    if (first_player === 1){
        setTimeout(bot_move, 100);
    }
}

function display_board() {
    var alloted_width = container.offsetWidth;    
    for (var y = 0; y < board_height; y++){
        for (var x = 0; x < board_width; x++){
            if (board[y][x] === 0){
                html_board[y][x].style.background = gray_color;
            }
            else if (board[y][x] === 1){
                html_board[y][x].style.background = player_color;
            }
            else if (board[y][x] === 2){
                html_board[y][x].style.background = bot_color;
            }
        }
    }
    console.log(winner);
    switch (winner) {
        case 0:
            container.style.background = base_color;
            win_text.style.color = base_color;
            win_text.style.display = 'none';
            break;
        case 1:
            container.style.background = player_color;
            win_text.style.color = player_color;
            win_text.style.display = 'inline';
            win_text.innerHTML = 'PLAYER WON';
            break;
        case 2:
            container.style.background = bot_color;
            win_text.style.display = 'inline';
            win_text.style.color = bot_color;
            win_text.innerHTML = 'BOT WON';
            break;
        case 3:
            container.style.background = gray_color;
            win_text.style.color = gray_color;
            win_text.style.display = 'inline';
            win_text.innerHTML = 'TIED';
            break;
    }
}

function new_board() {
    winner = 0;
    board = []
    for (var a = 0; a < html_board.length; a++) {
        for (var b = 0; b < html_board[a].length; b++) {
            html_board[a][b].remove();
        }
    }
    html_board = []; // clear the board
    
    for (var y = 0; y < board_height; y++){
        board[y] = [];
        for (var x = 0; x < board_width; x++){
            board[y][x] = 0;

        }
    }

    for (var y = 0; y < board_height; y++){
        html_board[y] = [];
        for (var x = 0; x < board_width; x++){
            html_board[y][x] = document.createElement("button");
            html_board[y][x].classList.add('ttt-box');
            html_board[y][x].id = x.toString() + "," + y.toString();
            html_board[y][x].addEventListener('click', input);
            container.appendChild(html_board[y][x]);
        }
    }
    var adder = '';
    for (var x = 0; x < board_width; x++){
        adder += 'auto ';
    }
    container.style.gridTemplateColumns = adder;
    display_board();
}

function bot_move(){
    var new_square = bot(2, board_width, board_height, board, 2, 1, score_to_win, 1);
    played_squares.push(new_square); // wont repeat again
    console.log(played_squares.length);
    board[new_square[1]][new_square[0]] = 2; // player is 1, bot is 2
    if (win_check(board_width, board_height, board, new_square, score_to_win)[0]) {
        console.log("***FINISHED***");
        winner = 2;
        started = false;
        played_squares = [];
    }
    else if (played_squares.length >= (board_height * board_width)){
        //its a draw
        console.log("***FINISHED***");
        winner = 3;
        started = false;
        played_squares = [];
    }
    display_board();
}

function input(event){
    if (started === false){
        started = true;
        new_board();
        play_start();
    }
    else{
        const clicked = event.target;
        var new_square = read_square(clicked);   
        player_selection = new_square; //this will be played on the player's turn. Allows for premoving as well.
        if (contains_subarray(played_squares, new_square) === true) {
            console.log("invalid, retry");
        } else {
            played_squares.push(new_square); // wont repeat again
            console.log(played_squares.length);
            board[new_square[1]][new_square[0]] = 1; // player is 1, bot is 2
            
            if (win_check(board_width, board_height, board, new_square, score_to_win)[0]) {
                console.log("***FINISHED***");
                winner = 1;
                started = false;
                played_squares = [];
                // win code
            } 
            // no remaining places and no winner
            else if (played_squares.length >= (board_height * board_width)){
                //its a draw
                console.log("***FINISHED***");
                started = false;
                played_squares = [];
            }
            
            else{
                setTimeout(bot_move, 100);
            }   
            display_board();
        }
    }
}


function send_settings(){
    if (width_input.value<15 &&
        height_input.value<15  &&
        length_input.value<15)
    {
        board_width = width_input.value;
        board_height = height_input.value;
        score_to_win = length_input.value;
        started = false;
        played_squares = [];
        new_board();
    }
}

function read_square(square){
    var text = square.id.split(",");
    return [parseInt(text[0]), parseInt(text[1])];  // x and y
}

function shrink(){
    container.style.width = parseInt(container.style.width)/1.1 + "%";
}

function expand(){
    container.style.width = parseInt(container.style.width)*1.1 + "%";
}

document.addEventListener('DOMContentLoaded', function() {
    container.style.width = 100 + "%";
    enter_button.addEventListener("click", send_settings);
    shrink_button.addEventListener("click", shrink);
    expand_button.addEventListener("click", expand);
    new_board();
}, false);