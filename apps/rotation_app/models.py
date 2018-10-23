# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib, urllib.request, ssl

from django.db import models
from django.contrib import messages
from apps.login_registration.models import User

class ClothingManager(models.Manager):
    def basic_validator(self, newrequest):
        bFlashMessage = False

        name = newrequest.POST['name']
        imageURL = newrequest.POST['imageURL']

        # Name - Required; Can't be blank
        if len(name) < 1:
            messages.error(newrequest, u"Name cannot be blank", extra_tags="name")
            bFlashMessage = True  

        # Image URL - Required; Can't be blank
        if len(imageURL) < 1:
            messages.error(newrequest, u"Image URL cannot be blank", extra_tags="imageurl")
            bFlashMessage = True  

        # Image URL must be publically visible and have a content type of image
        ssl._create_default_https_context = ssl._create_unverified_context
        r = urllib.request.urlopen(imageURL)
        if (r.headers.get_content_maintype() != 'image'):
            messages.error(newrequest, u"Image URL must be public and valid and resolve to content type of image", extra_tags="imageurl")
            bFlashMessage = True          

        return bFlashMessage

class Top(models.Model):
    name = models.CharField(max_length=255)
    imageURL = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #relationships
    top_added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="combo_top_added_by")
    objects = ClothingManager()

class Bottom(models.Model):
    name = models.CharField(max_length=255)
    imageURL = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # relationships
    bottom_added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="combo_bottom_added_by")
    objects = ClothingManager()   

class Combo(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # relationships
    top_chosen = models.ForeignKey(Top, null=True, on_delete=models.SET_NULL, related_name="combo_top")
    bottom_chosen = models.ForeignKey(Bottom, null=True, on_delete=models.SET_NULL, related_name="combo_bottom")    
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="combo_by")  

class Schedule(models.Model):
    date_scheduled = models.DateTimeField(auto_now_add = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # relationships
    combo_chosen = models.ForeignKey(Top, null=True, on_delete=models.SET_NULL, related_name="chosen_combo")
    scheduled_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="combo_scheduled_by")    