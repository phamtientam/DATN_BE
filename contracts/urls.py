from django.urls import path
from . import views

# define the urls
urlpatterns = [
    path('contract_by_status/', views.analyze_contract_by_status),
    path('contract_by_contract_name/', views.analyze_contract_by_contract_name),
]
