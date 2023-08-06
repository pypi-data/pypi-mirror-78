from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


def badge(label, color):
    return mark_safe(render_to_string('components/badge.html', {
        'color': color,
        'label': label
    }))


def href(content, url, blank=True):
    blank = "target='_blank'" if blank else ''
    html = '<a href="{url}" {blank}>{content}</a>'.format(url=url, content=content, blank=blank)
    return mark_safe(html)


def icon(icon_, label='', extra_class=''):
    html = "<i class='%s %s mr-1'></i> %s" % (icon_, extra_class, label)
    return mark_safe(html)


def button(label, classe, icon):
    return mark_safe(render_to_string('components/button.html', {
        'class': classe,
        'icon': icon,
        'label': label
    }))


def confirm(label='', url='', text='', icon='info', title='Aviso', button_text='Sim'):
    html = '<a href="{url}" data-confirm="true" ' \
           'data-confirm-url="{url}" data-confirm-text="{text}" data-confirm-icon="{icon}" ' \
           'data-confirm-button-text="{button_text}" data-confirm-title="{title}">{label}</a>'.format(
        label=label, url=url, icon=icon, text=text, title=title, button_text=button_text
    )

    return mark_safe(html)


def avatar(url, image=None, label=None, circle=False, size='md', color=''):
    return mark_safe(render_to_string('components/media.html',
                                      {
                                          'size': size,
                                          'url': url,
                                          'label': label,
                                          'image': image,
                                          'color': color,
                                          'circle': circle,

                                      }))


def progress(label, percentage, color=None, style=1):
    if style == 1:
        template = 'components/progress.html'
    elif style == 2:
        template = 'components/progressv2.html'
    else:
        template = 'components/progressv3.html'

    content = render_to_string(template, {'color': color, 'percentage': percentage, 'label': label, })
    return mark_safe(content)


def user_card(title, subtitle=None, image='', url=''):
    content = render_to_string('components/user_card.html',
                               {'title': title, 'subtitle': subtitle, 'image': image, 'url': url})
    return mark_safe(content)


def icon_link(label, url, icon, color):
    content = render_to_string('components/icon_link.html',
                               {'icon': icon, 'url': url, 'label': label, 'color': color})
    return mark_safe(content)


def dropdown(options, direction='v'):
    content = render_to_string('components/dropdown_inline.html',
                               {'options': options, 'direction': direction})
    return mark_safe(content)


def helper(tittle):
    content = render_to_string('components/help.html',
                               {'tittle': tittle, })
    return mark_safe(content)


def flag(obj, atributo):
    valor = getattr(obj, atributo, None)
    if valor:
        return badge(icon('fas fa-check', 'Sim'), 'success')

    return badge(icon('fas fa-times', 'Não'), 'danger')
