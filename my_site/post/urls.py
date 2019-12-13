from django.urls import path
from . import views


app_name = 'post'

urlpatterns = [
    path('', views.post_list, name='home'),
    path('post-list/', views.post_list, name='post_list'),
    path('post-update/<int:id>/', views.post_update, name='post_update'),
    path('post-create/', views.post_create, name='post_create'),
    path('post-detail/<int:id>/', views.post_detail, name='post_detail'),
    
]