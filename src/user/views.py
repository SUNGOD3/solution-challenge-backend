
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .models import User
from .serializers import UserSerializer

from .mailHandler import MailHandler


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='User Email'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password')
    }),
    responses={200: '{User Token}', 405: 'METHOD NOT ALLOWED', 400: 'Bad Request'})
@api_view(['POST'])
def user_login(request):
    try:
        user = User.objects.get(email=request.data['email'])
        if user.password == request.data['password']:
            return Response({"token": user.token}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except User.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    def get_object(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return False

    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request, format=format):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User Email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='User name')
        }), responses={201: 'CREATED', 405: 'METHOD NOT ALLOWED', 400: 'BAD REQUEST'})
    def post(self, request, format=format):
        serializer = UserSerializer(data=request.data)
        if self.get_object(request.data['email']):
            return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            if serializer.is_valid():
                serializer.save()
                mail = MailHandler(request.data['name'], request.data['email'], User.objects.get(email=request.data['email']).verify_code)
                mail.verify()
                return Response(status.HTTP_201_CREATED)
            return Response(status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get_object(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return Http404

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            name='Token',
            in_=openapi.IN_QUERY,
            description='User Token',
            type=openapi.TYPE_STRING
        )
    ], responses={200: UserSerializer, 405: 'METHOD NOT ALLOWED'})
    def get(self, request, email, format=format):
        print(email)
        user = self.get_object(email)
        if request.GET.get('Token') == user.token:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(request_body=UserSerializer, responses={200: 'OK', 400: 'BAD REQUEST'})
    def put(self, request, email, format=format):
        user = self.get_object(email)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: 'OK'})
    def delete(self, request, email, format=format):
        user = self.get_object(email)
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)
