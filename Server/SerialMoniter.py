import serial
import json


def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True


ser = serial.Serial(port = "COM5", baudrate = 115200)
while 1:
    data = ser.readline().decode("ascii")
    if is_json(data):
        print(data)