"""postsAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^api-auth/', include('rest_framework.urls')),
    url(r'^profiles/$', views.profile_list),
    url(r'^profiles/insights/$', views.profile_insights),
    url(r'^profiles/(?P<pk>[0-9]+)/$', views.profile_detail),
    url(r'^profiles/(?P<pk>[0-9]+)/posts/$', views.user_posts),
    url(r'^profiles/(?P<pk>[0-9]+)/posts/(?P<pk_post>[0-9]+)/$', views.user_posts_detail),
    url(r'^profiles/(?P<user>[0-9]+)/posts/(?P<post>[0-9]+)/comments/$', views.post_comments),
    url(r'^profiles/(?P<user>[0-9]+)/posts/(?P<post>[0-9]+)/comments/(?P<comment>[0-9]+)/$', views.post_comment_details),
    url(r'^posts/$', views.post_list),
    url(r'^profile-posts/$', views.profile_posts),
    url(r'^profile-posts/(?P<pk>[0-9]+)/$', views.profile_posts_detail),
    # path(r'^', include('snippets.urls')),
]
