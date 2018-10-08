#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify
from random import randint

import serial
import thread

serial_port = "/dev/tty.HC-05-DevB"


class InjuryType:
    ALL_OK = 0
    BLEEDING = 1
    LIMB_MISSING = 2
    ALL_OK_TEXT = ''
    BLEEDING_TEXT = 'Verejooks'
    LIMB_MISSING_TEXT = 'Eemaldunud jäse'


class BodyPart:
    id = None
    instructions = {
        InjuryType.ALL_OK: '',
        InjuryType.BLEEDING: ['Aseta side haava peale!'],
        InjuryType.LIMB_MISSING: ['Aseta peale žgutt.', 'Evakueeri.']
    }

    @classmethod
    def get_instruction(cls, injury_type):
        return cls.instructions.get(injury_type, [])


class LeftArm(BodyPart):
    id = 'leftArm'


class RightArm(BodyPart):
    id = 'rightArm'


class BodyPartInjuryDetector:
    def __init__(self, body_part):
        self.is_bleeding = False
        self.is_removed = False
        self.body_part = body_part

    def update_values(self, is_bleeding, is_removed):
        self.is_bleeding = is_bleeding
        self.is_removed = is_removed

    def get_json_values(self):
        injury_type, injury_text = self.get_injury()
        return {
            'bodyPart': self.body_part.id,
            'injury': injury_text,
            'injuryType': injury_type,
            'instructions': self.body_part.get_instruction(injury_type)
        }

    def get_injury(self):
        if self.is_removed:
            return InjuryType.LIMB_MISSING, InjuryType.LIMB_MISSING_TEXT
        elif self.is_bleeding:
            return InjuryType.BLEEDING, InjuryType.BLEEDING_TEXT
        else:
            return InjuryType.ALL_OK, InjuryType.ALL_OK_TEXT


right_arm = BodyPartInjuryDetector(RightArm)
left_arm = BodyPartInjuryDetector(LeftArm)


# reading bluetooth data
def read_sensor_data():
    try:
        serial_connection = serial.Serial(port=serial_port)
        serial_connection.flush()
        while True:
            line = serial_connection.readline()
            if line:
                try:
                    data = line.replace('\n', '').replace('\r', '').split(",")
                    bleeding = data[0] == "1"
                    missing = data[1] == "1"
                    left_arm.update_values(bleeding, missing)
                    right_arm.update_values(bleeding, missing)
                except Exception as e:
                    print('Parsing bluetooth data failed', e)
    except Exception as e:
        print("Bluetooth error", e)


try:
    thread.start_new_thread(read_sensor_data, ())
except Exception:
    print("Error: unable to start thread")

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    page_name = "index"
    version = randint(0, 999999)
    return render_template('%s.html' % page_name, version=version)


@app.route("/injuries", methods=['GET', 'POST'])
def get_injuries():
    return jsonify(left_arm.get_json_values())


if __name__ == "__main__":
    app.run()
