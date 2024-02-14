from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import person
from .models import LoginRequest
import json

from firebase_admin import db
from firebase_admin import firestore

# Get a Firestore client
db = firestore.client()

# Get a database reference
#ref = db.reference('/')
signedPic = "assets/images/usersign.jpg"
guestPic = "assets/images/userpic.jpg"
context = {
                'auth' : False,
                'username': "Guest",
                'signedPic': guestPic,
                        }
# Read data
#data = ref.get()

# Write data
#ref.set({'key': 'value'})

def index(request):
    return render(request, "index.html", context)

def vote(request):
    return render(request, "page_vote.html", context)

def register(request):
    return render(request, "page_register.html", context)

def login(request):
    
    return render(request, "page_login.html", context)



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
        
        voter = person(firstname, surname, idnumber, email, password, conPass)
        
        
        if voter.checkID() == False:
            return JsonResponse({'message': 'Please enter a valid South African identification number'}, status = 400)
        
        
        elif voter.checkPassword() == False:
            return JsonResponse({'message': 'Please ensure that the passwords match'}, status = 400)
        
        else: 
            #print(voter.postNewUserToDatabase())
            if voter.postNewUserToDatabase() == "Exists":
                return JsonResponse({'message': 'Your account already exists, please try logging in'}, status = 400)
                
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
        
        if LoginRequest.confirmLogin(idnumber, password) == "Success":
            global status 
            status = "sign" 
            global context
            context = {
                'auth': True,
                'username': LoginRequest.fetchUser(idnumber),
                'signedPic': signedPic,
                        }
            #return render(request, 'page_login.html', context)
            return JsonResponse({'message': 'GoVote'})
        else:
            return JsonResponse({'message': 'Incorrect ID number or password'}, status = 400)
            
            
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})
