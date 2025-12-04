from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_album, name='create_album'),
    path('upload/', views.upload_album, name='upload_album'),
    path('view/', views.view_albums, name='view_albums'),
    path('search/', views.search_albums, name='search_albums'),
    path('edit/<int:album_id>/', views.edit_album, name='edit_album'),
    path('delete/<int:album_id>/', views.delete_album, name='delete_album'),
]