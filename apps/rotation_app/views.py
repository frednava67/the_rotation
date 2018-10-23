# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import re, bcrypt

from .models import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX  = re.compile('[0-9]')

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
    # if request.user_agent.is_mobile:
        # pageToRender = 'mhome.html'
    else:
        pageToRender = 'home.html'
    return render(request, pageToRender, context)

    