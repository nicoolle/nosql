from django.urls import path, include

from .views import view_profile, view_users, login_user, register, logout_user

urlpatterns = [
    path('', view_users, name='view_users'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout_user'),
    path('<str:username>/', view_profile, name='view_profile'),
    ]