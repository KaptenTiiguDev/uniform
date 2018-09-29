from flask import Flask, render_template, request, jsonify
import json
from random import randint
app = Flask(__name__, static_url_path='/static')
questionsFile = "data/questions.json"

@app.route("/")
def index():
    page_name="index"
    version = randint(0,999999)
    question = getQuestion()
    #question = getFollowup(0)
    answers = getAnswers()
    return render_template('%s.html' % page_name, question=question, answers=answers, version=version)

@app.route("/injuries", methods=['POST'])
def getInjuries():
    #1 = bleeding, 2 = missing limb
    fakeInjury = {'no':'a1','inj':1}
    return jsonify(fakeInjury)

 #@app.route("/advice/", methods=['GET','POST'])
@app.route("/advice/", methods=['GET','POST'])
def getAdvice():
 	arg = json.loads(request.args.get('st'))
 	no = arg['no']
 	inj = arg['inj']
 	with open("data/advice.json", "r") as read_file:
 		data = json.load(read_file)
 		return data[no][inj]
 	return None

def getQuestion():
    with open(questionsFile, "r") as readFile:
        data = json.load(readFile)
        return(data['question'])
    
def getFollowup(answer):
    with open(questionsFile, "r") as readFile:
        data = json.load(readFile)
        answer = data['answers'][answer]
        print(answer)
        if 'followup' in answer:
            return answer['followup']['question']
        else:
            return answer['solution']
    return 0
    
def getAnswers():
    return ["Yes","No"]
    
@app.route('/getAnswer/', methods=['GET', 'POST'])
def getAnswer():
    answer = request.args.get('answ')
    return answer
 
if __name__ == "__main__":
    app.run()