from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime

# wagtail-related
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

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
    # Database Fields
    pub_date = models.DateTimeField('date published', default=timezone.now)
    edit_date = models.DateTimeField('date last modified', auto_now=True)
    author = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    search_fields = [
        index.SearchField('author'),
    ]

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('pub_date'),
        FieldPanel('likes'),
        FieldPanel('dislikes'),
    ]

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
    
    def should_display_updated(self, comp = 'day'):
        is_future = self.pub_date > timezone.now() or self.edit_date > timezone.now()
        # if either date is in the future, this is not something we want users to see
        if is_future:
            return False
        else:
            if comp == 'day':
                # if day is different or any either month or year are different
                return (self.pub_date.day() != self.edit_date.day()) or \
                       (self.pub_date - self.edit_date > datetime.timedelta(days=1))
            else: 
                raise NotImplementedError(f'{comp} not implemented')



class Post(Page, PublishMeta):
    # Database fields
    #title = models.CharField(max_length=1000)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True)

    # Search index configuration
    search_fields = Page.search_fields + PublishMeta.search_fields + [
        #index.SearchField('title'),
        index.SearchField('body'),
    ]

    # Editor panels configuration
    content_panels = PublishMeta.content_panels + [
        FieldPanel('body'),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('feed_image'),
    ]

    # Parent page / subpage type rules
    #parent_page_types = ['blog.BlogIndex'] # TODO
    #subpage_types = []

    def __str__(self):
        return f'"{self.pk} - {self.title}"'
    @property
    def short_description(self):
        return self.body[0][:30]

# a group of comments will be listed in a thread
class Thread(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return f'Comment Thread on {self.post.__str__()}'

    # ordered by creation date, newest thread first
    class Meta:
        ordering = ['-pk']

    @property
    def chain_id(self):
        return f'thread_{self.pk}_post_{self.post.pk}'

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

class BlogPageRelatedLink(Orderable):
    page = ParentalKey(Post, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

# Create your models here.
