"""
URL configuration for electionBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from election import views
urlpatterns = [
    path('', views.index, name = "index"),
    path('login', views.login, name='page_login'),
    path('register', views.register, name='page_register'),
    path('vote', views.vote, name='page_vote'),
     path('process-registration/', views.recieveRegistration, name='registration_data'),
     path('process-login/', views.recieveLogin, name='login_data'),
     path('process-signOut/', views.signOut, name = 'sign_out'),
     path('process-vote/', views.submitVote, name="submit_vote"),
     path('fetch-polldata/', views.refreshPoll, name = "refresh_poll"),
    
]
