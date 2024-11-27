from django.urls import path
from . import views

#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),

    #path('accounts/login/', auth_views.LoginView.as_view(), name='login'),

]
