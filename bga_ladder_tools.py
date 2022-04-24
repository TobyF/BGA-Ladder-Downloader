import json
import requests
from urllib.request import urlopen
import ssl
import re
import shutil
import os
import zipfile
import io
import concurrent.futures

def get_pilot_id(name):
    pass

def get_names():
    query_url = f"https://bgaladder.net/API/pilots"
    page = requests.get(query_url)
    page_json = json.loads(page.content)
    return page_json

def get_flight_ids(pilot_id,start_year=2022,end_year=2022):
    flightIDs = []
    for year in range(start_year,end_year+1):
        query_url = f"https://bgaladder.net/API/DailyScores?Season={year}&Pilot={pilot_id}"
        page = requests.get(query_url)
        page_json = json.loads(page.content)
        for flight in page_json["rows"]:
            flightIDs.append(flight["FlightID"])
    return flightIDs

def download_igc_file(flight_id, dir):
    url = f'http://bgaladder.net/FlightIGC/{flight_id}'
    r = requests.get(url, allow_redirects=True)
    try:
        d = r.headers['content-disposition']
        fname = ((re.findall("filename=(.+)", d)[0]).split(';')[0]).strip('"') #extracts filename, likely dodgy.
    except KeyError:
        fname=f"{flight_id}.igc"
    print(fname)
    print(dir)
    print(os.path.join(dir,fname))
    with open(os.path.join(dir,fname), 'wb') as f:
        f.write(r.content)

def get_and_zip_igcs(flight_ids,tmpdir,multithreading=True):
    base_path = os.path.join(tmpdir,'flights')
    os.makedirs(base_path)
    print(base_path)

    if multithreading:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for flight_id in flight_ids:
                futures.append(executor.submit(download_igc_file,flight_id=flight_id, dir=base_path))
    else:
        for flight_id in flight_ids:
            download_igc_file(flight_id=flight_id, dir=base_path)


    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in os.listdir(path=base_path):
            z.write(os.path.join(base_path,f_name),arcname = f_name)
    data.seek(0)
    #zip_loc = shutil.make_archive(os.path.join(tmpdir,'flights'),'zip',os.path.join(tmpdir,'flights'))
    return data

if __name__ == '__main__':
    print("Testing...")
    print("Getting Names:")
    print(get_names())
    #print('Flight IDs :')
    #print(get_flight_ids(3851))
    print('Downloading IGC file:')
    #download_igc_file(66505, 'test_data')


    dir = os.path.join(os.getcwd(),'test_data')
    print(f"Making a test directory: {dir}")
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

    print(get_and_zip_igcs(get_flight_ids(3851),dir))
