import re

from django import template
from django.contrib.admin.views.main import PAGE_VAR
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='addclass')
def addclass(value, arg):
    try:
        return value.as_widget(attrs={'class': arg})
    except Exception:
        match = re.search('class="', value)
        if match:
            final = match.regs[0][1]
            return mark_safe(value[:final] + arg + ' ' + value[final:])

        if value.startswith('<label'):
            return mark_safe(value.replace('<label ', '<label class="{}"'.format(arg)))

        return value


@register.simple_tag
def admin_url(request, url, *largs):
    values = list(request.resolver_match.kwargs.values())
    values += largs

    while values:
        try:
            return reverse(url, args=values)
        except Exception:
            values.pop()
    try:
        return reverse(url)
    except Exception:
        return '#'


@register.simple_tag
def filter_class(choices):
    for choice in choices:
        if choice.get('selected', False) and choice.get('display') != "Todos":
            return 'btn-primary'
    return 'btn-secondary'


@register.simple_tag
def paginator_item(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == '.':
        return '… '
    elif i == cl.page_num:
        return format_html('<a class="kt-datatable__pager-link kt-datatable__pager-link-number '
                           'kt-datatable__pager-link--active" data-page="{}" title="{}">{}</a>', i + 1, i + 1, i + 1)
    else:
        base_class = 'class="kt-datatable__pager-link kt-datatable__pager-link-number"'
        end_class = 'class="kt-datatable__pager-link kt-datatable__pager-link-number end"'
        css_class = mark_safe(end_class if i == cl.paginator.num_pages - 1 else base_class)
        return format_html(
            '<a  data-page="{}" title="{}" href="{}"{}>{}</a> ', i + 1, i + 1,
            cl.get_query_string({PAGE_VAR: i}), css_class, i + 1,
        )


@register.simple_tag
def get_filter_selected(used_parameters, choices):
    if used_parameters == {}:
        return None

    for choice in choices:
        if choice.get('selected'):
            return choice

    return None
