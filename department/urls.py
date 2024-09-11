from django.urls import path
from . import views

# define the urls
urlpatterns = [
    path('get_list_department/', views.get_list_department),
    path('analyze_count_department_by_employee/', views.analyze_count_department_by_employee),
    path('get_employee_by_department/', views.get_employee_by_department),
]
