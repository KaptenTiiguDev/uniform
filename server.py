#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import json
from random import randint

import serial
import thread

serial_port = "/dev/rfcomm2"


class InjuryType:
    ALL_OK = 0
    BLEEDING = 1
    LIMB_MISSING = 2


class BodyPart:
    id = None
    instructions = {
        InjuryType.ALL_OK: '',
        InjuryType.BLEEDING: 'Aseta side haava peale.',
        InjuryType.LIMB_MISSING: 'Aseta peale žgutt ja evakueeri.'
    }

    @classmethod
    def get_instruction(cls, injury_type):
        return cls.instructions.get(injury_type)


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
        injury = self.get_injury_type()
        return {
            'bodyPart': self.body_part.id,
            'injuryType': injury,
            'instruction': self.body_part.get_instruction(injury)
        }

    def get_injury_type(self):
        if self.is_removed:
            return InjuryType.LIMB_MISSING
        elif self.is_bleeding:
            return InjuryType.BLEEDING
        else:
            return InjuryType.ALL_OK


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
                data = line.replace('\n', ' ').replace('\r', '').split(",", 1)
                right_arm_bleeding = data[0] == "1"
                right_arm_removed = data[1] == "1 "
                left_arm.update_values(right_arm_bleeding, right_arm_removed)
                right_arm.update_values(right_arm_bleeding, right_arm_removed)
    except Exception:
        print("Bluetooth not connected on port ", serial_port)


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
