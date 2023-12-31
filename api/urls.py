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
    path('search/', views.search_bookmarks, name='search_bookmarks'),
    path('download/csv/<str:type>/', views.download_csv, name='all_download_csv'),
    path('download/csv/<str:type>/<str:identifier>/', views.download_csv, name='download_csv'),
]
