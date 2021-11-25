import requests
import json
import numpy
import mysql.connector

#creating a small datatype to avoid parsing the complex data again
element_types={1:"GKP",2:"DEF",3:"MID",4:"FWD"}

#connection to database that I have already created in MySQL
con=mysql.connector.connect(
    host="localhost",
    user="your username",
    password="your password",
    database="your database name"
)
cur=con.cursor()
cur.execute("create table if not exists `fpl` (`ID` INTEGER, `Player Name` TEXT, `Position` TEXT, `Team` TEXT, `Cost` FLOAT, `Total Points` INT, `Points/Game` FLOAT, `In Squad Consistency %` FLOAT, `Good Points Consistency %` FLOAT, `Form (Last 3 Games Mean Points)` FLOAT, `Fixture Difficulty (Next 3)` FLOAT);")
con.commit()

# requsting data from fpl API
r=requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
data=r.text
info=json.loads(data)

#scrapping for id and basic stats of players
for players in info["elements"]:

    ID=players["id"] #player's ID on FPL
    name=players["first_name"] +" " + players["second_name"] #Player's full name
    position= element_types[players["element_type"]] # playing position of player
    cost=players["now_cost"]/10 #player's cost on FPL
    team=info["teams"][players["team"]-1]["name"] # players team
    total_points=players["total_points"] # Total points obtained till current gameweek
    mean_points=float(players["points_per_game"]) # average points per game

    # creating an empty list to store each gameweek points to find player's Consistency
    GW_scores=[]

    #creating empty list to store players last 3 performances to find players current form
    recent_scores=[]

    #creating empty list to store fixtures of team to find fixture difficulty
    fixture=[]

    #empty list to store scores above a certain threshold to find player's good scoring capability
    good_scores=[]

    #fetching detail info about players
    r1=requests.get("https://fantasy.premierleague.com/api/element-summary/"+str(ID)+"/")
    data1=r1.text
    info1=json.loads(data1)
    GWs=len(info1["history"])

    for details in info1["history"]:
        if details["minutes"]!=0: #adding to the list only if player has played more than 0 minutes
            GW_scores.append(details["total_points"])
            if details["total_points"]>=4: #good score threshold=4
                good_scores.append(details["total_points"])

    playing_consistency=float(round((len(GW_scores)/GWs)*100,2)) #number of games played / total game weeks
    if mean_points!=0:
         points_consistency=float(round((len(good_scores)/len(GW_scores))*100,2)) # number of games above threshold score/ number of games palyed
    else:
        points_consistency=0

    for i in range(3):
        if GWs>3:
            recent_scores.append(info1["history"][GWs-1-i]["total_points"])
        fixture.append(info1["fixtures"][i]["difficulty"])

    if GWs>3:
        form=float(round(numpy.mean(recent_scores),1)) #mean points of recent 3 games
    else:
        form=mean_points
    fixture_difficulty=float(round(numpy.mean(fixture),1)) # mean difficulty out of 5 for next 3 gameweeks

    #inserting data into MySQL table
    cur.execute("insert into `fpl`(`ID`, `Player Name`, `Position`, `Team`, `Cost`, `Total Points`, `Points/Game`, `In Squad Consistency %`, `Good Points Consistency %`, `Form (Last 3 Games Mean Points)`, `Fixture Difficulty (Next 3)`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (ID,name,position,team,cost,total_points,mean_points,playing_consistency,points_consistency,form,fixture_difficulty))
    con.commit()
    # print(ID," ",name," ",position," ",cost," ",team," t:",total_points," m:",mean_points," PlC:",playing_consistency," Poc:",points_consistency," f:",form," d:",fixture_difficulty)
