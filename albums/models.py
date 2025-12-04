from django.db import models
from django.core.exceptions import ValidationError

class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название альбома")
    artist = models.CharField(max_length=100, verbose_name="Исполнитель")
    release_year = models.IntegerField(verbose_name="Год выпуска")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    duration = models.CharField(max_length=50, verbose_name="Продолжительность")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        unique_together = ['title', 'artist', 'release_year']
        ordering = ['-created_at']
    
    def clean(self):
        if self.release_year < 1900 or self.release_year > 2030:
            raise ValidationError("Введите корректный год выпуска (1900-2030).")
    
    def __str__(self):
        return f"{self.title} - {self.artist} ({self.release_year})"