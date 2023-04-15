from django.urls import path,include
from . import views

urlpatterns = [


    path('me', views.GetUser.as_view()),
    path('my_users', views.GetMyUsers.as_view()),
    path('add_user', views.AddUser.as_view()),
    path('update', views.UserUpdate.as_view()),
    path('recover_password', views.UserRecoverPassword.as_view()),
    path('activate', views.ActivateUser.as_view()),
    path('send_confirm_code', views.SendConfirmCode.as_view()),
    path('change_password', views.ChangePassword.as_view()),







]
