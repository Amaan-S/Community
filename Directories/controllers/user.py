import random
import flask
import json
import sys
import os
from datetime import datetime, timedelta


class User:
    def __init__(self, userType, userID, email, joinDate, username, password):
        self.userType = userType # 0 == regular volunteer user, 1 == organizer
        self.userID = userID
        self.email = email
        self.joinDate = joinDate
        self.username = username
        self.password = password


class Volunteer(User):
    def __init__(self, userType, userID, email, joinDate, username, password, firstName, lastName, DOB, location = None, gender = None, preferredCats = None, hours = 0, history = None):
        super().__init__(userType, userID, email, joinDate, username, password)
        self.firstName = firstName
        self.lastName = lastName
        self.DOB = DOB
        self.location = location
        self.gender = gender
        self.preferredCats = preferredCats if preferredCats else []
        self.hours = hours
        self.history = history if history is not None else []

    def calculate_age(self):
        today = datetime.today()
        birthday = datetime.strptime(self.DOB, "%m-%d-%Y")
        return today.year - birthday.year - ((today.month, today.day)  < (birthday.month, birthday.day))

    def update_profile_info(self, firstName = None, lastName = None, email = None, gender = None, DOB= None):
        if firstName:
            self.firstName = firstName

        if lastName:
            self.lastName = lastName

        if email:
            self.email = email

        if gender:
            self.gender = gender

        if DOB:
            self.DOB = DOB

        print(f"Profile Information Updated.")

    def change_password(self, newPassword):
        self.password = newPassword
        print(f"Password Changed Successfully.")

    def update_hours(self, hoursToAdd):
        self.hours += hoursToAdd

    def update_places_volunteered(self, eventOrgName, eventName, eventDate, eventHours, eventDescription):
    
        event_history_details = {

            'eventOrgName': eventOrgName,
            'eventName': eventName,
            'eventDate': eventDate,
            'eventHours': eventHours,
            'eventDescription': eventDescription
        }

        self.history.append(event_history_details)

    def relevant_events(self, events):

        events = Events.load_events()

        filtered_events = []
        for event in events:
            eventDate = datetime.strptime(event['date'], "%m-%d-%Y")
            if eventDate > datetime.now() and event['category'] in self.preferredCats:
                filtered_events.append(event)
        return filtered_events
    
    def apply_for_event(self, event):
        event.add_applicant(self)


class Organizer(User): 
    def __init__(self, userType, userID, email, joinDate, username, password, orgName, events = None):
        super().__init__(userType, userID, email, joinDate, username, password)
        self.orgName = orgName
        self.events = events if events is not None else []

    def add_event(self, name, date, start_time, end_time, address, category, vAmount, hoursReward, description):
        event = Events(name, date, start_time, end_time, address, category, vAmount, hoursReward, description, orgName=self.orgName)
        self.events.append(event)
        print(f" Event '{name}' created successfully ")

    def delete_event(self, eventID):
        eventToDelete = next((event for event in self.events if event.eventID == eventID), None)

        if eventToDelete: 
            self.events.remove(eventToDelete) 
            print(f"Event '{eventToDelete.name}' Has Been Deleted")

    def fetch_events(self):
        return self.events


