from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import person
import json

def index(request):
    return render(request, "index.html")

def vote(request):
    return render(request, "page_vote.html")

def register(request):
    return render(request, "page_register.html")

def login(request):
    return render(request, "page_login.html")

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
        
        if voter.checkID() == True:
            return redirect('page_vote')
        else:
            return JsonResponse({'message': 'Please enter a valid South African identification number'}, status = 400)
        
        
        if voter.checkPassword() == True:
             return redirect('page_vote')
        else:
            return JsonResponse({'message': 'Please ensure that the passwords match'}, status = 400)
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
        
        
        
        print(posted_data)
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})
