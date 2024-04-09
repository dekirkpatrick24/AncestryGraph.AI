import mysql.connector
from flask import jsonify
from lib.ReadConfig import readConfig

initConfig = readConfig()

db_params = {
    'host': initConfig['SQLDatabase']['host'],
    'database': initConfig['SQLDatabase']['database'],
    'user': initConfig['SQLDatabase']['username'],
    'password': initConfig['SQLDatabase']['password'],
    'port': initConfig['SQLDatabase']['port']
}

def readSQL(query, params):
	connection = mysql.connector.connect(**db_params)
	cursor = connection.cursor()
	cursor.execute(query, params)
	result_set = cursor.fetchall()
	cursor.close()
	connection.close()
	return result_set

def writeSQL(query,values):
	connection = mysql.connector.connect(**db_params)
	cursor = connection.cursor()
	cursor.execute(query, values)
	connection.commit()
	cursor.close()
	connection.close()


def sqlGetPeopleList():	
	Query = """SELECT
				p.id AS PersonID,
				p.firstname AS PersonFirstName,
				p.lastname AS PersonLastName,
				GROUP_CONCAT(CONCAT(p_parent.firstname, ' ', p_parent.lastname)) AS ParentNames
			FROM
				people p
			LEFT JOIN
				families f1 ON p.id = f1.child_id
			LEFT JOIN
				people p_parent ON f1.parent_id = p_parent.id
			GROUP BY
				p.id, p.firstname, p.lastname"""
	SQLOutput = readSQL(Query,None)
	# print(SQLOutput)
	return SQLOutput

def sqlGetTaxonomyLineage(ID,UpDown):
	Parent = "r.parent_id"
	Child = "r.child_id"
	if UpDown == "down":
		Parent = "r.child_id"	
		Child = "r.parent_id"	
	print("updown",UpDown)
	Query = f"""WITH RECURSIVE Genealogy AS (
		SELECT id, firstname, lastname, NULL AS parent_id, 0 AS generation, summary
		FROM people
		WHERE id = %s -- Assuming you want to start with John

		UNION ALL

		SELECT p.id, p.firstname, p.lastname, r.child_id, g.generation + 1, p.summary
		FROM people p
		JOIN families r ON p.id = {Parent}
		JOIN Genealogy g ON {Child} = g.id
	)
	SELECT DISTINCT Genealogy.id, Genealogy.firstname, Genealogy.lastname, Genealogy.generation,people_events.raw_date,people_events.place,people_events.lat,people_events.lng, Genealogy.summary 
	FROM Genealogy
	JOIN people_events
	ON Genealogy.id = people_events.people_id"""
	SQLOutput = readSQL(Query,(ID,))
	return SQLOutput

def sqlGetTaxonomyLastname(ID,Name):
	Query = """SELECT DISTINCT people.id, people.firstname, people.lastname, NULL,people_events.raw_date,people_events.place,people_events.lat,people_events.lng, people.summary 
	FROM people
	JOIN people_events
	ON people.id = people_events.people_id """
	if ID != None:
		print(ID,Name)
		Query += """WHERE people.lastname = %s ORDER BY people.id"""
		SQLOutput = readSQL(Query,(Name,))	
	else:
		Query += """ORDER BY people.id"""
		SQLOutput = readSQL(Query, None)	
	return SQLOutput