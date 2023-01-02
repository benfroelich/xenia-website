from django.contrib import admin
from .models import Author, Social

class SocialInline(admin.TabularInline):
    model = Social

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
            SocialInline,
            ]

admin.site.register(Author, AuthorAdmin)
