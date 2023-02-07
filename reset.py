import serial


ser = serial.Serial("COM7", baudrate=115200)
ser.write("hello".encode("utf-8"))