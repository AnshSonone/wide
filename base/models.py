from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomerManager

# Create your models here.

class CustomUserModel(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='video',null=True, default='https://res.cloudinary.com/da25rozpm/image/upload/v1745331876/images_cpca3c.png')
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomerManager()

    def __str__(self):
        return self.username

    
    
class VideoModel(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='profile')
    videoDescription = models.TextField(max_length=10000)
    videoUrl = models.ImageField(null=True, blank=True)
    tag = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.videoDescription
    

class AnswerModel(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='paticipants')
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE)
    comment = models.TextField()
    commentDate = models.DateTimeField(auto_now_add=True)
    commentUpdatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    

