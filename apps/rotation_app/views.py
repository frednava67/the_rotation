# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import re, bcrypt, datetime

from .models import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX  = re.compile('[0-9]')

def getScheduledCombo(user_id):
    current_date = datetime.datetime.today()
    retObj = Schedule.objects.filter(date_scheduled=current_date).count()
    if retObj.count() == 0:
        return False
    else:
        return retObj




# the index function is called when root is visited
def index(request):
    print("index()")


    if "user_id" not in request.session:
        return redirect("/login_registration")

    logged_in_user_id = request.session['user_id']
    
    user = User.objects.get(id=logged_in_user_id)
    tops = Top.objects.all().filter(top_added_by_id=int(logged_in_user_id))
    bottoms = Bottom.objects.all().filter(bottom_added_by_id=int(logged_in_user_id))

    context = {
        "user": user,
        "tops": tops,
        "bottoms": bottoms,
    }
    if request.user_agent.is_mobile:
        pageToRender = 'mhome.html'
    else:
        pageToRender = 'home.html'
    return render(request, pageToRender, context)

def show_add_top(request):
    print("show_add_top()")

    logged_in_user_id = request.session['user_id']
    user = User.objects.get(id=logged_in_user_id)

    context = {
        "user": user,
    }

    return render(request, "addtop.html", context)

def show_add_bottom(request):
    print("show_add_bottom()")

    logged_in_user_id = request.session['user_id']
    user = User.objects.get(id=logged_in_user_id)

    context = {
        "user": user,
    }

    return render(request, "addbottom.html", context)    

def process_add_top(request):
    print("process_add_top()")

    if request.method == "POST":
        bFlashMessage = Top.objects.basic_validator(request)

        if bFlashMessage:
            return redirect("/add_top")
        
        print(request.POST['userid'])
        print(request.POST['textName'])
        print(request.POST['textImageURL'])  

        name_to_add = request.POST['textName']
        url_to_add = request.POST['textImageURL']
        user_id_adding = request.POST['userid']

        Top.objects.create(name=name_to_add, imageURL=url_to_add, top_added_by_id=user_id_adding)

    return redirect('/')

def process_add_bottom(request):
    print("process_add_top()")

    if request.method == "POST":
        bFlashMessage = Bottom.objects.basic_validator(request)

        if bFlashMessage:
            return redirect("/add_bottom")
        
        print(request.POST['userid'])
        print(request.POST['textName'])
        print(request.POST['textImageURL'])  

        name_to_add = request.POST['textName']
        url_to_add = request.POST['textImageURL']
        user_id_adding = request.POST['userid']

        Bottom.objects.create(name=name_to_add, imageURL=url_to_add, top_added_by_id=user_id_adding)

    return redirect('/')

def show_combomaker(request):
    print("show_combomaker()")
    
    return render(request, "combomaker.html")

def edit_top(request):
    if "user_id" not in request.session:
        return redirect("/login_registration")

    logged_in_user_id = request.session['user_id']
    
    user = User.objects.get(id=logged_in_user_id)
    tops = Top.objects.all().filter(top_added_by_id=int(logged_in_user_id))
    bottoms = Bottom.objects.all().filter(bottom_added_by_id=int(logged_in_user_id))

    context = {
        "user": user,
        "tops": tops,
        "bottoms": bottoms,
    }
    return render(request, 'edittop.html', context)

def logoff(request):
    print("logoff()")
    return redirect('/login_registration/logoff')