"""StreamFields live in here"""

from wagtail.core import blocks


class RichTextBlock(blocks.RichTextBlock):
    """Richtext"""

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Full RichText"