"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path, include
from django.contrib.sitemaps import views as sitemap_views

from blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView, SearchView, AuthorView
)
from config.views import LinkListView
from comment.views import CommentView

from blog.rss import LastestPostFeed
from blog.sitemap import PostSitemap
from django.views.decorators.cache import cache_page

from typeidea.settings import develop
from .custom_site import custom_site

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category-list'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag-list'),
    path('post/<int:post_id>.html/', PostDetailView.as_view(), name='post-detail'),
    path('links/', LinkListView.as_view(), name='links'),
    path('search/', SearchView.as_view(), name='search'),
    path('author/<int:owner_id>/', AuthorView.as_view(), name='author'),
    path('comment/', CommentView.as_view(), name='comment'),


    path('super_admin/', admin.site.urls, name='super-admin'),
    path('admin/', custom_site.urls, name='admin'),

    re_path(r'^rss|feed/', LastestPostFeed(), name='rss'),
    re_path(r'^sitemap\.xml', cache_page(60 * 20, key_prefix='sitemap_cache_')
    (sitemap_views.sitemap), {'sitemaps':{'posts':PostSitemap}}),
]

if develop.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
