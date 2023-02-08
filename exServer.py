from flask import Flask, render_template, jsonify
import json
import xlwings as xw
import pythoncom
import pandas as pd
import threading
import time
import os


app = Flask(__name__)
pythoncom.CoInitialize()
# wb = xw.Book('db.xlsx')
# retro = wb.sheets['RETROMANIA']


def listTeams():
    # teamCount = retro.range('A' + str(retro.cells.last_cell.row)).end('up').row -1
    # teams = []
    # for i in range(teamCount):
    #     teams.append(retro.range(i+2,2).value)
    df = pd.read_excel('db.xlsx',0) # can also index sheet by name or fetch all sheets
    teams = df['teams'].tolist()
    print(teams)
    return teams

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/RetroMenia')
def RetroMeniaTeams():
    teams = listTeams()
    return  render_template('retroTeams.html', teams=teams,)

@app.route('/NinjaClash')
def NinjaClashTeams():
    return '''
<a href="/NinjaClash/team2">Team 2 </a>
'''

@app.route('/PackRunner')
def PackRunnerTeams():
    return '''
<a href="/PackRunner/team3">Team 3 </a>
'''

@app.route('/RetroMenia/<path:team>')
def RetroMenia(team):
    try:
        data = data_json(team)
    except PermissionError: 
        time.sleep(1)
        data = data_json(team)
    return render_template('retromenia.html', scores=data,)


@app.route('/NinjaClash/<path:team>')
def NinjaClash(team):
    data = data_json("NinjaClash", team)
    return render_template('ninjaclash.html', scores=data.json,)
        

@app.route('/PackRunner/<path:team>')
def PackRunner(team):
    data = data_json("PackRunner", team)
    return render_template('packrunner.html',scores=data.json,)


def data_json(team):
    df = pd.read_excel('db.xlsx',0) 
    teamIndex = df['teams'].tolist().index(team)
    data = [
            {
                "id": 1,
                "check": "checkpoint 1",
                "status": "NA",
                "time" : ""
            },
            {
                "id": 2,
                "check": "checkpoint 2",
                "status": "NA",
                "time" : ""
            },
            {
                "id": 3,
                "check": "checkpoint 3",
                "status": "NA",
                "time" : ""
            },
            {
                "id": 4,
                "check": "checkpoint 4",
                "status": "NA",
                "time" : ""
            },
            {
                "id": 5,
                "check": "checkpoint 5",
                "status": "NA",
                "time" : ""
            },
            {
                "id": 6,
                "check": "checkpoint 6",
                "status": "NA",
                "time" : ""
            },
            {
                "id": 7,
                "check": "checkpoint 7",
                "status": "NA",
                "time" : ""
            },
            {
                "id": 8,
                "check": "checkpoint 8",
                "status": "NA",
                "time" : ""
            },
            {
                "id": 9,
                "check": "checkpoint 9",
                "status": "NA",
                "time" : ""
            },
            {
                "id": 10,
                "check": "checkpoint 10",
                "status": "NA",
                "time" : ""
            }
        ]
    
    teamStat = df.values.tolist()[teamIndex]
    teamStat.pop(0)
    teamStat.pop(0)
    teamStat.pop()
    teamStat.pop()
    count = 0
    for i, stat in enumerate(teamStat):
        if not (i % 2):
            data[count]["status"] = stat
            count+=1

    return data


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=True)
