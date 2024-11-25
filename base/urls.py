from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/register/', views.RegisterApiView.as_view(), name='RegisterApiView'),
    path('users/login/', views.LoginApiView.as_view(), name="LoginApiView"),
    path('users/logout/', views.LogoutApiView.as_view(), name='logout'),
    path('users/profile/', views.ProfileApiView.as_view(), name='ProfileApiView'),
    path('profile/', views.RetriveVideoByProfileView.as_view(), name='RetriveVideoByProfileView'),
    path('refresh/', TokenRefreshView.as_view(), name='token_obtain_pair'), 
    path('videos/', views.VideoApiView.as_view(), name='VideoApiView'),
    path('videos/<int:id>/', views.VideoApiView.as_view(), name='VideoApiView'),
    path('video/', views.RetriveVideoApiView.as_view(), name='RetriveVideoApiView'),
    path('search/', views.SearchApiView.as_view(), name='SearchApiView'),
    path('answer/', views.AnswerApiView.as_view(), name='AnswerApiView'),
    path('answer/<int:id>/', views.AnswerApiView.as_view(), name='AnswerApiView'),
]