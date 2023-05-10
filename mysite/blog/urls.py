from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.blog,name ='article-list'),
    path('<int:pk>/',views.blog_detail,name='blog-detail'),
    path('add-article/',views.add_article,name='add-article'),
    path('edit-article/<int:pk>/',views.edit_article,name="edit-article"),
    path('delete-article/<int:pk>/',views.delete_article,name='delete-article')
] 