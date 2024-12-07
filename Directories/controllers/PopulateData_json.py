import os
import json
from dotenv import load_dotenv
from user import User, Volunteer, Organizer, Events
from your_module import db_connection, fetch_attributes_user, fetch_attributes_volunteer, fetch_attributes_organizer

load_dotenv()

def fetch_all_data():
    # Fetch user data using fetch
    user_instance = User(userType=None, userID=None, email=None, joinDate=None, username=None, password=None)
    user_data = fetch_attributes_user(user_instance)

    # Fetch volunteer data
    volunteer_instance = Volunteer(userType=None, userID=None, email=None, joinDate=None, username=None, password=None, firstName=None, lastName=None, DOB=None)
    volunteer_data = fetch_attributes_volunteer(volunteer_instance)

    # Fetch organizer data
    organizer_instance = Organizer(userType=None, userID=None, email=None, joinDate=None, username=None, password=None, orgName=None)
    organizer_data = fetch_attributes_organizer(organizer_instance)

    return user_data, volunteer_data, organizer_data

'''

def update_json_file(file_path, user_data, volunteer_data, organizer_data):
    try:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []
        
    # Transform data into JSON format
    user_json = {                                  #populate data for the user base class instances
        "firstName": user_data.username,  # Assuming username is used as firstName
        "lastName": "",  # Add logic to fetch lastName if available
        "email": user_data.email,
        "DOB": "",  # Add logic to fetch DOB if available
        "joinDate": user_data.joinDate,
        "gender": "",  # Add logic to fetch gender if available
        "userID": user_data.userID,
        "hours": 0,  # Add logic to fetch hours if available
        "history": [],  # Add logic to fetch history if available
        "username": user_data.username,
        "password": user_data.password,
        #populate the fields of the user base class
        "userType": user_data.userType,
        "userID": user_data.userID,
        "username": user_data.username,
        "password": user_data.password,
        "email": user_data.email,
        "joinDate": user_data.joinDate,
        "orgName": "Jihad Company2",
        "events": [],
        "address": {
            "street": "300 Laurel Lane",
            "city": "Euless",
            "state": "TX",
            "zipCode": "76039
        }
    }

    volunteer_json = {
        "role": "volunteer",
        "username": volunteer_data.username,
        "password": volunteer_data.password,
        "first_name": volunteer_data.firstName,
        "last_name": volunteer_data.lastName,
        "email": volunteer_data.email,
        "gender": volunteer_data.gender,
        "dob": volunteer_data.DOB,
        "zipcode": volunteer_data.location  # Assuming location is used as zipcode
    }

    organizer_json = {
        "role": "organizer",
        "username": organizer_data.username,
        "password": organizer_data.password,
        "organization_name": organizer_data.orgName,
        "email": organizer_data.email,
        "address": {}  # Add logic to fetch address if available
    }


'''

    # Update existing data
    existing_data.extend([user_json, volunteer_json, organizer_json])

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

def main():
    user_data, volunteer_data, organizer_data = fetch_all_data()
    update_json_file('users.json', user_data, volunteer_data, organizer_data)

if __name__ == "__main__":
    main()
