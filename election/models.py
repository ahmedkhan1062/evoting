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
        
    def checkPassword(self):
        if self.tempPass == self.confirmPass:
            self.password = self.tempPass
            return True
        else:
            return False