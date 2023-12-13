from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'event'

    def __str__(self):
        return self.title

    def get_event_date(self):
        return self.event_date.strftime('%m/%d/%Y %H:%M')

    def get_date_input_event(self):
        return self.event_date.strftime('%Y-%m-%dT%H:%M')

    def get_late_events(self):
        if self.event_date < datetime.now():
            return True
        else:
            return False
