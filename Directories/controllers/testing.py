import unittest
import time
from user import User, Volunteer, Organizer, Events

class TestUserMethods(unittest.TestCase):

    def setUp(self):
        self.volunteer = Volunteer(
            userType=0, userID="V123", email="volunteer@example.com", joinDate="11-01-2024", 
            username="john_doe", password="pass123", firstName="John", lastName="Doe", 
            DOB="05-12-1990", location="City", gender="Male", 
            preferredCats=["Community Service", "Health & Wellness"]
        )
        
        self.organizer = Organizer(
            userType=1, userID="O456", email="organizer@example.com", joinDate="10-01-2024", 
            username="jane_smith", password="pass456", orgName="Community Org"
        )
        
        self.event = Events(
            name="Community Cleanup", date="11-20-2024", start_time="10:00 AM", 
            end_time="2:00 PM", address="Park St.", category="Community Service", 
            vAmount=5, hoursReward=4, description="A community event to clean up the park", 
            orgName="Community Org"
        )

    def test_calculate_age(self):
        print("Running test_calculate_age...")
        expected_age = 34  # Adjust as needed based on the current date
        calculated_age = self.volunteer.calculate_age()
        print(f"Expected Age: {expected_age}, Calculated Age: {calculated_age}")
        self.assertEqual(calculated_age, expected_age)
        print("Test passed: test_calculate_age\n")
        time.sleep(1)

    def test_update_profile_info(self):
        print("Running test_update_profile_info...")
        self.volunteer.update_profile_info(firstName="Jonathan", lastName="Doe", email="new_email@example.com")
        print(f"Updated Info: First Name: {self.volunteer.firstName}, Last Name: {self.volunteer.lastName}, Email: {self.volunteer.email}")
        self.assertEqual(self.volunteer.firstName, "Jonathan")
        self.assertEqual(self.volunteer.lastName, "Doe")
        self.assertEqual(self.volunteer.email, "new_email@example.com")
        print("Test passed: test_update_profile_info\n")
        time.sleep(1)

    def test_change_password(self):
        print("Running test_change_password...")
        self.volunteer.change_password("newpassword123")
        print(f"Updated Password: {self.volunteer.password}")
        self.assertEqual(self.volunteer.password, "newpassword123")
        print("Test passed: test_change_password\n")
        time.sleep(1)

    def test_apply_for_event(self):
        print("Running test_apply_for_event...")
        self.volunteer.apply_for_event(self.event)
        print(f"Event Applicants: {[v.username for v in self.event.eventApplicants]}")
        self.assertIn(self.volunteer, self.event.eventApplicants)
        print("Test passed: test_apply_for_event\n")
        time.sleep(1)

    def test_add_volunteer(self):
        print("Running test_add_volunteer...")
        self.event.add_volunteer(self.volunteer)
        print(f"Event Volunteers After Adding: {[v.username for v in self.event.eventVolunteers]}")
        self.assertIn(self.volunteer, self.event.eventVolunteers)
        print("Test passed: test_add_volunteer\n")
        time.sleep(1)

    def test_remove_volunteer(self):
        print("Running test_remove_volunteer...")
        self.event.add_volunteer(self.volunteer)
        self.event.remove_volunteer(self.volunteer.username)
        print(f"Event Volunteers After Removing: {[v.username for v in self.event.eventVolunteers]}")
        self.assertNotIn(self.volunteer, self.event.eventVolunteers)
        print("Test passed: test_remove_volunteer\n")
        time.sleep(1)

    def test_add_event(self):
        print("Running test_add_event...")
        self.organizer.add_event(
            name="Charity Run", date="12-05-2024", start_time="9:00 AM", end_time="12:00 PM", 
            address="Main St.", category="Fairs & Events", vAmount=10, hoursReward=3, 
            description="A charity run for a cause"
        )
        print(f"Organizer Events After Adding: {[e.name for e in self.organizer.fetch_events()]}")
        self.assertEqual(len(self.organizer.fetch_events()), 1)
        print("Test passed: test_add_event\n")
        time.sleep(1)

    def test_delete_event(self):
        print("Running test_delete_event...")
        self.organizer.add_event(
            name="Charity Run", date="12-05-2024", start_time="9:00 AM", end_time="12:00 PM", 
            address="Main St.", category="Fairs & Events", vAmount=10, hoursReward=3, 
            description="A charity run for a cause"
        )
        event_count_before = len(self.organizer.fetch_events())
        self.organizer.delete_event(self.organizer.events[0].eventID)
        event_count_after = len(self.organizer.fetch_events())
        print(f"Event Count Before: {event_count_before}, Event Count After: {event_count_after}")
        self.assertEqual(event_count_before - 1, event_count_after)
        print("Test passed: test_delete_event\n")
        time.sleep(1)

if __name__ == "__main__":
    unittest.main()
