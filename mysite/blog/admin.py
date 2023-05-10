from django.contrib import admin
from .models import Article,ArticleImage,Author,Tag
# Register your models here.

admin.site.register(ArticleImage)
admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Tag)