from .models import CallRecord
from rest_framework import serializers


class CallRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallRecord
        fields = (
            'id',
            'start_call',
            'end_call',
            'source',
            'destination',
        )
