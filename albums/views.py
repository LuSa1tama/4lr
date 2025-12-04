from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .forms import AlbumForm
from .models import Album
from .utils import save_album_to_json, validate_json_file, get_all_albums

import json

def home(request):
    return render(request, 'albums/home.html')

def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            storage_choice = request.POST.get('storage_choice', 'db')
            
            if storage_choice == 'db':
                # Проверяем дубликат ДО сохранения
                title = form.cleaned_data['title']
                artist = form.cleaned_data['artist']
                release_year = form.cleaned_data['release_year']
                
                # Проверяем существование дубликата
                if Album.objects.filter(title=title, artist=artist, release_year=release_year).exists():
                    messages.warning(request, 'Такой альбом уже существует в базе данных!')
                    return render(request, 'albums/create_album.html', {'form': form})
                else:
                    # Сохраняем если нет дубликата
                    album = form.save()
                    messages.success(request, f'Альбом "{album.title}" сохранен в БД!')
                    form = AlbumForm()
            else:
                # Сохранение в файл
                filename = save_album_to_json(form.cleaned_data)
                messages.success(request, f'Альбом сохранен в файл: {filename}')
                form = AlbumForm()
    else:
        form = AlbumForm()
    
    return render(request, 'albums/create_album.html', {'form': form})

def view_albums(request):
    source = request.GET.get('source', 'db')  # По умолчанию из БД
    
    if source == 'file':
        # Данные из файлов
        albums_data, message = get_all_albums()
        context = {'albums': albums_data, 'message': message, 'source': 'file'}
    else:
        # Данные из БД
        albums_data = Album.objects.all()
        context = {'albums': albums_data, 'source': 'db'}
    
    return render(request, 'albums/view_albums.html', context)

# Остальные функции пока оставим как есть
def upload_album(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        uploaded_file = request.FILES['json_file']
        success, result = validate_json_file(uploaded_file)
        
        if success:
            messages.success(request, f'Файл загружен: {result}')
            return redirect('home')
        else:
            messages.error(request, result)
    
    return render(request, 'albums/upload_album.html')

# AJAX поиск по БД
def search_albums(request):
    query = request.GET.get('q', '')
    if query:
        albums = Album.objects.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(genre__icontains=query)
        )[:10]
        results = [
            {
                'id': album.id,
                'title': album.title,
                'artist': album.artist,
                'year': album.release_year,
                'genre': album.genre
            } for album in albums
        ]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

def edit_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, f' Альбом "{album.title}" успешно обновлен!')
            return redirect('view_albums')
    else:
        form = AlbumForm(instance=album)
    
    return render(request, 'albums/edit_album.html', {'form': form, 'album': album})

def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    
    if request.method == 'POST':
        album_title = album.title
        album.delete()
        messages.success(request, f' Альбом "{album_title}" успешно удален!')
        return redirect('view_albums')
    
    return render(request, 'albums/delete_album.html', {'album': album})