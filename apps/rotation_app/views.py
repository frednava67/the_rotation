# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import re, bcrypt, datetime, random

from .models import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX  = re.compile('[0-9]')

def getScheduledCombos(user_id):
    print("getScheduledCombo()")
    current_date = datetime.datetime.today()
    start = datetime.date.today()
    end = start + datetime.timedelta(days=1)
    retObj = Schedule.objects.filter(scheduled_by_id=user_id).all().filter(date_scheduled__range=(start, end))
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

    # if request.user_agent.is_mobile:
    #     pageToRender = 'mhome.html'
    # else:
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
        bFM2 = Top.objects.db_check(request)
        if bFlashMessage or bFM2:
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


def tops(request):
    if "user_id" not in request.session:
        return redirect("/login_registration")

    logged_in_user_id = request.session['user_id']
    
    user = User.objects.get(id=logged_in_user_id)
    tops = Top.objects.all().filter(top_added_by_id=int(logged_in_user_id))

    context = {
        "user": user,
        "tops": tops,
    }
    return render(request, 'tops.html', context)

def bottoms(request):
    if "user_id" not in request.session:
        return redirect("/login_registration")

    logged_in_user_id = request.session['user_id']
    
    user = User.objects.get(id=logged_in_user_id)
    bottoms = Bottom.objects.all().filter(bottom_added_by_id=int(logged_in_user_id))

    context = {
        "user": user,
        "bottoms": bottoms,
    }
    return render(request, 'bottoms.html', context)


def edit_top(request, id):
    top = Top.objects.get(id = id)
    if int(request.session['user_id']) == top.top_added_by_id: 
        context = {
            'top' : top,
        }
        return render(request, 'edittop.html', context)
    return redirect('/')

def process_edit_top(request, id):
    if request.method == 'POST':
        top = Top.objects.get(id = id)
        top.name = request.POST['textName']
        top.save()
    return redirect('/tops')



def edit_bottom(request, id):
    bottom = Bottom.objects.get(id = id)
    if int(request.session['user_id']) == bottom.bottom_added_by_id: 
        context = {
            'bottom' : bottom,
        }
        return render(request, 'editbottom.html', context)
    return redirect('/')


def process_edit_bottom(request, id):
    if request.method == 'POST':
        bottom = Bottom.objects.get(id = id)
        bottom.name = request.POST['textName']
        bottom.save()
    return redirect('/bottoms')




def process_combo(request):
    print("process_combo()")

    logged_in_user_id = request.session['user_id']

    if request.method == "POST":
        print(request.POST['currentTopID'])
        print(request.POST['currentBottomID'])  
        bFlashMessage = Combo.objects.combo_validator(request)    
        if bFlashMessage:
            print("COMBO ALREADY EXISTS")
            return redirect('/browse_combos')

        top_id = request.POST['currentTopID']
        bottom_id = request.POST['currentBottomID']

        Combo.objects.create(top_chosen_id=top_id, bottom_chosen_id=bottom_id, created_by_id=logged_in_user_id)

    return redirect('/browse_combos')                

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

def delete_top(request, id):
    top = Top.objects.get(id=id)
    if int(request.session['user_id']) == top.top_added_by_id: 
        top.delete()
    return redirect('/tops')

def delete_bottom(request, id):
    bottom = Bottom.objects.get(id=id)
    if int(request.session['user_id']) == bottom.bottom_added_by_id: 
        bottom.delete()
    return redirect('/bottoms')

def delete_scheduled_combo(request):
    logged_in_user_id = request.session['user_id']

    if request.method == "POST":
        scheduled_combo_to_delete = request.POST['scheduledcomboid']
        objScheduledCombo = Schedule.objects.get(id=scheduled_combo_to_delete)
        objScheduledCombo.delete()

    return redirect('/show_schedule')

def delete_combo(request):
    print("delete_combo")

    logged_in_user_id = request.session['user_id']

    if request.method == "POST":
        combo_id = request.POST['deleteComboID']
        combo_to_delete = Combo.objects.get(id=combo_id)
        combo_to_delete.delete()

    return redirect('/browse_combos')

def random_combo(request):
    print("random_combo")

    logged_in_user_id = request.session['user_id']
    combos = Combo.objects.filter(created_by_id=logged_in_user_id)

    if combos.count() == 0:
        return redirect('browse_combos')

    ceiling = combos.count()
    lucky_number = random.randint(0,ceiling-1)
    print(lucky_number)
    combo = combos[lucky_number]
    user = User.objects.get(id=logged_in_user_id)

    context = {
        "user": user,
        "combo": combo,
    }

    return render(request, "random_combo.html", context)

def logoff(request):
    print("logoff()")
    return redirect('/login_registration/logoff')