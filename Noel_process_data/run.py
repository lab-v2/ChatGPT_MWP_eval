#     __          __       _    _____ 
#    / /   ____ _/ /_     | |  / /__ \
#   / /   / __ `/ __ \    | | / /__/ /
#  / /___/ /_/ / /_/ /    | |/ // __/ 
# /_____/\__,_/_.___/     |___//____/ 
#   At Arizona State University

import warnings
warnings.filterwarnings("ignore")
import os

for dir in os.listdir('config'):
    print(dir, "*********************")
    CAUSALITY_OUTPUT_FILE_PATH = 'output/3_causality_' + dir[:-3] + '.json'
    SPLIT_DATASET_FILE_PATH = 'output/5_split_dataset_' + dir[:-3] + '.json'
    IS_CORRECT_VALID_PY_FILE = 'config/' + dir
    CLASSIFICATION_STRATIFIED_FILE_PATH = 'output/6_classification_stratified_' + dir[:-3] + '.pdf'
    exec(open("src/execute.py").read())

input("Press Enter to continue...")