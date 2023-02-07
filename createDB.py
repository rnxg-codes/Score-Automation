import json
import sys
import pandas as pd

DB = {
    "RetroMenia":{},
    "NinjaClash":{},
    "PackRunner":{}
}

def checkpoints(arena):
    arena = arena.lower()
    check = 0
    checkpoint = []
    if arena == "retromenia":
        check = 12
    elif arena == "packrunner":
        check = 5
    elif arena == "ninjaclash":
        checkpoint = {
            "panelty": 0,
            "score": 0 
        }
    else :
        print("Invalid arena :(")
    
    if check:
        for i in range(check):
            name = "checkPoint_" + str(i+1)
            checkpoint.append(
                {
                "id":(i+1),
                "check":name,
                "status":"NA"
            }
            )
    return checkpoint

def write():
    json_object = json.dumps(DB, indent=4)
    with open("db.json", "w") as outfile:
        outfile.write(json_object)

def create():
    if len(sys.argv) > 1:
        file = sys.argv[1]
        df = pd.read_excel(file, sheet_name=0)
        arena = df['Arena'].tolist()
        teams = df['TeamName'].tolist()
        for team in teams:
            ar = arena[teams.index(team)]
            DB[ar][team] = checkpoints(ar)
    else:
        print(f"\nUsage: {sys.argv[0]} <excel file> \n")


if __name__=="__main__":
    create()
    write()