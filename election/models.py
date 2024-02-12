from django.db import models

# Create your models here.
class person:
    def __init__(self, firstname, surname, id,email, password):
        self.firstname = firstname
        self.surname = surname
        self.id = id
        self.email = email
        self.password = password