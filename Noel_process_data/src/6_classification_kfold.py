#     __          __       _    _____ 
#    / /   ____ _/ /_     | |  / /__ \
#   / /   / __ `/ __ \    | | / /__/ /
#  / /___/ /_/ / /_/ /    | |/ // __/ 
# /_____/\__,_/_.___/     |___//____/ 
#   At Arizona State University

import os
import pandas as pandas
import numpy as numpy
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import precision_score, recall_score

load_dotenv()

TEST_SIZE = 0.2
RANDOM_STATE = 42
INPUT_FILE_PATH = SPLIT_DATASET_FILE_PATH
OUTPUT_FILE_PATH = CLASSIFICATION_STRATIFIED_FILE_PATH

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

# negation -- 
# OUTPUT: returns a column of 0s and 1s of the negation of [column]. 1s are flipped to 0 and vice versa
# INPUT: [column] should be a column of 0s and 1s
def negation(column):
    return 1 - column

data = pandas.read_json(INPUT_FILE_PATH)
data = remove_non_binary_columns(data)

data_y = data[CORRECT_COLUMN]
data_x = data.drop(columns=[CORRECT_COLUMN, VALID_COLUMN])

# Split the data set into training and test set using Stratified Sampling
split = StratifiedKFold(n_splits=5,random_state=RANDOM_STATE, shuffle=True)
current_fold = 0
for train_index, test_index in split.split(data_x, data_y):
    strat_train_set_x, strat_train_set_y = data_x.loc[train_index], data_y.loc[train_index]
    strat_test_set_x, strat_test_set_y = data_x.loc[test_index], data_y.loc[test_index]

    # Perform grid search to tune hyperparameters
    param_grid = {
        "clf__n_estimators": [100, 500, 1000],
        "clf__max_depth": [1, 5, 10, 25],
        "clf__max_features": [*numpy.arange(0.1, 1.1, 0.1)],
    }

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier())
    ])

    # grid_search_csv = GridSearchCV(pipe, param_grid=param_grid, scoring='roc_auc', cv=3)
    # grid_search_csv.fit(strat_train_set_x, strat_train_set_y)

    # best_params = grid_search_csv.best_params_
    # print(best_params)

    # pipe = Pipeline([
    #     ('scaler', StandardScaler()),
    #     ('rf', RandomForestClassifier(random_state=RANDOM_STATE, max_features=best_params['clf__max_features'], n_estimators=best_params['clf__n_estimators'], max_depth=best_params['clf__max_depth']))
    # ])

    pipe.fit(strat_train_set_x, strat_train_set_y)
    pipe_predict_y = pipe.predict(strat_test_set_x)

    auc = metrics.roc_auc_score(strat_test_set_y, pipe_predict_y)

    current_fold = current_fold + 1
    print("FOLD:", current_fold)
    print("AUC score:", auc)
    print("1 Precision:", precision_score(strat_test_set_y, pipe_predict_y))
    print("1 Recall:", recall_score(strat_test_set_y, pipe_predict_y))

    print("0 Precision:", precision_score(negation(strat_test_set_y), negation(pipe_predict_y)))
    print("0 Recall:", recall_score(negation(strat_test_set_y), negation(pipe_predict_y)))

    # Get the ROC curve
    fpr, tpr, _ = metrics.roc_curve(strat_test_set_y, pipe_predict_y)
    plt.plot(fpr,tpr)
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    
plt.savefig(OUTPUT_FILE_PATH)
plt.clf()