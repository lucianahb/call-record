from django.db import models
from datetime import datetime


class CallRecord(models.Model):

    call_id = models.IntegerField(unique=True)
    start_call = models.DateTimeField(default=datetime.now())
    end_call = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=13, null=True, blank=True)
    destination = models.CharField(max_length=13, null=True, blank=True)

    class Meta:
        unique_together = ('call_id', 'source')

    def __str__(self):
        return f"Id {self.call_id} | Source: {self.source} | Destination: {self.destination}"
