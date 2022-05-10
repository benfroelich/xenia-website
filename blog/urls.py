from django.urls import path

from . import views

urlpatterns = [
    # ex: blog/
    path('', views.index, name='index'),
    # ex: blog/123/
    path('<int:post_id>/', views.post, name='post'),
    # ex: blog/123/comment/
    path('<int:post_id>/comment/', views.comment, name='comment'),
]
