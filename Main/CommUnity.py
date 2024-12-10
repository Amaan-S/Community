import json
from flask import Flask, render_template, request, redirect, session
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

# File path for users.json in the project root
file_path = os.path.join(project_root, 'users.json')

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
    user_data = None  # Default: no user found
    if request.method == 'POST':
        username = request.form.get('username')  # Get the username from the form
        
        # Path to users.json
        users_file_path = os.path.join(os.path.dirname(__file__), '../users.json')
        
        try:
            # Load users from the JSON file
            with open(users_file_path, 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        # Search for the user by username
        for user in users:
            if user.get('username') == username:
                user_data = user
                break
    
    # Render the user search page with the found user data (if any)
    return render_template('usersearch.html', user_data=user_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
