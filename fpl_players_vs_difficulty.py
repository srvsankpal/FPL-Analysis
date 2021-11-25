import json
import re
import requests
import numpy as np
import matplotlib.pyplot as plt

player_name=input("Player Name:\n")

performance=[[],[],[],[]] # creating lists inside list for respective team strengths 2,3,4,5
mean_performance=[] #list for mean performances for respective strength
difficulty=["2","3","4","5"]
ID=0

# Team strengths at home and away out of 5
#  1 - Arsenal (away:3 home:4)
#  2 - Aston Villa (away:3 home:3)
#  3 - Brentford (away:2 home:2)
#  4 - Brighton (away:3 home:3)
#  5 - Burnley (away:2 home:2)
#  6 - Chelsea (away:4 home:5)
#  7 - Crystal (Palace away:2 home:2)
#  8 - Everton (away:3 home:4)
#  9 - Leicester (away:3 home:3)
# 10 - Leeds (away:2 home:3)
# 11 - Liverpool (away:5 home:5)
# 12 - Man City (away:4 home:5)
# 13 - Man Utd (away:4 home:4)
# 14 - Newcastle (away:2 home:2)
# 15 - Norwich (away:2 home:2)
# 16 - Southampton (away:2 home:2)
# 17 - Spurs (away:3 home:3)
# 18 - Watford (away:2 home:2)
# 19 - West Ham (away:4 home:4)
# 20 - Wolves (away:2 home:2)
team_strength=[["Away","Home"],[3,4],[3,3],[2,2],[3,3],[2,2],[4,5],[2,2],[3,4],[3,3],[2,3],[5,5],[4,5],[4,4],[2,2],[2,2],[2,2],[3,3],[2,2],[4,4],[2,2]]

r=requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
data=r.text
info=json.loads(data)

# finding playes ID from input name
for players in info["elements"]:
    name=players["first_name"] +" " + players["second_name"]
    if re.search(".*"+player_name+".*", name, re.IGNORECASE) != None:
        ID=players["id"]
        display_name=name
        break
if ID==0:
    print("enter player name corectly")
    exit()

#getting players' details 
r1=requests.get("https://fantasy.premierleague.com/api/element-summary/"+str(ID)+"/")
data1=r1.text
info1=json.loads(data1)

for details in info1["history"]:
    opp_team=details["opponent_team"]
    if details["was_home"]: 
        i=0 #creating variable i to choose strength for either home or away depending on current fixture
    else:
        i=1
    diff=team_strength[opp_team][i] #selecting opponent team strength for current gameweek
    performance[diff-2].append(details["total_points"]) #storing the points scored in respective list of strengths


for each in performance:
    try:
        mean_performance.append(np.mean(each)) #storing mean performance to list for plotting y cordinates
    except:
        mean_performance.append(0)

x = np.array(difficulty)
y = np.array(mean_performance)
c = ["red", "blue", "yellow", "green"]

plt.bar(x, y, color = c, width=0.5)
plt.title(display_name)
plt.xlabel("Fixture difficulty (2-5)")
plt.ylabel('Average points per game')

# Annotating the bar plot with the values
for k in range(len(difficulty)):
    plt.annotate(mean_performance[k], (-0.1+k, mean_performance[k]))
plt.show()
