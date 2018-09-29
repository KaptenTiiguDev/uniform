from flask import Flask, render_template, jsonify
import json
from random import randint

import serial #pyserial module required
import thread

right_arm_bleeding = False
right_arm_removed = False

#reading bluetooth data
def read_sensor_data():
    global right_arm_bleeding
    global right_arm_removed

    import serial

    serialConnection = serial.Serial(port='COM5')
    serialConnection.flush()

    while True:
        line = serialConnection.readline()
        if line:
            data = line.replace('\n', ' ').replace('\r', '').split(",", 1)
            right_arm_bleeding = data[0] == "1"
            right_arm_removed = data[1] == "1"

try:
   thread.start_new_thread(read_sensor_data, ())
except:
   print "Error: unable to start thread"

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
    fakeInjury = {'no': right_arm_bleeding,'inj':1}
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
