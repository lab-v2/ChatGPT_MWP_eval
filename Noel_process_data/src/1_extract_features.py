#     __          __       _    _____ 
#    / /   ____ _/ /_     | |  / /__ \
#   / /   / __ `/ __ \    | | / /__/ /
#  / /___/ /_/ / /_/ /    | |/ // __/ 
# /_____/\__,_/_.___/     |___//____/ 
#   At Arizona State University

import os
import pandas as pandas
from dotenv import load_dotenv

load_dotenv()

PROBLEMS_INPUT_FILE_PATH = os.getenv('PROBLEMS_INPUT_FILE_PATH')
OUTPUT_FILE_PATH = os.getenv('EXTRACT_FEATURES_OUTPUT_FILE_PATH')

COLUMNS_WITH_EQUATIONS = os.getenv('COLUMNS_WITH_EQUATIONS')

NUM_OF_SYMBOL_MAX_VALUE = int(os.getenv('NUM_OF_SYMBOL_MAX_VALUE'))

# Some string consts so the column names can be modified a bit easier
NUM_OF_ADDITION_SUFFIX = "_num_of_addition"
NUM_OF_SUBTRACTION_SUFFIX = "_num_of_subtraction"
NUM_OF_ADDITION_AND_SUBTRACTION_SUFFIX = "_num_of_addition_and_subtraction"

NUM_OF_MULTIPLICATION_SUFFIX = "_num_of_multiplication"
NUM_OF_DIVISION_SUFFIX = "_num_of_division"
NUM_OF_MULTIPLICATION_AND_DIVISION_SUFFIX = "_num_of_multiplication_and_division"

NUM_OF_EQUATIONS_SUFFIX = "_num_of_equations"

# Calculates the number of '+' symbols in [equations]
# INPUT: [equations] should be an array of strings which represent equations
# INPUT: [symbol] should be a character.
def num_of_symbol(equations, symbol):
    count = 0
    for equation in equations:
        count += equation.count(symbol)
    return count

# Calculates the number of '+' symbols in [equations]
# INPUT: [equations] should be an array of strings which represent equations
def num_of_addition(equations):
    return num_of_symbol(equations, '+')

# Calculates the number of '-' symbols in [equations]
# INPUT: [equations] should be an array of strings which represent equations
def num_of_subtraction(equations):
    return num_of_symbol(equations, '-')

# Calculates the number of '*' symbols in [equations]
# INPUT: [equations] should be an array of strings which represent equations
def num_of_multiplication(equations):
    return num_of_symbol(equations, '*')

# Calculates the number of '/' symbols in [equations]
# INPUT: [equations] should be an array of strings which represent equations
def num_of_division(equations):
    return num_of_symbol(equations, '/')

# Calculates the number of equations in [equations]
# INPUT: [equations] should be an array of strings which represent equations
def num_of_equations(equations):
    return len(equations)

# Generates greater than or equal binary columns of a mathematical feature.
# Once we calculate the number (amount) of each mathematical feature, 
# we generate columns of 0s and 1s representing whether the equations have greater than or equal
# number of a particular feature
def generate_geq_columns(data, column, max_value):
    for value in range(1, max_value + 1):
        data[column + "_geq_" + str(value)] = generate_geq_column(data, column, value)
    return data

# Generates a column of 0s and 1s which represents whether or not the rows in data[column] are >= value. 1 means True and 0 means False
def generate_geq_column(data, column, value):
    return data.apply(lambda row : 1 if row[column] >= value else 0, axis=1)



# Load data from files
data = pandas.read_json(PROBLEMS_INPUT_FILE_PATH)

# Calculate the number (amount) of each particular mathematical features
# We calculate the number of additions (+), subtractions (-), multiplications (*), divisions (*) and equations.
columns_with_equations = COLUMNS_WITH_EQUATIONS.split(',')
for column in columns_with_equations:
    data[column + NUM_OF_ADDITION_SUFFIX] = data.apply(lambda row : num_of_addition(row[column]), axis=1)
    data[column + NUM_OF_SUBTRACTION_SUFFIX] = data.apply(lambda row : num_of_subtraction(row[column]), axis=1)
    data[column + NUM_OF_MULTIPLICATION_SUFFIX] = data.apply(lambda row : num_of_multiplication(row[column]), axis=1)
    data[column + NUM_OF_DIVISION_SUFFIX] = data.apply(lambda row : num_of_division(row[column]), axis=1)
    data[column + NUM_OF_EQUATIONS_SUFFIX] = data.apply(lambda row : num_of_equations(row[column]), axis=1)
    
    data[column + NUM_OF_ADDITION_AND_SUBTRACTION_SUFFIX] = data[column + NUM_OF_ADDITION_SUFFIX] + data[column + NUM_OF_SUBTRACTION_SUFFIX]
    data[column + NUM_OF_MULTIPLICATION_AND_DIVISION_SUFFIX] = data[column + NUM_OF_MULTIPLICATION_SUFFIX] + data[column + NUM_OF_DIVISION_SUFFIX]

    # data = generate_geq_columns(data, column + NUM_OF_ADDITION_SUFFIX, NUM_OF_SYMBOL_MAX_VALUE)
    # data = generate_geq_columns(data, column + NUM_OF_SUBTRACTION_SUFFIX, NUM_OF_SYMBOL_MAX_VALUE)
    data = generate_geq_columns(data, column + NUM_OF_ADDITION_AND_SUBTRACTION_SUFFIX, NUM_OF_SYMBOL_MAX_VALUE)

    # data = generate_geq_columns(data, column + NUM_OF_MULTIPLICATION_SUFFIX, NUM_OF_SYMBOL_MAX_VALUE)
    # data = generate_geq_columns(data, column + NUM_OF_DIVISION_SUFFIX, NUM_OF_SYMBOL_MAX_VALUE)
    data = generate_geq_columns(data, column + NUM_OF_MULTIPLICATION_AND_DIVISION_SUFFIX, NUM_OF_SYMBOL_MAX_VALUE)

    data = generate_geq_columns(data, column + NUM_OF_EQUATIONS_SUFFIX, NUM_OF_SYMBOL_MAX_VALUE)

# Save data to output file
data.to_json(OUTPUT_FILE_PATH, orient='records')