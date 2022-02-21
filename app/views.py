# -*- encoding: utf-8 -*-
from django.conf import ENVIRONMENT_VARIABLE, settings
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
from django import template
from .models import ProcessLayout, RtuSetting, SaveFile, UserDetail, ProcessList, Report, VariableDefault, Progress, ReportValue
from django.db.models import F, Func, Value, CharField
import json, datetime, os, time, re
from os import walk



# ==================================================================================================
# page requests
# ==================================================================================================

def login_handler(request):
    # if not logged in, then log into guest account
    if not request.user.is_authenticated: 
        guest = authenticate(username = 'guest', password = '123123')
        if guest is not None:
            login(request, guest)
            return 1
    return 0

# @login_required(login_url="/login/")
def index(request):
    if login_handler(request) == 1:
        print('login to guest')
    elif login_handler(request) == 0:
        print('already logged in')
    context = {
        'segment': 'index',
        'date': datetime.datetime.now().strftime('%-d %b %Y'),
        'time': datetime.datetime.now().strftime('%-I:%M %p'),
        'process_running': 'test',
    }
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))



# ==================================================================================================
# ajax
# ==================================================================================================

# ------------------- user -------------------
@login_required(login_url="/login/")
def user_profile(request):
    if request.method == 'POST':
        if request.POST.get('mode') == 'create':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            role = request.POST.get('role')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            form_valid = check_create_UserDetail(username, password1, password2)
            if form_valid == 'no_error':
                try:
                    user = User(username=username, password=make_password(password1), email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    UserDetail(user_id=user.id, phone_number=phone_number, role=role).save()
                    SaveFile(username=username, layout='[]', device='[]').save()
                    success = True
                    message = 'User profile created successfully'
                except:
                    success = False
                    message = 'Failed to create user profile'
            else:
                success = False
                message = form_valid
            data = {
                    'success': success,
                    'message': message,
                }
            return JsonResponse(data)
        
        elif request.POST.get('mode') == 'update':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            role = request.POST.get('role')
            try:
                User.objects.filter(username=username).update(email=email, first_name=first_name, last_name=last_name)
                user = User.objects.get(username=username)
                UserDetail.objects.filter(user_id=user.id).update(phone_number=phone_number, role=role)
                success = True
                message = 'User profile update successful'
            except:
                success = False
                message = 'Failed to update user profile'
            data = {
                'success': success,
                'message': message,
            }
            return JsonResponse(data)

        elif request.POST.get('mode') == 'update_password':
            print('update password')
            user = User.objects.get(username=request.user.username)
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            password_old = request.POST.get('password_old')
            try:
                if (check_password(password_old,user.password)):
                    if (password1 == password2):
                        user.set_password(password1)
                        user.save()
                        success = True
                        message = 'Password changed successfully'
                        login(request, user)
                    else:
                        success = False
                        message = 'Password does not match'
                else:
                    success = False
                    message = 'Invalid old password'
                pass
            except:
                success = False
                message = 'Failed to change password'

            data = {
                'success': success,
                'message': message,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'message': 'invalid request'})

    elif request.method == 'GET':
        if request.GET.get('mode') == 'get all':
            user_list = []
            for user in User.objects.all():
                temp ={}
                temp['username'] = user.username
                temp['email'] = user.email
                temp['first_name'] = user.first_name
                temp['last_name'] = user.last_name
                temp['phone_number'] = user.user_details.phone_number
                temp['role'] = user.user_details.role
                user_list.append(temp)
            data = {
                'success' : True,
                'message' : 'Retrieve all user profile successful',
                'user_list' : user_list,
            }
            return JsonResponse(data)

        elif request.GET.get('mode') == 'get one':
            username = request.GET.get('username')
            if username =='self':
                username = request.user.username 
            user = User.objects.get(username = username)
            data = {
                'success' : True,
                'message' : 'User profile retrieval successful',
                'username' : user.username,
                'email' : user.email,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'user_role' : user.user_details.role,
                'phone_number' : user.user_details.phone_number,
            }
            print(data)
            return JsonResponse(data)

    else: 
        return JsonResponse({'message': 'invalid request'})



