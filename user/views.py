from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse

# Create your views here.


class Create(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Create')


class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Update')


class LogIn(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LogIn')


class LogOut(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LogOut')
