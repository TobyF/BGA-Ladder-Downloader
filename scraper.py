import requests
from bs4 import BeautifulSoup
import re
import json


PILOT_ID = 3851
for year in range(2017,2021):

    query_url = f"https://bgaladder.net/API/DailyScores?Season={year}&Pilot={PILOT_ID}"
    page = requests.get(query_url)
    page_json = json.loads(page.content)
    for flight in page_json["rows"]:
        print(flight["FlightID"])

#URL_BASE = "https://bgaladder.net/FlightDetails/"
#84318 is a toby flight
#3851 is toby id
#for flight_id in range(80000,98931):
#    page = requests.get(URL_BASE+str(flight_id))
#    soup = BeautifulSoup(page.content, "html.parser")
#    pilotID_line = soup.find(attrs={"id": "hidPilotID"})
#    if pilotID_line is None:
#        print(soup)
#        continue
#    pilotID = int(pilotID_line['value'])
#    print(f'Flight ID: {flight_id}, Pilot ID: {pilotID}')
#    if pilotID == 3851:
#        print('We found a toby flight!!!!!!!!!!!!!!!!!!')
    #<input type="hidden" id="hidPilotID" value="3851" />
