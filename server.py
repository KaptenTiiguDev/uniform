from flask import Flask, render_template
import json
app = Flask(__name__)
 
@app.route("/")
def index():
    page_name="index"
    question = getQuestion()
    answers = getAnswers()
    return render_template('%s.html' % page_name, question=question, answers=answers)

def getData():
	return "abc"

def getQuestion():
    return "Is the person breathing?"
    
def getAnswers():
    return ["Yes","No"]
 
if __name__ == "__main__":
    app.run()