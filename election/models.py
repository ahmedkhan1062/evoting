from datetime import datetime
from django.db import models
from firebase_admin import db
from firebase_admin import firestore
from django.db import transaction
import bcrypt
import requests

# Get a Firestore client
db = firestore.client()

# Create your models here.
class Person:
    def __init__(self, firstname, surname, id,email, tempPass, confirmPass):
        self.firstname = firstname
        self.surname = surname
        self.id = id
        self.email = email
        self.tempPass = tempPass
        self.confirmPass = confirmPass
        self.password = ""
        self.voteStatus = False
        
    #Method to check if the two passwords entered match
    def checkPassword(self):
        if self.tempPass == self.confirmPass:
            self.password = self.tempPass
            return True
        else:
            return False
    
    
    def checkEmail(self):
        response = requests.get('https://api.mailcheck.ai/email/'+self.email)

        data = response.json()
        print(data)
        if data['disposable'] == False:
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
        
    def postNewUserToDatabase(self):
        hashedPass,salt = DatabaseMethods.hash_password(self.password)
        data = {
                'firstName': self.firstname,
                'secondName': self.surname,
                'id': self.id,
                'email': self.email,
                'voteStatus': False,
                'password': hashedPass,
                'salt': salt,
                
                }
            
        newUser = db.collection("People").document(self.id)
        if newUser.get().exists:
            return "Exists"
        else:
            newUser.set(data)
            return "Success"
        

#**************************DATABASE FUNCTIONS****************************
        
class DatabaseMethods:
    
       
    def confirmLogin( userID, userPassword):
        document = db.collection('People').document(userID)

        # Get the document snapshot
        doc_values = document.get()

        # Check if the document exists
        if doc_values.exists:
            # Get the value of the specified field
            savedPassword = doc_values.get('password')
            savedSalt = doc_values.get('salt')
            
            hashedUserPassword = bcrypt.hashpw(userPassword.encode('utf-8'), savedSalt)
            
            if savedPassword == hashedUserPassword:
                return "Success"
            else:
                return "Error"
            
    def fetchUser(userID):
        document = db.collection('People').document(userID)

        # Get the document snapshot
        doc_values = document.get()

        # Check if the document exists
        if doc_values.exists:
            # Get the value of the specified field
            username = doc_values.get('firstName')
            return username
        else:
            return "Guest"
        
    def hash_password(password, salt=None):
        # Generate a salt if not provided
        if salt is None:
            salt = bcrypt.gensalt()

        # Hash the password with the salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password, salt

class Vote:
    @transaction.atomic
    def setVote(userID, candidateID):
        if userID == "":
            return "Error"
        else:
            voterbase = db.collection('People').document(userID) 
            status = voterbase.get()
            if status.get('voteStatus') == True:
                return "alreadyvoted"
            else:
                voterbase.update({'voteStatus': True})
    
                candidatebase = db.collection('Candidates').document(candidateID)
                vote_count = candidatebase.get()
                totalVotes = vote_count.get('voteCount')
                totalVotes = totalVotes + 1
                
                candidatebase.update({'voteCount': totalVotes})
                
                return "Success"
    
    def returnAllVotes():
        candidatebase = db.collection('Candidates')
        
        pollLabels = []
        pollResults = []
        
        polldata = candidatebase.stream()
        
        for candidate in polldata:
    # Extract the value of a single attribute from each document
            candidateName = candidate.to_dict().get('firstName')
            pollCount = candidate.to_dict().get('voteCount')
            pollLabels.append(candidateName)
            pollResults.append(pollCount)
            
        return pollLabels, pollResults
        
    
        
    
        

            