from django.urls import path

from .views import *

urlpatterns = [
    path('register', register),
    path('check_mail', check_mail),
    path('login', login),
    path('logout', logout),
    path('get_user', get_user),
    path('update_user', update_user),
    path('save_element', save_element),
    path('delete_element', delete_element),
    path('create_document', create_document),
    path('open_document', open_document),
    path('delete_document', delete_document),
    path('delete_document', delete_document),
    path('create_folder', create_folder),
    path('delete_folder', delete_folder),
    path('try_prototype', try_prototype),
    path('get_prototype', get_prototype),
    path('update_document', update_document),
    path('update_prototype', update_prototype),
    path('check_document', check_document),
    path('delete_prototype', delete_prototype),
    path('update_title', update_title)
]
