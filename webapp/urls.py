from django.urls import path 
from webapp import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard/all_bookmarks", views.all_bookmarks, name="all_bookmarks"),
    path("dashboard/unsorted", views.unsorted, name="unsorted"),
    path("dashboard/trash", views.trash, name="trash"),
    path("dashboard/collections/<int:id>", views.collections, name="collections"),
    path("dashboard/tags/<int:id>", views.tags, name="tags"),
    path("dashboard/filter/notes", views.notes, name="notes"),
    path("dashboard/filter/audios", views.audios, name="audios"),
    path("dashboard/filter/videos", views.videos, name="videos"),
    path("dashboard/filter/articles", views.articles, name="articles"),
    path("dashboard/filter/documents", views.documents, name="documents"),
    path("dashboard/bookmark/delete/<int:id>", views.deleteBookmark, name="deleteBookmark"),
]