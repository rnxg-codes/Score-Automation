from flask import Flask, render_template, jsonify
import json
import ESP
import threading
import time
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/RetroMenia')
def RetroMeniaTeams():
    return '''
<a href="/RetroMenia/team1">Team 1 </a>
'''

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
    data = data_json("RetroMenia",team)
    return render_template('retromenia.html', scores=data.json,)


@app.route('/NinjaClash/<path:team>')
def NinjaClash(team):
    data = data_json("NinjaClash", team)
    return render_template('ninjaclash.html', scores=data.json,)
        

@app.route('/PackRunner/<path:team>')
def PackRunner(team):
    data = data_json("PackRunner", team)
    return render_template('packrunner.html',scores=data.json,)


def data_json(arena, team):
    with open('db.json', 'r') as openfile:
        data = json.load(openfile)
    return jsonify(data[arena][team])

# def runFlask():
#     app.run(host="0.0.0.0", port=5000, debug=True)

# def updateEsp(port, baudrate=115200):
#     while 1:
#         inp = ESP.read(port)
#         data = ESP.filterData(inp)
#         with open('db.json', '+') as openfile:
#             db = json.load(openfile)["RetroMenia"]["team1"]
        
#         lActive = 0
#         for i in range(len(db)):
#             if data[i]:
#                 db[i]["status"] = "Pass"
#                 lActive = i
#             else:
#                 db[i]["status"] = "NA"
        
#         for i in range(lActive-1).__reversed__():
#             if db[i]["status"] == "NA":
#                 db[i]["status"] == "Skip"



# os.system(r"powershell .\env\Scripts\Activate.ps1 && py .\ESP.py")

if __name__ == "__main__":
    # espPort = ESP.getPort()
    # t1 = threading.Thread(target=updateEsp, args=(espPort, 115200,))
    # t2 = threading.Thread(target=runFlask)
 
    # t1.start()
    # t2.start()
 
    # t1.join()
    # t2.join()
 
    # print("Exiting!")
    app.run(host="0.0.0.0", port=5000, debug=True)
