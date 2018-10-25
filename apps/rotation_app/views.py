# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import re, bcrypt, datetime

from .models import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX  = re.compile('[0-9]')

def getScheduledCombos(user_id):
    print("getScheduledCombo()")
    current_date = datetime.datetime.today()
    start = datetime.date.today()
    end = start + datetime.timedelta(days=1)
#Model.objects.filter(datetime__range=(start, end))        <h5>Here is your scheduled combo for the day!</h5>

    retObj = Schedule.objects.filter(scheduled_by_id=user_id).all().filter(date_scheduled__range=(start, end))
#    print(retObj.values())
    if retObj.count() == 0:
        return None
    else:
        return retObj.all()

# the index function is called when root is visited
def index(request):
    print("index()")

    if "user_id" not in request.session:
        return redirect("/login_registration")

    logged_in_user_id = request.session['user_id']
    user = User.objects.get(id=logged_in_user_id)

    scheduled_combos = getScheduledCombos(logged_in_user_id)
    print(scheduled_combos.count())

    if scheduled_combos == None:
        context = {
            "user": user,
        }
        return render(request, "home_none.html", context)
    elif scheduled_combos:
        print(scheduled_combos)
        strdate = datetime.datetime.strftime(datetime.datetime.today(), "%m-%d-%Y")
        
        context = {
            "user": user,
            "date": strdate,
            "combos": scheduled_combos,
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
    logged_in_user_id = request.session['user_id']

    user = User.objects.get(id=logged_in_user_id)
    user_tops = Top.objects.filter(top_added_by_id=logged_in_user_id).all()
    user_bottoms = Bottom.objects.filter(bottom_added_by_id=logged_in_user_id).all()

    context = {
        "user":  user,
        "tops": user_tops,
        "bottoms": user_bottoms,
    }

    return render(request, "combomaker.html", context)

def show_combobrowser(request):
    print("show_combobrowser()")

    logged_in_user_id = request.session['user_id']
    user = User.objects.get(id=logged_in_user_id)

    combos = User.objects.get(id=logged_in_user_id).combo_by.all()

    context = {
        "user":  user,
        "combos": combos,
    }

    return render(request, "combobrowser.html", context)


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

def process_combo(request):
    print("process_combo()")

    logged_in_user_id = request.session['user_id']

    if request.method == "POST":
        print(request.POST['currentTopID'])
        print(request.POST['currentBottomID'])        

        top_id = request.POST['currentTopID']
        bottom_id = request.POST['currentBottomID']

        Combo.objects.create(top_chosen_id=top_id, bottom_chosen_id=bottom_id, created_by_id=logged_in_user_id)

    return redirect('/')                

def show_comboscheduler(request):
    print("show_comboscheduler()")

    logged_in_user_id = request.session['user_id']

    if request.method == "POST":
        combo_id = request.POST['currentComboID']
        user = User.objects.get(id=logged_in_user_id)
        chosen_combo = Combo.objects.get(id=combo_id)

        context = {
            "user": user,
            "combo": chosen_combo,
        }

    return render(request, "comboscheduler.html", context)

def process_schedulecombo(request):
    print("process_schedulecombo()")

    if request.method == "POST":
        print(request.POST['userid'])
        print(request.POST['comboid'])
        print(request.POST['chosendate'])

        uid = request.POST['userid']
        comboid = request.POST['comboid']
        strscheduleddate = request.POST['chosendate']

        objdt = datetime.datetime.strptime(strscheduleddate, '%m-%d-%Y')
        Schedule.objects.create(date_scheduled=objdt, combo_chosen_id=int(comboid), scheduled_by_id=int(uid))

    return redirect('/show_schedule')

def show_schedule(request):
    print("show_schedule()")

    logged_in_user_id = request.session['user_id']
    user = User.objects.get(id=logged_in_user_id)

    scheduledcombos = Schedule.objects.filter(scheduled_by_id=logged_in_user_id).order_by("date_scheduled")

    context = {
        "user": user,
        "scheduledcombos": scheduledcombos,
    }

    return render(request, "comboschedule.html", context)    


def logoff(request):
    print("logoff()")
    return redirect('/login_registration/logoff')