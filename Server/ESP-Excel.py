import serial
import json
import serial.tools.list_ports as ports
import xlwings as xw


wb = xw.Book('db.xlsx')
retro = wb.sheets['RETROMANIA']
ch = 0

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


def listTeams():
    teamCount = retro.range('A' + str(retro.cells.last_cell.row)).end('up').row -1
    teams = []
    for i in range(teamCount):
        teams.append(retro.range(i+2,2).value)
    return teams


def getTeam():
    try:
        teamindex = int(input("TeamIndex: "))
        team = listTeams()[teamindex - 0]
        return teamindex, team
    except Exception as e:
        print(e)
        exit(1)


def excelFetch(teamIndex, what):
    colums = retro.range( 1, int(wb.sheets[0].cells.last_cell.column)).end('left').column
    if what == "checkpoint":
        checkState = []
        for i in range(colums):
            if not i % 2 :
                checkState.append(retro.range(1+teamIndex,i+1).value)
        checkState.pop()
        checkState.pop(0)
        return checkState
    elif what == "time":
        checkState = []
        for i in range(colums):
            if i % 2 :
                checkState.append(retro.range(1+teamIndex,i+1).value)
        checkState.pop()
        checkState.pop(0)
        return checkState
    elif what == "score":
        return retro.range(1+teamIndex,24).value
    elif what == "tt":
        return retro.range(1+teamIndex,23).value


def excelWrite(teamIndex, what, data):
    previous = excelFetch(teamIndex, what)
    colums = retro.range( 1, int(wb.sheets[0].cells.last_cell.column)).end('left').column
    if what == "checkpoint":
        for i in range(colums):
            if not (i % 2) and i != 0 and i != colums-2:
                retro.range(1+teamIndex,i+1).value = data.pop(0)
    elif what == "time":
        colums = retro.range( 1, int(wb.sheets[0].cells.last_cell.column)).end('left').column
        if what == "time":
            for i in range(colums):
                if (i % 2) and i != 1 and i != colums-1:
                    # print(i)
                    retro.range(1+teamIndex,i+1).value = data.pop(0)
    elif what == "score":
        retro.range(1+teamIndex,24).value = data
    elif what == "tt":
        retro.range(1+teamIndex,23).value = data
    
    wb.save()

ESPdata = [0,0,0,0,0,0,0,0,0,0]
def updateESP(teamIndex, port, baudrate=115200):
    cmp = str([0,0,0,0,0,0,0,0,0,0])
    ser = serial.Serial(port = port, baudrate = baudrate)
    LastPass = 0

    while 1:
        jdata = ser.readline().decode("ascii")
        if is_json(jdata):
            print(jdata)
            df = json.loads(jdata)
            for i in df:
                ESPdata[int(str(i).split(" ")[-1])-1] = df[i]
        flag = 0
        if str(ESPdata) != cmp:
            flag = 1
            cmp = str(ESPdata)

        retroDB = excelFetch(teamIndex, "checkpoint")
        for i in range(len(ESPdata)):
            if (bool(ESPdata[i])):
                retroDB[i] = "Pass"
                LastPass = i
            else:
                retroDB[i] = "na"

        for i in (range(LastPass).__reversed__()):
            if retroDB[i] == "na":
                retroDB[i] = "Skip"

        if flag:
            excelWrite(teamIndex, "checkpoint", retroDB)


if __name__=="__main__":
    port = getPort()
    teamIndex, team = getTeam()
    try:
        updateESP(teamIndex,port)
    except Exception as e:
        print(f"Error: {e}")

