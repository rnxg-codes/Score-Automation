import serial
import json
import serial.tools.list_ports as ports



def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

def getPort():
    com_ports = list(ports.comports())
    print("\nAvailable Ports: ")
    for i in com_ports:
        print(i.device)
    if len(com_ports):
        port = str(com_ports[int(input("Index of selected port: "))].device)
        return port
    else:
        print("Port not detected :(")
        exit(0)

ser = serial.Serial(port = getPort(), baudrate = 115200)
while 1:
    data = ser.readline().decode("ascii")
    if is_json(data):
        print(data)