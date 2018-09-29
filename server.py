from flask import Flask, render_template, request, jsonify
import json
from random import randint

import serial #pyserial module required
import thread

serial_port = "COM5"

right_arm_bleeding = False
right_arm_removed = False

#reading bluetooth data
def read_sensor_data():
    global serial_port

    global right_arm_bleeding
    global right_arm_removed

    import serial

    try:
        serialConnection = serial.Serial(port=serial_port)
        serialConnection.flush()

        while True:
            line = serialConnection.readline()
            if line:
                data = line.replace('\n', ' ').replace('\r', '').split(",", 1)
                right_arm_bleeding = data[0] == "1"
                right_arm_removed = data[1] == "1"
    except:
        print "Bluetooth not connected on port " + serial_port

try:
   thread.start_new_thread(read_sensor_data, ())
except:
   print "Error: unable to start thread"

app = Flask(__name__, static_url_path='/static')
questionsFile = "data/questions.json"

@app.route("/")
def index():
    page_name="index"
    version = randint(0,999999)
    #question = getQuestion()
    #question = getFollowup(0)
    #answers = getAnswers()
    return render_template('%s.html' % page_name, version=version)

@app.route("/injuries", methods=['POST'])
def getInjuries():
    #1 = bleeding, 2 = missing limb
    fakeInjury = {'no': right_arm_bleeding,'inj':1}
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
