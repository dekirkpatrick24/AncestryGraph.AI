
import requests,time,json, mysql.connector, re
from datetime import datetime
import dateparser

PlaceGPS = {}


# Function to convert date strings to 'YYYY-MM-DD' format
def convert_to_mysql_date(date_string):
    try:
        # Attempt to parse the date string using dateutil.parser
        parsed_date = parser.parse(date_string)
        # Format the parsed date as 'YYYY-MM-DD'
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        return formatted_date
    except ValueError:
        # Handle parsing errors or invalid dates
        return None




DBRead = """SELECT people.ID, people.name, people_events.event_name, people_events.event_date
FROM people
JOIN people_events ON people.ID = people_events.ID;"""

# Replace these values with your MySQL database credentials
db_params = {
    'host': 'localhost',
    'database': 'ancestry',
    'user': 'root',
    'password': 'M3d1t3ch1@dm1n',
    'port': '3306'
}
def WriteToSQL(Array,Type):
    conn = mysql.connector.connect(**db_params)
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO people (id, lastname,firstname)
        VALUES (%s, %s, %s);
        """
    if Type == "people_events":#, lat, lng)#, %s, %s);
        insert_query = """
            INSERT INTO people_events (people_id, date, raw_date, place, lat, lng)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
    #print(tuple(Array))
    cursor.execute(insert_query, tuple(Array))
    conn.commit()
    cursor.close()
    conn.close()


#
# Path to your `.ged` file
file_path = "Kirkpatrick_05_11_18.ged"
CurrentPlace = ""

with open(file_path, 'r') as input_file:
	lines = input_file.readlines()
	# Flag to indicate when to start processing lines
	start_processing = False
	current_id = 0
	individuals_info = {}  # Dictionary to store information for each individual
	NewPerson =0
	# Loop through lines in the file
	for index,line in enumerate(lines):
		if "0 @F1@ FAM" in line:
			break
		# Check if the line contains the specified keyword
		if '1 NAME Ancestry.com Member Trees Submitter' in line:
			start_processing = True
			continue  # Skip this line, do not print it

		# If the flag is True, process lines
		if start_processing:
			# Check if the line starts with '0' (ID)
			#print(line)
			if line.startswith('0'):
				#if current_id != 0:
				#	with open("Backup.json", 'w') as json_file:
	    		#			json.dump(individuals_info, json_file)
				#print(individuals_info)
				current_id = line.strip()
				NewPerson = 0
				CurrentPlace = ""
				individuals_info[current_id] = {'Name': None, 'Events': []}
			# Check if the line starts with '1 NAME'
			elif line.startswith('1 NAME') and current_id != 0 and NewPerson == 0:
				#if "/Spangler/" in line or "/Spengler/" in line:
				#if "/Teal/" in line:	
				print("name",line)		
				NewPerson = current_id
				FirstName = ' '.join(line.split(' ')[2:]).strip().split("/")[0].strip()
				print(len(line.split("/")))
				if len(line.split("/")) == 1:
					current_id = 0
				else:
					LastName = line.split("/")[1].replace("/","").strip()
					individuals_info[current_id]['Name'] = ' '.join(line.split(' ')[2:]).strip().replace("/","")
					WriteToSQL([current_id.replace("0 @I","").replace("@ INDI",""),LastName,FirstName],"people")
					print([current_id.replace("0 @I","").replace("@ INDI",""),LastName,FirstName],"people")
				#else:
				#	del individuals_info[current_id]
				#	current_id = 0

			# Check if the line starts with '1 BIRT' or '1 RESI'
			elif (line.startswith('1 BIRT') or line.startswith('1 RESI') or line.startswith('1 DEAT')) and current_id != 0:
				date_line = lines[index + 1].strip()
				place_line = lines[index + 2].strip() 
				if date_line.startswith('2 PLAC') or date_line.startswith('2 DATE'): #date_line.startswith('2 DATE') and 
					if date_line.startswith('2 DATE') and place_line.startswith('2 PLAC'):
						date = date_line.split(' ', 2)[2].strip()
						place = place_line.split(' ', 2)[2].strip()
					elif date_line.startswith('2 PLAC'):
						place = date_line.split(' ', 2)[2].strip()
						date = ""	
					else:
						print("NO PLACE, MOVING ON")
						continue					
					if CurrentPlace.split(" ")[0] != place.split(" ")[0]:
						if place not in PlaceGPS:
							PlaceGeo = requests.get("https://api.opencagedata.com/geocode/v1/json?key=2e05f3a5a6f14c7d814afa6f2857f3e8&q=" + place.replace(",",""))
							if PlaceGeo.status_code != 200:
								quit()
							PlaceGeoJSON = PlaceGeo.json()
							print("FROM OPENCAGE")
							if PlaceGeoJSON["results"] != []:
								Lat = PlaceGeoJSON["results"][0]["geometry"]["lat"]
								Lng = PlaceGeoJSON["results"][0]["geometry"]["lng"]
								#PlaceGPS.setdefault(place,[])
								PlaceGPS[place] = [PlaceGeoJSON["results"][0]["geometry"]["lat"],PlaceGeoJSON["results"][0]["geometry"]["lng"]]
							else:
								Lat = 0
								Lng = 0
						else:
							print("FROM CACHE")
							#print(PlaceGPS)
							Lat = PlaceGPS[place][0]
							Lng = PlaceGPS[place][1]
						#print(PlaceGeoJSON)
						if Lat != 0 and Lng != 0:
							individuals_info[current_id]['Events'].append({'Date': date, 'Place': place, 'LatLng': [Lat,Lng]})
							try:
								parsed_date = dateparser.parse(date.replace("abt.",""))
								ParsedDate = parsed_date.strftime('%Y-%m-%d')
								if len(date) == 4:
									ParsedDate = parsed_date.replace(month=1, day=1).strftime('%Y-%m-%d')
							except Exception as e:
								# If dateutil.parser encounters an unknown format, try to find the first date string and parse it
								first_date_match = re.search(r'\b(\d{4})\b', date)
								if first_date_match:
									first_date = first_date_match.group(1)
									parsed_date = dateparser.parse(first_date).replace(month=1, day=1)
									ParsedDate = parsed_date.strftime('%Y-%m-%d')
								else:
									ParsedDate = None
									date = None
							print([current_id.replace("0 @I","").replace("@ INDI",""),ParsedDate,date,place,Lat,Lng],"people_events") #PlaceGeoJSON["results"][0]["geometry"]["lat"],PlaceGeoJSON["results"][0]["geometry"]["lng"]],"people_events")
							WriteToSQL([current_id.replace("0 @I","").replace("@ INDI",""),ParsedDate,date,place,Lat,Lng],"people_events")						
						
						time.sleep(1)

						#individuals_info[current_id]['Events'].append({'Date': date, 'Place': place})
						#print(individuals_info[current_id]['Name'],date,place)
						#print(current_id)
						CurrentPlace = place

print(individuals_info)
print(len(individuals_info))
print("DONE")
	
	
	
	
	
	



