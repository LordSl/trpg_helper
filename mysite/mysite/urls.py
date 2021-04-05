"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
import sys
sys.path.append('..')
from testapp import views as testapp_views
urlpatterns = [
    path('register', testapp_views.register),
    path('login', testapp_views.login),
    path('createRoom', testapp_views.createRoom),
    path('changeState', testapp_views.changeState),
    path('getAll', testapp_views.getAll),
    path('getRoom', testapp_views.getRoom),
    path('delAll', testapp_views.delAll),
    path('delRoom', testapp_views.delRoom),
    path('delUser', testapp_views.delUser),
]
