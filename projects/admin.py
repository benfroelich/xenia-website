from django.contrib import admin
from .models import Stats, StatCategory

class StatCategoryAdmin(admin.ModelAdmin):
    model = StatCategory
    #list_display = ('title', 'owner', 'first_published_at', 'last_published_at')
    search_fields = ['name', 'units']

admin.site.register(StatCategory, StatCategoryAdmin)
#admin.site.register(Stats, StatCategoryAdmin)
