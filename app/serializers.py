from rest_framework import serializers
from app.models import Profile, Comment, Post


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'profile',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'name',)


class PostProfileSerializer(serializers.ModelSerializer):

    comments = serializers.IntegerField(
        source='comments.count',
        read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'comments')


class ProfilePostSerializer(serializers.ModelSerializer):
    posts = PostProfileSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('id', 'name', 'posts')
        depth = 1


class ProfilePostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.IntegerField(
        source='comments.count',
        read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'comments')


class CommentPostSerializer(serializers.ModelSerializer):
    # post = PostProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'name', 'email', 'body', 'post')
        # depth = 1


class ProfileInsightSerializer(serializers.ModelSerializer):
    total_comments = serializers.IntegerField(
        source='posts__comments.count',
        read_only=True
    )

    total_posts = serializers.IntegerField(
        source='posts.count',
        read_only=True
    )

    class Meta:
        model = Profile
        fields = ('id', 'name', 'total_comments', 'total_posts',)
        depth = 2