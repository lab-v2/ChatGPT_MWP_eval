COLUMN_TO_CHECK = "result"

# Various constants with text defined by Abhinav
# These constants are here so that, if Abhinav changes his mind on what the strings will look like, 
# the information is centralized
ALL_ANSWERS = "has all the answers"
ALL_ANSWERS_ROUNDED = "has all the answers when rounded"
SOME_SOLUTION = "has one or more of the answers, but not all of them"
SOME_SOLUTION_ROUNDED = "has one or more of the answers when rounded, but not all of them"
NO_SOLUTION = "says no solution"
INVALID = "invalid"

CORRECT_SOLUTIONS = [ALL_ANSWERS, ALL_ANSWERS_ROUNDED]

# is_correct --
# Checks to see if a row is "correct". We define what's "correct" here. Currently, wrong is right
# INPUT: [row] is a dict
def is_correct(row):
    for correct_solution in CORRECT_SOLUTIONS:
        if row[COLUMN_TO_CHECK] == correct_solution: return 0
    return 1

# is_valid --
# Checks to see if a row is "valid". We define what's "valid" here
# INPUT: [row] is a dict
def is_valid(row):
    return 1
