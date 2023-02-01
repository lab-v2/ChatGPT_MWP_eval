import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

data = pd.read_json(SPLIT_DATASET_FILE_PATH)
output = data[CORRECT_COLUMN]

total_records = data[data[VALID_COLUMN] == 1][VALID_COLUMN].sum()

data = remove_non_binary_columns(data)
data = data.drop(columns=[CORRECT_COLUMN])

numerical_data = np.stack([data[col].values for col in data.columns], 1)
numerical_data = torch.tensor(numerical_data, dtype=torch.float)

output = torch.tensor(output.values).flatten()

print(total_records)
print(numerical_data)
print(output)
print(numerical_data.shape)
print(output.shape)

test_records = int(total_records * .2)

numerical_train_data = numerical_data[:total_records-test_records]
categorical_train_data = pd.DataFrame()
numerical_test_data = numerical_data[total_records-test_records:total_records]
train_outputs = output[:total_records-test_records]
test_outputs = output[total_records-test_records:total_records]

class Model(nn.Module):

    def __init__(self, num_numerical_cols, output_size, layers, p=0.4):
        super().__init__()
        self.embedding_dropout = nn.Dropout(p)
        self.batch_norm_num = nn.BatchNorm1d(num_numerical_cols)

        all_layers = []
        input_size = num_numerical_cols

        for i in layers:
            all_layers.append(nn.Linear(input_size, i))
            all_layers.append(nn.ReLU(inplace=True))
            all_layers.append(nn.BatchNorm1d(i))
            all_layers.append(nn.Dropout(p))
            input_size = i

        all_layers.append(nn.Linear(layers[-1], output_size))

        self.layers = nn.Sequential(*all_layers)

    def forward(self, x_numerical):
        x_numerical = self.batch_norm_num(x_numerical)
        x = torch.tensor(x_numerical)
        x = self.layers(x)
        return x

model = Model(numerical_data.shape[1], 2, [200,100,50], p=0.4)
loss_function = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

epochs = 1000
aggregated_losses = []

for i in range(epochs):
    i += 1
    y_pred = model(numerical_train_data)
    single_loss = loss_function(y_pred, train_outputs)
    aggregated_losses.append(single_loss)

    if i%25 == 1:
        print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')

    optimizer.zero_grad()
    single_loss.backward()
    optimizer.step()

with torch.no_grad():
    y_val = model(numerical_test_data)
    loss = loss_function(y_val, test_outputs)
print(f'Loss: {loss:.2f}')
y_val = np.argmax(y_val, axis=1)
print(y_val)

from sklearn.metrics import precision_score, recall_score
print("1 Precision:", precision_score(y_val, test_outputs))
print("1 Recall:", recall_score(y_val, test_outputs))

print("0 Precision:", precision_score(negation(y_val), negation(test_outputs)))
print("0 Recall:", recall_score(negation(y_val), negation(test_outputs)))