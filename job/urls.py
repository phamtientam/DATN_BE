from django.urls import path
from . import views

# define the urls
urlpatterns = [
    path('get_list_job_position/', views.get_list_job_position),
    path('analyze_count_job_by_employee/', views.analyze_count_job_by_employee),
    path('get_employee_by_job/', views.get_employee_by_job),
]
