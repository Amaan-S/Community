import json
import random
import re
from datetime import datetime
#from usersearch import load_users

def load_users(file_path = 'Users.json'):
    with open(file_path, 'r') as file:
        return json.load(file)


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        return False

def add_new_user(file_path):
    users = load_users(file_path)

    #checks if there are 1000 users
    if len(users) >= 1000:
        print("Limit reached. Cannot add more than 1000 users")
        return

    #user input 
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    usertype = input("Are you a Volunteer or an organizer?: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")

    DOB = input("Enter date of birth (MM/DD/YYYY) format: ")

    while True:
        email = input("Enter your email: ")
        if is_valid_email(email):
            break  #breaks if email good
  
    while True:     #checks gender is valid, its 2024 but its easier to code m/f only
        gender = input("Enter gender (male/female): ").lower()
        if gender == "male" or gender == "female":
            break  #breaks if valid

    user_id = random.randint(100000, 999999)

    while True:     #checks hour input is good
        try:
            hours = int(input("Enter total volunteer hours: "))
            break   #breaks if good
        except ValueError:
            pass    #asks again if bad


    joinDate = datetime.now().date().isoformat()

    #gets volunteer history info
    history = []
    print("Enter places volunteered (type 'done' when finished):")
    while True:
        place = input("> ")
        if place.lower() == 'done':
            break
        history.append(place)

    #makes new user
    new_user = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "DOB": DOB,
        "joinDate": joinDate,
        "gender": gender,
        "userID": user_id,
        "hours": hours,
        "history": history,
        "username": username,
        "password": password,
        "usertype": usertype
    }

    #adds the new user to the bottom of the json file 
    users.append(new_user)
    
    #saves the updated file 
    with open('Users.json', 'w') as file:
        json.dump(users, file, indent=4)
    
    print("New user added successfully!")


def user_login(file_path, entered_username, entered_password):
    users = load_users(file_path)

    for user in users:
        if user.get('username') == entered_username and user.get('password') == entered_password:
            print("Login Successful")
            print(f"Welcome {user['firstName']} {user['lastName']}!")
            #print("User Info:", user)
            if user.get('usertype') == "0":
                print("Organizer")
            if user.get('usertype') == "1":
                print("Volunteer")
            print(f"Join Date: {user.get('joinDate', 'N/A')}")
            print(f"Volunteer Hours: {user.get('hours', 'N/A')}")
            print(f"Volunteer History: {', '.join(user.get('history', []))}")
            return True

    print("Invalid username or password")
    return False