# ------------------- widgets -------------------
@login_required(login_url="/login/")
def widget(request):
    if request.method == 'GET':
        if request.GET.get('mode') == 'get layout':
            try:
                all_widgets = SaveFile.objects.filter(username=request.user.username)
                if (len(all_widgets) == 0):
                    all_widgets = open(os.path.join(settings.BASE_DIR, 'static/assets/widget/default.txt')).read()
                    message = 'No saved widget layout found. Default layout loaded'
                else:
                    all_widgets = all_widgets[0].layout
                    message = 'Load saved widget layout successful'
                success = True
            except:
                success = False
                message = 'Failed to load widget layout'
                all_widgets = []
            data = {
                'success' : success, 
                'all_widgets':all_widgets,
                'message': message,
            }
            return JsonResponse(data)

        elif request.GET.get('mode') == 'get available':
            url = os.path.join(settings.BASE_DIR, 'static/assets/widget/')
            widget = [f.split('.')[0] for f in os.listdir(url) if (os.path.isfile(os.path.join(url, f)) and f.endswith('.html'))]
            message = 'Get available widget successful'
            success = True
            data = {
                'success': success,
                'widget': widget,
                'message': message,
            }
            return JsonResponse(data)

        # elif request.GET.get('mode') == 'get new widget id':

        #     widget_id = [f.split('.')[0] for f in os.listdir(url) if (os.path.isfile(os.path.join(url, f)) and f.endswith('.html'))]
        #     message = 'Get available widget successful'
        #     success = True
        #     data = {
        #         'success': success,
        #         'widget': widget,
        #         'widget_id': widget_id,
        #     }
        #     return JsonResponse(data)

        elif request.GET.get('mode') == 'get widget html':
            widget_type = request.GET.get('widget_type')
            url = os.path.join(settings.BASE_DIR, 'static/assets/widget/%s.html' % widget_type)
            widget = open(url).read()
            success = True
            message = 'Load widget successful'
            data = {
                'success': success,
                'html': widget,
                'message': message,
            }
            return JsonResponse(data)

        elif request.GET.get('mode') == 'get widget html all':
            widgets_html = []
            widget_layout = json.loads(list(SaveFile.objects.filter(username=request.user.username))[0].layout)

            for widget in widget_layout:
                widget_id = widget['widget_id']
                widget_type = widget['widget_type']
                url = os.path.join(settings.BASE_DIR, 'static/assets/widget/%s.html' % widget_type)
                widgets_html.append({'widget_id': widget_id, 'widget_html':open(url).read()})

            success = True
            message = 'Load widget successful'
            data = {
                'success': success,
                'widgets_html': widgets_html,
                'message': message,
            }
            return JsonResponse(data)

    elif request.method == 'POST':
        if request.POST.get('mode') == 'save layout':
            try:
                data = request.POST.get('widgets')
                SaveFile.objects.update_or_create(username=request.user.username, defaults={'layout':data})
                success = True
                message = 'Widget layout saved successfully'
            except:
                success = True
                message = 'Failed to save widget layout'
            data = {
                'success': success,
                'message': message,
            }
            return JsonResponse(data)

    else:
        return JsonResponse({'message': 'invalid request'})
    



