from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse 
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from PIL import Image
import os

User = get_user_model()

def article_image_path(instance, filename):
    # Генерируем путь для сохранения изображения
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.title)}_{instance.id}.{ext}"
    return os.path.join('articles', filename)

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок', db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    content = RichTextUploadingField(verbose_name='Содержание')
    excerpt = models.TextField(max_length=300, blank=True,verbose_name='Краткое описание')
    featured_image = models.ImageField(upload_to=article_image_path, blank=True, null=True)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, db_index=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Сохраняем модель, чтобы получить ID
        super().save(*args, **kwargs)
        
        # Обрабатываем изображение после сохранения
        if self.featured_image:
            try:
                img = Image.open(self.featured_image.path)
                
                # Определяем максимальные размеры
                max_width = 1200
                max_height = 630
                
                # Получаем текущие размеры
                width, height = img.size
                
                # Вычисляем новые размеры, сохраняя пропорции
                if width > max_width or height > max_height:
                    ratio = min(max_width/width, max_height/height)
                    new_size = (int(width * ratio), int(height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                    
                    # Determine format and save with optimized quality
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    
                    img.save(self.featured_image.path, quality=75, optimize=True)
            except Exception as e:
                print(f"Error processing image: {e}")

    def get_likes_count(self):
        return self.likes.count()

    def get_comments_count(self):
        return self.comments.count()    