from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserSerializer, ProductSerializer
from .models import User, Products
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404

# Token encoding
def encode_token(payload):
    token = AccessToken()
    token.payload = payload
    return str(token)

# Token payload handling
def generate_payload(user):
    # Customize the payload data as needed
    payload = {
        'user_id': user.id,
        'email': user.email,
        # Other payload fields
    }
    return payload

class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # print(request.data)
        serializer = UserSerializer(data=request.data)
        print(serializer.initial_data)
        # is_admin = request.data.get('is_admin', False)  # Check if the user is registering as an admin
    
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            
            # user.is_staff = is_admin  # Set the 'is_staff' field to True for admin users
            user.save()

            payload = generate_payload(user)
            token = encode_token(payload)
            return Response({'token': token}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # print(request.data)
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')
        # user = authenticate(request, username=username_or_email, password=password)
        user = authenticate(request, email=username_or_email, password=password)

        # if user is None:
            

        if user:
            login(request, user)
            payload = generate_payload(user)
            token = encode_token(payload)
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class AdminLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user and user.is_staff:
            login(request, user)
            payload = generate_payload(user)
            token = encode_token(payload)
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class ProductCreateUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated]
    # parser_classes = [MultiPartParser]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)