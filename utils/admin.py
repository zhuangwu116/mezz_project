# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from utils.urls import admin_url

class SingletonAdmin(admin.ModelAdmin):
    def handle_save(self,request,response):
        form_valid = isinstance(response,HttpResponseRedirect)
        if request.POST.get("_save") and form_valid:
            return redirect("admin:index")
        return response
    def add_view(self,*args,**kwargs):
        try:
            singleton = self.model.objects.get()
        except (self.model.DoesNotExist,self.model.MultipleObjectsReturned):
            kwargs.setdefault("extra_context",{})
            kwargs["extra_context"]["singleton"]=True
            response=super(SingletonAdmin,self).add_view(*args,**kwargs)
            return self.handle_save(args[0],response)
        return redirect(admin_url(self.model,"change",singleton.id))
    def changelist_view(self,*args,**kwargs):
        try:
            singleton = self.model.objects.get()
        except self.model.MultipleObjectsReturned:
            return super(SingletonAdmin,self).changelist_view(*args,**kwargs)
        except self.model.DoesNotExist:
            return redirect(admin_url(self.model,"add"))
        return redirect(admin_url(self.model,"change",singleton.id))
    def change_view(self, *args,**kwargs):
        kwargs.setdefault("extra_context",{})
        kwargs["extra_context"]["singleton"] = self.model.objects.count() == 1
        response = super(SingletonAdmin,self).change_view(*args,**kwargs)
        return self.handle_save(args[0],response)