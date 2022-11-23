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

class HomePage(Page):
    # database fields
    hero = models.CharField(max_length=300,
            help_text='Enter the headline for the entire project. This will be the first thing new users see.',)

    hero_background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True)

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('hero'),
        index.SearchField('body'),
    ]

    # Editor panels configuration
    content_panels = [
        FieldPanel('hero'),
        FieldPanel('hero_background'),
        FieldPanel('body'),
    ] + Page.content_panels

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    # Parent page / subpage type rules
    #parent_page_types = []
    #subpage_types = []
