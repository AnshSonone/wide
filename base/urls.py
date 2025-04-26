from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("endpoints/", views.EndPoint, name='endpoints'),
    path('users/register/', views.RegisterApiView.as_view(), name='RegisterApiView'),
    path('users/activate/<str:uid>/<str:token>/', views.Activation_ConfrimView.as_view(), name='activate'),
    path('users/login/', views.LoginApiView.as_view(), name="LoginApiView"),
    path('users/logout/', views.LogoutApiView.as_view(), name='logout'),
    path('users/forgot/', views.ForgotView.as_view(), name='forgot_view'),
    path('users/reset/<str:uid>/<str:token>/', views.Forgot_passwordView.as_view(), name='forgot'),
    path('users/profile/', views.ProfileApiView.as_view(), name='ProfileApiView'),
    path('users/profile/<int:id>/', views.RetriveProfileById    .as_view(), name='ProfileApiView'),
    path('question/<int:id>/', views.RetriveVideoByProfileView.as_view(), name='RetriveVideoByProfileView'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_obtain_pair'), 
    path('videos/', views.VideoApiView.as_view(), name='VideoApiView'),
    path('videos/<int:id>/', views.VideoApiView.as_view(), name='VideoApiView'),
    path('video/', views.RetriveVideoApiView.as_view(), name='RetriveVideoApiView'),
    path('search/', views.SearchApiView.as_view(), name='SearchApiView'),
    path('answer/', views.AnswerApiView.as_view(), name='AnswerApiView'),
    path('answer/<int:id>/', views.AnswerApiView.as_view(), name='AnswerApiView'),
]