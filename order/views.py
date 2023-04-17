from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse


class Pay(ListView):
    def get(self, *args, **kwargs):
        return HttpResponse('Pay')


class CloseOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Close Order')


class Detail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detail')

# Create your views here.
