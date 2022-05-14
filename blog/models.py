import datetime

from django.db import models
from django.utils import timezone


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
    def is_recent(self):
        days_back = 3
        threshold = timezone.now() - datetime.timedelta(days=days_back)
        return self.pub_date >= threshold or self.edit_date >= threshold

class Post(PublishMeta):
    title = models.CharField(max_length=1000)
    text = models.TextField(max_length=10000)
    def __str__(self):
        return f'"{self.text}" - {super().__str__()}'

class Comment(PublishMeta):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    regarding = models.ForeignKey(Comment, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=10000)
    def __str__(self):
        return f'"{self.comment_text}" - {super().__str__()} on post {self.post}'

