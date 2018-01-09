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
                        id integer primary key autoincrement,
                        name text,
                        num text,
                        year int,
                        use text,
                        lat decimal,
                        lng decimal,
                        filePath text)''')
        conn.commit()

    # Set query
    query = INITIAL_QUERY

    # Generate map and grab data
    mymap, data = generate_map(conn, c, query)
    
    return render_template('index.html', mymap=mymap, data=data)

# Function to run when form is submitted
@app.route("/", methods=['POST'])
def hello_data():

    # Handle input from entry form
    if request.form['submit'] == 'Submit':
        
        name = request.form['name']
        number = request.form['number']
        try:
            year = int(request.form['year'])
        except ValueError:
            year = ''
        uses = request.form['uses']
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

        c.execute('INSERT INTO projects VALUES (?,?,?,?,?,?,?,?)',
                  (None,
                   name,
                   number,
                   year,
                   uses,
                   lat,
                   lng,
                   ', '.join(filePaths)))
        conn.commit()

        return redirect(request.url)

    # Handle deletions
    # TODO: Delete project files as well!!
    elif RepresentsInt(request.form['submit']):
            
        project_id = request.form['submit']

        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        c.execute('DELETE FROM projects WHERE id=?',
                  (project_id,))
        conn.commit()
        
        return redirect(request.url)

    else:
        print('This should not print!')

# --- FUNCTIONS ---

# Function to generate map from DB
def generate_map(conn, c, query):
    # Queries the database and creates a results array of marker dictionaries
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    results = []
    for row in rows:
        name = row[1]
        number = row[2]
        year = row[3]
        use = row[4]
        files = row[7]
        if number == '':
            numberEntry = ''
        else:
            numberEntry = '<p>Project #: %s</p>' % number
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
        entry = {'title': str(row[0]),
                 'lat': row[5],
                 'lng': row[6],
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

# Function to check if string contains an integer
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# --- MAIN FUNCTION ---

if __name__ == "__main__":
    app.run(debug=True)
