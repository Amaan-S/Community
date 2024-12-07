import json

def load_users(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def user_search_fn(file_path, first_name_search):
    users_data = load_users(file_path)
    
    #checks if search_name matches users first or last names
    found_users = [
        user for user in users_data 
        if user['firstName'].lower() == first_name_search.lower()
    ]
    
    # Print found users names
    if found_users:
        for user in found_users:
            print(f"{user['firstName']} {user['lastName']}")
    else:
        print("No users found with that name.")

#function to seach by ID
def ID_search(file_path,UserIDSearch):
    users_data = load_users(file_path) 
    found_users = [
        user for user in users_data 
        if user['userID'] == UserIDSearch
    ]

    if found_users:
        for user in found_users:
            print("UserID matches: ")
            print(f"{user['firstName']} {user['lastName']}")
    else:
        print("No users with that ID")

#function to search userType
def Type_search(file_path,UserTypeSearch):
    users_data = load_users(file_path) 
    found_users = [
        user for user in users_data 
        if user['userType'] == UserTypeSearch
    ]

    if found_users == 0:
        print("This user is an organizer.")
    elif found_users == 1:
        print("This user is a volunteer.")
    else:
        print("userType incorrect.")
