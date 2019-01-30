'''heyingge_Farmer_Fox_etc.py
by Freddie He

Assignment 2, in CSE 415, Winter 2018.

This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# <METADATA>
PROBLEM_NAME = "Farmer_Fox_etc"
PROBLEM_VERSION = "1.0"


# </METADATA>

# <COMMON_DATA>
# LEFT = False  # False stands for left side of river
# RIGHT = True  # True stands for right side of river.
# </COMMON_DATA>

# <COMMON_CODE>
class State:
    def __init__(self, d):
        self.d = d

    def __eq__(self, s2):
        for p in ['farmer', 'fox', 'chicken', 'grain']:
            if self.d[p] != s2.d[p]: return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        txt = "Left: ["
        left_passengers = 0
        right_passengers = 0
        for passenger in ['farmer', 'fox', 'chicken', 'grain']:
            if not self.d[passenger]:
                txt += passenger + " ,"
                left_passengers += 1
        if left_passengers != 0:
            txt = txt[:-2]
        txt += "] Right: ["
        for passenger in ['farmer', 'fox', 'chicken', 'grain']:
            if self.d[passenger]:
                txt += passenger + " ,"
                right_passengers += 1
        if right_passengers != 0:
            txt = txt[:-2]
        return txt + "]"

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        for passenger in ['farmer', 'fox', 'chicken', 'grain']:
            news.d[passenger] = self.d[passenger]
        return news

    def can_move(self, passenger):
        '''Tests whether it's legal to move a passenger in state s
           from one side of river to the other.'''
        try:
            farmer = self.d['farmer']  # the side where the farmer is
            fox = self.d['fox']  # the side where the fox is
            chicken = self.d['chicken']  # the side where the chicken is
            grain = self.d['grain']  # the side where the grain is
            old_side = farmer
            # whether farmer is on the same side of the passenger
            same_side = not (self.d[passenger] ^ farmer)
            if passenger == 'farmer':
                # neither fox and chicken nor chicken
                # and grain can be on the old side
                return ((fox != old_side or chicken != old_side) and
                        (chicken != old_side or grain != old_side))
            elif passenger == 'fox':
                # chicken and grain cannot be on the old side
                return same_side and (chicken != old_side or grain != old_side)
            elif passenger == 'grain':
                # fox and chicken cannot be on the old side
                return same_side and (fox != old_side or chicken != old_side)
            elif passenger == 'chicken':
                return same_side
        except Exception as e:
            print(e)

    def move(self, passenger):
        '''Assuming it's legal to make the move, this computes
         the new state resulting from moving the boat carrying
         farmer (and one passenger).'''
        news = self.copy()  # start with a deep copy.
        news.d['farmer'] = not self.d['farmer']  # always move farmer
        if passenger == 'fox':
            news.d['fox'] = not self.d['fox']  # move fox
        elif passenger == 'chicken':
            news.d['chicken'] = not self.d['chicken']  # move chicken
        elif passenger == 'grain':
            news.d['grain'] = not self.d['grain']  # move grain
        return news  # return new state


def goal_test(s):
    '''If the farmer, the fox, the chicken and the grain
    are on the right bank, then s is a goal state.'''
    p = s.d
    # all the passengers are on the right side of the river
    return p['farmer'] and p['fox'] and p['chicken'] and p['grain']


def goal_message(s):
    return "Congratulations on successfully guiding the farmer, the fox," \
           " the chicken and the grain across the river!"


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
# all of passengers are at the left side of the river
INITIAL_DICT = {'farmer': False, 'fox': False,
                'chicken': False, 'grain': False}
CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT)

# <OPERATORS>
passenger = [('farmer', 'farmer')] + [(p, 'both farmer and ' + p) for p in
                                      ['fox', 'chicken', 'grain']]
OPERATORS = [Operator("Move " + q + " to the other side of river",
                      lambda s, p1=p: s.can_move(p1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, p1=p: s.move(p1))
             for (p, q) in passenger]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>
