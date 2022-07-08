import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# TODO
#class Author(models.Model):
#    name = models.CharField(max_length=200)
#    email = models.EmailField()
#
#    def __str__(self):
#        return self.name

# information that comes with any published content, e.g.
# blog posts, comments, reviews
class PublishMeta(models.Model):
    pub_date = models.DateTimeField('date published', default=timezone.now)
    edit_date = models.DateTimeField('date last modified', auto_now=True)
    author = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    # this class is only used as a add-on to others, never on it's own
    # so it doesn't need a table in the db
    class Meta:
        abstract = True

    def __str__(self):
        return f'published {self.pub_date} by {self.author}. edited {self.edit_date}. {self.likes} likes / {self.dislikes} dislikes'
    
    # recently posted or updated
    @admin.display(boolean=True, ordering='pub_date', description='recent post',)
    def is_recent(self):
        days_back = 3
        threshold = timezone.now() - datetime.timedelta(days=days_back)
        is_future = self.pub_date > timezone.now()
        # edit date is concurrent or newer than publication date
        # so it is adequate to check only edit date
        return not is_future and self.edit_date >= threshold 


class Post(PublishMeta):
    title = models.CharField(max_length=1000)
    text = models.TextField(max_length=10000)
    def __str__(self):
        return f'"{self.pk} - {self.title}"'
    @property
    def short_description(self):
        return self.text[:30]

# a group of comments will be listed in a thread
class Thread(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return f'Comment Thread on {self.post.__str__()}'

    # ordered by creation date, newest thread first
    class Meta:
        ordering = ['-pk']

class Comment(PublishMeta):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, default=0)
    comment_text = models.TextField(max_length=10000)
    def __str__(self):
        return f'"{self.short_description}" - on thread {self.thread.__str__()}'
    @property
    def short_description(self):
        return self.comment_text[:30]

    # within a thread, comments are ordered oldest to newest
    # so that it reads like a normal conversation
    class Meta:
        ordering = ['pub_date']

