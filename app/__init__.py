import os 
import sqlalchemy 
from sqlalchemy import text, exc
from yaml import load, Loader 
from flask import Flask, render_template, request
import mysql.connector
app = Flask(__name__)

def init_connect_engine():
    if os.environ.get('GAE_ENV') != 'standard': #a file that will appear on GCP 
        variables = load(open("app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername = "mysql+pymysql",
            username = os.environ.get('MYSQL_USER'),
            password = os.environ.get('MYSQL_PASSWORD'), 
            database = os.environ.get('MYSQL_DB'), 
            host = os.environ.get('MYSQL_HOST'),
            port=3306,  # Replace with your MySQL port
            query={"charset": "utf8"}
        )
    )
    return pool 

db = init_connect_engine()

def getMaximumRecordNumber():
    conn = db.connect()
    query = text('SELECT MAX(Record_Number) FROM Cases;')
    max_record = conn.execute(query)
    conn.close()

    to_return = 0

    for result in max_record:
        to_return = result[0]

    return to_return + 1

max_record_number = getMaximumRecordNumber()

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        crime_code = request.form.get("crime_code")
        location = request.form.get("location")
        weapon = request.form.get("weapon")
        result_count = int(request.form.get('result_count', 10))  # Default to 10 if not selected

        print(weapon)
        print(crime_code)
        print(location)
        if (not crime_code and not location and not weapon):
            query = text(f"""
            SELECT  Crime_Code_Desc, Area_Name, Weapon_Code_Desc, Victim_Age, Victim_Sex, Date_Occurred
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            LIMIT {result_count}
            """)   
            long = text(f"""
            SELECT Longitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            LIMIT {result_count}         
            """)    

            lat = text(f"""
            SELECT Latitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            LIMIT {result_count}  """)  

        if(crime_code and not location and not weapon):
            query = text(f"""
            SELECT  Crime_Code_Desc, Area_Name, Weapon_Code_Desc, Victim_Age, Victim_Sex, Date_Occurred
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Crime_Code_Desc = "{crime_code}" 
            LIMIT {result_count}
            """)    
            #query for returning longittude and latitude from the main query 
            long = text(f"""
            SELECT Longitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE  Crime_Code_Desc = "{crime_code}" 
            LIMIT {result_count}         
            """)    

            lat = text(f"""
            SELECT Latitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE  Crime_Code_Desc = "{crime_code}" 
            LIMIT {result_count}         
            """) 

        if(not crime_code and location and not weapon):
            query = text(f"""
            SELECT  Crime_Code_Desc, Area_Name, Weapon_Code_Desc, Victim_Age, Victim_Sex, Date_Occurred
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" 
            LIMIT {result_count}
            """)    
            #query for returning longittude and latitude from the main query 
            long = text(f"""
            SELECT Longitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" 
            LIMIT {result_count}         
            """)    

            lat = text(f"""
            SELECT Latitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" 
            LIMIT {result_count}         
            """)     
        
        if(not crime_code and not location and weapon):

            query = text(f"""
            SELECT  Crime_Code_Desc, Area_Name, Weapon_Code_Desc, Victim_Age, Victim_Sex, Date_Occurred
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}
            """)    
            #query for returning longittude and latitude from the main query 
            long = text(f"""
            SELECT Longitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}         
            """)    

            lat = text(f"""
            SELECT Latitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}         
            """) 
        if(crime_code and location and not weapon):
            query = text(f"""
            SELECT  Crime_Code_Desc, Area_Name, Weapon_Code_Desc, Victim_Age, Victim_Sex, Date_Occurred
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" AND Crime_Code_Desc = "{crime_code}" 
            LIMIT {result_count}
            """)    
            #query for returning longittude and latitude from the main query 
            long = text(f"""
            SELECT Longitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" AND Crime_Code_Desc = "{crime_code}" 
            LIMIT {result_count}         
            """)    

            lat = text(f"""
            SELECT Latitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" AND Crime_Code_Desc = "{crime_code}" 
            LIMIT {result_count}         
            """)

        if(crime_code and not location and weapon):
            query = text(f"""
            SELECT  Crime_Code_Desc, Area_Name, Weapon_Code_Desc, Victim_Age, Victim_Sex, Date_Occurred
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Crime_Code_Desc = "{crime_code}" AND Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}
            """)    
            #query for returning longittude and latitude from the main query 
            long = text(f"""
            SELECT Longitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Crime_Code_Desc = "{crime_code}" AND Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}         
            """)    

            lat = text(f"""
            SELECT Latitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Crime_Code_Desc = "{crime_code}" AND Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}         
            """)         
            
        if(not crime_code and location and weapon):
            query = text(f"""
            SELECT  Crime_Code_Desc, Area_Name, Weapon_Code_Desc, Victim_Age, Victim_Sex, Date_Occurred
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}"  AND Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}
            """)    
            #query for returning longittude and latitude from the main query 
            long = text(f"""
            SELECT Longitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" AND Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}         
            """)    

            lat = text(f"""
            SELECT Latitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" AND Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}         
            """)         

        if(crime_code and location and weapon):
            query = text(f"""
            SELECT  Crime_Code_Desc, Area_Name, Weapon_Code_Desc, Victim_Age, Victim_Sex, Date_Occurred
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" AND Crime_Code_Desc = "{crime_code}" AND Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}
            """)    
            #query for returning longittude and latitude from the main query 
            long = text(f"""
            SELECT Longitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" AND Crime_Code_Desc = "{crime_code}" AND Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}         
            """)    

            lat = text(f"""
            SELECT Latitude
            FROM Cases NATURAL JOIN Weapons NATURAL JOIN Location NATURAL JOIN Victim NATURAL JOIN CrimeCodes
            WHERE Area_name = "{location}" AND Crime_Code_Desc = "{crime_code}" AND Weapon_Code_Desc = "{weapon}"
            LIMIT {result_count}         
            """)         

        results = db.connect().execute(query).fetchall()
        longitude = db.connect().execute(long).fetchall()
        latitude = db.connect().execute(lat).fetchall()
        longitude = listhelper(longitude)
        latitude = listhelper(latitude)

        #lower_limit = 0.1
        #upper_limit = 0.5

        #longitude = [x + random.uniform(lower_limit, upper_limit) for x in longitude]
        #latitude = [x + random.uniform(lower_limit, upper_limit) for x in latitude]

        coordinates = [{'lat': lat, 'lng': lng} for lat, lng in zip(latitude, longitude)]
        print(coordinates)
        print(longitude)
        print(latitude)
        
        return render_template("index.html", results=results, location=location, crime_code=crime_code, weapon = weapon, coordinates = coordinates, result_count = result_count)
            
    return render_template("index.html")


