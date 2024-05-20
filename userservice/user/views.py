from django.shortcuts import render

from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': ('Tài khoản hoặc mật khẩu không chính xác!')
    }
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    _user = user.username
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['username'],
            email = data['email'],
            password = make_password(data['password']),
            is_staff = data['is_staff']
        )
        serializer = UserSerializerWithToken(user, many=False)

        return Response(serializer.data)
    except:
        message = {'detail': 'Tên đăng nhập đã được sử dụng!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    try:
        user = request.user
        data = request.data
        User.objects.filter(id=user.id).update(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])
        )
        return Response({'success': True})
    except NameError:
        print(NameError)
        message = {'detail': 'Error'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
