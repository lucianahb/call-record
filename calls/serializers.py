from .models import CallRecord
from rest_framework import serializers


class CallRecordSerializer(serializers.ModelSerializer):

    def validate_source(self, data):
        if not data.isdigit():
            raise serializers.ValidationError('Hey, put a phone number, please!')

    def validate_destination(self, data):
        if not data.isdigit():
            raise serializers.ValidationError('Hey, put a phone number, please!')

    class Meta:
        model = CallRecord
        fields = (
            'id',
            'start_call',
            'end_call',
            'source',
            'destination',
        )
