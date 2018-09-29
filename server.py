from flask import Flask, render_template, request
import json
from random import randint
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    page_name="index"
    version = randint(0,999999)
    question = getQuestion()
    answer = 0
    question = getFollowup(0)
    print(question)
    answers = getAnswers()
    return render_template('%s.html' % page_name, question=question, answers=answers, version=version)

def getData():
	return "abc"

def getQuestion():
    with open("data/questions.json", "r") as read_file:
        data = json.load(read_file)
        return(data['question'])
    
def getFollowup(answer):
    with open("data/questions.json", "r") as read_file:
        data = json.load(read_file)
        answer = data['answers'][answer]
        print(answer)
        if 'followup' in answer:
            return answer['followup']['question']
        else:
            return answer['solution']
    return 0
    
def getAnswers():
    return ["Yes","No"]
    
@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    print("here")
    print(request.)
    return ""
 
if __name__ == "__main__":
    app.run()