@app.route('/report', methods=['GET', 'POST'])
def report():

    global max_record_number
    
    print(max_record_number)

    if request.method == "POST":

        weapon_code = request.form.get("weapon_code")
        date_occurred = request.form.get("date_occurred") + " 12:00:00 AM"
        time_occurred = request.form.get("time_occurred")
        crime_code = request.form.get("crime_code")
        victim_age = request.form.get("victim_age")
        gender = request.form.get("gender")
        descent = request.form.get("descent")
        location = request.form.get("location")
        longitude = request.form.get("longitude")
        latitude = request.form.get("latitude")
    
        case_query = 'INSERT INTO Cases VALUES("{}","{}","{}","{}","{}");'.format(max_record_number, weapon_code, date_occurred, time_occurred, crime_code)
        victim_query = 'INSERT INTO Victim VALUES("{}","{}","{}","{}");'.format(max_record_number, victim_age, gender, descent)
        location_query = 'INSERT INTO Location VALUES("{}","{}","{}","{}");'.format(max_record_number, location, longitude, latitude)

        mydb = mysql.connector.connect(
            host="34.31.229.136",
            user="root",
            password="12345",
            database="cs411database"
        )

        mycursor = mydb.cursor()
        mycursor.execute(case_query, params=None)
        results = mycursor.fetchall()
        mydb.commit()

        max_record_number += 1

    return render_template('report.html')

@app.route('/funfacts')
def funfacts():

    conn = db.connect()

    call_procedure = text('CALL data_procedure;')
    query_location = text('SELECT * FROM LocationDescent')
    query_victim = text('SELECT * FROM VictimAge ORDER BY VictimCount DESC')

    conn.execute(call_procedure)

    query_location_results = conn.execute(query_location).fetchall()
    query_victim_results = conn.execute(query_victim).fetchall()
    conn.close()

    return render_template('funfacts.html', results_location_descent=query_location_results, results_victim_age=query_victim_results)

@app.route('/delete', methods=['GET', 'POST'])
def delete():

    if request.method == "POST":

        record_number = request.form.get("record_number")
        print("record number: " + record_number)

        conn = db.connect()
        query = text('DELETE FROM Cases WHERE Record_Number = {};'.format(int(record_number)))
        print(query)
        conn.execute(query)
        conn.close()

    return render_template('delete.html')

@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == "POST":

        record_number = request.form.get("record_number")
        crime_code = request.form.get("crime_code")
        print("record number: " + record_number)
        print("crime code: " + crime_code)

        conn = db.connect()
        query = text('UPDATE Cases SET Crime_Code = {} WHERE Record_Number = {};'.format(int(crime_code), int(record_number)))
        print(query)
        conn.execute(query)
        conn.close()

    return render_template('update.html')


def listhelper(x):
    newx = []
    for i in range(len(x)):
        newx.append(x[i][0])
    return newx

