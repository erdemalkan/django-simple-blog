from django.urls import path, re_path
from .views import *

app_name = 'post'

urlpatterns = [
    path('all/', post_index, name='index'),
    path('create/', post_create, name='create'),
    re_path(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    re_path(r'^(?P<id>\d+)/edit/$', post_edit, name='edit'),
    re_path(r'^(?P<id>\d+)/delete/$', post_delete, name='delete'),
]