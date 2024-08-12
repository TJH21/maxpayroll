from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PayrollRunViewSet

router = DefaultRouter()
router.register(r'payroll-runs', PayrollRunViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
