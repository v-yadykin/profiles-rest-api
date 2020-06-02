from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

class HelloAPIView(APIView):
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        an_apiview = [
            'Methods get, post, patch, put, delete',
            'It is derived from Django ClassView'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        name = serializer.validated_data.get('name')
        message = f'Hello {name}'

        return Response({'message': message})

    def put(self, request, pk=None):
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    serializers_class = serializers.HelloSerializer

    def list(self, request):
        a_viewset = [
            'Uses actions: list, create, retrieve, update, partial_update',
            'Automaticly maps to URLs using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message': 'Hello!', 'an_viewset': a_viewset})

    def create(self, request):
        serializer = self.serializers_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        name = serializer.validated_data.get('name')
        message = f'Hello {name}'

        return Response({'message': message})

    def retrieve(self, request, pk=None):
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        return Response({'http_method': 'PATCH'})

    def delete(self, request, pk=None):
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
    # Включаем отображение в браузере (по умолчанию выключено) 
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)