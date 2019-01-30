from random import *
import math


def run_Guess_My_Number():
    n = randint(0, 1000)
    count = 0
    not_quit = True
    incorrect = True
    # this game keeps running if user does not quit
    # and does not guess correctly
    while incorrect and not_quit:
        answer = input('a) Ask\nb) Guess\nc) Quit\n>> ')
        if answer == 'a':  # user chooses to ask a question
            k = 0
            m = 0
            valid = False

            # the program keeps asking the user if
            # s/he doesn't input a valid answer
            while not valid:
                guess = input('If we subtract k from n, is the result '
                              'divisible by m?\nInput your values of k'
                              ' and m int the form (k, m)\n>> ')
                lst = guess.strip(' ()').split(',')

                # this checks the user inputs a valid form of k, m
                if len(lst) == 2:
                    k = lst[0]
                    m = lst[1]
                    valid = (
                            k.strip(' ').isdigit() and
                            m.strip(' ').isdigit() and
                            isPrimeUnder1000(int(m)) and
                            0 <= int(k) <= int(m))

                if not valid:
                    print('Invalid input. Try again...')
            if is_n_minus_k_divisible_by_m(n, int(k), int(m)):
                print('Yes. n-' + k + ' is divisible by ' + m)
            else:
                print('No. n-' + k + ' is not divisible by ' + m)
            count += 1
        elif answer == 'b':  # user chooses to make a guess
            valid = False
            guess_num = 0

            # the program keeps asking the user if
            # s/he doesn't input a valid answer
            while not valid:
                guess_num = input('Input the number you guess\n>> ')
                # this checks the user inputs an integer in range [0,1000]
                if guess_num.strip(' ').isdigit() and \
                        0 <= int(guess_num) <= 1000:
                    valid = True
                else:
                    print('Invalid input. Try again...')
            count += 1
            if guess_num == str(n):  # end the game and show score
                incorrect = False
                print('The guess is correct! Your score: '
                      + str(math.ceil(n / count)))
            else:
                print('Your guess is incorrect')
        elif answer == 'c':  # user chooses to quit the game
            not_quit = False
            print('Your Score: 0')  # end the game and show score
        else:  # user inputs an invalid answer
            print('Invalid input. Try again...')


# this function check if m a prime number less than 1000
# return true if it is; return false otherwise
def isPrimeUnder1000(m):
    if m < 2 or m > 1000:
        return False
    for i in range(2, m):
        if m % i == 0:
            return False
    return True


# this function return the result of n minus k divided by
# return true if divisible; return false otherwise
def is_n_minus_k_divisible_by_m(n, k, m):
    return (n - k) % m == 0


if __name__ == '__main__':
    run_Guess_My_Number()
