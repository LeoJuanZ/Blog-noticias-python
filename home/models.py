from django.db import models

from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (InlinePanel, FieldPanel, PageChooserPanel, MultiFieldPanel, StreamFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.snippets.models import register_snippet


from streams import blocks

class CategoriasOrdenables(Orderable):
    """Nos deja seleccionar uno o más categorias para la noticia"""

    page = ParentalKey("home.BlogDetailPage", related_name="categoria_noticia")
    categoria = models.ForeignKey(
        "home.Categorias",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("categoria"),
    ]

class Categorias(models.Model):
    """Snippets"""

    name = models.CharField(max_length=100)

    panels = FieldPanel("name"),

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:  # noqa
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


register_snippet(Categorias)

class HomePage(Page):
    """home page model"""
    template = "home/home_page.html"
    max_count = 1

    categories = ParentalManyToManyField('home.Categorias', blank=True)



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
        context["posts"] = BlogDetailPage.objects.live().public()

        context["categorias"] = Categorias.objects.all()
        return context

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural="Home Pages"

class BlogDetailPage(Page):
    """Blog detail page."""

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
                InlinePanel("categoria_noticia", label="Categoría", min_num=1)
            ],
            heading="Categoría(s)"
        ),
        StreamFieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Pagina de noticia"
        verbose_name_plural="Pagina de noticias"