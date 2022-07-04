from django.db import models
from django import forms
import datetime

from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (InlinePanel, FieldPanel, PageChooserPanel, MultiFieldPanel, StreamFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.snippets.models import register_snippet


from streams import blocks

# class CreationDate(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)

#     panels = [
#         FieldPanel("date_time"),
#     ]

#     class Meta:
#         icon = "placeholder"
#         label = "Fecha y tiempo de creación"

class NewsCategory(models.Model):
    """Categorías de snippets"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Categoría de noticia"
        verbose_name_plural = "Categorías de noticias"
        ordering = ["name"]

    def __str__(self):
        return self.name

register_snippet(NewsCategory)

class HomePage(Page):
    """home page model"""
    template = "home/home_page.html"
    max_count = 1

    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content = StreamField(
        [
            ("cta", blocks.CTABlock())
        ],
        null = True,
        blank = True
    )

    content_panels = Page.content_panels + [
        PageChooserPanel("banner_cta"),
        StreamFieldPanel("content"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)

        if request.GET.get('category'):
            context["posts"] = BlogDetailPage.objects.live().public().filter(categories__slug__in=[request.GET.get('category')])
        elif request.GET.get('title'):
            context["posts"] = BlogDetailPage.objects.live().public().filter(custom_title__in=[request.GET.get('custom_title')])
        
        else:
            context["posts"] = BlogDetailPage.objects.live().public()

        context["categories"] = NewsCategory.objects.all()
        return context

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural="Home Pages"

class BlogDetailPage(Page):
    """Blog detail page."""

    created_at = models.DateTimeField(auto_now_add=True)

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )
    
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    categories = ParentalManyToManyField("home.NewsCategory", blank=False)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )
    

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categorías"
        ),
        StreamFieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Pagina de noticia"
        verbose_name_plural="Pagina de noticias"