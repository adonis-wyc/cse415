# Freddie He
#1560733
#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Rubik Cube 2x2"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Y. He, S. Wang']
PROBLEM_CREATION_DATE = "3-March-2018"
PROBLEM_DESC=\
'''This formulation of the Rubik Cube Problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
'''
#</METADATA>
import random
# <COMMON_CODE>
class State:
    def __init__(self, d):
        self.d = d

    def __eq__(self, s2):
        for face in ['A', 'B', 'C', 'D', 'E', 'F']:
            if self.d[face] != s2.d[face]: return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        txt = "\n        " + self.d['D'][2] + "  " + self.d['D'][3] + "\n" + \
              "        " + self.d['D'][0] + "  " + self.d['D'][1] + "\n"

        txt += "\n" + self.d['C'][2] + "  " + self.d['C'][0] + "    " + \
               self.d['A'][0] + "  " + self.d['A'][1] + "    " + \
               self.d['E'][0] + "  " + self.d['E'][2] + "\n" + \
               self.d['C'][3] + "  " + self.d['C'][1] + "    " + \
               self.d['A'][2] + "  " + self.d['A'][3] + "    " + \
               self.d['E'][1] + "  " + self.d['E'][3] + "\n"

        txt += "\n        " + self.d['B'][0] + "  " + self.d['B'][1] + "  \n" + \
               "        " + self.d['B'][2] + "  " + self.d['B'][3] + "  \n"

        txt += "\n        " + self.d['F'][2] + "  " + self.d['F'][3] + "  \n" + \
               "        " + self.d['F'][0] + "  " + self.d['F'][1] + "  \n"
        return txt

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        for face in ['A', 'B', 'C', 'D', 'E', 'F']:
            news.d[face] = self.d[face][:]
        return news

    def can_move(self, action):
        '''Tests whether it's legal to make a rotation.'''
        try:
            return action in list(range(0,6))
        except (Exception) as e:
            print(e)

    def move(self, action):
        '''Assuming it's legal to make the move, this computes
           the new state resulting from rotating the cube.'''
        news = self.copy()  # start with a deep copy.
        if action == 0:
            a = self.d['A'][::-1]
            b = self.d['D'][1:2] + self.d['D'][0:1] + self.d['B'][2:4]
            c = self.d['E'][1:2] + self.d['E'][0:1] + self.d['C'][2:4]
            d = self.d['B'][1:2] + self.d['B'][0:1] + self.d['D'][2:4]
            e = self.d['C'][1:2] + self.d['C'][0:1] + self.d['E'][2:4]
            f = self.d['F']
        if action == 1:
            a = self.d['A']
            b = self.d['B'][0:2] + self.d['D'][3:4] + self.d['D'][2:3]
            c = self.d['C'][0:2] + self.d['E'][3:4] + self.d['E'][2:3]
            d = self.d['D'][0:2] + self.d['B'][3:4] + self.d['B'][2:3]
            e = self.d['E'][0:2] + self.d['C'][3:4] + self.d['C'][2:3]
            f = self.d['F'][::-1]
        if action == 2:
            a = self.d['F'][2:3] + self.d['A'][1:2] + self.d['F'][0:1] + self.d['A'][3:4]
            b = self.d['D'][2:3] + self.d['B'][1:2] + self.d['D'][0:1] + self.d['B'][3:4]
            c = self.d['C'][::-1]
            d = self.d['B'][2:3] + self.d['D'][1:2] + self.d['B'][0:1] + self.d['D'][3:4]
            e = self.d['E']
            f = self.d['A'][2:3] + self.d['F'][1:2] + self.d['A'][0:1] + self.d['F'][3:4]
        if action == 3:
            a = self.d['A'][0:1] + self.d['F'][3:4] + self.d['A'][2:3] + self.d['F'][1:2]
            b = self.d['B'][0:1] + self.d['D'][3:4] + self.d['B'][2:3] + self.d['D'][1:2]
            c = self.d['C']
            d = self.d['D'][0:1] + self.d['B'][3:4] + self.d['D'][2:3] + self.d['B'][1:2]
            e = self.d['E'][::-1]
            f = self.d['F'][0:1] + self.d['A'][3:4] + self.d['F'][2:3] + self.d['A'][1:2]
        if action == 4:
            a = self.d['A'][0:2] + self.d['F'][3:4] + self.d['F'][2:3]
            b = self.d['B'][::-1]
            c = self.d['C'][0:1] + self.d['E'][3:4] + self.d['C'][2:3] + self.d['E'][1:2]
            d = self.d['D']
            e = self.d['E'][0:1] + self.d['C'][3:4] + self.d['E'][2:3] + self.d['C'][1:2]
            f = self.d['F'][0:2] + self.d['A'][3:4] + self.d['A'][2:3]
        if action == 5:
            a = self.d['F'][1:2] + self.d['F'][0:1] + self.d['A'][2:4]
            b = self.d['B']
            c = self.d['E'][2:3] + self.d['C'][1:2] + self.d['E'][0:1] + self.d['C'][3:4]
            d = self.d['D'][::-1]
            e = self.d['C'][2:3] + self.d['E'][1:2] + self.d['C'][0:1] + self.d['E'][3:4]
            f = self.d['A'][1:2] + self.d['A'][0:1] + self.d['F'][2:4]
        news.d['A'] = a
        news.d['B'] = b
        news.d['C'] = c
        news.d['D'] = d
        news.d['E'] = e
        news.d['F'] = f
        return news  # return new state


def make_goal_state():
    global GOAL_STATE, N_disks
    GOAL_STATE = State({'A': ['R'] * 4,
               'B': ['O'] * 4,
               'C': ['G'] * 4,
               'D': ['P'] * 4,
               'E': ['B'] * 4,
               'F': ['W'] * 4})
    # print("GOAL_STATE="+str(GOAL_STATE))
make_goal_state()


def goal_test(s):
    '''Made stricter for use in Reinforcement Learning app.
    If the third peg has all N_disk disks on it, then s is a goal state.'''
    global GOAL_STATE
    for face in ['A', 'B', 'C', 'D', 'E', 'F']:
        if len(s.d[face]) < 4:
            return False
        for i in range(0,3):
            if s.d[face][i] != s.d[face][i+1]:
                return False
    return True


def goal_message(s):
    return "The Rubik Cube Is Solved!"


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
#  INITIAL_DICT = {'peg1': list(range(N_disks,0,-1)), 'peg2':[], 'peg3':[] }
#  CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT)
# DUMMY_STATE =  {'peg1':[], 'peg2':[], 'peg3':[] }
def CREATE_INITIAL_STATE():
    s = State({'A': ['R'] * 4,
               'B': ['O'] * 4,
               'C': ['G'] * 4,
               'D': ['P'] * 4,
               'E': ['B'] * 4,
               'F': ['W'] * 4})
    for i in range (0,50):
        action = random.randint(0,5)
        s = s.move(action)
    return s

# </INITIAL_STATE>

# <OPERATORS>
OPERATORS = [Operator("Rotate " + p + " part for 180 degrees",
                      lambda s, q1=q, : s.can_move(q1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, q1=q: s.move(q1))
             for (p, q) in [("upper", 0), ("lower", 1), ("left", 2),
                            ("right", 3), ("front", 4), ("back", 5)]]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>
