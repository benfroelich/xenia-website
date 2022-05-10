#register blog models with admin so they can be edited from there
from django.contrib import admin

from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)
