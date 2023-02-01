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

INPUT_FILE_PATH = os.getenv('COMBINE_OUTPUT_FILE_PATH')
OUTPUT_FILE_PATH = CAUSALITY_OUTPUT_FILE_PATH

# These are just constants which define what sort of values we're looking for and the column which indicates whether a row is valid
CORRECT_COLUMN = os.getenv('CORRECT_COLUMN')
VALID_COLUMN = os.getenv('VALID_COLUMN')

MAX_NAME_DIFFERENCE = 3

# negation -- 
# OUTPUT: returns a column of 0s and 1s of the negation of [column]. 1s are flipped to 0 and vice versa
# INPUT: [column] should be a column of 0s and 1s
def negation(column):
    return 1 - column

# conjunction -- 
# output: returns a column of 0s and 1s of the conjunction between [column_1] and [column_2].
# INPUT: [column_1] and [column_2] should be columns of 0s and 1s
def conjunction(column_1, column_2):
    return column_1 * column_2

# disjunction -- 
# OUTPUT: returns a column of 0s and 1s of the disjunction between [column_1] and [column_2].
# INPUT: [column_1] and [column_2] should be columns of 0s and 1s
def disjunction(column_1, column_2):
    return column_1 | column_2

# conditional_probability -- 
# OUTPUT: returns a number which represents the conditional probability p(occurence | condition)
# INPUT: [occurence_column] and [condition_column] should be columns of 0s and 1s
def conditional_probability(occurence_column, condition_column):
    return conjunction(occurence_column, condition_column).sum() / condition_column.sum()

# prior -- 
# OUTPUT: returns a number which represents the prior
# INPUT: [data] should be a Pandas dataframe with the columns [CORRECT_COLUMN] and [VALID_COLUMN].
# TODO : Possible optimizations can be made where we cache the result instead of calling this expensive operation again and again
def prior(data):
    return conditional_probability(data[CORRECT_COLUMN], data[VALID_COLUMN])

# is_prima_facie -- 
# OUTPUT: returns a boolean which determines whether the column indicated by [column_name] is a prima facie
# INPUT: [data] should be a Pandas dataframe with the columns [CORRECT_COLUMN] and [VALID_COLUMN].
# INPUT: [column_name] should be a valid column in [data]
# INPUT: The [CORRECT_COLUMN] and [VALID_COLUMN] columns should be columns of 0s and 1s 
def is_prima_facie(data, column_name):
    return conditional_probability(data[CORRECT_COLUMN], data[column_name]) > prior(data)

# is_cooccur -- 
# OUTPUT: returns a boolean based on if there is at least one row where both [column_1] and [column_2] is equal to 1
# INPUT: [column_1] and [column_2] should both be columns of 0s and 1s
def is_cooccur(column_1, column_2):
    return conjunction(column_1, column_2).sum() > 0

# same_category -- 
# OUTPUT: Returns a boolean signifying whether the [column_name_1] and [column_name_2] are different by [MAX_NAME_DIFFERENCE]
#         If the two words are not different by [MAX_NAME_DIFFERENCE], they are in the same category so it returns true
def is_same_category(column_name_1, column_name_2):
    count = 0
    shortest = min(len(column_name_1), len(column_name_2))
    for i in range(0, shortest):
        if column_name_1[i] == column_name_2[i]:
            count = count + 1
    return count < MAX_NAME_DIFFERENCE

# rel -- 
# OUTPUT: returns a list of the names of other columns which cooccur with [column_name] and are prima facie
# INPUT: [data] should be a Pandas dataframe with the columns [CORRECT_COLUMN] and [VALID_COLUMN].
# INPUT: [column_name] should be a valid column in [data]
# INPUT: The [CORRECT_COLUMN] and [VALID_COLUMN] columns should be columns of 0s and 1s 
def rel(data, column_name):
    # If it is not a prima facie cause, we don't bother to find its rel
    if not is_prima_facie(data,column_name): return[]
    
    name_list = []
    for potential_cause in data.columns:
        # Make sure we are not including the [CORRECT_COLUMN] and [VALID_COLUMN] as part of rel
        if potential_cause == CORRECT_COLUMN or potential_cause == VALID_COLUMN:
            continue

        if is_same_category(potential_cause, column_name): continue

        if is_cooccur(data[column_name], data[potential_cause]) and is_prima_facie(data, potential_cause):
            name_list.append(potential_cause)
    return name_list

# calculate_causality -- 
# OUTPUT: returns a number which represents the causality value of the column indicated by [column_name]
# INPUT: [data] should be a Pandas dataframe with the columns [CORRECT_COLUMN].
# INPUT: [column_name] should be a valid column in [data]
# INPUT: The [CORRECT_COLUMN] and [VALID_COLUMN] columns should be columns of 0s and 1s 
def calculate_causality(data, column_name):

    # If it's not a prima facie cause, we don't bother to calculate its causality value
    if not is_prima_facie(data, column_name):
        return "n/a"

    relateds = rel(data, column_name)

    total_probability = 0
    for related in relateds:
        conj = conjunction(data[column_name], data[related])
        negj = conjunction(negation(data[column_name]), data[related])

        conj = conditional_probability(data[CORRECT_COLUMN], conj)
        negj = conditional_probability(data[CORRECT_COLUMN], negj)

        total_probability += (conj - negj)

    if (len(relateds) > 0): return total_probability / len(relateds)
    else: return 0

# is_binary_column --
# Checks to see if a column is a column of 1s and 0s
# INPUT: [data] is a dataframe
# INPUT: [column_name] should be the name of a valid column in [data]
def is_binary_column(data, column_name):
    return data.apply(lambda row : 0 if (isinstance(row[column_name], int) and (row[column_name] <= 1)) else 1, axis=1).sum() <= 0

# remove_non_binary_columns --
# Removes all columns that are not 0s or 1s in the dataset
# INPUT: [data] is a dataframe
def remove_non_binary_columns(data):
    non_binary = []
    for i in data.columns:
        if not is_binary_column(data, i):
            non_binary.append(i)

    return data.drop(columns=non_binary)

# generate_row --
# TODO: This is kind of a terrible name but I can't really think of anything more descriptive. If anyone has any ideas, feel free to modify it
# It basically creates a row, which is actually a data frame with all the data that is needed
# OUTPUT: It outputs a row with all the required values
# INPUT: [data] should be a dataframe
# INPUT: [column_name] should be a string representing a valid column in [data]
def generate_row(data, column_name):
    toReturn = pandas.DataFrame({
        "name": [column_name], 
        "support": conjunction(data[column_name], data[VALID_COLUMN]).sum(),
        "causality": calculate_causality(data, column_name),
        "rel": ','.join(rel(data, column_name)),
        "conditional_probability":[conditional_probability(data[CORRECT_COLUMN], data[column_name])], 
        "prior": prior(data),
        "conditional - prior": conditional_probability(data[CORRECT_COLUMN], data[column_name]) - prior(data)
    })
    return toReturn

# Load data
data = pandas.read_json(INPUT_FILE_PATH)

# Then remove all the non binary columns
data = remove_non_binary_columns(data)

# TODO: I'm not sure if there's another way to do this, so feel free to make modifications
# Generate a dud data frame with a single so we can append to it.
to_save = generate_row(data, VALID_COLUMN)
for column in data.columns:
    if column == VALID_COLUMN or column == CORRECT_COLUMN:
        continue

    to_save = to_save.append(generate_row(data, column))

# Remove the dud first row
to_save = to_save[1:]

to_save.to_json(OUTPUT_FILE_PATH, orient='records')