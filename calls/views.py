from .serializers import CallRecordSerializer
from .models import CallRecord
from datetime import datetime, date, time, timedelta
from django.shortcuts import get_list_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response


CALL_STANDING_CHARGE = 0.36
CALL_MIN_CHARGE = 0.09


class CallRecordViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.all()
    serializer_class = CallRecordSerializer
    filter_fields = ('source', 'start_call')

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        instance = self.queryset.get(id=data.get('id'))
        serializer = self.serializer_class(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BillViewSet(viewsets.ModelViewSet):
    def create(self, request):
        data = request.data
        source = data.get('source')
        period = data.get('period')
        bill = {'total_price': 00.00, 'source': source,
                'period': period, 'call_record': []}

        if not source:
            return Response("Invalid request. Missing source",
                            status=status.HTTP_400_BAD_REQUEST)

        if period:
            queryset = CallRecord.objects.filter(source=source).filter(
                end_call__year=period.split('/')[1],
                end_call__month=period.split('/')[0])
        else:
            default_date = date.today().replace(day=1) - timedelta(days=1)
            bill['period'] = f'{default_date.month}/{default_date.year}'
            queryset = CallRecord.objects.filter(source=source).filter(
                end_call__year=default_date.year,
                end_call__month=default_date.month)

        list_call = get_list_or_404(queryset)

        for call in list_call:
            destination = call.destination
            start_date = call.start_call.date().strftime('%d/%b/%Y')
            start_time = call.start_call.time()
            duration = call.end_call - call.start_call
            price = self.get_call_rec_price(
                call.start_call, call.end_call, duration)

            call_record = {
                'destination': destination, 'start_call_date': start_date,
                'start_call_time': start_time, 'duration': str(duration),
                'price': round(price, 2)}

            bill['total_price'] += price
            bill['call_record'].append(call_record)

        return Response(data=bill, status=status.HTTP_200_OK)

    def get_call_rec_price(self, initial_call, final_call, duration):
        t_limit_6 = time(6)
        t_limit_22 = time(22)
        end_call_time = final_call.time()
        start_call_time = initial_call.time()
        charge = timedelta(0, 0, 0)

        if end_call_time >= start_call_time:
            if t_limit_6 <= start_call_time <= t_limit_22:
                if t_limit_6 <= end_call_time <= t_limit_22:
                    charge = final_call - initial_call
                else:
                    charge = datetime.combine(
                        date.min, t_limit_22) - datetime.combine(
                            date.min, start_call_time)
            else:
                if t_limit_6 <= end_call_time <= t_limit_22:
                    charge = datetime.combine(
                        date.min, end_call_time) - datetime.combine(
                            date.min, t_limit_6)
                else:
                    charge = datetime.combine(
                        date.min, t_limit_22) - datetime.combine(
                            date.min, t_limit_6)
        else:
            if t_limit_6 <= start_call_time <= t_limit_22:
                charge = datetime.combine(
                    date.min, t_limit_22) - datetime.combine(
                        date.min, start_call_time)
            if t_limit_6 <= end_call_time <= t_limit_22:
                charge += datetime.combine(
                    date.min, end_call_time) - datetime.combine(
                        date.min, t_limit_6)

        total_min_charge = int(charge.total_seconds()/60)

        if duration.days > 0:
            charge_per_day = datetime.combine(
                date.min, t_limit_22) - datetime.combine(
                    date.min, t_limit_6)
            total_min_charge += int(
                charge_per_day.total_seconds()/60) * duration.days

        total_charge = round(
            total_min_charge * CALL_MIN_CHARGE + CALL_STANDING_CHARGE, 2)

        return total_charge
