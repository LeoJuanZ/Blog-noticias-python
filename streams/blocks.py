"""StreamFields live in here"""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    """Title and text"""

    title = blocks.CharBlock(required=True, help_text='Add yout yiyle')
    text = blocks.TextBlock(required=True, help_text='Add additional text')

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Titulo y texto"

class CardBlock(blocks.StructBlock):
    """Cards with multi media"""

    title=blocks.CharBlock(required=False, help_text='Add yout yiyle')
    cards = blocks.ListBlock(
        blocks.StructBlock (
            [
                ("image", ImageChooserBlock(required = True)),
                ("title", blocks.CharBlock(required = True)),
                ("text", blocks.TextBlock(required = True)),
                ("button_page", blocks.PageChooserBlock(required=True)),
                ("button_url", blocks.URLBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Tarjetas horizontales"

class RichTextBlock(blocks.RichTextBlock):
    """Richtext"""

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Full RichText"

class CTABlock(blocks.StructBlock):
    """Call to action section"""

    title = blocks.CharBlock(required = True)
    text = blocks.RichTextBlock(required = True)
    button_page = blocks.PageChooserBlock(required = False)
    button_url = blocks.URLBlock(required = False)
    button_text = blocks.CharBlock(required = True)

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"