# ------------------- rtu -------------------
@login_required(login_url="/login/")
def rtu_manager(request):
    if request.method == 'POST':
        if request.POST.get('mode') == 'save settings':
            try:
                rtu_id = request.POST.get('rtu_id')
                rtu_location = request.POST.get('rtu_location')
                moist_threshold = request.POST.get('moist_threshold')
                wet_threshold = request.POST.get('wet_threshold')
                min_tag_reading = request.POST.get('min_tag_reading')
                reading_average = request.POST.get('reading_average')
                reading_time = request.POST.get('reading_time')
                # print('settings update for reader_id: %s' % reader_id)

                RtuSetting.objects.filter(rtu_id=rtu_id).update(rtu_location=rtu_location, moist_threshold=moist_threshold, wet_threshold=wet_threshold, average=reading_average, min_tag_read=min_tag_reading, data_sampling_interval=reading_time, sent=0)
                success = True
                message = 'Reader Settings Updated Successfully'
            except Exception as e:
                success = False
                message = 'Reader settings update failed. %s' % e
            data = {
                'success': success,
                'message': message,
            }
            return JsonResponse(data)
        
    elif request.method == 'GET':
        if request.GET.get('mode') == 'readertable_datatable':
            reader_list = list(RtuSetting.objects.filter(enabled=1).extra(select={'last_connected':"DATE_FORMAT(last_connected, '%%Y-%%m-%%d %%H:%%i:%%S')"}).values('rtu_name', 'status', 'last_connected', 'rtu_location'))
            return JsonResponse(reader_list, safe=False)

        elif request.GET.get('mode') == 'get settings':
            try:
                rtu_id = request.GET.get('rtu_id')
                RtuSettings = list(RtuSetting.objects.filter(rtu_id=rtu_id).values('moist_threshold', 'wet_threshold', 'average', 'data_sampling_interval', 'rtu_location', 'min_tag_read'))
                success = True
                message = 'Get rtu settings successful'
            except:
                success = False
                RtuSettings = 'none'
                message = 'Failed to get rtu settings'
            data = {
                'success': success,
                'message': message,
                'rtu_settings': RtuSettings,
            }
            print(data)
            return JsonResponse(data)

        elif request.GET.get('mode') == 'get rtu list':
            username = request.user.username
            rtu_list = list(RtuSetting.objects.filter(enabled=1).values('rtu_name', 'rtu_id', 'rtu_location'))
            location_list = list(RtuSetting.objects.filter(enabled=1).values('rtu_location').distinct())
            success = True
            message = 'Get rtu list successful'
            data = {
                'success': success,
                'message': message,
                'rtu_list': rtu_list,
                'location_list': location_list,
            }
            # print(data)
            return JsonResponse(data)
    else:
        return JsonResponse({'message': 'invalid request'})


# ==================================================================================================
# functions
# ==================================================================================================

def check_create_UserDetail(username, password1, password2):
    error = 'no_error'
    if password1 != password2:
        error = 'Password does not match'
    if User.objects.filter(username=username).exists():
        error = 'Username already exists'
    return error








# ==================================================================================================
# monitoring_sys
# ==================================================================================================


