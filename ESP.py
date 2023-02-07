import serial.tools.list_ports as ports
import serial
import json
import time

filteredData = [0,0,0,0,0,0,0,0,0,0,0,0]

def read(port,  baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate=baudrate)
        data = ser.readline().decode()
        return data
    except:
        print(" -- error -- ")
        return "error"

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
        return 0

def filterData(data):
    try:
        df = json.loads(data)
        for i in df:
            if df[i]!=None:
                filteredData[int(str(i).split(" ")[-1])-1] = df[i]
    except ValueError:
        print("\nUnwanted Data :( \n")
    return filteredData

def updateEsp(port, baudrate=115200):
    lActive = 0
    while 1:
        inp = read(port, baudrate)
        print(inp)
        data = filterData(inp)
        # print(data)
        with open('db.json', 'r') as openfile:
            db = json.load(openfile)

        RetroDB = db["RetroMenia"]["team1"]
        for i in range(len(RetroDB)):
            if (bool(data[i])):
                RetroDB[i]["status"] = "Pass"
                lActive = i
            else:
                RetroDB[i]["status"] = "NA"
        
        for i in (range(lActive).__reversed__()):
            if RetroDB[i]["status"] == "NA":
                RetroDB[i]["status"] = "Skip"
        
        db["RetroMenia"]["team1"] = RetroDB

        json_object = json.dumps(db, indent=4)
        with open("db.json", "w") as outfile:
            outfile.write(json_object)
        
        time.sleep(0.1)



if __name__=="__main__":
    port = getPort()
    # data = read(port)
    # fData = filterData(data)
    # print(f"original data: {data}\nfiltered values: {fData}")
    # for i in range(5).__reversed__():
    #     print(i)
    updateEsp(port)

