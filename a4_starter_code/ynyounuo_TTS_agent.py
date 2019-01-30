"""ynyounuo_TTS.py
by Chao Ma

Assignment 4, in CSE 415, Winter 2018.

This file contains Toro-Tile Straight Game play agent
"""
from TTS_State import TTS_State
from random import choice, getrandbits
import time
import copy

USE_CUSTOM_STATIC_EVAL_FUNCTION = True
mRows = 4
nColumns = 4
K = 0
my_side = 'W'
op_side = 'B'
reach_limit = False
zobristnum = []
TIMED = True
N_STATES_EXPANDED = 0
N_STATIC_EVALS_PERFORMED = 0
MAX_DEPTH_REACHED = 0
TIMED = True
USE_ITERATIVE_DEEPENING = True

neg_remark = [
    "Failure is only a temporary change in direction to set you straight for "
    "your next success. --Denis Waitley",
    "We don't develop courage by being happy every day. We develop it by "
    "surviving difficult times and challenging adversity. --Barbara De "
    "Angelis",
    "The eagle has no fear of adversity. We need to be like the eagle and "
    "have a fearless spirit of a conqueror! --Joyce Meyer",
    "Sometimes by losing a battle you find a new way to win the war. "
    "--Donald Trump",
    "I love to win, but I love to lose almost as much. I love the thrill of "
    "victory, and I also love the challenge of defeat. -- Lou Gehrig",
    "You can't win unless you learn how to lose. -- Kareem Abdul-Jabbar",
    "Really? No way! Really? No way! Really? No way! Really? No way! — "
    "Clarissa"]
normal_remark = [
    "My dad always taught me never to give up in my mind. You can never "
    "really beat me. --Chad le Clos",
    "I don't think I'm that intelligent. I think I'm semi-intelligent. -- "
    "Gail Porter",
    "You know nothing, John Snow. -- Ygritte",
    "Seize Your Moment. -- Ernesto de la Cruz",
    "Life was like a box of chocolates, you never know what you're gonna get. "
    "--Forest Gump's Mother"]
win_remark = ["I always played to win. --Hansie Cronje",
              "Hard work always wins in the end. --Lucas Till",
              "You were born to win, but to be a winner, you must plan to "
              "win, prepare to win, and expect to win. --Zig Ziglar",
              "Mada mada dane(まだまだだね) --Ryoma Echizen (越前 リョーマ)"]
near_win = [
    "All genius is a conquering of chaos and mystery. -- Otto Weininger",
    "Welcome to the real world.It sucks.You're gonna love it! -- Monica",
    "Cheer up, Child. It'll turn out alright in the end. You'll see...—Mrs. "
    "Potts"]


