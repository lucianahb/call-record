from .serializers import CallRecordSerializer
from .models import CallRecord
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action


class CallRecordViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.all()
    serializer_class = CallRecordSerializer
    filter_fields = ('source', 'start_call')

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(call_id=request.data.get('call_id'))
        print(self.queryset)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
