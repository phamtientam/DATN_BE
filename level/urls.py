from django.urls import path
from . import views

# define the urls
urlpatterns = [
    path('analyze_count_level_by_employee/', views.analyze_count_level_by_employee),
    path('get_employee_by_level/', views.get_employee_by_level),
]
