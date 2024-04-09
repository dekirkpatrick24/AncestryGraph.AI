import google.generativeai as genai
import os
import time
from itertools import groupby
from datetime import datetime
from lib.PostgresMySQLLibrary import readSQL, writeSQL
from lib.ReadConfig import readConfig

initConfig = readConfig()
     
Query = """SELECT DISTINCT people.id, people.firstname, people.lastname, people_events.date, people_events.place
			FROM people
			JOIN people_events
			ON people.id = people_events.people_id
            WHERE people.summary = ''
			ORDER BY people.id,people_events.date;
			"""
SQLOutput = readSQL(Query,None)
OutputArray = {
    person_id: "".join(
        (f"{Event[1]} {Event[2]} was born in {Event[4]}" +
         (f" on {Event[3]}" if Event[3] is not None else "") if i == 0 else "")
        + (f" and then moved to {Event[4]}" +
         (f" on {Event[3]}" if Event[3] is not None else "") * (i > 0))  # Add "then moved to" for subsequent events
        for i, Event in enumerate(events)
    )
    for person_id, events in groupby(SQLOutput, key=lambda Event: Event[0])
}

# print(OutputArray)
# quit()

genai.configure(api_key=initConfig['Gemini']['key'])

def GeminiCall(PersonHistory):
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content(f"""You are a knowledgeable historian on the migration of people. In 50 words, explain what you think this person's life was life including occupation and hobbies. Then, list the top 3 possible reasons, in around a 20 word paragraph each, based on historical events of the times, what factors influenced this persons life and migrations: 
    { PersonHistory }                                  
    Base this on known historical events, the person's last name and gender, and do not include generally vague information.""")
    return response.text

for Person in OutputArray:
    try:
        GenAIHistory = GeminiCall(OutputArray[Person])
        # print(GenAIHistory)
        SQLOutput = writeSQL("UPDATE people SET summary = %s WHERE id = %s", (GenAIHistory,Person))
        print(Person)
        time.sleep(5)
    except:
        print("Gemini Error, trying again...")
        time.sleep(30)
    # quit()
