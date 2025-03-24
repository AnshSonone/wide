from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny 
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from . import  serializers
from .models import VideoModel, AnswerModel
# from .renderers import UserRenderers
from .utils import encode_url, decode_url, get_token
from .emails import send_activation_email, send_forgot_password_email, send_notify_email
from .pagination import PageResultPagination

# Create your views here.

User = get_user_model()

# =====================
#   JWT TOKEN VIEWS
#=======================

class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer

ObtainTokenPairWithColorView = ObtainTokenPairWithColorView.as_view()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# =====================
#   AUTHENTICATION VIEWS
#=======================

class RegisterApiView( APIView ):

    # renderer_classes = [UserRenderers]
    permission_classes = [AllowAny]

    def post(self, request): 
        try:
            serializer = serializers.UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.create(serializer.validated_data)
                activation_url = encode_url(user, route='activate')
                send_activation_email(user.email, activation_url)
                return Response({'message': 'User register successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            get_object_or_404(User, id=user.id).delete()
            return Response(e, status=status.htt400)
    
class LoginApiView(
    APIView
):
    
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        exist = get_object_or_404(User, email=email)
        if not exist.is_active:
            return Response({"message": "Account is not activated"}, status=status.HTTP_401_UNAUTHORIZED)
        user = authenticate(request, email=email, password=password)    
        if user is not None:
            login(request, user) 
            token = get_tokens_for_user(user)
            # send_notify_email(email)
            return Response({
                     'token': token,
                     'message': 'Login Successfully'
                     }, status=status.HTTP_200_OK)
        return Response({"message" : "Email or Passwrod are invalid"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutApiView( APIView ):

    def post(self, request):
        logout(request)
        return Response({'message': 'User logout successfully'}, status=status.HTTP_200_OK)

class ActivationView( APIView ):
    permission_classes = [ AllowAny ]

class Activation_ConfrimView( APIView ):
    
    permission_classes = [ AllowAny ]
    
    def patch(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')

        if not uid and not token:
            return Response({'messgae': 'Uid or token is invalid'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = decode_url(uid)
        user = get_object_or_404(User, id=user_id)
        
        if get_token(user, token):
            if user.is_active == True:
                return Response({'message': 'User Account already activated'}, status=status.HTTP_200_OK)

            user.is_active = True
            user.save()
            return Response({'message': 'User account activated successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'User or token is not exist'}, status=status.HTTP_400_BAD_REQUEST)

class ForgotView( APIView ):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'message': 'Email is requied'}, status=status.HTTP_400_BAD_REQUEST) 

        user = get_object_or_404(User, email=email)

        if user is None:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        forgot_url = encode_url(user, 'forgot')
        send_forgot_password_email(email, forgot_url)
        return Response({'message': 'forgot password email send succesfully'}, status=status.HTTP_200_OK)

class Forgot_passwordView( APIView ):
    
    permission_classes = [AllowAny]
    
    def patch(self, request):
        uid = request.data.get('uid')
        token  = request.data.get('token')
        password = request.data.get('password')

        if not uid and not token:
            return Response({'message': 'Uid or token is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = decode_url(uid)
        user =  get_object_or_404(User, id=user_id)

        if user is None:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        
        
        if get_token(user, token):
            user.set_password(password)
            user.save()
            return Response({'message': 'User password update successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)

# =====================
#   FUNCTIONANLLITY VIEWS
#=======================

class ProfileApiView( APIView ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):    
        user = request.user
        serializer = serializers.UserRegisterSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RetriveProfileById(APIView):
    
    def get(self, request, id):
        user = User.objects.get(id=id)
        print(user.id)
        if user is None:
            return Response({'message': user.id}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.UserProfileSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)     

class RetriveVideoByProfileView( APIView ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        video = VideoModel.objects.filter(user=id)
        serializer  = serializers.GetVideoSerializer(video, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VideoApiView( APIView, PageResultPagination ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            videos = VideoModel.objects.all().order_by('-created')
            paginated_queryset = self.paginate_queryset(videos, request)
            next_page = self.get_next_link()
            return self.get_paginated_response({
                'result': serializers.GetVideoSerializer(paginated_queryset, many=True).data,
                'is_last_page': next_page,
            })
        except Exception as e:
            return Response(e)

    def post(self, request):
        user_id = request.data.get('user')
        videoDescription = request.data.get('videoDescription')
        videoUrl = request.data.get('videoUrl')  
        tag = request.data.get('tag')

        try:
            # Retrieve the user instance
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    
        video = VideoModel.objects.create(
            user = user,
            videoDescription = videoDescription,
            videoUrl = videoUrl,
            tag = tag,
        )

        if video is not None:
            video.save()
            return Response({'message' : 'Video uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Video failed to upload'}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def put(self, request):
        id = request.data['id']
        videoDescription = request.data['videoDescription']
        videoUrl = request.data['videoUrl']
        tag = request.data['tag']

        video = VideoModel.objects.filter(id=id)
        video.update(
            isinstance=True,
            videoDescription= videoDescription,
            videoUrl=videoUrl,
            tag=tag
        )
        return Response({'message': 'Video upoalded successfully'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, id):
        video = VideoModel.objects.filter(id=id)
        if video is not None:
            video.delete()
            return Response({'message': 'Video delete successfully'}, status=status.HTTP_200_OK)

class RetriveVideoApiView( APIView ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user_id = request.query_params.get('video')
        video = VideoModel.objects.filter(id=user_id) 
        serializer = serializers.GetVideoSerializer(video, many=True)
        if serializer.data != []:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "you haven't post any question yet"}, status=status.HTTP_200_OK)
    
class SearchApiView( APIView ):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        video = VideoModel.objects.all()
        q = request.query_params.get('q')
        if q != None and q != '':
            video = video.filter(
                Q(tag__icontains=q) |
                Q(videoDescription__icontains=q)
            )
        serializer = serializers.GetVideoSerializer(video, many=True)
        if serializer is not None:
            return  Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"No search Result found {q}"})

class AnswerApiView( APIView ):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            video =  request.query_params.get('q')
            answer = AnswerModel.objects.filter(video=video)
            
            serializer = serializers.getAnswerSerializer(answer, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e)


    def post(self, request):
        serializer = serializers.AnswerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            answer = serializer.save()
        if answer is not  None:
            return Response({"message": "Answer uploaded successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def put(self, request, id):
        video = AnswerModel.objects.filter(id=id)
        if video is not None:
            serializer = serializers.getAnswerSerializer(data=request.data)
            serializer.update(isinstance=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, id):
        video = AnswerModel.objects.get(id=id)
        if video is not None:
            video.delete()
            return Response({'message': 'Video delete successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Answer does not exist'}, status=status.HTTP_400_BAD_REQUEST)

