# Chat GPT

# Folders
## input
chatgpt.json - Responses from ChatGPT received by Abhinav  
draw.json - Original data set with math equations, intermediary steps and solutions.  

## output
1_extract_features.json - Json containing extracted features from the math equations in draw.json. Features such as number of additions, subtractions, etc.

## src
1_extract_features.ipynb - Uses pandas to extract various mathematical features from math equations from draw.json  
2_visualize_data.ipynb - Visualizes data in 1_extract_features.json graphs number of [certain mathematical feature] against its count  
3_combine_chatgpt_draw.ipynb - This combines both the actual data set with the data collected by Abhinav. It also goes through Abhinav's answers and labels rows as valid or invalid  
4_calculate_probability.ipynb - This calculates the conditional probability of success of all possible causes and splits the number of a certain mathematical feature into numerous columns.  
5_calculate_causality.ipynb - This calculates the causality value of each potential cause.  

# How it works
I currently think of this as an assembly line, each file saves the modified data to a new csv where it is passed on to the next script

