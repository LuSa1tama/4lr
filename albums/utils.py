import os
import json
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def ensure_albums_dir():
    albums_dir = os.path.join(settings.MEDIA_ROOT, 'albums_json')
    if not os.path.exists(albums_dir):
        os.makedirs(albums_dir)
    return albums_dir

def save_album_to_json(album_data):
    albums_dir = ensure_albums_dir() 
    filename = f"album_{uuid.uuid4().hex[:8]}.json"
    file_path = os.path.join(albums_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(album_data, f, ensure_ascii=False, indent=4)
    return filename



def validate_json_file(uploaded_file):
    if not uploaded_file.name.lower().endswith('.json'):
        return False, "Файл должен быть в формате JSON"
    
    safe_name = f"uploaded_{uuid.uuid4().hex[:8]}_{uploaded_file.name}"
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'albums_json'))
    filename = fs.save(safe_name, uploaded_file)
    temp_file_path = fs.path(filename)
    
    try:
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        required_fields = ['title', 'artist', 'release_year', 'genre', 'duration']
        if not all(field in json_data for field in required_fields):
            os.remove(temp_file_path)
            return False, "Неверная структура JSON файла"
        
        return True, filename
        
    except json.JSONDecodeError:
        os.remove(temp_file_path)
        return False, "Файл содержит невалидный JSON"
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return False, f"Ошибка при обработке файла: {e}"

def get_all_albums():
    albums_dir = os.path.join(settings.MEDIA_ROOT, 'albums_json')
    
    if not os.path.exists(albums_dir):
        return None, "Папка с альбомами не существует"
    
    json_files = [f for f in os.listdir(albums_dir) if f.endswith('.json')]
    
    if not json_files:
        return None, "Нет сохраненных альбомов"
    
    albums_data = []
    for filename in json_files:
        file_path = os.path.join(albums_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                album_info = json.load(f)
                album_info['filename'] = filename
                albums_data.append(album_info)
        except Exception as e:
            albums_data.append({
                'filename': filename,
                'error': f'Ошибка чтения файла: {e}'
            })
    
    return albums_data, None