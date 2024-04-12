from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import check_password

from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from random import choice

from .models import CustomUser, CustomUserManager, RefreshToken, AccessToken
from .serializers import GroupSerializer, UserSerializer, TokenSerializer


@api_view(['POST'])
def register(request):
    """
    Register user. Require: email and password
    """
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user_manager = CustomUserManager()
        user = user_manager.create_user(email=email, password=password)
        return Response({"id": user.id, "email": email})
    
    if request.method == 'OPTIONS':
        return Response({"name": 'register', "description": "Register user"})
    
@api_view(['POST'])
def login(request):
    """Login
    Params:
        - email
        - password
    Returns:
        - refresh_token
        - access_token
    """
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        exists = CustomUser.objects.filter(email=email)
        if exists:
            user = CustomUser.objects.get(email=email)
            if not user.check_password(password):
                return Response({"message": "email and/or password are incorrect"})
            access_token = AccessToken.create(user_id=user.id)
            token_exists = RefreshToken.objects.filter(user_id=user.id)
            if token_exists:
                refresh_token =  RefreshToken.objects.get(user_id=user.id)
                return Response({"refresh_token": refresh_token.token, "access_token": access_token, "message": "Refresh token already exists"})
            else:
                refresh_token = RefreshToken.create(user)
                refresh_token.save()
                return Response({"refresh_token": refresh_token.token, "access_token": access_token})
            
        return Response({"message": "email and/or password are incorrect"})

@api_view(["POST"])
def logout(request):
    """Logout
    Params:
        - refresh_token
    """
    if request.method == "POST":
        refresh_token = request.data.get("refresh_token")
        token_exists = RefreshToken.objects.filter(token=refresh_token)
        if token_exists:
            token = RefreshToken.objects.get(token=refresh_token)
            token.delete()
            return Response({"success": "User logged out."})
        else:
            return Response({"error": "error"})

@api_view(['POST'])
def refresh(request):
    """Updates access and refresh tokens
    Params:
        - refresh_token
    Returns:
        - refresh_token
        - access_token
    """
    if request.method == "POST":
        refresh_token = request.data.get("refresh_token")
        token_exists = RefreshToken.objects.filter(token=refresh_token)
        if token_exists:
            token = RefreshToken.objects.get(token=refresh_token)
            now = timezone.now().timestamp()
            expired = token.expired.timestamp()
            if now < expired:
                token.update()
                access_token = AccessToken.create()
                return Response({"refresh_token": token.token, "access_token": access_token})

@api_view(['GET', "PUT"])
def me(request):
    """Retrieve or updatepersonal inforamtion
    Params:
        - HTTP header w/ Refresh token
        - new_username [optional]
        - new enail [optional]
    Returns:
        - user information
    """
    headers = request.headers
    auth = headers.get('Authorization')
    if auth is None:
        return Response({"message": "Not authorized"})
    auth_  = auth.split(' ')
    if auth_[0] != 'Bearer':
        return Response({"message": "Not authorized"})
    access_token = auth_[1]
    data = AccessToken.decode(access_token)
    if data is None:
        return Response({"message": "Not authorized"})
    if not data['is_valid']:
        return Response({"message": "Token expired"})
    user_id = data['user_id']
    user = CustomUser.objects.get(id=user_id)
    if request.method == "GET":
        return Response({"id": user.id, "username": user.username, "email": user.email})
    elif request.method == "PUT":
        new_email = request.data.get('email')
        new_username =  request.data.get('username')
        if any([new_email, new_username]):
            if new_username is not None:
                user.username = new_username
            if new_email is not None:
                user.email = new_email
            user.save()
        return Response({"id": user.id, "username": user.username, "email": user.email})
    return Response({"error": "something is wrong"})
    

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class TokenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = RefreshToken.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [permissions.IsAuthenticated]
	
	