from django.urls import path 
from webapp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard/all_bookmarks", views.all_bookmarks, name="all_bookmarks"),
    path("dashboard/unsorted", views.unsorted, name="unsorted"),
    path("dashboard/trash", views.trash, name="trash"),
    path("dashboard/collections/<str:name>", views.collections, name="collections"),
    path("dashboard/tags/<str:name>", views.tags, name="tags"),
    path("dashboard/filter/notes", views.notes, name="notes"),
    path("dashboard/filter/audios", views.audios, name="audios"),
    path("dashboard/filter/videos", views.videos, name="videos"),
    path("dashboard/filter/articles", views.articles, name="articles"),
    path("dashboard/filter/documents", views.documents, name="documents"),
    path("dashboard/bookmark/delete/<int:id>", views.deleteBookmark, name="deleteBookmark"),
    path("dashboard/bookmark/restore/<int:id>", views.restoreBookmark, name="restoreBookmark"),
    path("dashboard/search/", views.search, name="search"), 
    path("accounts/login/", views.user_login, name="login"),   
    path("accounts/signup/", views.user_register, name="register"),   
    path("accounts/logout/", views.user_logout, name="logout"), 
    path('download-csv/<str:type>/', views.download_csv, name='all_download_csv'),
    path('download-csv/<str:type>/<str:identifier>/', views.download_csv, name='category_download_csv'),
    path("download-file/", views.download_file_from_url, name="download_file")
]