class MY_TTS_State(TTS_State):
    global my_side, op_side, nColumns, mRows

    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval(self):
        cnt_m = 0
        cnt_o = 0
        for i in range(mRows):
            for j in range(nColumns):
                temp_m = 0
                temp_o = 0
                legible_m = True
                legible_o = True
                for k in range(K):
                    row = i + k
                    if row >= mRows:
                        row = row - mRows
                    if self.board[row][j] == my_side:
                        temp_m += 1
                    elif not self.board[row][j] == ' ':
                        legible_m = False
                    if self.board[row][j] == op_side:
                        temp_o += 1
                    elif not self.board[row][j] == ' ':
                        legible_o = False
                if temp_o == 2 and legible_o:
                    cnt_o += 1
                elif temp_m == 2 and legible_m:
                    cnt_m += 1

                temp_m = 0
                temp_o = 0
                legible_m = True
                legible_o = True
                for k in range(K):
                    col = i + k
                    if col >= nColumns:
                        col = col - nColumns
                    if self.board[i][col] == my_side:
                        temp_m += 1
                    elif not self.board[i][col] == ' ':
                        legible_m = False
                    if self.board[i][col] == op_side:
                        temp_o += 1
                    elif self.board[i][col] == ' ':
                        legible_o = False
                if temp_o == 2 and legible_o:
                    cnt_o += 1
                elif temp_m == 2 and legible_m:
                    cnt_m += 1

                temp_m = 0
                temp_o = 0
                legible_m = True
                legible_o = True
                for k in range(K):
                    row = i + k
                    if row >= mRows:
                        row = row - mRows
                    col = i + k
                    if col >= nColumns:
                        col = col - nColumns
                    if self.board[row][col] == my_side:
                        temp_m += 1
                    elif self.board[row][col] == ' ':
                        legible_m = False
                    if self.board[row][col] == op_side:
                        temp_o += 1
                    elif self.board[row][col] == ' ':
                        legible_o = False
                if temp_o == 2 and legible_o:
                    cnt_o += 1
                elif temp_m == 2 and legible_m:
                    cnt_m += 1

                temp_m = 0
                temp_o = 0
                legible_m = True
                legible_o = True
                for k in range(K):
                    row = i + k
                    if row >= mRows:
                        row = row - mRows
                    col = i - k
                    if col < 0:
                        col = col + nColumns
                    if self.board[row][col] == my_side:
                        temp_m += 1
                    elif self.board[row][col] == ' ':
                        legible_m = False
                    if self.board[row][col] == op_side:
                        temp_o += 1
                    elif self.board[row][col] == ' ':
                        legible_o = False
                if temp_o == 2 and legible_o:
                    cnt_o += 1
                elif temp_m == 2 and legible_m:
                    cnt_m += 1
        return cnt_m - cnt_o

    def custom_static_eval(self):
        score = 0
        score_board = [10 ** i for i in range(K)]
        my_distribution = [0] * K
        op_distribution = [0] * K
        for i in range(mRows):
            for j in range(nColumns):
                cnt_w = 0
                cnt_b = 0
                legible_w = True
                legible_b = True
                for k in range(K):
                    if self.board[(i + k) % mRows][j] == my_side:
                        cnt_w += 1
                    elif not self.board[(i + k) % mRows][j] == ' ':
                        legible_w = False
                    if self.board[(i + k) % mRows][j] == op_side:
                        cnt_b += 1
                    elif not self.board[(i + k) % mRows][j] == ' ':
                        legible_b = False
                if legible_b and cnt_b != 0: op_distribution[cnt_b - 1] += 1
                if legible_w and cnt_w != 0: my_distribution[cnt_w - 1] += 1

                cnt_w = 0
                cnt_b = 0
                legible_w = True
                legible_b = True
                for k in range(K):
                    if self.board[i][(j + k) % nColumns] == my_side:
                        cnt_w += 1
                    elif not self.board[i][(j + k) % nColumns] == ' ':
                        legible_w = False
                    if self.board[i][(j + k) % nColumns] == op_side:
                        cnt_b += 1
                    elif self.board[i][(j + k) % nColumns] == ' ':
                        legible_b = False
                if legible_w and cnt_w != 0: my_distribution[cnt_w - 1] += 1
                if legible_b and cnt_b != 0: op_distribution[cnt_b - 1] += 1

                cnt_w = 0
                cnt_b = 0
                legible_w = True
                legible_b = True
                for k in range(K):
                    if self.board[(i + k) % mRows][
                        (j + k) % nColumns] == my_side:
                        cnt_w += 1
                    elif self.board[(i + k) % mRows][
                        (j + k) % nColumns] == ' ':
                        legible_w = False
                    if self.board[(i + k) % mRows][
                        (j + k) % nColumns] == op_side:
                        cnt_b += 1
                    elif self.board[(i + k) % mRows][
                        (j + k) % nColumns] == ' ':
                        legible_b = False
                if legible_w and cnt_w != 0: my_distribution[cnt_w - 1] += 1
                if legible_b and cnt_b != 0: op_distribution[cnt_b - 1] += 1

                cnt_w = 0
                cnt_b = 0
                legible_w = True
                legible_b = True
                for k in range(K):
                    if self.board[(i + k) % mRows][
                        (j - k) % nColumns] == my_side:
                        cnt_w += 1
                    elif self.board[(i + k) % mRows][
                        (j - k) % nColumns] == ' ':
                        legible_w = False
                    if self.board[(i + k) % mRows][
                        (j - k) % nColumns] == op_side:
                        cnt_b += 1
                    elif self.board[(i + k) % mRows][
                        (j - k) % nColumns] == ' ':
                        legible_b = False
                if legible_w and cnt_w != 0: my_distribution[cnt_w - 1] += 1
                if legible_b and cnt_b != 0: op_distribution[cnt_b - 1] += 1

        for i in range(K):
            score += score_board[i] * (my_distribution[i] - op_distribution[i])
        return score


# noinspection PyUnusedLocal,PyUnusedLocal
def take_turn(current_state, last_utterance, time_limit):
    global reach_limit, neg_remark, normal_remark, win_remark, K, near_win
    reach_limit = False
    score_board = [10 ** i for i in range(K)]
    # Compute the new state for a move.
    # Start by copying the current state.
    start_time = time.time()
    # Fix up whose turn it will be.
    who = current_state.whose_turn

    # Place a new tile
    location = _find_next_vacancy(current_state.board)
    if not location:
        return [[False, current_state], "I don't have any moves!"]

    # Construct a representation of the move that goes from the
    # currentState to the newState.

    # Make up a new remark
    max_ply = 0
    if USE_ITERATIVE_DEEPENING:
        while not reach_limit:
            max_ply += 1
            score, new_state = minimax(current_state, who, max_ply, start_time,
                                       time_limit)
    else:
        score, new_state = minimax(current_state, who, 2)

    if score < 0:
        new_utterance = choice(neg_remark)
    elif score > score_board[-1]:
        new_utterance = choice(win_remark)
    elif score > 2 * score_board[-2]:
        new_utterance = choice(near_win)
    else:
        new_utterance = choice(normal_remark)

    move = [0, 0]
    for i in range(mRows):
        for j in range(nColumns):
            if current_state.board[i][j] != new_state.board[i][j]:
                move = [i, j]

    return [[move, new_state], new_utterance]


