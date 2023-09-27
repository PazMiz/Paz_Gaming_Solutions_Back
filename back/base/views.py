from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from django.contrib.auth import authenticate
from rest_framework import generics
from django.core import serializers
from django.http import JsonResponse
from .serializers import ProductSerializer
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
# from .models import BlacklistedToken
    
import secrets
from rest_framework import status

from .models import BlacklistedToken  # Import the BlacklistedToken model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User  # If you are using Django's built-in User model
from PIL import Image  # For image processing
from io import BytesIO  # For handling binary data in memory
from django.core.files.base import ContentFile  # For working with files and content
from rest_framework.decorators import api_view  # For defining API views
from rest_framework.response import Response  # For sending API responses


from django.contrib.auth.models import AbstractUser
from rest_framework import viewsets
from .serializers import TopicSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Topic
from .serializers import TopicSerializer

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.http import JsonResponse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework import generics
from .models import FriendList
from .serializers import FriendListSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User  # Import the User model
from django.contrib.auth import authenticate

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.http import JsonResponse

# # # # # # # # # # # # # PCTopics # # # # # # # # # # # # # # # # 


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopicListView(APIView):
    def get(self, request, format=None):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

class TopicDetailView(APIView):
    def get_object(self, pk):
        try:
            return Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        topic = self.get_object(pk)
        if topic:
            serializer = TopicSerializer(topic)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        topic = self.get_object(pk)
        if topic:
            serializer = TopicSerializer(topic, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        topic = self.get_object(pk)
        if topic:
            topic.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

# # # # # # # # # # # # # PCTopics # # # # # # # # # # # # # # # # 

#### Login ######## Login ######## Login ####



from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile  # Import the Profile model
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')  # Get email from request data

    if not username or not password or not email:
        return Response({'error': 'Username, password, and email are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)

    # Handle the uploaded photo
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        # Resize and save the photo to the user's profile
        img = Image.open(photo)
        img.thumbnail((200, 200))  # Resize the image to fit within 200x200 pixels
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        user.customuser.photo.save(photo.name, ContentFile(thumb_io.getvalue()))

    return Response({'message': 'User registered successfully'})

from django.contrib.auth import authenticate, login
from django.http import JsonResponse


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Authentication successful
        login(request, user)
        
        # You can generate and return an access token here if needed
        # access_token = generate_access_token(user)
        
        # Return the username in the response
        return JsonResponse({
            'username': username,
            'access': 'your_access_token_here',
            'refresh': 'your_refresh_token_here'
        })
    else:
        # Authentication failed
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    
#### Login ####

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']
        # Process the uploaded file as needed
        # Save the file to a desired location, e.g., using `uploaded_file.save()`
        return JsonResponse({'message': 'File uploaded successfully.'})
    return JsonResponse({'error': 'Invalid request.'}, status=400)

def get_photo_data(request):
    tasks = Task.objects.all()
    photo_data = [TaskSerializer(task).data for task in tasks]
    return JsonResponse(photo_data, safe=False)



from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        # Process the form and send the password reset email
        response = super().form_valid(form)
        
        # Return a JSON response indicating the success of the email sending process
        return JsonResponse({'message': 'Password reset email has been sent.'})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        form.save()
        return JsonResponse({'message': 'Password has been reset successfully.'})

class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Password reset completed.'})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                raise TokenError('Access token not provided')

            access_token = auth_header.split(' ')[1]
            token = AccessToken(access_token)

            # Perform any additional logic for logout

            return Response({'message': 'Logout successful'}, status=200)
        except TokenError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['staff'] = user.is_staff
        token['email'] = user.email

        # ...

        return token

 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    # Add any other custom fields or methods to your user model

    def __str__(self):
        return self.username
    

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            email = user.email

            return JsonResponse({
                'access': access_token,
                'refresh': str(refresh),
                'email': email,  # Include the email field in the response
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Invalid request'}, status=400)



def generate_access_token(user):
    # Generate a random access token
    token = secrets.token_hex(32)

    # Save the access token to the user or your preferred storage

    return token




class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        new_refresh_token = response.data.get('refresh')
        if new_refresh_token:
            response.set_cookie('refresh_token', new_refresh_token, httponly=True, samesite='Strict')
        return response


######### Friends list #####

class FriendListView(generics.ListCreateAPIView):
    queryset = FriendList.objects.all()
    serializer_class = FriendListSerializer

class FriendDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FriendList.objects.all()
    serializer_class = FriendListSerializer

class AddFriendView(generics.CreateAPIView):
    queryset = FriendList.objects.all()
    serializer_class = FriendListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Assuming the request data includes the user and friend usernames
            user = request.user  # Assuming you have authentication in place
            friend_usernames = serializer.validated_data['friends']

            # Retrieve the user's friend list
            friend_list, created = FriendList.objects.get_or_create(user=user)

            # Add friends to the friend list
            for username in friend_usernames:
                friend = User.objects.get(username=username)
                friend_list.friends.add(friend)

            return Response({'message': 'Friends added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


               ######  Friendlist END ###########



###### XBOX  #######

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import XboxTopic
from .serializers import XboxTopicSerializer

class XboxTopicViewSet(viewsets.ModelViewSet):
    queryset = XboxTopic.objects.all()
    serializer_class = XboxTopicSerializer
    #permission_classes = [IsAuthenticated]

class CreateXboxTopicView(generics.CreateAPIView):
    queryset = XboxTopic.objects.all()
    serializer_class = XboxTopicSerializer

    def perform_create(self, serializer):
        # Get the username from the request data
        username = self.request.data.get('author')

        # Get the user object based on the username
        user = User.objects.get(username=username)

        # Associate the user with the XboxTopic
        serializer.save(author=user)

class XboxTopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = XboxTopic.objects.all()
    serializer_class = XboxTopicSerializer
    
    
class DeleteXboxTopicView(generics.DestroyAPIView):
    queryset = XboxTopic.objects.all()
    serializer_class = XboxTopicSerializer

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#### XBOX ####