import json
#from chatgpt_wrapper import ChatGPT
import time
import re


#Method to read data from a json file, and analyze if it was correct or wrong

f = open('testPlus.json')
data = json.load(f)
g = open('draw.json')
d2 = json.load(g)

       
def write_json(new_data, filename='chatGPT+Test.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["Answers"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def find_Ans(statement):
    pos = statement.rfind("\n")
    if pos == -1:
        return statement
    else:
        return statement[pos+1:]

def compare_answers(student_answers, correct_answers):
    if(student_answers == "Unusable response produced, maybe login session expired. Try 'pkill firefox' and 'chatgpt install'"):
        return "unusable"
    if(student_answers == ""):
        return "says no solution"
    student_numbers = student_answers.split(',')
    for i in range(len(student_numbers)):
        try:
            student_numbers[i] = float(student_numbers[i])
        except ValueError:
            return "says no solution"
        
    student_set = set(student_numbers)
    correct_set = set(correct_answers)
    
    rounded_student_answers = [round(x) for x in student_numbers]
    student_rounded_set = set(rounded_student_answers)
    rounded_correct_answers = [round(x) for x in correct_answers]
    correct_rounded_set = set(rounded_correct_answers)
    
    if student_set == correct_set:
        return "has all the answers"
    elif student_set.issubset(correct_set):
        return "has one or more of the answers, but not all of them"
    elif student_rounded_set == correct_rounded_set:
        return "has all the answers when rounded"
    elif student_rounded_set.issubset(correct_rounded_set):
        return "has one or more of the answers when rounded, but not all of them"
    else:
        return "has none of the answers"

#Method to extract the answer from the last sentence of the answer

def Scan_Answers(response, correct_answers):
    
    if(response == "Unusable response produced, maybe login session expired. Try 'pkill firefox' and 'chatgpt install'"):
            return "unusable"
        
    sentences = response.split("\n\n")
    
    if len(sentences) > 1:
        last_sentence = sentences[-1]
    else:
        last_sentence = response
    last_sentence = last_sentence.replace(",", "")
        
    #pattern = r"(\d+(?:,\s*\d+)*)\." #pattern for regular expression
    pattern = r'\d+(?:\.\d+)?'
    #pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d+)?'
    #pattern = r'\$?\d{1,3}(?:[, ]\d{3})*(?:\.\d+)?%?'
    numbers = re.findall(pattern, last_sentence)
    #check = re.search(pattern, last_sentence)  
    if len(numbers) == 0:
        return "says no solution"  
    #numbers = [float(num.replace(',', '').replace(' ', '').replace('$', '').replace('%', '')) for num in numbers]
    numbers = [float(num) for num in numbers]
    student_numbers = set(numbers)
    if student_numbers.issubset(correct_answers):
        return "has all the answers"
    elif student_numbers.intersection(correct_answers):
        return "has one or more of the answers, but not all of them"
    else: 
        rounded_student_numbers = set(map(round, student_numbers)) # rounded set
        rounded_correct_answers = set(map(round, correct_answers)) # rounded set
        if rounded_student_numbers.issubset(rounded_correct_answers):
            return "has all the answers when rounded"
        elif rounded_student_numbers.intersection(rounded_correct_answers):
            return "has one or more of the answers when rounded, but not all of them"
        else:
            return "has none of the answers"




QuestionNo = 0
for i in data['Answers']:
    response = i["response"]
    question = d2['Questions'][QuestionNo]
    
    result = Scan_Answers(response,question["lSolutions"])
    #ans = find_Ans(response)
    #think of combinging these
    dictionary = {
        "question_No": QuestionNo,
        "response": response,
        #"final_answer": ans,
       "result": result
    }
    write_json(dictionary)
    QuestionNo = QuestionNo + 1

#print(response)


f.close()
g.close()


