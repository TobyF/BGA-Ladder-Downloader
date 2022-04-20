from flask import Flask, render_template, request
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
        f"POST Result"
        form_data = request.form
        return render_template('data.html',form_data = form_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
