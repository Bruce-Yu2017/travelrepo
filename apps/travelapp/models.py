# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime
# Create your models here.
class UserManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        name_regex = re.compile(r'^[A-Z][a-z][a-z\\s]+$')
        pw_regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        username_regex = re.compile(r'^[A-Za-z]{3,}$')

        if len(postData['name']) < 1 :
            errors['name'] = 'Name field can not be empty!'
        else:
            if len(postData['name']) < 3 :
                errors['name'] = 'Name field should have at least 3 characters!'
            else:                
                if not name_regex.match(postData['name']):
                    errors['name']= 'Incorrect name format!!'
        ##############
        if len(postData['username']) <1:
            errors['username'] = 'Username field can not be empty!!!'
        else:
            if len(postData['username']) < 3 :
                errors['username'] = 'Username field should have at least 3 characters!'
            else:
                if not username_regex.match(postData['username']):
                    errors['username'] = 'Incorrect Username format'
                else:
                    if User.objects.filter(username = postData['username']):
                        errors['username'] = 'username has been registered, Please use other username.'
        #################
        if len(postData['password']) < 1:
            errors['password']= 'Password field can not be empty!!!'
        else:
            if len(postData['password']) < 8:
                errors['password']= 'Password should have at least 8 characters!!!!'
            else:
                if not pw_regex.match(postData['password']):
                    errors['password'] = "Password should have at least one letter and one number!"
        ################### 
        if len(postData['con_pw']) < 1:
            errors['con_pw']= 'Confirm password field can not be empty!!!'
        else:
            if postData['con_pw'] != postData['password']:
               errors['con_pw'] = "Password confirmation do not match!!"  

        return errors

    def login_validator(self, postData):
        errors = {}
        pw_regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        username_regex = re.compile(r'^[A-Za-z]{3,}$')       
        
        if len(postData['login_user']) <1 :
            errors['login_user'] = 'Username field can not be empty!!!'
        else:
            if not username_regex.match(postData['login_user']):
                errors['login_user'] = 'Incorrect username format'
            else:
                if not User.objects.filter(username = postData['login_user']):
                    errors['login_user'] = 'Please enter correct Username!!'
        #################
        if len(errors) < 1:
            if len(postData['login_pass']) < 1:
                errors['login_pass'] =  'Password field can not be empty!!!'
            else:
                if not pw_regex.match(postData['login_pass']):
                    errors['login_pass'] = "Password should have at least 8 characters!"
                else:
                    user = User.objects.get(username = postData['login_user'])
                    print user.password
                    if not bcrypt.checkpw(postData['login_pass'].encode(), user.password.encode()):
                        errors['login_pass'] = "Incorrect password!"
        return errors

    def trip_validator(self, postData):
        errors = {}
        date_regex = re.compile(r'^(((0?[1-9]|1[012])/(0?[1-9]|1\d|2[0-8])|(0?[13456789]|1[012])/(29|30)|(0?[13578]|1[02])/31)/(19|[2-9]\d)\d{2}|0?2/29/((19|[2-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[3579][26])00)))$') 
        if len(postData['destination']) < 1 :
            errors['destination'] = "Destination filed can not be empty!"

        if len(postData['desc']) < 1 :
            errors['desc'] = "Description filed can not be empty!"

        if len(postData['date_from']) < 1 :
            errors['date_from'] = "Starting date filed can not be empty!"
        else:
            if not date_regex.match(postData['date_from']):
                errors['date_from'] = "Incorrect date format!"
            else:
                date_object = datetime.strptime(postData['date_from'], '%m/%d/%Y')
                if date_object < datetime.now():
                    errors['date_from'] = "Starting date should be future date!!"

        if len(postData['date_to']) < 1 :
            errors['date_to'] = "Ending date filed can not be empty!"
        else:
            if not date_regex.match(postData['date_to']):
                errors['date_to'] = "Incorrect date format!"
            else:
                date_object1 = datetime.strptime(postData['date_from'], '%m/%d/%Y')
                date_object2 = datetime.strptime(postData['date_to'], '%m/%d/%Y')
                if date_object1 > date_object2:
                    errors['date_to'] = "Starting date should be before Ending date!!"
        
        return errors

            


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at =  models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
    def __str__(self):
           return self.name

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    creator = models.ForeignKey(User,related_name = 'trips')
    followers = models.ManyToManyField(User,related_name = 'plans')
    created_at =  models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __str__(self):
           return self.destination
