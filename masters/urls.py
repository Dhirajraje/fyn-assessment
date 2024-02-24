from django.urls import path
from .views import (DBPView,DayDropdown,AuditTrailView,DAPView,
                    TMFView,WCView,CalculationView)


urlpatterns = [
    path('dbp-master/',DBPView.as_view()),
    path('dap-master/',DAPView.as_view()),
    path('tmf-master/',TMFView.as_view()),
    path('wc-master/',WCView.as_view()),
    path('day-dropdown/',DayDropdown.as_view()),
    path('audits/',AuditTrailView.as_view()),
    path('calculations/',CalculationView.as_view()),
]