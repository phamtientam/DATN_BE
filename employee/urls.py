from django.urls import path
from . import views

# define the urls
urlpatterns = [
    path('avg_age/', views.analyze_data_avg_age),
    path('employee_by_department/', views.analyze_data_employee_by_department),
    path('employee_by_family_and_single/', views.analyze_employee_breakdown_by_family_and_single),
]
