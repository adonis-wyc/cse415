'''heyingge_Find_the_Number.py
by Freddie He

Assignment 2, in CSE 415, Winter 2018.

This file contains my problem formulation for the problem of
finding the secret number.
'''

# <METADATA>
PROBLEM_NAME = "Find_the_Number"
PROBLEM_VERSION = "1.0"
# </METADATA>

# <COMMON_DATA>
GUESS_NUM = 2  # Use default, but override if new value supplied
MAX_NUMBER = 10
# by the user on the command line.
try:
    import sys

    arg2 = sys.argv[2]  # takes the 2nd argument to be the secret number
    GUESS_NUM = int(arg2)
    arg3 = sys.argv[3]  # takes the 2nd argument to be the range
    MAX_NUMBER = int(arg3)
    print("A new secret number was successfully read in from the command"
          " line. A new maximum number (range limit) was successfully"
          " read in from the command line.")
except:
    print("Using default secret number: " + str(GUESS_NUM)
          + "and default range" + str(MAX_NUMBER))
    print(" (To use a specific number, enter it on the command line, e.g.,")
    print("python3 ../Int_Solv_Client.py heyingge_Find_the_Number 3 10)")


# </COMMON_DATA>

# <COMMON_CODE>
class State:
    def __init__(self, d):
        self.d = d

    def __eq__(self, s2):
        return self.d['possibilities'] == s2.d['possibilities']\
            and self.d['phase'] == s2.d['phase']

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        return "question_phase: " + str(self.d['phase']) + \
               "\nlast_m: " + str(self.d['last_m']) + \
               "\npossibilities: " + str(self.d['possibilities'])

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        news.d['possibilities'] = self.d['possibilities'][:]
        news.d['phase'] = self.d['phase']
        news.d['last_m'] = self.d['last_m']
        return news

    def can_move(self, p, phase):
        '''Tests whether it's legal to do the calculation of (n - k) % m.'''
        try:
            if self.d['phase'] == 0:
                # the value of m must be a prime smaller than the max number
                return isPrimeUnderMax(p, MAX_NUMBER) and phase == 0
            else:
                # the value of k must be smaller than m and greater than 0
                return 0 <= p < self.d['last_m'] and phase == 1
        except Exception as e:
            print(e)

    def move(self, k):
        '''Assuming it's legal to make the move, this computes
           the new state resulting from (k, m) which is chosen by user.'''
        news = self.copy()  # start with a deep copy.
        if self.d['phase'] == 1:
            m = self.d['last_m']
            if (GUESS_NUM - k) % m == 0:
                for p in self.d['possibilities'][:]:
                    if (p - k) % m != 0:
                        news.d['possibilities'].remove(p)
            else:
                for p in self.d['possibilities'][:]:
                    if (p - k) % m == 0:
                        news.d['possibilities'].remove(p)
            news.d['phase'] = 0  # set phase to 0
        else:
            news.d['last_m'] = k  # update last_m
            news.d['phase'] = 1  # set phase to 1
        return news  # return new state


def goal_test(s):
    '''If there is only one possible answer left, then s is a goal state.'''
    return len(s.d['possibilities']) == 1 and \
           s.d['possibilities'][0] == GUESS_NUM


def goal_message(s):
    return "You figure out the secret number!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>

# <INITIAL_STATE>
INITIAL_DICT = {'possibilities': list(range(MAX_NUMBER + 1)),
                'phase': 0, 'last_m': None}
CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT)
# </INITIAL_STATE>

# <OPERATORS>
possibilities = list(range(MAX_NUMBER + 1))
OPERATORS = [Operator("Is N divisible by " + str(p) + " after ...",
                      lambda s, p1=p: s.can_move(p1, 0),
                      # The default value construct is needed
                      # here to capture the value of p separately
                      # in each iteration of the list comp. iteration.
                      lambda s, p1=p: s.move(p1))
             for p in possibilities[:]] + \
            [Operator("... subtracting " + str(p) + " ?",
                      lambda s, p1=p: s.can_move(p1, 1),
                      # The default value construct is needed
                      # here to capture the value of p separately
                      # in each iteration of the list comp. iteration.
                      lambda s, p1=p: s.move(p1))
             for p in possibilities[:]]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)


# </GOAL_MESSAGE_FUNCTION>

# this function returns whether m is a prime number within [0, max]
def isPrimeUnderMax(m, max):
    if m < 2 or m > max:
        return False
    for i in range(2, m):
        if m % i == 0:
            return False
    return True
