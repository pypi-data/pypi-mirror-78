from wagtail.utils.apps import get_app_submodules
from django.conf import settings

_block_list = []

_searched_for_hooks = False


def search_for_hooks():
    global _searched_for_hooks
    if not _searched_for_hooks:
        list(get_app_submodules(getattr(settings, WAGTAILBLOCK_COLLECTOR, "blocks")))
        _searched_for_hooks = True


def register_block(block=None):
    if block is None:
        search_for_hooks()
        return _block_list
    else:
        if block().label is None:
            label = block.__name__
        else:
            label = block().label
            
        block_label = block.__name__

        if block().meta.icon == "placeholder":
            icon = "fa-leaf"
        else:
            icon = block().meta.icon

        _block_list.append((block_label, block(icon=icon, label="{}".format(label))))


def call_blocks():
    return _block_list