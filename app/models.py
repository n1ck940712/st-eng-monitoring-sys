# -*- encoding: utf-8 -*-

from enum import auto, unique
from os import set_inheritable
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, IntegerField
from django.utils import timezone
from datetime import datetime
from time import strftime


# ==============================================================
# custom field type for timestamp field
# ==============================================================

class UnixTimestampField(models.DateTimeField):
    """UnixTimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """
    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        typ=['TIMESTAMP']
        # See above!
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        # Use '%Y%m%d%H%M%S' for MySQL < 4.1
        return strftime('%Y-%m-%d %H:%M:%S',value.timetuple())


# ==============================================================
# general
# ==============================================================


class RtuSetting(models.Model):
    rtu_id = models.IntegerField()
    rtu_name = models.CharField(max_length=264)
    rtu_location = models.CharField(max_length=264)
    moist_threshold = models.FloatField()
    wet_threshold = models.FloatField()
    min_tag_read = models.IntegerField()
    average = models.IntegerField()
    data_sampling_interval = models.IntegerField()
    alarm = models.IntegerField()
    reboot = models.IntegerField()
    last_connected = models.DateTimeField(auto_now=True)
    sent = models.IntegerField()
    enabled = models.IntegerField()
    status = models.CharField(max_length=264)


class SaveFile(models.Model):
    username = models.CharField(max_length=264)
    layout = models.TextField(null=True)
    device = models.TextField(null=True)


class UserDetail(models.Model):
    user = models.OneToOneField(User, related_name='user_details', on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, null=True)


# monitoring sys

class ProcessLayout(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    layout = models.TextField(null=True)

    
class ProcessList(models.Model):
    order = models.IntegerField()
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    last_complete = UnixTimestampField()


class LogData(models.Model):
    batch = models.IntegerField()
    type = models.CharField(max_length=100)
    flow = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    flow_unit = models.CharField(max_length=10, null=True)
    pressure = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    pressure_unit = models.CharField(max_length=10, null=True)
    temperature = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    temperature_unit = models.CharField(max_length=10, null=True)
    heater_set = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    heater_set_unit = models.CharField(max_length=10, null=True)
    timestamp= UnixTimestampField()


class LogDataType(models.Model):
    type = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)


class Report(models.Model):
    type = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100, null=True)
    time_completed = UnixTimestampField()
    

class VariableDefault(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    value_set = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=10)
    process = models.CharField(max_length=100)
    prompt = models.CharField(max_length=100)
    check = models.CharField(max_length=100)
    enable_set = models.CharField(max_length=100)

class SensorReading(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=10)
    set_point = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    status = models.CharField(max_length=10, null=True)

class Progress(models.Model):
    process = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    percentage = models.DecimalField(max_digits=3, decimal_places=1)
    timestamp = UnixTimestampField()