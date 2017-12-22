
# Create your models here.
#login-register models#
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, postData):
        print postData

        #validations go here
        #not blank
        errors = []
        if len(postData['name']) < 1:
            errors.append("Name cannot be blank")
        if len(postData['alias']) < 1:
            errors.append("Alias cannot be blank")
        if len(postData['email']) < 1:
            errors.append("Email cannot be blank")
        #password > 8
        if len(postData['password']) < 8:
            errors.append("Password must be atleast 8 characters")
        if postData['password'] != postData['c_password']:
            errors.append("Passwords don't match")
        if len(postData['birthday']) < 1:
            errors.append("Your birthday cannot be blank")

        if len(errors) > 0:
            return (False, errors) 
        else:
            #create the user if no errors
            datetime_object = datetime.strptime(postData['birthday'],'%Y-%m-%d')
            user = self.create(
                name=postData['name'],
                alias=postData['alias'],
                email=postData['email'],
                birthday=postData['birthday'],
                password=postData['password'],
            )
            #go to register and validate if [0]
            #return to ("/poke") in the project level URL, it will then go to poke_app URL, then poke/index.html
            return (True, user)       
        #validate login
    def validate_login(self, postData):
        errors=[]
        print postData
        if len(postData['email']) < 1 or len(postData['password']) < 1:
            errors.append("Login fields cannot be empty")
            return (False, errors)
        user = User.objects.filter(email=postData['email'])

        print user
        print user[0].password
        print postData['password']
        #print type(postData['password']) #type of what kind of data

        if postData['password'] != user[0].password:
            errors.append("Email password combination invalid")
            return (False, errors)
        else:
            return (True, user[0])

        #once validations entered -- in views
#make sure to migrate and import model into views.py
class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()


class Wish_ItemsManager(models.Manager):
    def product_validation(self, data):
        errors = {}
        if len(data['product']) < 3:
            errors["product"] = "Cannot add blank item. Must be more than 3 characters."
        return errors

        

class Wish_Items(models.Model):
    product = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='created_product')
    joined_by = models.ManyToManyField(User, related_name='product_joined')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = Wish_ItemsManager()
    def __repr__(self):
        return "{}, {} ".format(self.product)