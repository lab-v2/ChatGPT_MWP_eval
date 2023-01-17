# ChatGPT Math Word Problem Evaluation
The emergence of large language models (LLMs) have gained much popularity in recent years, with OpenAI's GPT-3 series models being considered as the state-of-the-art. In particular, the variant of GPT-3 tuned for natural dialog, known as ChatGPT, has gathered much popular interest. However, LLMs have known performance issues, specifically when reasoning tasks are involved. This project aims to investigate aspects of math word problems (MWPs) that can indicate the success or failure of ChatGPT on such problems.

## Dataset
The dataset used in this project is the DRAW-1K dataset, which includes 1,000 MWPs with associated answers and template algebraic equations that one would use to solve such a word problem. Each object includes the following information:

"sQuestion": This key holds the text of the math word problem.

"lSolutions": This key holds a list of solutions for the problem, represented as a float.

"Template": This key holds a list of algebraic equations that can be used to solve the problem.

"lEquations": This key holds a list of equations that can be used to solve the problem.

"iIndex": This key holds an identifier for the problem, represented as an integer.

"Alignment": This key holds a list of objects that provide additional information about how the problem relates to the solutions and equations.

"Equiv": This key holds a list of any additional equivalent expressions that can be used to solve the problem.

The complete DRAW-1K dataset can be found on: 
[S. Upadhyay, M.-W. Chang, Annotating derivations: A new evaluation
strategy and dataset for algebra word problems](URL: http://arxiv.org/abs/1609.07197).

## TestResults
The test results of evaluating ChatGPT's performance on the questions from the DRAW-1K dataset are stored in the "test.json" file. This file contains a JSON object with a single key "Answers", which corresponds to an array of objects. Each object in this array represents a single math word problem and its corresponding answer provided by ChatGPT.

The objects within the array contain three keys:

"question_No": This key holds the unique identifier for the question, represented as an integer.

"final_answer": This key holds the answer provided by ChatGPT for the corresponding question, represented as a string.

"result": This key holds a brief description of the answer provided by ChatGPT, represented as a string. This key is used to evaluate the quality of the answer provided by ChatGPT.



The possible values for the "result" key are: "says no solution" (ChatGPT was not able to provide a solution for the problem), "has none of the answers" (ChatGPT provided an answer but it is not correct), "has one or more of the answers, but not all of them" (ChatGPT provided one or more correct answers, but not all of them), "has one or more of the answers when rounded, but not all of them" (ChatGPT provided one or more correct answers when rounded, but not all of them), "has all the answers" (ChatGPT provided all the correct answers), "has all the answers when rounded" (ChatGPT provided all the correct answers when rounded).



## Usage
Here is an example of how you can read the JSON file in Python:
```python
import json

# Open the file
with open('test.json') as json_file:
    data = json.load(json_file)

# Iterate through the array of objects
for question in data["Answers"]:
    question_number = question["question_No"]
    final_answer = question["final_answer"]
    result = question["result"]
```
## Results
The results of this project show that ChatGPT fails in 84% of DRAW-1K problems, even if we accept partial and rounded solutions. Additionally, several factors about MWPs relating to the number of unknowns and number of operations were identified that lead to a higher probability of failure. The probability of failure was also found to increase linearly with the number of addition and subtraction operations.


