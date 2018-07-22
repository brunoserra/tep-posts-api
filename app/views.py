import json

from django.db.models import Prefetch, Count
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from app.models import Profile, Post, Comment
from app.serializers import ProfileSerializer, PostSerializer, ProfilePostSerializer, ProfilePostDetailSerializer, \
    CommentPostSerializer, ProfileInsightSerializer

@csrf_exempt
def profile_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Profile.objects.all()
        serializer = ProfileSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    return JsonResponse({"Method Not Allowed": "True"}, status=405)


@csrf_exempt
def profile_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProfileSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

    return JsonResponse({"Method Not Allowed": "True"}, status=405)


@csrf_exempt
def post_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Post.objects.all()
        serializer = PostSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    return JsonResponse({"Method Not Allowed": "True"}, status=405)


@csrf_exempt
def user_posts(request, pk):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Post.objects.filter(profile=pk)
        serializer = PostSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    return JsonResponse({"Method Not Allowed": "True"}, status=405)

@csrf_exempt
def user_posts_detail(request, pk, pk_post):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        print(pk)
        print(pk_post)
        snippets = Post.objects.get(id=pk_post, profile=pk)
        serializer = PostSerializer(snippets, many=False)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        original = Post.objects.get(id=pk_post, profile=pk)
        serializer = PostSerializer(original, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        Post.objects.get(id=pk_post, profile=pk).delete()
        return JsonResponse({"Deleted": "True"}, status=201, safe=False)

    return JsonResponse({"Method Not Allowed": "True"}, status=405)


@csrf_exempt
def profile_posts(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Profile.objects.all().prefetch_related('posts', 'posts__comments')
        serializer = ProfilePostSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        return JsonResponse({"Method Not Allowed": "True"}, status=405)


@csrf_exempt
def profile_posts_detail(request, pk):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Post.objects.all().filter(profile=pk)
        serializer = ProfilePostDetailSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        return JsonResponse({"Method Not Allowed": "True"}, status=405)


@csrf_exempt
def post_comments(request, user, post):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Comment.objects.all().filter(post=post)
        serializer = CommentPostSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data["profile"] = user
        data["post"] = post

        serializer = CommentPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    return JsonResponse({"Method Not Allowed": "True"}, status=405)


@csrf_exempt
def post_comment_details(request, user, post, comment):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Comment.objects.get(post=post, id=comment)
        serializer = CommentPostSerializer(snippets, many=False)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        original = Comment.objects.get(id=comment, post=post)
        serializer = CommentPostSerializer(original, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':

        Comment.objects.get(id=comment, post=post).delete()
        return JsonResponse({"Deleted": "True"}, status=201, safe=False)

    return JsonResponse({"Method Not Allowed": "True"}, status=405)


@csrf_exempt
def profile_insights(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Profile.objects.prefetch_related(Prefetch('posts', queryset=Post.objects
                                                             .all()),
                                                    Prefetch('posts__comments', queryset=Comment.objects.select_related('post').all())
                                                    ).all()

        serializer = ProfileInsightSerializer(snippets, many=True)
        print(Comment.objects.select_related('post').all()[0].comments)

        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({"Method Not Allowed": "True"}, status=405)
