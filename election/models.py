from datetime import datetime
from django.db import models

# Create your models here.
class person:
    def __init__(self, firstname, surname, id,email, tempPass, confirmPass):
        self.firstname = firstname
        self.surname = surname
        self.id = id
        self.email = email
        self.tempPass = tempPass
        self.confirmPass = confirmPass
        self.password = ""
        
    #Method to check if the two passwords entered match
    def checkPassword(self):
        if self.tempPass == self.confirmPass:
            self.password = self.tempPass
            return True
        else:
            return False
        
    #Method to check validity of SA id number
    def checkID(self):
        # Check if the ID number is of correct length
        if len(self.id) != 13:
            return False
        
        # Extract components of the ID number
        dob = self.id[:6]
        gender = int(self.id[6:10])
        citizenship_status = int(self.id[10])
        
        # Check if components are valid
        try:
            dob_year = int(dob[:2])
            dob_month = int(dob[2:4])
            dob_day = int(dob[4:6])
            
            if not (0 < dob_month <= 12):
                return False
            
            if not (0 < dob_day <= 31):
                return False
            
            # Handle leap year for February
            if dob_month == 2 and dob_day > 29:
                return False
            
           
            # Check if year is in valid range
            current_year = int(datetime.now().strftime("%Y")[-2:])
            #if not (current_year - 100 <= dob_year <= current_year):
                #return False
            print("bot")
            # Check if gender number is in correct range
            if not (0 <= gender <= 9999):
                return False
            
            # Check if citizenship status is valid
            if not (citizenship_status in [0, 1]):
                return False
            
            return True
            
        except ValueError:
            return False

            