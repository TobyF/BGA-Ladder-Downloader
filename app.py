from flask import Flask, render_template, request, send_from_directory, send_file
from bga_ladder_tools import get_flight_ids, get_pilot_id, get_and_zip_igcs
import tempfile
import zipfile
import io
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/downloader')
def downloader():
    return render_template('downloader.html')

@app.route('/data', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/downloader' to submit form"
    if request.method == 'POST':

        pilot_id = request.form['pilot_id']
        flight_ids = get_flight_ids(pilot_id)
        with tempfile.TemporaryDirectory() as tmpdir:
            print('created temporary directory', tmpdir)
            flights_zip = get_and_zip_igcs(flight_ids,tmpdir)
        #flights_zip_loc = 'test_data/flights.zip'
        #print(flights_zip_loc)
        #with open(flights_zip_loc,'r') as f:
        #    content = f.read()
        return send_file(flights_zip,as_attachment=True, download_name='flights.zip')

@app.route('/pilotdata')
def pilotdata():
    return send_from_directory('static','active_pilots.txt',as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
