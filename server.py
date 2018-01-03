''' --- TODO ---
    Account for entries with no files
    Allow for multiple file entries
    Add query form
    Add table of projects (delete, select, etc.)
'''

# Import flask
from flask import Flask, flash, request, render_template, redirect, url_for
from flask_googlemaps import Map, GoogleMaps

# Create instance of Flask
app = Flask(__name__)

# Import modules
import sqlite3
import os.path
from werkzeug.utils import secure_filename

GoogleMaps(app, key="AIzaSyCXQrHx19mk6AFy8wny93mhdBslSNxptbw")

UPLOAD_FOLDER = 'static\\projectfiles'
ALLOWED_EXTENSIONS = set(['pdf', 'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assign a function to a URL
# Google Maps example
@app.route("/")
def mapview():

    # Set up DB connection
    if os.path.exists('data.db'):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

    # Creates new table if one does not exist
    else:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE projects(
                        name text,
                        num text,
                        year int,
                        use text,
                        lat decimal,
                        lng decimal,
			filePath text)''')
        sampleData = [('Kings/Flatbush Parking', '26179.00', 2017, 'Destination Retail', 40.6460, -73.9561, 'example.pdf'),
                      ('Bobover School', '29586.00', 2017, 'School K-5', 40.6412, -73.9837, 'example.pdf'),
                      ('Lower Concourse North', '29753.00', 2016, 'Residential, Local Retail, Open Space', 40.8197, -73.9310, 'example.pdf')]    
        c.executemany('INSERT INTO projects VALUES (?,?,?,?,?,?,?)', sampleData)
        conn.commit()

    # Generate map and grab data
    mymap, data = generate_map(conn, c)
    
    return render_template('index.html', mymap=mymap, data=data)

# Function to run when button is pressed
@app.route("/", methods=['POST'])
def hello_data():
    
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
    else:
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    name = request.form['name']
    number = request.form['number']
    year = int(request.form['year'])
    uses = request.form['uses']
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])
    filePath = file.filename.replace(' ', '_')

    c.execute('INSERT INTO projects VALUES (?,?,?,?,?,?,?)',
              (name,
               number,
               year,
               uses,
               lat,
               lng,
               filePath))
    conn.commit()

    # Generate map and grab data
    mymap, data = generate_map(conn, c)
    
    return render_template('index.html', mymap=mymap, data=data)

'''
# File upload
@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
'''
    
# Function to generate map from DB
def generate_map(conn, c):
    # Queries the database and creates a results array of marker dictionaries
    c.execute('SELECT * FROM projects')
    rows = c.fetchall()
    conn.close()
    results = []
    for row in rows:
        entry = {'lat': row[4],
                 'lng': row[5],
                 'infobox': '<h3>%s (%s)</h3><p>Project #: %s</p><p>Land Use: %s</p><a href="static/projectfiles/%s" target="_blank">%s</a>' % (row[0], row[2], row[1], row[3], row[6], row[6].split("/")[-1])}
        results.append(entry)
    
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=40.7348,
        lng=-73.9229,
        zoom=10,
        style="height:600px;width:600px;margin:0;",
        markers=results,
    )

    return mymap, rows

# Function to check filenames
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
if __name__ == "__main__":
    app.run(debug=True)
