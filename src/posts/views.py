from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from posts.service import PostService


@login_required(login_url='/users/login/')
def feed(request):
    if request.method == "GET":
        print("name = " + request.user.username)
        return render(
            request,
            'feed.html',
            {
                "posts": PostService.get_posts_for_user(request.user.username),
                "username": request.user.username
            }
        )
    title = request.POST.get('title')
    content = request.POST.get('content')
    if title and content:
        PostService.create_post(
            author=request.user.username,
            title=title,
            content=content
        )
    return render(
        request,
        'feed.html',
        {
            "posts": PostService.get_posts_for_user(request.user.username),
            "username": request.user.username
        }
    )


@login_required(login_url='/users/login/')
def get_post(request, title, author):
    """
    get single post route

    :param request:
    :param title:
    :param author:
    :return:
    """
    post = PostService.get_post(title=title, author=author)
    return JsonResponse({'post': post})


@login_required(login_url='/users/login/')
def leave_comment(request, title, author):
    """
    leave comment to post by title and author

    :param request:
    :param title:
    :param author:
    :return:
    """
    result = {'added': False}
    if request.method == "POST":
        comment = request.POST.get('comment')
        if len(comment) > 0:
            PostService.add_comment(
                post_author=author,
                post_title=title,
                comment_author=request.user.username,
                comment=comment
            )
            result['added'] = True
            result['author'] = request.user.username
    return JsonResponse(result)
