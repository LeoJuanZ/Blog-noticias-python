from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import django_filters

import datetime

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.models import Page, Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (InlinePanel, FieldPanel, PageChooserPanel, MultiFieldPanel, StreamFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

# Codigo propio
# streams/blocks.py
from streams import blocks

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

        # Consigue todas las publicaciones de noticias en ORDEN DE PUBLICACIÓN
        # all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')

        print(request)

        if request.GET.get('category'):
            all_posts = BlogDetailPage.objects.live().public().filter(categories__slug__in=[request.GET.get('category')]).order_by('-first_published_at')
        # elif request.GET.get('title'):
        #     # all_posts = BlogDetailPage.objects.live().public().filter(custom_title__in=[request.GET.get('custom_title')]).order_by('-first_published_at')

        else:
            all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')

        # Paginación cada 5 publicaciones
        paginator = Paginator(all_posts, 2)
        # Intentando conseguir el valor de ?page=x
        page = request.GET.get("page")
        try:
            # Si la pagina existe y ?page=x es un entero
            posts = paginator.page(page)
        except PageNotAnInteger:
            # Si ?page=x no es un entero, manda a la primera pagina
            posts = paginator.page(1)
        except EmptyPage:
            # Si ?page=x esta fuera de rango
            # retorna la ultima pagina
            posts = paginator.page(paginator.num_pages)

        # "posts" tendra paginas hijos (Child pages); necesitaras usar el .especifico en los templates
        # para llamar las propiedades de los hijos
        context["posts"] = posts

        context["categories"] = NewsCategory.objects.all()
        return context

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural="Home Pages"

class BlogDetailPage(Page):
    """Blog detail page."""

    created_at_date_time = models.DateTimeField(auto_now_add=True)

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