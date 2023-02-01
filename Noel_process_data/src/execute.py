#     __          __       _    _____ 
#    / /   ____ _/ /_     | |  / /__ \
#   / /   / __ `/ __ \    | | / /__/ /
#  / /___/ /_/ / /_/ /    | |/ // __/ 
# /_____/\__,_/_.___/     |___//____/ 
#   At Arizona State University

print("RUNNING :: 1_extract_features.py                    --------------------------------------------------------------------")
exec(open("src/1_extract_features.py").read())

print("RUNNING :: 2_combine.py                             --------------------------------------------------------------------")
exec(open("src/2_combine.py").read())

print("RUNNING :: 3_causality.py                           --------------------------------------------------------------------")
exec(open("src/3_causality.py").read())

print("RUNNING :: 4_chatgpt_stats.py                       --------------------------------------------------------------------")
exec(open("src/4_chatgpt_stats.py").read())

print("RUNNING :: 5_split_dataset.py                       --------------------------------------------------------------------")
exec(open("src/5_split_dataset.py").read())

print("RUNNING :: 6_classification_kfold.py           --------------------------------------------------------------------")
exec(open("src/6_classification_kfold.py").read())

print("RUNNING :: 7_neural_network.py                      --------------------------------------------------------------------")
exec(open("src/7_neural_network.py").read())

print("SUCCESSFULLY COMPLETED ALL OPERATIONS               --------------------------------------------------------------------")
print("")