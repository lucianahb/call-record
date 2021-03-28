from django.contrib import admin
from .models import CallRecord


@admin.register(CallRecord)
class CallRecordAdmin(admin.ModelAdmin):
    list_display = ('call_id','start_call', 'end_call', 'source', 'destination')
