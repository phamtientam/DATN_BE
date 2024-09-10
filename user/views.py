from django.shortcuts import render
from rest_framework import permissions, status, mixins, viewsets
from rest_framework.response import Response

from .serializers import UserSerializers
from .models import User
from django.contrib.auth.hashers import make_password
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()

    def get_queryset(self):
        query_set = User.objects.all()
        return query_set

    def create(self, request, *args, **kwargs):
        data = request.data
        data['password'] = make_password(data['password'])
        serializer = UserSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
