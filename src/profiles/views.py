from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User

from posts.service import PostService
from profiles.service import ProfileService


@login_required
def view_profile(request, username):
    """

    :param request:
    :param username:
    :return:
    """
    user = ProfileService.get_profile(username)
    current = request.user.username == username
    is_following = request.user.username in user['followers']
    if request.method == "POST":
        if not current:
            if is_following:
                ProfileService.unfollow_user(
                    follower_name=request.user.username,
                    user_name=username
                )
            else:
                ProfileService.follow_user(
                    follower_name=request.user.username,
                    user_name=username
                )

    user = ProfileService.get_profile(username)
    is_following = request.user.username in user['followers']
    distance = ProfileService.get_distance(
        user_from=request.user.username,
        user_to=username
    )
    return render(
        request,
        'profile.html',
        {
            "user": user,
            "posts": PostService.get_posts_by_author(username),
            "current": current,
            "is_following": is_following,
            "distance": distance,
            "current_user": request.user.username,
        }
    )


@login_required
def view_users(request):
    """

    :param request:
    :return:
    """
    users = ProfileService.get_all_profiles()
    return render(
        request,
        'users.html',
        {
            "users": users,
            "current": request.user.username
        }
    )


def register(request):
    """if POST method, checks whether username or email are already in use by
    other accounts
        if GET method, renders register page.
    Returns:
        returns login page, if new user was created,
        reloads register page otherwise.
    """
    if request.method == "GET":
        return render(request, 'register.html')
    if request.POST.get('check_username'):
        username = str(request.POST['check_username'])
        return JsonResponse({
            'name_available': not User.objects.filter(username=username)})
    if request.POST.get('check_mail'):
        email = str(request.POST['check_mail'])
        return JsonResponse({'mail_available': not User.objects.filter(email=email)})
    name = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    user = ProfileService.create_user(username=name, password=password, email=email)
    if user:
        return redirect('login')
    return render(request, 'register.html', status=400)


def login_user(request):
    """if GET method, renders login page.
    Returns:
        returns homepage, if user was authorized,
        reloads login page with proper message otherwise.
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    name = request.POST['username']
    password = request.POST['password']
    if User.objects.filter(username=name):
        print(name)
        print(password)
        user = authenticate(username=name, password=password)
        if user:
            login(request, user)
            return redirect('feed')
        return render(request,
                      'login.html',
                      {
                          'error': 'Wrong password',
                          'username': name
                      },
                      status=400)
    return render(request, 'login.html', {'error': 'No such user'}, status=400)


@login_required
def logout_user(request):
    """logs user out
    Returns:
        returns login page
    """
    logout(request)
    return redirect('login')