def trigger_event(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        if request.GET.get('mode') == 'trigger event':
            event_name = request.GET.get('event_name').replace(' ', '_')
            url = os.path.join(settings.BASE_DIR, 'static/assets/widget/%s.html' % event_name)
            html = open(url).read()
            success = True
            message = 'test message'
            data = {
                'success': success,
                'message': message,
                'html': html,
            }
            print(data)
            return JsonResponse(data)
        
        elif request.GET.get('mode') == 'get status':
            current_process = ProcessList.objects.filter(status='active')
            if len(current_process) > 0:
                current_process_name = current_process[0].category
                process_running = True
            else:
                current_process_name = 'idle'
                process_running = False

            layout = ProcessLayout.objects.filter(name=current_process_name.replace('_', ' '))[0].layout
            url = os.path.join(settings.BASE_DIR, 'static/assets/widget/%s.html' % current_process_name.replace(' ', '_'))
            html = open(url).read()

            success = True
            message = 'test message'
            data = {
                'success': success,
                'message': message,
                'layout': layout,
                'html': html,
                'process_running': process_running,
            }
            # print(data)
            return JsonResponse(data)

def get_progress(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        if request.GET.get('mode') == 'get progress':
            description = list(Progress.objects.all().extra(select={'timestamp':"DATE_FORMAT(timestamp, '%%I:%%i:%%S %%p')"}).values('description', 'timestamp').order_by('timestamp'))
            percentage = list(Progress.objects.filter(percentage__isnull=False).order_by('-timestamp').values('percentage'))
            if len(percentage) > 0:
                percentage = float(percentage[0]['percentage'])
            else:
                percentage = 0
            success = True
            message = 'get progress succesful'
            data = {
                'success': success,
                'message': message,
                'description': description,
                'percentage': percentage,
            }
            print(data)
            return JsonResponse(data)

def report(request):
    if request.method == 'POST':
        if request.POST.get('mode') == 'export report':
            report_list = json.loads(request.POST.get('report_list'))
            for report in report_list:
                print(report)
            success = True
            message = 'Export report successful'
            data = {
                'success': success,
                'message': message,
            }
        
            print(data)
            return JsonResponse(data)

    elif request.method == 'GET':
        if request.GET.get('mode') == 'get reports':
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%Y/%m/%d')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%Y/%m/%d').replace(hour=23, minute=59, second=59, microsecond=999999)
            report_list2 = list(Report.objects.filter(time_completed__range = [start_date, end_date], deleted=False).extra(select={'time_completed':"DATE_FORMAT(time_completed, '%%d %%b %%Y - %%I:%%i %%p')"}).values('file_name', 'time_completed'))
            x = []
            report_list = []
            report_dir = os.path.join(settings.BASE_DIR, 'static/assets/reports/')
            for (dirpath, dirnames, filenames) in walk(report_dir):
                x.extend(filenames)
                break
            for filename in x:
                created_time = os.path.getmtime(report_dir+filename)
                report_list.append({'reportname': filename, 'created_time':created_time})
            success = True
            message = 'test message'
            data = {
                'success': success,
                'message': message,
                'report_list': x,
            }
            return JsonResponse(report_list2, safe=False)

        if request.GET.get('mode') == 'get report fields':
            file_name = request.GET.get('file_name')
            report_fields = list(ReportValue.objects.filter(file_name=file_name).values('fields'))
            return JsonResponse(report_fields, safe=False)

        
def default_values(request):
    if request.method == 'POST':
        if request.POST.get('mode') == 'save default values':
            values = json.loads(request.POST.get('value_list'))
            for i in values:
                name = i['name'].replace('settings ', '')
                process = i['process']
                value = i['value']
                VariableDefault.objects.filter(process=process, name=name).update(value=value, value_set=value)
            success = True
            message = 'Settings updated succesfully.'
            data = {
                'success': success,
                'message': message,
            }
            return JsonResponse(data)

    elif request.method == 'GET':
        if request.GET.get('mode') == 'get default values':
            default_value_list = list(VariableDefault.objects.filter(enable_set='true').values('name', 'value', 'process', 'unit').order_by('process'))
            success = True
            message = 'get default value SUCCESSFUL'
            data = {
                'success': success,
                'message': message,
                'default_value_list': default_value_list,
            }
            return JsonResponse(data)

        elif request.GET.get('mode') == 'get default values specific':
            process_name = request.GET.get('process_name')
            parameters = json.loads(request.GET.get('parameters'))
            variables_list = list(VariableDefault.objects.filter(process=process_name, name__in=parameters).values('name', 'value', 'unit').order_by('name'))
            success = True
            message = 'get default value SUCCESSFUL'
            data = {
                'success': success,
                'message': message,
                'variables_list': variables_list,
            }
            print(data)
            return JsonResponse(data)


def date_time_clock(request):
    if request.method == 'GET':
        if request.GET.get('mode') == 'get date time':
            date = datetime.datetime.now().strftime('%-d %b %Y')
            time = datetime.datetime.now().strftime('%-I:%M %p')
            data = {
                'date': date,
                'time': time,
                'username': request.user.username,
            }
            return JsonResponse(data)