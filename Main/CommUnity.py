import json
from flask import Flask, render_template, request, redirect, session, jsonify
from Directories.controllers.user import Events, Organizer
from Directories.controllers.DatabasePush import update_database_from_json
from Directories.controllers.PopulateData_json import fetch_all_data, update_json_file
import os
import sys
from flask_session import Session
from datetime import datetime
import random
from flask_cors import CORS



# Dynamically adjust Python's search path to include the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))  # Path to Main
project_root = os.path.dirname(current_dir)              # Path to project root
sys.path.append(project_root)                            # Add project root to module search path

# File path for users.json and all_events.json in the project root
file_path = os.path.join(project_root, 'users.json')
events_file = os.path.join(project_root, 'all_events.json')


# Synchronize JSON data to the database
update_database_from_json()

# Fetch all data from the database
user_data, volunteer_data, organizer_data, event_data = fetch_all_data()

# Update JSON file with fetched data
update_json_file('users.json', user_data, volunteer_data, organizer_data, event_data)


app = Flask(__name__, template_folder='../Directories/templates')
CORS(app, resources={r"/*": {"origins": "https://communitytaajj.my"}})        #ensure that communitytaajj.my (domain) can interact with flask backend


# Configure Flask-Session
app.secret_key = "your_secret_key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Function to load users from the JSON file
def load_users():
    if not os.path.exists(file_path):
        print("users.json not found. Initializing an empty user list.")
        return []
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error decoding users.json. Initializing an empty user list.")
        return []

# Function to save users to the JSON file
def save_users(users):
    try:
        with open(file_path, 'w') as file:
            json.dump(users, file, indent=4)
            print("Users successfully saved.")
    except Exception as e:
        print(f"Error saving users: {e}")

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/direction.html')
def direction():
    return render_template('direction.html')

# Route to serve the signup page
@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

# Route to handle signup form submission
@app.route('/signupsubmit', methods=['POST','GET'])
def process_signup():
    role = request.form.get("role")
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    join_date = datetime.now().strftime("%Y-%m-%d")
    user_id = str(random.randint(100000, 999999))
    user_type = 0 if role == "volunteer" else 1

    user_data = {
        "userType": user_type,
        "userID": user_id,
        "username": username,
        "password": password,
        "email": email if role == "volunteer" else request.form.get("orgEmail"),
        "joinDate": join_date,
    }

    if role == "volunteer":
        user_data.update({
            "firstName": request.form.get("firstName"),
            "lastName": request.form.get("lastName"),
            "DOB": request.form.get("dob"),
            "location": request.form.get("zipcode"),
            "gender": request.form.get("gender"),
            "preferredCats": [],
            "hours": 0,
            "history": [],
        })
    elif role == "organizer":
        user_data.update({
            "orgName": request.form.get("orgName"),
            "events": [],
            "address": {
                "street": request.form.get("street"),
                "city": request.form.get("city"),
                "state": request.form.get("state"),
                "zipCode": request.form.get("zipCode"),
            },
        })

    users = load_users()

    if any(user.get("username") == username for user in users):
        return "Username already exists. Please choose another one.", 400

    users.append(user_data)
    save_users(users)
    return redirect('/login')

# Route to serve the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = load_users()

        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['username'] = username
            session['userID'] = user['userID']  # Ensure userID is set here
            user_type = user.get('userType')
            if user_type == 0:
                return redirect(f'/volunteer_home?username={username}')
            elif user_type == 1:
                return redirect(f'/organizer_home?username={username}')
        return "Invalid username or password. Please try again.", 401
    return render_template('login.html')

# Route to serve the volunteer home page
@app.route('/volunteer_home')
def volunteer_home():
    username = request.args.get('username') or session.get('username')
    users = load_users()
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        return "User not found", 404
    return render_template('volunteerhomepage.html', user=user)

