from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from .views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'}), name=''),
    path('add/', UserViewSet.as_view({'post': 'create'}), name='add'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
