from flask import Flask, render_template, request, jsonify
import json
from random import randint

import serial #pyserial module required
import thread

serial_port = "/dev/rfcomm2"


class BodyPartInjuryDetector:
    def __init__(self, body_part):
        self.is_bleeding = False
        self.is_removed = False
        self.body_part = body_part

    def update_values(self, is_bleeding, is_removed):
        self.is_bleeding = is_bleeding
        self.is_removed = is_removed

    def get_json_values(self):
        if self.is_bleeding or self.is_removed:
            return {
                'no': self.body_part,
                'inj': 2 if self.is_removed else 1,
                'advice': 'Put on a tourniquet and evacuate.' if self.is_removed else 'Put a bandage on.'
            }
        return {'no':'armLeft','inj':1,'advice':'put bad'}


right_arm = BodyPartInjuryDetector('armRight')
left_arm = BodyPartInjuryDetector('armLeft')


# reading bluetooth data
def read_sensor_data():

    try:
        serial_connection = serial.Serial(port=serial_port)
        serial_connection.flush()

        while True:
            line = serial_connection.readline()
            if line:
                data = line.replace('\n', ' ').replace('\r', '').split(",", 1)
                right_arm_bleeding = data[0] == "1"
                right_arm_removed = data[1] == "1 "
                left_arm.update_values(right_arm_bleeding,right_arm_removed)
                right_arm.update_values(right_arm_bleeding, right_arm_removed)
    except:
        print("Bluetooth not connected on port ", serial_port)

try:
   thread.start_new_thread(read_sensor_data, ())
except:
   print("Error: unable to start thread")

app = Flask(__name__, static_url_path='/static')
questionsFile = "data/questions.json"

@app.route("/")
def index():
    page_name = "index"
    version = randint(0, 999999)
    return render_template('%s.html' % page_name, version=version)

@app.route("/injuries", methods=['GET', 'POST'])
def get_injuries():
    return jsonify(left_arm.get_json_values())


@app.route("/advice/", methods=['GET','POST'])
def get_advice():
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
