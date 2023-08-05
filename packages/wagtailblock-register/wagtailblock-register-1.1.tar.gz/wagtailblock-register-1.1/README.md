# Wagtailblock Register

## Usage

Add in settings.py.

``` 
# Default WAGTAILBLOCK_COLLECTOR = "blocks"
WAGTAILBLOCK_COLLECTOR = "itemblocks"
```

String in ```WAGTAILBLOCK_COLLECTOR```
is a file. Default collector file is blocks.py.

Wagtailblock register will search for the file.

### Add block to collector

Above each block in the collectors file add ```@register_block```

Example:

```python
from wagtailblock_register import register_block
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

@register_block
class ImageTextBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Afbeelding")
    text = blocks.TextBlock(label="Tekst")
    text_color = blocks.CharBlock(default="#007BFF", label="Tekst kleur")
    position = blocks.ChoiceBlock(choices=(('left','Tekst links, afbeelding rechts'), ('right','Tekst rechts, afbeelding links')), label="Positioneren")
    
    class Meta:
        template = "website/blocks/tekst_image.html"
        icon = "image"
        label = "Afbeelding met tekst"

```

### Call all blocks in models.py

Example:

```python
from wagtail.core.models import Page

from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from wagtailblock_register import call_blocks


class ContentPage(Page):
    template = "website/pages/content.html"

    body = StreamField(call_blocks(), null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]

    class Meta:
        verbose_name_plural = "Content pagina"
```