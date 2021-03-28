from django.urls import include, path
from rest_framework import routers
from .views import CallRecordViewSet


router = routers.DefaultRouter()
router.register(r'Call-Record', CallRecordViewSet, basename="CallRecord")


urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]
