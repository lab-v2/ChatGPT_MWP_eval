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

PROBLEMS_INPUT_FILE_PATH = os.getenv('EXTRACT_FEATURES_OUTPUT_FILE_PATH')
CHATGPT_INPUT_FILE_PATH = os.getenv('CHATGPT_INPUT_FILE_PATH')

OUTPUT_FILE_PATH = os.getenv('COMBINE_OUTPUT_FILE_PATH')

QUESTION_NO = 'question_No'

# These are just constants which define what sort of values we're looking for and the column which indicates whether a row is valid
CORRECT_COLUMN = os.getenv('CORRECT_COLUMN')
VALID_COLUMN = os.getenv('VALID_COLUMN')

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

# Injecting code here using exec. It's just so that it's easier to modify how we define whether a row is correct and valid
# We won't have to search thrpugh the entire code base to change something and it's easier to generate multiple files at once without
# making the code total spaghetti
exec(open(IS_CORRECT_VALID_PY_FILE).read())

problems = pandas.read_json(PROBLEMS_INPUT_FILE_PATH)
chatgpt = pandas.read_json(CHATGPT_INPUT_FILE_PATH)


for column in chatgpt.columns:
    if column == QUESTION_NO:
        continue

    problems.loc[chatgpt[QUESTION_NO], column] = chatgpt[column]

problems[CORRECT_COLUMN] = problems.apply(lambda row : is_correct(row),axis=1)
problems[VALID_COLUMN] = problems.apply(lambda row : is_valid(row),axis=1)

problems.to_json(OUTPUT_FILE_PATH, orient='records')