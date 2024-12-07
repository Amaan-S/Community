from Directories.controllers.user import User, Volunteer, Organizer, UserProfiles

import random

from datetime import datetime

# to test in terminal, will be added to profile.y after user class construction is finilized
def profileDisplay(self):
    
            print(f"\t\tProfile Information For User {self.firstName} {self.lastName}\t\t\nName: {self.firstName} {self.lastName}\nDate of Birth: {self.DOB}\nID: {self.userID}\nGender: {self.gender}\nEmail: {self.email}\nCommUnity Join Date: {self.joinDate}\nTotal Volunteered Hours: {self.hours}")
            print("Volunteering Locations History:")
            for place in self.history:
                print(f"- {place}") # type: ignore so far
