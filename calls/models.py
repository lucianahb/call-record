from django.db import models
from datetime import datetime


class CallRecord(models.Model):

    start_call = models.DateTimeField(default=datetime.now())
    end_call = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=13, null=True, blank=True)
    destination = models.CharField(max_length=13, null=True, blank=True)

    class Meta:
        unique_together = ('start_call', 'end_call')

    def __str__(self):
        return f"Id {self.id} | Source: {self.source} | Start at: {self.start_call}"