def _find_next_vacancy(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == ' ':
                return i, j
    return False


def moniker():
    return "Buddy"  # Return your agent's short nickname here.


def who_am_i():
    return """My name is AlphaTTS, created by Chao Ma."""


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like setting up Zobrist hashing, here.d
    # initial_state = MY_TTS_State(initial_state.board)
    global mRows, nColumns, K, my_side, op_side, zobristnum
    board = initial_state.board
    mRows = len(board)
    nColumns = len(board[0])
    K = k
    my_side = who_i_play
    op_side = other(my_side)
    zobristnum = [[0] * 2 for i in range(mRows * nColumns)]
    for i in range(mRows * nColumns):
        for j in range(2):
            zobristnum[i][j] = getrandbits(32)
    # print(my_side)
    return "OK"


# The following is a skeleton for the function called tryout,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player
# and then it will be able to call tryout using something like this:
# tryout_results = player.tryout(**kwargs)

# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,
# PyUnusedLocal
# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,
# PyUnusedLocal
def tryout(
        game_initial_state=None,
        current_state=None,
        max_ply=2,
        use_iterative_deepening=False,
        use_row_major_move_ordering=False,
        alpha_beta=False,
        timed=False,
        time_limit=1.0,
        use_zobrist=False,
        use_custom_static_eval_function=False):
    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    current_state_dynamic_val = minimax(current_state,
                                        current_state.whose_turn, max_ply,
                                        time.time(), time_limit)
    current_state_static_val = MY_TTS_State(current_state).static_eval()
    n_states_expanded = N_STATES_EXPANDED
    n_static_evals_performed = N_STATIC_EVALS_PERFORMED
    max_depth_reached = MAX_DEPTH_REACHED

    # Those students doing the optional alpha-beta implementation,
    # return the correct number of cutoffs from your agent (either here or
    # below).
    n_ab_cutoffs = 0

    # For those of you doing Zobrist hashing, have your
    # agent determine these values and include the correct
    # values here or overwrite the default values below.
    n_zh_put_operations = 0
    n_zh_get_operations = 0
    n_zh_successful_gets = 0
    n_zh_unsuccessful_gets = 0
    zh_hash_value_of_current_state = 0

    # STUDENTS: You may create the rest of the body of this function here.

    # Prepare to return the results...
    results = [current_state_dynamic_val,
               current_state_static_val,
               n_states_expanded,
               n_static_evals_performed,
               max_depth_reached,
               n_ab_cutoffs,
               n_zh_put_operations,
               n_zh_get_operations,
               n_zh_successful_gets,
               n_zh_unsuccessful_gets,
               zh_hash_value_of_current_state]
    # Actually return the list of all results...
    return results


def successors(state):
    board = state.board
    current_player = state.whose_turn
    successor = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                temp = copy.deepcopy(board)
                temp[i][j] = current_player
                s = MY_TTS_State(temp)
                s.whose_turn = other(current_player)
                successor.append(s)
                # successor.append([temp, other(current_player)])
    return successor


def other(current_player):
    if current_player == 'W':
        return 'B'
    else:
        return 'W'


def minimax(state, whose_move, max_ply):
    state.__class__ = MY_TTS_State
    # MY_TTS_State.static_eval(state)
    if max_ply == 0:
        # Could add or if time_limit here
        # print(state.static_eval())
        return [state.static_eval(), state]
    if whose_move == my_side:
        provisional = -100000
    else:
        provisional = 100000
    # print(whose_move)
    # print(provisional)
    next_state = state

    ss = successors(state)
    for s in ss:
        # print(s.board)
        new_val, temp_state = minimax(s, other(whose_move), max_ply - 1)
        # print(new_val)
        # print(s.board)
        if whose_move == my_side and new_val > provisional \
                or whose_move == op_side and new_val < provisional:
            provisional = new_val
            next_state = s

    return [provisional, next_state]


def minimax(state, whose_move, max_ply, start_time, time_limit):
    # print(my_side)
    # print(state.board)
    global reach_limit
    state.__class__ = MY_TTS_State
    # MY_TTS_State.static_eval(state)
    if max_ply == 0:
        # Could add or if time_limit here
        # print(state.static_eval())
        reach_limit = True
        return [state.static_eval(), state]
    if TIMED and (time.time() - start_time) >= time_limit * 0.7:
        reach_limit = True
        return [state.static_eval(), state]
    if whose_move == my_side:
        provisional = -100000
    else:
        provisional = 100000
    # print(whose_move)
    # print(provisional)
    next_state = state

    ss = successors(state)
    for s in ss:
        # print(s.board)
        new_val, temp_state = minimax(s, other(whose_move), max_ply - 1,
                                      start_time, time_limit)
        # print(new_val)
        # print(s.board)
        if whose_move == my_side and new_val > provisional \
                or whose_move == op_side and new_val < provisional:
            provisional = new_val
            next_state = s

    return [provisional, next_state]
