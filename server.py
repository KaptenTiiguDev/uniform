from flask import Flask, render_template, jsonify
import json
from random import randint
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    page_name="index"
    version = randint(0,999999)
    question = getQuestion()
    answers = getAnswers()
    return render_template('%s.html' % page_name, question=question, answers=answers, version=version)

@app.route("/injuries", methods=['POST'])
def getInjuries():
    #1 = bleeding, 2 = missing limb
    fakeInjury = {'no':'a1','inj':1}
    return jsonify(fakeInjury)

def getQuestion():
    with open("data/questions.json", "r") as read_file:
        data = json.load(read_file)
        return(data['question'])
    
def getFollowupQuestion(question, answer):
    return ""

def getAnswers():
    return ["Yes","No"]
 
if __name__ == "__main__":
    app.run()