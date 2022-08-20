from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime

# wagtail-related
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
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
class PublishMeta(index.Indexed, ClusterableModel):
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

class BlogPost(Page, PublishMeta):
    # Database fields
    intro = models.CharField(max_length=1000)
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
        index.SearchField('title'),
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    # Editor panels configuration
    content_panels = [
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('related_links', label="Related links"),
    ] + PublishMeta.content_panels

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('feed_image'),
    ]

    # Parent page / subpage type rules
    parent_page_types = ['cmsblog.BlogIndex']
    subpage_types = []

    def __str__(self):
        return f'"{self.pk} - {self.title}"'
    @property
    def short_description(self):
        return self.body[0][:30]

class BlogIndex(Page):

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        FieldPanel('image'),
    ]
    
    # Speficies that only BlogPage objects can live under this index page
    subpage_types = ['BlogPost']

    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to add a list of all child items, that are live, 
    # by the date that they were published
    # https://docs.wagtail.org/en/stable/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(BlogIndex, self).get_context(request)
        # iterate over this in template 
        context['active_posts'] = BlogPost.objects.descendant_of(
            self).live().order_by(
            '-pub_date')
        return context

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child BlogPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self):
        return BlogPage.objects.live().descendant_of(self)

# a group of comments will be listed in a thread
class Thread(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
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
    page = ParentalKey(BlogPost, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

# Create your models here.
