import os
import json
from dotenv import load_dotenv
import mysql.connector
from Directories.controllers.user import User, Volunteer, Organizer, Events

load_dotenv()


def db_connection():                        #function to onnect to the MySQL databasea
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_host"),
            user=os.getenv("DB_user"),
            password=os.getenv("DB_password"),
            database=os.getenv("DB_database")
        )
        return db
    except mysql.connector.Error as error:
        print(f"MySQL error: '{error}' occurred")
        return None

def load_json_file(file_path):              #function to handle readin files
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Error reading {file_path}: {error}")
        return None

def push_attributes_user(user_instance):                       #function to push data from the User class instance to the MySQL table
    db = db_connection()
    if db is None:
        return 
    
    try:
        mycursor = db.cursor()
        
        #MySQL commaond to update user table (structured like as if it was working in MySQL workbench)
        SQLscript = """
        INSERT INTO user (username, userType, userID, email, joinDate, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            userType=VALUES(userType),
            userID=VALUES(userID),
            email=VALUES(email),
            joinDate=VALUES(joinDate),
            password=VALUES(password);
        """
        Values = (
            user_instance.username, user_instance.userType, user_instance.userID,
            user_instance.email, user_instance.joinDate, user_instance.password
        )                                   #values to insert into MySQL user table
        mycursor.execute(SQLscript,Values)      #query table in mySQL database for the user table 
        
        
        db.commit()                             #push updated attributes of User class to MySQL database

    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()

def push_attributes_volunteer(volunteer_instance):         #function to push data from the Volunteer class instance to the MySQL table
    db = db_connection()
    if db is None:
        return 
    
    try:
        mycursor = db.cursor()
        
        #MySQL commaond to update volunteer table (structured as if in MySQL workbench)
        SQLscript = """
        INSERT INTO volunteer (firstName, lastName, DOB, location, gender, hours, preferredCats, history, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            lastName=VALUES(lastName), 
            DOB=VALUES(DOB), 
            location=VALUES(location), 
            gender=VALUES(gender),
            hours=VALUES(hours),
            preferredCats=VALUES(preferredCats),
            history=VALUES(history),
            address=VALUES(address);
        """            
        Values = (
            volunteer_instance.firstName, volunteer_instance.lastName, volunteer_instance.DOB,
            volunteer_instance.location, volunteer_instance.gender, volunteer_instance.hours,
            json.dumps(volunteer_instance.preferredCats), json.dumps(volunteer_instance.history),
            json.dumps(volunteer_instance.address)
        )             #query table in mySQL database for the volunteer table


        db.commit()
    
    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()

def push_attributes_organizer(org_instance):           #function to push data from the Organizer class instance to the MySQL table
    db = db_connection()
    if db is None:
        return 
    
    try:
        mycursor = db.cursor()
        
        #MySQL commaond to update organizer table (structured as if in MySQL workspace)
        SQLscript = """
        INSERT INTO organizer (orgName, EventList)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            EventList=VALUES(EventList);
        """
        Values = (org_instance.orgName, json.dumps(org_instance.events))        #values to insert into MySQL organizer table
        mycursor.execute(SQLscript,Values)             #query table in mySQL database for the organizer table

    
        db.commit()

    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()

def push_attributes_events(event_instance):                #function to push data from the Event class instance to the MySQL table  
    db = db_connection()
    if db is None:
        return event_instance
    
    try:
        mycursor = db.cursor()
        
        #MySQL commaond to update event table (structured as if in MySQL workbench)
        SQLscript = """
        INSERT INTO events (eventID, Name, CurrDate, start_time, end_time, category, vAmount, hoursReward, EventDescription, orgName, ApplicantList, VolunteerList, attendance, hoursDeadline, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Name=VALUES(Name),
            CurrDate=VALUES(CurrDate),
            start_time=VALUES(start_time),
            end_time=VALUES(end_time),
            category=VALUES(category),
            vAmount=VALUES(vAmount),
            hoursReward=VALUES(hoursReward),
            EventDescription=VALUES(EventDescription),
            orgName=VALUES(orgName),
            ApplicantList=VALUES(ApplicantList),
            VolunteerList=VALUES(VolunteerList),
            attendance=VALUES(attendance),
            hoursDeadline=VALUES(hoursDeadline),
            address=VALUES(address);
        """
        Values = (
            event_instance.eventID, event_instance.Name, event_instance.date, event_instance.start_time,
            event_instance.end_time, event_instance.category, event_instance.vAmount, event_instance.hoursReward,
            event_instance.description, event_instance.orgName, json.dumps(event_instance.eventApplicants),
            json.dumps(event_instance.eventVolunteers), event_instance.attendance, event_instance.hoursDeadline,
            json.dumps(event_instance.address)
        )                                                #values to insert into MySQL event table
        mycursor.execute(SQLscript,Values)                #query table in MySQL for the events table  //FIX


        db.commit()

    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()
        

def update_database_from_json():
    users_data = load_json_file('users.json')
    events_data = load_json_file('all_events.json')

    if users_data:
        for user in users_data:
            if user["userType"] == 0:                       #Volunteer
                volunteer_instance = Volunteer(**user)
                push_attributes_volunteer(volunteer_instance)
            elif user["userType"] == 1:                     #Organizer
                organizer_instance = Organizer(**user)
                push_attributes_organizer(organizer_instance)

    if events_data:
        for event in events_data.get("events", []):
            event_instance = Events(**event)
            push_attributes_events(event_instance)
