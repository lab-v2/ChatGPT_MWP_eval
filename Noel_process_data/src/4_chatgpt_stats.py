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

INPUT_FILE_PATH = os.getenv('CHATGPT_INPUT_FILE_PATH')
OUTPUT_FILE_PATH = os.getenv('CHATGPT_STATS_OUTPUT_FILE_PATH')

data = pandas.read_json(INPUT_FILE_PATH)

count = data['result'].value_counts().rename_axis('value').reset_index(name='count')

count.to_json(OUTPUT_FILE_PATH, orient='records')