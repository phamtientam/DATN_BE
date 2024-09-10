from django.urls import path
from . import views

# define the urls
urlpatterns = [
    path('data_menu_dashboard/', views.get_data_menu_dashboard),
    path('analyze_employee_active_by_month/', views.analyze_employee_active_by_month),
    path('analyze_status_project/', views.analyze_status_project),
    path('analyze_number_of_project/', views.analyze_number_of_project),
]
