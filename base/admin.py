from django.contrib import admin
from .models import CustomUserModel, VideoModel, AnswerModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
admin.site.register(CustomUserModel)
admin.site.register(VideoModel)
admin.site.register(AnswerModel)