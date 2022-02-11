# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    
    # ===============================
    # ajax
    # ===============================
    
    # path('get_device_status/', views.get_device_status, name='get_device_status'),

    path('widget/', views.widget, name='widget'),

    path('user_profile/', views.user_profile, name='user_profile'),

    path('rtu_manager/', views.rtu_manager, name='rtu_manager'),

    path('trigger_event/', views.trigger_event, name='trigger_event'),

    path('report/', views.report, name='report'),

    path('default_values/', views.default_values, name='default_values'),

    path('get_progress/', views.get_progress, name='get_progress'),

    path('date_time_clock/', views.date_time_clock, name='date_time_clock'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]

# urlpatterns = [
# 
#     # The home page
#     path('monitoring-sys/', views.index, name='home'),
#     
#     # ===============================
#     # ajax
#     # ===============================
#     
#     # path('get_device_status/', views.get_device_status, name='get_device_status'),
# 
#     path('monitoring-sys/widget/', views.widget, name='widget'),
# 
#     path('monitoring-sys/user_profile/', views.user_profile, name='user_profile'),
# 
#     path('monitoring-sys/rtu_manager/', views.rtu_manager, name='rtu_manager'),
# 
#     path('monitoring-sys/trigger_event/', views.trigger_event, name='trigger_event'),
# 
#     path('monitoring-sys/report/', views.report, name='report'),
# 
#     path('monitoring-sys/default_values/', views.default_values, name='default_values'),
# 
#     path('monitoring-sys/get_progress/', views.get_progress, name='get_progress'),
# 
#     path('monitoring-sys/date_time_clock/', views.date_time_clock, name='date_time_clock'),
# 
#     # Matches any html file
#     re_path(r'^.*\.*', views.pages, name='pages'),
# 
# ]
