from flask import Flask,request,jsonify,render_template, redirect, abort, make_response
import requests,time,json, re
from datetime import datetime
from lib.IdentifyUser import identifyUser, authUser
from lib.ReadConfig import readConfig

initConfig = readConfig()

MasterDB = initConfig['Init']['MasterDB']
if MasterDB == "neo4j":
	from lib.Neo4jLibrary import neo4jGetTaxonomyLineage, neo4jGetTaxonomyLastname, neo4jGetPeopleList
else:
	from lib.PostgresMySQLLibrary import sqlGetTaxonomyLineage,sqlGetTaxonomyLastname, sqlGetPeopleList

def getPeopleList():
	databaseFunction = globals()[f"{MasterDB}GetPeopleList"]
	DBOutput = databaseFunction()
	OutputJSON = []
	LastNameArray = []
	CurrentID = 0
	for Row in DBOutput:
		ParentsDisplay = []
		if Row[3] != None:
			Parents = Row[3].split(",")[:2]
			for Parent in Parents:
				ParentArray = Parent.split(" ")
				if len(ParentArray) == 3:
					ParentsDisplay.append(ParentArray[0] + " " + ParentArray[2])
				else:
					ParentsDisplay.append(" ".join(ParentArray[:3]))
				
		OutputJSON.append({"ID": Row[0], "Name": Row[1] + " " + Row[2], "Parents": " / ".join(ParentsDisplay), "Group": "Lineage"})
		if Row[2] not in LastNameArray:
			LastNameArray.append(Row[2])
			OutputJSON.append({"ID": Row[0], "Name": Row[2], "Group": "Lastname"})
	return jsonify(OutputJSON)

def getTaxonomy(ID, Group, Name, UpDown):
	if Group == "Lineage":	
		databaseFunction = globals()[f"{MasterDB}GetTaxonomyLineage"]
		DBOutput = databaseFunction(ID,UpDown)		
	else:
		databaseFunction = globals()[f"{MasterDB}GetTaxonomyLastname"]
		DBOutput = databaseFunction(ID,Name)		
	print(DBOutput)
	print(len(DBOutput))
	OutputJSON = {}
	TempArray = []
	CurrentID = 0
	for Row in DBOutput:
		if CurrentID != Row[0] and CurrentID != 0:
			OutputJSON[CurrentID] = {"Name": Name, "Generation": Generation, "Summary": Summary, "Events": TempArray}
			TempArray = []
		TempArray.append({"Date": "" if Row[4] is None else Row[4], "Place": Row[5], "LatLng": [Row[6],Row[7]]})
		Generation = Row[3]
		Summary = Row[8]#.replace("*","")
		Name = Row[1] + " " + Row[2]
		CurrentID = Row[0]
	OutputJSON[CurrentID] = {"Name": Name, "Generation": Generation, "Summary": Summary, "Events": TempArray}

	return jsonify(OutputJSON)




app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	Token = request.cookies.get('portal_token')
	Email = request.cookies.get('portal_user')
	RequestURL = request.base_url
	if not Token or not Email:
		return render_template('login.html')
	return identifyUser(request,render_template('index.html'))



@app.route('/auth')
def authUserEndpoint():
	return authUser(request)


@app.route("/api/v1/GetTaxonomy", methods=["GET"])
def sqlGetTaxonomyEndpoint():
	UserIdentity = identifyUser(request,None)
	if type(UserIdentity) is not tuple:
		return UserIdentity
	ID = request.args.get("id")
	Group = request.args.get("group")
	Name = request.args.get("name")
	UpDown = request.args.get("updown")
	return getTaxonomy(ID, Group, Name, UpDown)

@app.route("/api/v1/GetPeopleList", methods=["GET"])
def sqlGetPeopleListEndpoint():
	UserIdentity = identifyUser(request,None)
	if type(UserIdentity) is not tuple:
		return UserIdentity
	return getPeopleList()










	
