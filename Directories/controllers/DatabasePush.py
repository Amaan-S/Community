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

def push_attributes_user(user_instance):                       #function to push data from the User class instance to the MySQL table
    db = db_connection()
    if db is None:
        return user_instance
    
    try:
        mycursor = db.cursor()
        
        SQLscript = "UPDATE user SET username=%s, userType=%s, userID=%s, joinDate=%s, password=%s WHERE email=%s"              #MySQL commaond to update user table
        Values = (user_instance.username, user_instance.userType, user_instance.userID, user_instance.joinDate, user_instance.password, user_instance.email)        #values to insert into MySQL user table
        mycursor.execute(SQLscript,Values)      #query table in mySQL database for the user table 
        
        
        db.commit()                             #push updated attributes of User class to MySQL database

    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()
    return user_instance                        #return updated class instance

def push_attributes_volunteer(volunteer_instance):         #function to push data from the Volunteer class instance to the MySQL table
    db = db_connection()
    if db is None:
        return volunteer_instance
    
    try:
        mycursor = db.cursor()
        SQLscript = "UPDATE volunteer SET lastName=%s, DOB=%s, location=%s, gender=%s, preferredCats=%s, hours=%s, history=%s WHERE firstName=%s"              #MySQL commaond to update volunteer table
        Values = (volunteer_instance.lastName,volunteer_instance.DOB,volunteer_instance.location,volunteer_instance.gender,volunteer_instance.preferredCats,volunteer_instance.hours,volunteer_instance.history,volunteer_instance.firstName)        #values to insert into MySQL volunteer table
        mycursor.execute(SQLscript,Values)             #query table in mySQL database for the volunteer table


        db.commit()
    
    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()
    return volunteer_instance           #return updated class instance

def push_attributes_organizer(org_instance):           #function to push data from the Organizer class instance to the MySQL table
    db = db_connection()
    if db is None:
        return org_instance
    
    try:
        mycursor = db.cursor()
        SQLscript = "UPDATE organizer SET EventList=%s WHERE orgName=%s"              #MySQL commaond to update organizer table
        Values = (org_instance.events,org_instance.orgName)        #values to insert into MySQL organizer table
        mycursor.execute(SQLscript,Values)             #query table in mySQL database for the organizer table

    
        db.commit()

    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()
    return org_instance                 #return updated class instance

def push_attributes_events(event_instance):                #function to push data from the Event class instance to the MySQL table  
    db = db_connection()
    if db is None:
        return event_instance
    
    try:
        mycursor = db.cursor()
        SQLscript = "UPDATE user SET Name=%s,CurrDate=%s,start_time=%s,end_time=%s,address=%s,category=%s,vAmount=%s,hoursReward=%s,EventDescription=%s,orgName=%s,ApplicantList=%s,VolunteerList=%s,attendance=%s,hoursDeadline=%s WHERE eventID=%s"              #MySQL commaond to update event table
        Values = (event_instance.Name,event_instance.date,event_instance.start_time,event_instance.end_time,event_instance.address,event_instance.category,event_instance.vAmount,event_instance.hoursReward,event_instance.description,event_instance.orgName,event_instance.eventApplicants,event_instance.eventVolunteers,event_instance.attendanceAccounted,event_instance.hoursDeadline,event_instance.eventID)        #values to insert into MySQL event table
        mycursor.execute(SQLscript,Values)                #query table in MySQL for the events table  //FIX


        db.commit()

    except mysql.connector.Error as error:
        print(f"Database error: {error}")
    finally:
        mycursor.close()
        db.close()
    return event_instance                   #return updated class instance