from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalManyToManyField

from wagtail.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (FieldPanel, PageChooserPanel, MultiFieldPanel, StreamFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

# 
# streams/blocks.py
from streams import blocks

# Category Snippets
class NewsCategory(models.Model):

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

    # Content searcher and filter
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Filter #
        # If get to search a title...
        if request.GET.get('title'):   
            # And get a category too...
            if request.GET.get('category'):
                # Filter all the posts with titles and the category selected
                all_posts = BlogDetailPage.objects.filter(custom_title__contains ='ipsum').live().public().filter(categories__slug__in=[request.GET.get('category')]).order_by('-first_published_at')
            # And don't get a category...
            else:
                # Filter posts only by the title
                all_posts = BlogDetailPage.objects.filter(custom_title__contains ='ipsum').live().public().order_by('-first_published_at')
        else:
            # If get to search just a category...
            if request.GET.get('category'):
                # Filter all the posts on that category
                all_posts = BlogDetailPage.objects.live().public().filter(categories__slug__in=[request.GET.get('category')]).order_by('-first_published_at')
            # If theres no search nor filters
            else:
                # Bring all the posts on time creation order
                all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')


        # Pagination#
        paginator = Paginator(all_posts, 5)
        # trying to get the value of ?page=x
        page = request.GET.get("page")
        try:
            # If the page exists and ?page=x is an integer
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If ?page=x it's not an integer, send to the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If ?page=x it's out of range
            # Return the last page
            posts = paginator.page(paginator.num_pages)

        # Context #
        # Posts
        context["posts"] = posts
        
        # Category snippets
        context["categories"] = NewsCategory.objects.all()

        # Searcher
        context["title"] = request.GET.get('title') if request.GET.get('title') is not None else ''
        context["category"] = request.GET.get('category') if request.GET.get('category') is not None else ''

        return context

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural="Home Pages"


class BlogDetailPage(Page):
    """Blog detail page."""
    template = "blog/blog_detail_page.html"

    # Time stamp of the creation and publication of the post
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
            ("full_richtext", blocks.RichTextBlock()),
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

    # Internal pagination of siblings
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        if self.get_prev_sibling():
            context["prev"] = self.get_prev_sibling().url
        else:
            context["prev"] = False

        if self.get_next_sibling():
            context["next"] = self.get_next_sibling().url
        else:
            context["next"] = False

        return context

    class Meta: 
        verbose_name = "Pagina de noticia"
        verbose_name_plural="Pagina de noticias"