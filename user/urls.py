from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.Create.as_view(), name='create'),
    path('update/', views.Update.as_view(), name='update'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),




]
