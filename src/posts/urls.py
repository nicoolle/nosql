from django.urls import path, include

from .views import feed, get_post, leave_comment

urlpatterns = [
    path('', feed, name='feed'),
    path('leave_comment/<str:title>/<str:author>', leave_comment, name='leave_comment'),
    path('<str:title>/<str:author>', get_post, name='get_post')
]