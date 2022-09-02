from django.contrib import admin

from .models import BlogPost, Comment, Thread

def comment_fieldsets(titles = False):
    if titles:
        content = 'Content'
        meta = 'Meta'
    else:
        content = None
        meta = None
    return (
            (content, {
                'fields': ('comment_text',)
            }),
            (meta, {
                'fields': (('owner', 'first_published_at'), ('likes', 'dislikes'))
            }),
        )

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('short_description', 'owner', 'first_published_at', 'last_published_at')
    list_filter = ['first_published_at', 'owner']
    search_fields = ['comment_text', 'owner']
    fieldsets = comment_fieldsets(True)
    
class CommentInline(admin.StackedInline):
    model = Comment
    show_change_link = True
    extra = 0
    fieldsets = comment_fieldsets()

class ThreadInline(admin.StackedInline):
    model = Thread
    show_change_link = True
    extra = 0

class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    inlines = [CommentInline]

class BlogPostAdmin(admin.ModelAdmin):
    inlines = [ThreadInline]
    list_display = ('title', 'owner', 'first_published_at', 'last_published_at')
    list_filter = ['first_published_at', 'owner']
    search_fields = ['text', 'title', 'owner']

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)
