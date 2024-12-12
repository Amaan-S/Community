import os
import json
from dotenv import load_dotenv
from user import User, Volunteer, Organizer, Events
from DatabasePull import db_connection, fetch_attributes_user, fetch_attributes_volunteer, fetch_attributes_organizer, fetch_attributes_events

def fetch_all_data():
    # Fetch user data using fetch
    user_data = fetch_attributes_user()

    # Fetch volunteer data
    volunteer_data = fetch_attributes_volunteer()

    # Fetch organizer data
    organizer_data = fetch_attributes_organizer()
    
    # Fetch events data
    event_data = fetch_attributes_events()

    return user_data, volunteer_data, organizer_data, event_data            #return all the data recieved from the database


def update_json_file(file_path, user_data, volunteer_data, organizer_data, event_data):
    
    # Load existing users.json data
    try:
        with open('users.json', 'r') as file:          #open json file for reading
            existing_data_users = json.load(file)
    except FileNotFoundError:
        existing_data_users = []


    # Load existing events.json data
    try:
        with open('all_events.json', 'r') as file:
            existing_events_data = json.load(file)
    except FileNotFoundError:
        existing_events_data = {"events": []}
    
    
    
    v_index = 0 #index for the volunteer data
    o_index = 0 #index for the organizer data
    
    volunteers = [] # list to hold the volunteer profiles
    organizers = [] # list to hold the organizer profiles
    events = []     # list to hold the event profiles
    
    
    # Transform data into JSON format and ensure that the data is assigned correctly to a user or volunteer
    for user in user_data:
        if user.userType == 0:  # Volunteer
            if v_index < len(volunteer_data):               #populate up until the number of volunteers
                vol_data = volunteer_data[v_index]          #assign the user data for one indexed volunteer to vol_data
                volunteer = Volunteer(
                    userType = user.userType,       #start populating data from the base user class
                    userID = user.userID,
                    email = user.email,
                    joinDate = user.joinDate,
                    username = user.username,
                    password = user.password,
                    firstName = vol_data["firstName"],      #start building the rest of the volunteer data
                    lastName = vol_data["lastName"],
                    DOB = vol_data["DOB"],
                    location = vol_data.get("location"),
                    gender = vol_data.get("gender"),
                    preferredCats = vol_data.get("preferredCats", []),
                    hours = vol_data.get("hours", 0),
                    history = vol_data.get("history", [])
                )
                volunteers.append(volunteer.to_dict())
                v_index += 1        #increment the index of the volunteer

        elif user.userType == 1:  # Organizer
            if o_index < len(organizer_data):
                org_data = organizer_data[o_index]      #assign the user data for one indexed organizer to org_data
                organizer = Organizer(
                    userType=user.userType,         #start populating data form the base user class
                    userID=user.userID,
                    email=user.email,
                    joinDate=user.joinDate,
                    username=user.username,
                    password=user.password,
                    orgName=org_data["orgName"],            #start building the rest of the organizer data
                    events=org_data.get("events", []),
                    address=org_data.get("address", {})
                )
                organizers.append(organizer.to_dict())
                o_index += 1
                
    total = volunteers + organizers   
                
    # Avoid duplicates in users.json
    existing_user_ids = {entry["userID"] for entry in existing_data_users}                              #check to see what userIDs currently exist in users.json
    updated_users_data = existing_data_users + [user for user in total if user["userID"] not in existing_user_ids]
        
                
    # Transform data into JSON format and ensure that the data is assigned correctly to events
    for event in event_data:
        event_instance = {
            "eventID" : event["eventID"],
            "Name" : event["Name"],
            "date" : event["date"],
            "start_time" : event["start_time"],
            "end_time" : event["end_time"],
            "address" : event["address"],
            "category" : event["category"],
            "vAmount" : event["vAmount"],
            "hoursReward" : event["hoursReward"],
            "description" : event["description"],
            "orgName" : event["orgName"],
            "eventApplicants" : event.get("eventApplicants", []),
            "eventVolunteers" : event.get("eventVolunteers", []),
            "attendenceAccounted" : event.get("attendenceAccounted", False),
            "hoursDeadline" : event["hoursDeadline"]
        }
        events.append(event_instance)           #add event instance to the total collection of events from the database

    # Avoid duplicates in events.json
    existing_event_ids = {event["eventID"] for event in existing_events_data["events"]}         #log events currently in the json file
    updated_events_data = existing_events_data              
    updated_events_data["events"].extend([                  
        event for event in events if event["eventID"] not in existing_event_ids
    ])

    # Write users.json
    with open('users.json', 'w') as file:
        json.dump(updated_users_data, file, indent=4)

    # Write all_events.json
    with open('all_events.json', 'w') as file:
        json.dump(updated_events_data, file, indent=4)
