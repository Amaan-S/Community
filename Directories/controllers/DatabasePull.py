import mysql.connector
from user import User, Volunteer, Organizer, Events

def db_connection():                        #function to onnect to the MySQL databasea
    try:
        db = mysql.connector.connect(
            host="127.7.5.2",
            user="root",
            password="BHeartedD123*",
            database="3444db-p1"
        )
        return db
    except mysql.connector.Error as error:
        print(f"MySQL error: '{error}' occurred")
        return None

def fetch_attributes_user(user_instance):                       #function to fetch data from the MySQL database for the User class instance
    db = db_connection()
    if db is None:
        return user_instance
    
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM user")      #query table in mySQL database for the user table
        result = mycursor.fetchall()

        if result:
            for row in result:                      #copy row data and assign it to each attribute in backend for User class
                user_instance.username = row[0]
                user_instance.userType = row[1]
                user_instance.userID = row[2]
                user_instance.email = row[3]
                user_instance.joinDate = row[4]
                user_instance.password = row[5]
    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()
    return user_instance                        #return updated class instance

def fetch_attributes_volunteer(volunteer_instance):         #function to fetch data grom the MySQL database for the Volunteer class instance
    db = db_connection()
    if db is None:
        return volunteer_instance
    
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM volunteer")             #query table in mySQL database for the volunteer table
        result = mycursor.fetchall()

        if result:
            for row in result:                              #copy row data and assign it to each attribute in backend for Volunteer class
                volunteer_instance.firstName = row[0]
                volunteer_instance.lastName = row[1]
                volunteer_instance.DOB = row[2]
                volunteer_instance.location = row[3]
                volunteer_instance.gender = row[4]
                volunteer_instance.preferredCats = row[5]
                volunteer_instance.hours = row[6]
                volunteer_instance.history = row[7]
    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()
    return volunteer_instance           #return updated class instance

def fetch_attributes_organizer(org_instance):           #function to fetch data from the mySQL database for the Organizer class instance
    db = db_connection()
    if db is None:
        return org_instance
    
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM organizer")             #query table in mySQL database for the organizer table
        result = mycursor.fetchall()

        if result:
            for row in result:              #copy row data and assign it to each attribute in backend for Organizer class
                org_instance.orgName = row[0]
                org_instance.events = row[1]
    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()
    return org_instance                 #return updated class instance

def fetch_attributes_events(event_instance):                #function to fetch data from the mySQL database for the Event class instance
    db = db_connection()
    if db is None:
        return event_instance
    
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM events")                #query table in MySQL for the events table
        result = mycursor.fetchall()

        if result:
            for row in result:                          #copy row data and assign it to each attribute in backend for Event class
                event_instance.eventID = row[0]
                event_instance.Name = row[1]
                event_instance.date = row[2]
                event_instance.start_time = row[3]
                event_instance.end_time = row[4]
                event_instance.address = row[5]
                event_instance.category = row[6]
                event_instance.vAmount = row[7]
                event_instance.hoursReward = row[8]
                event_instance.description = row[9]
                event_instance.orgName = row[10]
                event_instance.eventApplicants = row[11]
                event_instance.eventVolunteers = row[12]
                event_instance.attendanceAccounted = row[13]
                event_instance.hoursDeadline = row[14]
    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()
    return event_instance                   #return updated class instance
