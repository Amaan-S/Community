import os
import json
import mysql.connector
from dotenv import load_dotenv
from Directories.controllers.user import User, Volunteer, Organizer, Events
from decimal import Decimal

load_dotenv()

Volunteers = []         #list will hold the Volunteer class elements pulled from the database
Organizers = []         #list will hold the organizer class elements pulled from the database
events = []             #list will hold the events class elements pulled from the database

def db_connection():                        #function to onnect to the MySQL databasea
    try:
        db = mysql.connector.connect(               #reads environment variables from render and lads in database credentials
            host = os.getenv("DB_host"),
            user = os.getenv("DB_user"),
            password = os.getenv("DB_password"),
            database = os.getenv("DB_database")
        )
        return db
    except mysql.connector.Error as error:                      #error message for instance of unsucessful database connection
        print(f"MySQL error: '{error}' occurred")
        return None

def fetch_attributes_user():                       #function to fetch data from the MySQL database for the User class instance
    db = db_connection()
    if db is None:
        return []                #return an empty list on ocassion no database connection occurred
    
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM user")      #query table in mySQL database for the user table
        result = mycursor.fetchall()
        users = []              #list will hold the User class elements pulled from the database

        if result:
            for row in result:                      #copy row data and assign it to each attribute in backend for User class (do this for each instance of a user)
                user = User(
                    username = row[0],
                    userType = row[1],
                    userID = row[2],
                    email = row[3],
                    joinDate = row[4],
                    password = row[5]
                )
                users.append(user)              #add to the list that holds the users in the database
        return users               #return the list of users that holds all user data pulled from the database
    except mysql.connector.Error as error:
        print(f"Database error: {error}")
        return []   # return empty list on instance of no users being found
    finally:                #close the database after reading the user table
        mycursor.close()
        db.close()

def fetch_attributes_volunteer():         #function to fetch data grom the MySQL database for the Volunteer class instance
    db = db_connection()
    if db is None:
        return []
    
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM volunteer")             #query table in mySQL database for the volunteer table
        result = mycursor.fetchall()
        volunteers = []              #list will hold the Volunteer class elements pulled from the database

        if result:
            for row in result:                              #copy row data and assign it to each attribute in backend for Volunteer class
                volunteer = Volunteer(
                    firstName = row[0],
                    lastName = row[1],
                    DOB = row[2],
                    location = row[3],
                    gender = row[4],
                    hours = Decimal(str(row[6])),
                    preferredCats = json.loads(row[5]),
                    history = json.loads(row[7]),
                    address = json.loads(row[8])
                )
                volunteers.append(volunteer)              #add to the list that holds the volunteers in the database
        return volunteers                                   #return the list of Volunteer data
    except mysql.connector.Error as error:
        print(f"Database error: {error}")
        return []   # return empty list on instance of no volunteers being found
    finally:
        mycursor.close()
        db.close()

def fetch_attributes_organizer():           #function to fetch data from the mySQL database for the Organizer class instance
    db = db_connection()
    if db is None:
        return []
    
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM organizer")             #query table in mySQL database for the organizer table
        result = mycursor.fetchall()
        organizers = []         #list of organizer objects that stores information pulled from the database      
        
        if result:
            for row in result:              #copy row data and assign it to each attribute in backend for Organizer class
                organizer = Organizer(
                    orgName = row[0],
                    events = json.loads(row[1])
                )
            organizers.append(organizer)            #return the list with the organizer user data
        return organizers               #return the list of organizer data pulled from the database
    except mysql.connector.Error as error:
        print(f"Database error: {error}")
        return []   # return empty list on instance of no organizers being found
    finally:
        mycursor.close()
        db.close()

def fetch_attributes_events():                #function to fetch data from the mySQL database for the Event class instance
    db = db_connection()
    if db is None:
        return []
    
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM events")                #query table in MySQL for the events table
        result = mycursor.fetchall()
        events = []                                             #list of event objects that stores information pulled from the database

        if result:
            for row in result:                          #copy row data and assign it to each attribute in backend for Event class
                event = Events(
                    eventID=row[0],
                    Name=row[1],
                    date=row[2],
                    start_time=row[3],
                    end_time=row[4],
                    category=row[5],
                    vAmount=Decimal(str(row[6])),  
                    hoursReward=Decimal(str(row[7])),  
                    description=row[8],  
                    orgName=row[9],
                    eventApplicants=json.loads(row[10]),  # Parse JSON
                    eventVolunteers=json.loads(row[11]),  # Parse JSON
                    attendanceAccounted=row[12],
                    hoursDeadline=row[13], 
                    address=row[14]  # Parse address JSON
                )
                events.append(event)              #add to the list that holds the events in the database
        return events   #return the list of events
    except mysql.connector.Error as error:
        print(f"Database error: {error}")
        return []   # return empty list on instance of no events being found
    finally:
        mycursor.close()
        db.close()
