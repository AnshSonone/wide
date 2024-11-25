from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from . import  serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny 
from .models import VideoModel, AnswerModel
from .renderers import UserRenderers
from django.db.models import Q
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# Create your views here.

User = get_user_model()

class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer

ObtainTokenPairWithColorView = ObtainTokenPairWithColorView.as_view()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterApiView( APIView ):

    renderer_classes = [UserRenderers]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'User register successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginApiView(
    APIView
):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid()
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            token = get_tokens_for_user(user)
            return Response({
                'token': token,
                'message': 'Login Successfully'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'non_filed_errors' : 'Email or Passwrod are invalid'}}, )


class LogoutApiView( APIView ):

    def post(self, request):
        logout(request)
        return Response({'message': 'User logout successfully'}, status=status.HTTP_200_OK)


class ProfileApiView( APIView ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = serializers.UserRegisterSerializer(user, many=False)
        # user_id = serializer.data['id']
        # print("before encode", user_id)
        # Convert the user ID to bytes before Base64 encoding
        # user_id_bytes = force_bytes(user_id)
        # Encode the user ID in URL-safe Base64 format
        # user_id_base64_encode = urlsafe_base64_encode(user_id_bytes)
        # print("after encode", user_id_base64_encode)
        # data = serializer.data
        # if 'id' in data:
            #  data['id'] = user_id_base64_encode
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetriveVideoByProfileView( APIView ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videoUser = request.user
        # Decode the Base64-encoded ID back to the original ID
        decode_user_id_bytes = urlsafe_base64_decode(videoUser['id'])
        # Convert the decoded bytes back to the original integer (assuming the ID was an integer)
        decode_user_id = int(force_str(decode_user_id_bytes))
        print(decode_user_id)
        user_id = User.objects.get(id=decode_user_id)
        video = VideoModel.objects.filter(user=user_id)
        serializer  = serializers.GetVideoSerializer(video, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoApiView( APIView ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            videos = VideoModel.objects.all().order_by('-created')
            serializer = serializers.GetVideoSerializer(videos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
        video = AnswerModel.objects.filter(id=id)
        if video is not None:
            video.delete()
            return Response({'message': 'Video delete successfully'}, status=status.HTTP_200_OK)

