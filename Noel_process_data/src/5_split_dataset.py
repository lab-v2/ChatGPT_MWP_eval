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
OUTPUT_FILE_PATH = SPLIT_DATASET_FILE_PATH

# These are just constants which define what sort of values we're looking for and the column which indicates whether a row is valid
CORRECT_COLUMN = os.getenv('CORRECT_COLUMN')
VALID_COLUMN = os.getenv('VALID_COLUMN')

data = pandas.read_json(INPUT_FILE_PATH)

correct_data = data[data[CORRECT_COLUMN] == 1]
wrong_data = data[data[CORRECT_COLUMN] == 0]

min_len = min(len(correct_data.index), len(wrong_data.index))

correct_data = correct_data.head(min_len)
wrong_data = wrong_data.head(min_len)

correct_data = correct_data.append(wrong_data)
correct_data = correct_data.sample(frac = 1)

correct_data.to_json(OUTPUT_FILE_PATH, orient='records')

