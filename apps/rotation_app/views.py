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
    print(current_date)

    start = datetime.date.today()
    end = start + datetime.timedelta(days=1)
#Model.objects.filter(datetime__range=(start, end))

    retObj = Schedule.objects.filter(date_scheduled__range=(start, end))
    if retObj.count() == 0:
        return None
    else:
        print(retObj.values())
        return retObj[0]
        

# the index function is called when root is visited
def index(request):
    print("index()")


    if "user_id" not in request.session:
        return redirect("/login_registration")

    logged_in_user_id = request.session['user_id']
    user = User.objects.get(id=logged_in_user_id)

    scheduled_combo = getScheduledCombo(logged_in_user_id)

    if scheduled_combo == None:
        context = {
            "user": user,
        }
        return render(request, "home_none.html", context)
    elif scheduled_combo:
        combo_id = scheduled_combo.combo_chosen_id
        combo = Combo.objects.get(id=combo_id)
        top = combo.top_chosen
        bottom = combo.bottom_chosen
        
        context = {
            "user": user,
            "top": top,
            "bottom": bottom,
        }
        return render(request, "home_combo_found.html", context)
    

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

    