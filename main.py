import random
# from pprint import pprint


Q = {}

# hyperparameters
alpha = 0.5
gamma = 0.9
min_epsilon = 0.01
min_alpha = 0.001
epsilon = 1.0
# req_score = 0.7
no_of_games = 200000


turn = ' '
X_wins = 0
O_wins = 0
draws = 0


def get_epsilon():
    if not hasattr(get_epsilon, "counter"):
        get_epsilon.counter = 0  # it doesn't exist yet, so initialize it
    get_epsilon.counter += 1
    # to decay epsilon
    m = epsilon // no_of_games
    return epsilon - (m * get_epsilon.counter)


def get_alpha():
    if not hasattr(get_alpha, "counter"):
        get_alpha.counter = 0  # it doesn't exist yet, so initialize it
    # to decay alpha
    m = alpha // no_of_games
    return alpha - (m * get_alpha.counter)


def new_game():
    board = []
    for _ in range(9):
        board.append(' ')
    return board


def draw(a):
    print "\t", a[0], "|", a[1], "|", a[2]
    print "\t", "---------"
    print "\t", a[3], "|", a[4], "|", a[5]
    print "\t", "---------"
    print "\t", a[6], "|", a[7], "|", a[8], "\n"


def check_game_over(board):
    # check if game is over
    combinations = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                    (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for i in combinations:
        if board[i[0]] == board[i[1]] == board[i[2]] != ' ':
            return board[i[0]]
    if ' ' not in board:
        return 'TIE'
    else:
        return 'Not over'


def get_available_actions(board):
    available_actions = []
    for i in range(0, 9):
        if board[i] == ' ':
            available_actions.append(i)
    return available_actions


def get_Q(board, action):
    # returns the q value
    b = tuple(board)
    if Q.get((b, action)) is None:
        Q[(b, action)] = 0
    return Q[(b, action)]


def get_best_move(board, turn, human=False):
    # searchs all possible moves and returns best move given the board
    actions = get_available_actions(board)
    eps = get_epsilon()
    # if random number is less than eps, make a random move(Exploration)
    if random.uniform(0, 1) < eps and human is False:
        return random.choice(actions)
    qs = [get_Q(board, action) for action in actions]
    # If its X's turn return max q value
    if turn == 'X':
        max_or_minQ = max(qs)
    else:
        # If its O's turn return min q value (minimises score for X player)
        max_or_minQ = min(qs)
    # If there are multiple good moves, select one randomly
    best_actions = [actions[i] for i in range(len(actions))
                    if qs[i] == max_or_minQ]

    return random.choice(best_actions)


def simulate_game(board, quiet=True):
    turn = 'X'
    game_over = False
    status = ''
    # save each game which can be used for updating q table
    game_list = []
    reward = 0
    while game_over is False:
        num = get_best_move(board, turn)
        game_list.append((board[:], num))
        board[num] = turn
        status = check_game_over(board)
        if quiet is False:
            draw(board)
            # pprint(game_list)
        if status == 'Not over':
            if turn == 'X':
                turn = 'O'
            else:
                turn = 'X'
        else:
            game_over = True
    game_list.append((board[:], num))
    if status == 'TIE':
        # print status
        reward = 0
    elif status == 'X':
        # print 'Winner is ' + status
        reward = 1
    else:
        # print 'Winner is ' + status
        reward = -1

    return reward, game_list, turn


def play_with_human(board, human='O'):
    turn = 'X'
    game_over = False
    status = ''
    while game_over is False:
        if turn != human:
            num = get_best_move(board, turn, True)
        else:
            draw(board)
            n = input('Where do you want to play?')
            num = n - 1
        board[num] = turn
        status = check_game_over(board)
        if status == 'Not over':
            if turn == 'X':
                turn = 'O'
            else:
                turn = 'X'
        else:
            game_over = True
    draw(board)
    if status == 'TIE':
        print status
    elif status != human:
        print 'You lost'
    else:
        print 'You won'


if __name__ == "__main__":

    for i in range(no_of_games):
        board = new_game()
        quiet = True
        # if (i + 1) % (no_of_games / 10) == 0:
        # print i
        # print 'X wins: ' + str(X_wins) + ' O wins: ' + str(O_wins) + \
        # ' Draws: ' + str(draws)
        # variables to track performance
        # X_wins = 0
        # O_wins = 0
        # draws = 0
        # print '\n_____________________________________________________\n'
        # quiet = False
        reward, game_list, turn = simulate_game(board, quiet)
        # if reward == 1:
        #     X_wins += 1
        # elif reward == -1:
        #     O_wins += 1
        # else:
        #     draws += 1
        game_list.reverse()
        for i in range(9):
            Q[(tuple(game_list[0][0]), i)] = reward
        for i in range(1, len(game_list)):
            if turn == 'X':
                turn = 'O'
            else:
                turn = 'X'
            q_sa = get_Q(game_list[i][0], game_list[i][1])
            best_move = get_best_move(game_list[i][0], turn)
            new_q_sa = q_sa + get_alpha() * (reward +
                                             gamma *
                                             get_Q(game_list[i - 1]
                                                   [0], best_move) - q_sa
                                             )
            Q[(tuple(game_list[i][0]), game_list[i][1])] = new_q_sa
    # while True:
    board = new_game()
    play_with_human(board)
    print 'Thanks for playing!'
    # print reward, turn
    # pprint(game_list)
