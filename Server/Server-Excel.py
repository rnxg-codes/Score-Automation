from flask import Flask, render_template, jsonify
import json
import xlwings as xw
import pythoncom
import pandas as pd
import threading
import time
import os
from flask_cors import CORS


app = Flask(__name__)
pythoncom.CoInitialize()
# wb = xw.Book('db.xlsx')
# retro = wb.sheets['RETROMANIA']
CORS(app)

def listTeams(arena):
    # teamCount = retro.range('A' + str(retro.cells.last_cell.row)).end('up').row -1
    # teams = []
    # for i in range(teamCount):
    #     teams.append(retro.range(i+2,2).value)
    
    if arena == "p":
        df = pd.read_excel('db.xlsx',0) # can also index sheet by name or fetch all sheets

        teams = df['teams'].tolist()
        # print(teams)
        return teams

    if arena == "r":
        df = pd.read_excel('db.xlsx',1) # can also index sheet by name or fetch all sheets

        teams = df['teams'].tolist()
        # print(teams)
        return teams
    
    if arena == "n":
        df = pd.read_excel('db.xlsx',2) # can also index sheet by name or fetch all sheets

        teams = df['teams'].tolist()
        # print(teams)
        return teams

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/RetroMenia')
def RetroMeniaTeams():
    teams = listTeams("r")
    return  render_template('retroTeams.html', teams=teams,)

@app.route('/NinjaClash')
def NinjaClashTeams():
    teams = listTeams("n")
    
    return  render_template('ninjaTeams.html', teams=teams,)


@app.route('/PackRunner')
def PackRunnerTeams():
    teams = listTeams("p")
    return  render_template('pacTeams.html', teams=teams,)

@app.route('/RetroMenia/<path:team>')
def RetroMenia(team):
    try:
        data = data_json(team)
    except PermissionError: 
        time.sleep(1)
        data = data_json(team)
    return render_template('packrunner.html', scores=data,team = team)


@app.route('/NinjaClash/<path:team>')
def NinjaClash(team):
    # data = data_json(team)
    team1 = team.split(" Vs ")[0]
    team2 = team.split(" Vs ")[1]
    return render_template('ninjaclash.html', team1=team1,team2 = team2,)
        

@app.route('/PackRunner/<path:team>')
def PackRunner(team):
    # print(listTeams("p").index(team))
    index = 6
    # print(index)
    data = getPac(team)
    return render_template('packrunner.html',scores=data,team = team, index=index)



# @app.route("/PackRunner/api/ted Vs te2/2/score/add/12")
@app.route("/PackRunner/api1/<path:data>")
def pacScoreRcv(data):
    # print(data)
    d = data.split("/")
    teams = d[0]
    team = d[1] 
    fun = d[3]
    val = int(d[4])
    df = pd.read_excel('db.xlsx',2)
    # print(teams)
    teamIndex = df['teams'].tolist().index(teams)

    score = df[f'Score {team}'].tolist()[teamIndex]

    if fun == "add":
        score += int(val)
    elif fun == "sub":
        score -+ int(val)

    s1 = df[f'Score 1'].tolist()[teamIndex]
    s2 = df[f'Score 2'].tolist()[teamIndex]

    ob = {
        "score1": "s1",
        "score2": "s2"
    }
    with open("./PacSoc.txt", "w") as f:
        lin = f"{int(teamIndex)}:{int(s1)}:{int(s2)}"
        f.write(lin)
        
    return jsonify(ob)


@app.route("/PackRunner/api/<path:d>")
def pacScoreSnd(d):
    data = int(d) -1
    df = pd.read_excel('db.xlsx',2)
    
    s1 = df[f'Score 1'].tolist()[data]
    s2 = df[f'Score 2'].tolist()[data]

    ob = {
        "score1": s1,
        "score2": s2
    }
    return jsonify(ob)




def getPac(team):
    df = pd.read_excel('db.xlsx',0)
    # print(df['teams'].tolist())
    
    teamIndex = listTeams("p").index(team)
    # print(listTeams("p"))
    # print(team)
    data = [
            {
                "id": 1,
                "check": "A1",
                "status": "na",
                "time" : ""
            },
            {
                "id": 2,
                "check": "A2",
                "status": "na",
                "time" : ""
            },
            {
                "id": 3,
                "check": "B",
                "status": "na",
                "time" : ""
            },
            {
                "id": 4,
                "check": "C",
                "status": "na",
                "time" : ""
            },
            {
                "id": 5,
                "check": "D",
                "status": "na",
                "time" : ""
            }
        ]
    
    teamStat = df.values.tolist()[teamIndex]
    teamStat.pop(0)
    teamStat.pop(0)
    # print(teamStat)

    count = 0
    for i, stat in enumerate(teamStat):
        data[count]["status"] = stat
        count+=1
    # print(data)
    return data


def data_json(team):
    df = pd.read_excel('db.xlsx',1) 
    # teamIndex = df['teams'].tolist().index(team)
    teamIndex = listTeams("r").index(team)
    data = [
            {
                "id": 1,
                "check": "1",
                "status": "na",
                "time" : ""
            },
            {
                "id": 2,
                "check": "2",
                "status": "na",
                "time" : ""
            },
            {
                "id": 3,
                "check": "3",
                "status": "na",
                "time" : ""
            },
            {
                "id": 4,
                "check": "4",
                "status": "na",
                "time" : ""
            },
            {
                "id": 5,
                "check": "5",
                "status": "na",
                "time" : ""
            },
            {
                "id": 6,
                "check": "6",
                "status": "na",
                "time" : ""
            },
            {
                "id": 7,
                "check": "7",
                "status": "na",
                "time" : ""
            },
            {
                "id": 8,
                "check": "8",
                "status": "na",
                "time" : ""
            },
            {
                "id": 9,
                "check": "9",
                "status": "na",
                "time" : ""
            },
            {
                "id": 10,
                "check": "10",
                "status": "na",
                "time" : ""
            }
        ]
    
    teamStat = df.values.tolist()[teamIndex]
    print(teamStat)
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
