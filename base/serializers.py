from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .models import VideoModel, AnswerModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    default_validators = UniqueValidator(queryset=User.objects.all())
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'bio', 'password']

    def create(self, validated_data):
        user =  User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        user.bio = validated_data.get('bio', '')
        user.avatar = validated_data.get('avatar', None)
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.password = validated_data.get('username', instance.password)
        instance.save()

        return instance

class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password']
        

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'bio', 'password', 'is_active', 'date_joined']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = '__all__'

    def create(self, validated_data):
        return AnswerModel.objects.create(**validated_data)


class getAnswerSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()
    class Meta:
        model = AnswerModel
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields = ['id', 'user', 'videoDescription', 'videoUrl', 'tag', 'created']

    # def get_user(self, obj):
    #     return self.user

    def create(self, validated_data):
        return VideoModel.objects.create(**validated_data)


class GetVideoSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()
    class Meta:
        model = VideoModel
        fields = '__all__'
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token