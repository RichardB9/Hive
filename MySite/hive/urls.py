'''
Created on 29 Jul 2017

@author: Richard
'''

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^board$', views.board, name='board'),
]