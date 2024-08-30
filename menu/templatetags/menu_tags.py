from django import template
from menu.models import Menu, MenuItem
from django.utils.html import format_html
from django.urls import resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url_name = resolve(request.path_info).url_name

    menu = Menu.objects.get(name=menu_name)
    menu_items = menu.items.all()

    def render_menu(items, parent=None, level=0):
        html = '<ul>'
        for item in items:
            if item.parent == parent:
                active = current_url_name == item.named_url or request.path == item.url
                if active:
                    html += f'<li class="active">{item.name}{render_menu(item.children.all(), item, level + 1)}</li>'
                else:
                    html += f'<li>{item.name}{render_menu(item.children.all(), item, level + 1)}</li>'
        html += '</ul>'
        return html

    return format_html(render_menu(menu_items))
