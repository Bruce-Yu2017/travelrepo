# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
import bcrypt
from datetime import datetime
# Create your views here.
def index(request):
    if "id" in request.session:
        return render(request,'travelapp/index.html')
    else:
        request.session['id'] = ''
    return render(request,'travelapp/index.html')

def travels(request):
    the_user = User.objects.filter(id = request.session['id'])
    the_user = the_user[0]
    user_trips = Trip.objects.filter(creator = the_user)
    user_plans = the_user.plans.all()
    Other_plans = Trip.objects.all()

    user_plans = list(user_plans)
    Other_plans = list(Other_plans)
    Other_plans = [x for x in Other_plans if x not in user_plans]
    Other_plans = [x for x in Other_plans if x not  in user_trips]
    print Other_plans
    context ={
        'the_user':the_user,
        'user_trips':user_trips,
        'user_plans':user_plans,
        'Other_plans':Other_plans,
    }
    return render(request,'travelapp/travel.html', context)
    



def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error, extra_tags=tag )
        return redirect('/main')
    else:
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())        
        new_user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hash_pw)
        request.session['id'] = new_user.id
        return redirect('/travels')

def login(request):    
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error, extra_tags=tag )
        return redirect('/main')
    else:
        print request.POST['login_user']
        login_user = User.objects.filter(username = request.POST['login_user'])
        request.session['id'] = login_user[0].id    
        return redirect('/travels')


def logout(request):
    del request.session['id']
    return redirect('/')        

def add_travels(request):
    if request.method == 'GET':        
        return render(request,'travelapp/add.html')
    if request.method == 'POST':
        errors = User.objects.trip_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error, extra_tags=tag )
        return redirect('/travels/add')
    else:
        date_from = datetime.strptime(request.POST['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(request.POST['date_to'], '%Y-%m-%d')
        new_trip = Trip.objects.create(destination = request.POST['destination'],desc = request.POST['desc'], \
        creator = User.objects.get(id = request.session['id']), date_from = date_from, \
        date_to = date_to)
        return redirect('/travels')



def destination(request,travel_id):
    the_trip = Trip.objects.get(id = travel_id)
    followers = the_trip.followers.all()
    context ={
        'the_trip':the_trip,
        'followers':followers,
    }
    return render(request, 'travelapp/trip.html',context)

def join(request,travel_id):
    the_trip = Trip.objects.get(id = travel_id)
    the_user = User.objects.get(id = request.session['id'])
    the_trip.followers.add(the_user)
    return redirect('/travels')