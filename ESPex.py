from win32com.client import Dispatch
import xlwings as xw
import serial.tools.list_ports as ports
import serial
import json
import time
import threading as th

wb = xw.Book('db.xlsx')
retro = wb.sheets['RETROMANIA']
ch = 0

def listTeams():
    teamCount = retro.range('A' + str(retro.cells.last_cell.row)).end('up').row -1
    teams = []
    for i in range(teamCount):
        teams.append(retro.range(i+2,2).value)
    return teams

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
    
    if previous != data:
        wb.save()

    


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

ESPdata = [0,0,0,0,0,0,0,0,0,0]
def updateEsp(port, teamIndex, baudrate=115200):
    LastPass = 0
    lastData = excelFetch(teamIndex, "checkpoint")
    while 1:
        try:
            ser = serial.Serial(port, baudrate=baudrate)
            jdata = ser.readline().decode("ascii")
            print(jdata)
            ser.close()
        
        except PermissionError as e:
            ser.close()

        except Exception as e:
            print(e)
    
        try:
            df = json.loads(jdata)
            for i in df:
                if df[i]!=None:
                    ESPdata[int(str(i).split(" ")[-1])-1] = df[i]
        except ValueError as e:
            print(f"\nUnwanted Data :( \n{e}")

        retroDB = excelFetch(teamIndex, "checkpoint")
        # if retroDB != lastData:
        #     wb.save()
        #     lastData = retroDB

        for i in range(len(ESPdata)):
            if (bool(ESPdata[i])):
                retroDB[i] = "Pass"
                LastPass = i
            else:
                retroDB[i] = "na"
        
        for i in (range(LastPass).__reversed__()):
            if retroDB[i] == "na":
                retroDB[i] = "Skip"
        # print(retroDB)
        excelWrite(teamIndex, "checkpoint", retroDB)



def saveXl():
    time.sleep(3)
    wb.save()

if __name__=="__main__":
    port = getPort()
    updateEsp(port, 1)
