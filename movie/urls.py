from django.urls import path, include

from . import views
from .views import delete_post, my_post, movie_post

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.show_category_posts),
    path('tag/<str:slug>/', views.show_tag_posts),
    path('create_post/', views.PostCreate.as_view()),
    path('<int:pk>/update_post/', views.PostUpdate.as_view()),
    path('<int:pk>/addcomment/', views.addComment),
    path('<int:pk>/delete/', delete_post),
    path('my_post/', my_post),
    path('movie_post/', movie_post),
    path('search/', views.SearchFormView.as_view()),
]
