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
        # Check if the ID number is 13 digits long
        if len(self.id) != 13:
            return False

        # Check if all characters in the ID number are digits
        if not self.id.isdigit():
            return False

        # Extract the date portion from the ID number
        date_part = self.id[:6]

        # Extract the citizenship digit
        citizenship = int(self.id[10])

        # Extract the last digit (checksum)
        checksum = int(self.id[-1])

        # Perform ID number validation algorithm
        weights = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        checksum_calc = sum(int(digit) * weight for digit, weight in zip(self.id[:-1], weights))

        # Calculate the expected checksum
        expected_checksum = (10 - (checksum_calc % 10)) % 10

        # Special case for citizenship = 0
        if citizenship == 0:
            return checksum == expected_checksum

        # Check if the expected checksum matches the actual checksum
        return checksum == expected_checksum