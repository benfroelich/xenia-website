from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
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
from wagtailmenus.models import MenuPage

class ProjectPost(MenuPage):
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
    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    # Editor panels configuration
    content_panels = [
        FieldPanel('intro'),
        InlinePanel('stats', label="Project Stats"),
        FieldPanel('body'),
    ] + Page.content_panels

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('feed_image'),
    ]

    # Parent page / subpage type rules
    parent_page_types = ['projects.ProjectIndex']
    subpage_types = []

    def __str__(self):
        return f'"{self.pk} - {self.title}"'
    @property
    def short_description(self):
        return self.body[0][:30]

    # TODO: make this a class that is inherited here and in cmsblog
    # recently posted or updated
    @admin.display(boolean=True, ordering='last_published_at', description='recent post',)
    def is_recent(self):
        days_back = 14
        threshold = timezone.now() - datetime.timedelta(days=days_back)
        is_future = self.first_published_at > timezone.now()
        # edit date is concurrent or newer than publication date
        # so it is adequate to check only edit date
        return not is_future and self.last_published_at >= threshold 
    
    def should_display_updated(self, comp = 'day'):
        if self.first_published_at is None or self.last_published_at is None:
            return False
        is_future = self.first_published_at > timezone.now() or \
            self.last_published_at > timezone.now()
        # if either date is in the future, this is not something we want users to see
        if is_future:
            return False
        else:
            if comp == 'day':
                # if day is different or either month or year are different
                return (self.first_published_at.day != self.last_published_at.day) or \
                       (self.first_published_at - self.last_published_at > datetime.timedelta(days=1))
            else: 
                raise NotImplementedError(f'{comp} not implemented')

class ProjectIndex(MenuPage):
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
        
    content_panels = [ FieldPanel('introduction', classname="full"), ] \
        + Page.content_panels \
        + [ FieldPanel('image'), ]
    
    # Speficies that only ProjectPage objects can live under this index page
    subpage_types = ['ProjectPost']

    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to add a list of all child items, that are live, 
    # by the date that they were published
    # https://docs.wagtail.org/en/stable/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(ProjectIndex, self).get_context(request)
        # iterate over this in template 
        context['active_posts'] = ProjectPost.objects.descendant_of(
            self).live().order_by(
            '-first_published_at')
        return context

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child ProjectPage objects for this ProjectPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self):
        return ProjectPost.objects.live().descendant_of(self)

from taggit.models import TaggedItemBase
class StatCategory(models.Model):
    name = models.CharField(max_length=256)
    units = models.CharField(max_length=64, blank=True)
    def __str__(self):
        return f'{self.name} [{self.units}]'

class Stats(Orderable):
    post = ParentalKey(ProjectPost, on_delete=models.CASCADE, related_name="stats")

    category = models.ForeignKey("StatCategory", on_delete=models.CASCADE, related_name="category")
    value = models.DecimalField(max_digits=15, decimal_places=6)
    details = models.CharField(max_length=1024, blank=True)

    panels = [
        FieldPanel('category'),
        FieldPanel('value'),
        FieldPanel('details'),
    ]

    def __str__(self):
        return f'{name}: {value}'

