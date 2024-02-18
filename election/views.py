from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from .models import Person
from .models import DatabaseMethods, Vote
import json

from firebase_admin import db
from firebase_admin import firestore

# Get a Firestore client
db = firestore.client()


def index(request):
    return render(request, "index.html")


def vote(request):
    return render(request, "page_vote.html")


def register(request):
    return render(request, "page_register.html")


def login(request):
    return render(request, "page_login.html")


def refreshPoll(request):
        labels, results = Vote.returnAllVotes()
        
        print(labels)
        print(results)
        combined_data = {'labels': labels, 'data': results}
        return JsonResponse(combined_data)

def signOut(request):
    if request.method == 'POST':
        return JsonResponse({'message': 'GoVote'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def submitVote(request):
    if request.method == 'POST':
        
        raw_data = request.body

        # Decode from bytes to string
        decoded_data = raw_data.decode('utf-8')

        
        # Parse as JSON
        posted_data = json.loads(decoded_data)
        candidateID = posted_data['candidate']
        voterID = posted_data['voter']
        
        if voterID == "Guest":
            return JsonResponse({'message': 'Guest may not vote'})
        
        result = Vote.setVote(voterID, candidateID)
        
        if  result == "Success":
            return JsonResponse({'message': 'Vote successful'})
        
        elif result == "alreadyvoted":
            return  JsonResponse({'message': 'User has already voted'})
        
        else: return JsonResponse({'message': 'Guest may not vote'})
    

def recieveRegistration(request):
    if request.method == 'POST':
        
        # Process the data as needed
        response_data = {'message': 'Data received and processed successfully'}
        
        raw_data = request.body

        # Decode from bytes to string
        decoded_data = raw_data.decode('utf-8')

        # Parse as JSON
        posted_data = json.loads(decoded_data)
        
        firstname = posted_data['firstName']
        surname = posted_data['surname']
        idnumber = posted_data['idnumber']
        email= posted_data['email']
        password= posted_data['password']
        conPass= posted_data['confirmpass']
        
        voter = Person(firstname, surname, idnumber, email, password, conPass)
        
        passStrenth, message = voter.checkPasswordStrength()
        
        if voter.checkEmail() == False:
            return JsonResponse({'message': 'Please enter a valid email address'}, status = 400)
        
        if voter.checkID() == False:
            return JsonResponse({'message': 'Please enter a valid South African identification number'}, status = 400)
        
        if passStrenth == False:
            return JsonResponse({'message': message})
        
        elif voter.checkPassword() == False:
            return JsonResponse({'message': 'Please ensure that the passwords match'}, status = 400)
        
        else: 
            if voter.postNewUserToDatabase() == "Exists":
                return JsonResponse({'message': 'Your account already exists, please try logging in'}, status = 400)
                
            else: return JsonResponse({'message':"Success"})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
    
def recieveLogin(request):
    if request.method == 'POST':
         
        # Process the data as needed
        response_data = {'message': 'Data received and processed successfully'}
        
        raw_data = request.body

        # Decode from bytes to string
        decoded_data = raw_data.decode('utf-8')

        # Parse as JSON
        posted_data = json.loads(decoded_data)
        
        
        idnumber = posted_data['idnumber']
        password = posted_data['password']
        
        if DatabaseMethods.confirmLogin(idnumber, password) == "Success":
            userData = {
                'Login': "success",
                'ID': idnumber,
                'username': DatabaseMethods.fetchUser(idnumber),
                'voteStatus' : False,
                'gender' : 'm',
            }
            
            #userPacket = json.loads(userData)
            return JsonResponse({'message': userData})
        else:
            return JsonResponse({'message': 'Incorrect ID number or password'}, status = 400)
            
            
    else:
        return JsonResponse({'error': 'Invalid request method'})
