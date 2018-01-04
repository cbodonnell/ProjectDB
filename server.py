'''
# --- TODO ---
Change lane use form to dropdown with an option of other/custom if use has not been identified
Lane uses will be stored in a second database (or new table in data.db?)
Add query form (map and table respond)
Add table of projects (delete, select, etc.)
'''

# --- IMPORTS ---

# Import modules
import sqlite3
import os
# Import flask and other objects/functions
from flask import Flask, flash, request, render_template, redirect
from werkzeug.utils import secure_filename
from flask_googlemaps import Map, GoogleMaps

# --- PROJECT SETTINGS ---

INITIAL_QUERY = 'SELECT * FROM projects'
UPLOAD_FOLDER = 'static\\projectfiles'
ALLOWED_EXTENSIONS = set(['pdf', 'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx'])

# --- FLASK ---

# Create instance of Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- GOOGLE MAPS API ---

GoogleMaps(app, key="AIzaSyCXQrHx19mk6AFy8wny93mhdBslSNxptbw")

# --- URL REQUESTS ---

# Assign a function to a URL
# Index function
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
        conn.commit()

    # Generate map and grab data
    mymap, data = generate_map(conn, c)
    
    return render_template('index.html', mymap=mymap, data=data)

# Function to run when form is submitted
@app.route("/", methods=['POST'])
def hello_data():

    name = request.form['name']
    number = request.form['number']
    if number == '':
        number = 'n/a'
    try:
        year = int(request.form['year'])
    except ValueError:
        year = ''
    uses = request.form['uses']
    if uses == '':
        uses = 'n/a'
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])

    files = []
    for key in request.files:
        file = request.files[key]
        if file and allowed_file(file.filename):
            if not os.path.exists(UPLOAD_FOLDER + '\\' + name):
                os.makedirs(UPLOAD_FOLDER + '\\' + name)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], name, filename))
            files.append(file)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    filePaths = []
    for file in files:
        filePaths.append(file.filename.replace(' ', '_'))

    c.execute('INSERT INTO projects VALUES (?,?,?,?,?,?,?)',
              (name,
               number,
               year,
               uses,
               lat,
               lng,
               ', '.join(filePaths)))
    conn.commit()

    return redirect(request.url)

# --- FUNCTIONS ---

# Function to generate map from DB
def generate_map(conn, c):
    # Queries the database and creates a results array of marker dictionaries
    c.execute(INITIAL_QUERY)
    rows = c.fetchall()
    conn.close()
    results = []
    for row in rows:
        name = row[0]
        number = row[1]
        year = row[2]
        use = row[3]
        files = row[6]
        if number == '':
            numberEntry = ''
        else:
            numberEntry = '<p>Project #: %s</p>'
        if year == '':
            yearEntry = ''
        else:
            yearEntry = ' (%s)' % year
        if use == '':
            useEntry = ''
        else:
            useEntry = '<p>Land Use: %s</p>' % use
        fileEntry = ''
        for file in files.split(", "):
            fileEntry += '<div><a href="static/projectfiles/%s/%s" target="_blank">%s</a></div>' % (name, file, file.split("/")[-1])
        entry = {'lat': row[4],
                 'lng': row[5],
                 'infobox': '<h3>%s%s</h3>%s%s%s' % (name, yearEntry, numberEntry, useEntry, fileEntry)}
        results.append(entry)
    
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=40.7348,
        lng=-73.9229,
        zoom=10,
        style="height:600px;width:100%;margin:0;",
        markers=results,
    )

    return mymap, rows

# Function to check filenames
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- MAIN FUNCTION ---

if __name__ == "__main__":
    app.run(debug=True)