class Events:

    Event_Categories = [

        "Community Service",
        "Fairs & Events",
        "Education & Mentorship",
        "Health & Wellness",
        "Animal Welfare",
        "Religious",
        "Miscellaneous"
    ]

    def __init__(self, name, date, start_time, end_time, address, category, vAmount, hoursReward, description, orgName):
        self.eventID = str(random.randint(100000, 999999))
        self.name = name
        self.date = datetime.strptime(date, "%m-%d-%Y")
        self.start_time = start_time
        self.end_time = end_time
        self.address = address
        self.vAmount = vAmount
        self.hoursReward = hoursReward
        self.description = description
        self.orgName = orgName
        self.eventApplicants = []
        self.eventVolunteers = []
        self.attendenceAccounted = False
        self.hoursDeadline = self.date + timedelta(days=7)

        if category in Events.Event_Categories:
            self.category = category
        else: 
            raise ValueError(f"Invalid Category, Please Choose From Category Selection")

    def add_volunteer(self, volunteer):
        if len(self.eventVolunteers) < self.vAmount:
            self.eventVolunteers.append(volunteer)
            print(f"{volunteer.username} Has Been Added To The Volunteering Event '{self.name}'.")
        else:
            print(f"The Event '{self.name}' Does Not Require Anymore Volunteers.")

    def remove_volunteer(self, username):
        volunteer_to_remove = next((volunteer for volunteer in self.eventVolunteers if volunteer.username == username), None)

        if volunteer_to_remove:
            self.eventVolunteers.remove(volunteer_to_remove)
        else:
            print(f"Error With Applicant Removal.")

    def add_applicant(self, volunteer):
        if volunteer not in self.eventApplicants and volunteer not in self.eventVolunteers:
            self.eventApplicants.append(volunteer)
            print(f"Successfully applied to Event {self.name}.")
        else:
            print(f"Already Applied To or Are a Volunteer to {self.name}.")

    def get_applicant_info(self):
        return [
            f"{v.username} | {v.firstName} {v.lastName}, {v.calculate_age()}, {v.hours} Hours"
            for v in self.eventApplicants
        ]

    def edit_event(self, name = None, date = None, start_time = None, end_time = None, address = None, category = None, vAmount = None, description = None):
        if name is not None:
            self.name = name

        if date is not None:
            self.date = datetime.strptime(date, "%m-%d-%Y")

        if start_time is not None:
            self.start_time = start_time

        if end_time is not None:
            self.end_time = end_time

        if address is not None:
            self.address = address

        if category is not None:
            if category in Events.Event_Categories:
                self.category = category
        else: 
            raise ValueError("Invalid Category, Please Choose From Category Selection")

        if vAmount is not None:
            if vAmount < len(self.eventVolunteers):
                print(f"The Amount of Volunteers In This Event Are Full, Remove Volunteers Manually Then Lower Applicants Needed.")
            else:
                self.vAmount = vAmount

        if description is not None:
            self.description = description

        print(f"Event #'{self.eventID}': '{self.name}' Has Been Edited Successfully.")

    def confirm_applicants(self, selectedVolunteers):

        for volunteer in selectedVolunteers:
            if volunteer in self.eventApplicants:
                if len(self.eventVolunteers) <= self.vAmount:
                    self.eventVolunteers.append(volunteer)
                    self.eventApplicants.remove(volunteer)

                else:
                    print(f"Event Has Reached Maximum Volunteer Limit")
                    break

    def confirm_attendence(self, attended):
        if datetime.now() > self.date and datetime.now() <= self.hoursDeadline:
            self.attendenceAccounted = True
            # List of volunteers who were absent based on their usernames
            absent = [v for v in self.eventVolunteers if v.username not in [a.username for a in attended]]

            # Remove absent volunteers from eventVolunteers list
            for volunteer in absent:
                self.eventVolunteers.remove(volunteer)

            # Award hours to the volunteers who attended
            for volunteer in attended:
                volunteer.update_hours(self.hoursReward)
                volunteer.update_places_volunteered(
                    eventOrgName=self.orgName,
                    eventName=self.name,
                    eventDate=self.date,
                    eventHours=self.hoursReward,
                    eventDescription=self.description
                )
            print("Attendees Rewarded Correct Hours")


    def auto_reward(self):
        if not self.attendenceAccounted and datetime.now() > self.hoursDeadline:
            for volunteer in self.eventVolunteers:
                volunteer.update_hours(self.hoursReward)
                volunteer.update_places_volunteered(
                    eventOrgName = self.orgName, eventName = self.name, eventDate = self.date, eventHours = self.hoursReward, eventDescription = self.description
                )
            print("Deadline Passed: All Volunteers Rewarded Hours")

    def display_event(self):
        formatDate = self.date.strftime("%B %d, %Y")
        formatTime = f"{self.start_time} - {self.end_time}"
        print(f"Event Name: {self.name}")
        print(f"Date: {formatDate}")
        print(f"Time: {formatTime}")
        print(f"Location: {self.address}")
        print(f"Category: {self.category}")
        print(f"Description: {self.description}")

    def save_event(self):
        event_data = {

            "eventID": self.eventID,
            "name": self.name, 
            "date": self.date.strftime("%m-%d-%Y"), 
            "start_time": self.start_time, 
            "end_time": self.end_time, 
            "address": self.address, 
            "category": self.category, 
            "vAmount": self.vAmount, 
            "hoursReward": self.hoursReward, 
            "description": self.description, 
            "orgName": self.orgName
        }

        try:
            with open('all_events.json', 'r') as f:
                events = json.load(f)
        except FileNotFoundError:
            events = []

        events.append(event_data)

        with open('all_events.json', 'w') as f:
            json.dump(events, f, indent = 4)
        print("Event Saved Successfully.")

    @staticmethod
    def load_events():
        try:
            with open('all_events.json', 'r') as f:
                events = json.load(f)
                return events
        except FileNotFoundError:
            print("No Events Today")
            return []
            
    

class UserProfiles:
    def __init__(self):
        self.users = []