# Route to serve the organizer home page
@app.route('/organizer_home')
def organizer_home():
    username = request.args.get('username') or session.get('username')
    users = load_users()
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        return "User not found", 404
    return render_template('OrganizerHome.html', user=user)

@app.route('/usersearch', methods=['GET', 'POST'])
def user_search():
    logged_in_user = None
    if 'username' in session:
        # Load users from JSON
        try:
            with open(file_path, 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        # Find the logged-in user
        logged_in_user = next((u for u in users if u.get('username') == session['username']), None)

    # Render usersearch.html with logged-in user data
    return render_template('usersearch.html', logged_in_user=logged_in_user)


@app.route('/eventsearch.html', methods=['GET', 'POST'])
def event_search():
    logged_in_user = None
    if 'username' in session:
        # Load users from JSON
        try:
            users = load_users()
        except Exception as e:
            users = []
            print(f"Error loading users: {e}")

        # Find the logged-in user
        logged_in_user = next((u for u in users if u.get('username') == session['username']), None)

    # Render eventsearch.html with logged-in user data
    return render_template('eventsearch.html', logged_in_user=logged_in_user)

    

# Function to load all events
def load_events():
    if not os.path.exists(events_file):
        print("all_events.json not found. Initializing an empty events list.")
        with open(events_file, 'w') as file:
            json.dump([], file)  # Initialize with an empty list
        return []
    try:
        with open(events_file, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error decoding all_events.json. Initializing an empty events list.")
        return []

# Function to save all events
def save_events(events):
    try:
        with open(events_file, 'w') as file:
            json.dump(events, file, indent=4)
            print("Events successfully saved.")
    except Exception as e:
        print(f"Error saving events: {e}")

# Function to find an event by its ID
def find_event_by_id(event_id):
    events = load_events()
    return next((event for event in events if event["id"] == event_id), None)

@app.route('/create_event', methods=['POST'])
def create_event():
    event_data = request.json
    organizer_id = session.get('userID')  # Assuming session stores the organizer's user ID

    # Parse and validate event data
    name = event_data.get('name', 'Untitled Event')
    date = event_data.get('date', datetime.now().strftime("%m-%d-%Y"))  # Default to today's date
    start_time = event_data.get('start_time', '00:00')
    end_time = event_data.get('end_time', '00:00')
    address = event_data.get('address', 'No Address')
    category = event_data.get('category', 'Miscellaneous')
    vAmount = event_data.get('volunteers_needed', 0)
    hoursReward = event_data.get('hours_rewarded', 0)
    description = event_data.get('description', 'No Description')
    orgName = session.get('username', 'Unknown Organizer')  # Assuming organizer's username is in session

    # Create an Event object
    new_event = Event(name, date, start_time, end_time, address, category, vAmount, hoursReward, description, orgName)

    # Load existing events and check for duplicates
    all_events = load_events()
    if any(event["id"] == new_event.eventID for event in all_events):
        return jsonify({"success": False, "message": "Event with the same ID already exists."}), 400

    # Add the event to the list and save
    all_events.append(new_event.__dict__)
    save_events(all_events)

    return jsonify({"success": True, "event": new_event.__dict__})

@app.route('/edit_event', methods=['POST'])
def edit_event():
    edited_event = request.json
    event_id = edited_event.get("id")

    if not event_id:
        return jsonify({"success": False, "message": "Event ID is required."}), 400

    # Load existing events
    all_events = load_events()

    # Find the event by ID and update its data
    for event in all_events:
        if event["id"] == event_id:
            event.update(edited_event)
            save_events(all_events)
            return jsonify({"success": True, "message": "Event updated successfully."})

    return jsonify({"success": False, "message": "Event not found."}), 404

@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        events = load_events()
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users')
def get_users():
    user_type = request.args.get('userType', None)  # Optional filtering by userType
    users = load_users()

    if user_type is not None:
        users = [user for user in users if user['userType'] == int(user_type)]

    return jsonify(users)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
