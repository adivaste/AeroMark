from django.urls import path 
from api import views

urlpatterns = [
    path("", views.index, name="home"),
    path("bookmarks/", views.bookmarks_list, name="bookmarks-list"),
    path("bookmarks/<int:pk>", views.bookmarks_detail, name="bookmarks-detail"),
    path("collections/", views.collections_list, name="collections-list"),
    path("collections/<int:pk>", views.collections_detail, name="collections-detail"),
    path("tags/", views.tags_list, name="tags_list"),
    path("tags/<int:pk>", views.tags_detail, name="tags-detail"),
]
