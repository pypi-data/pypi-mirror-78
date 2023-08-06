from django import template
from django.conf import settings

register = template.Library()

keen_config_class = getattr(settings, 'KEEN_CONFIG_CLASS', 'keen_dashboard.config.KeenConfig')
test_path = keen_config_class.split('.')

# Allow for relative paths
if len(test_path) > 1:
    config_module_name = '.'.join(test_path[:-1])
else:
    config_module_name = '.'

config_module = __import__(config_module_name, {}, {}, test_path[-1])
keen_config = getattr(config_module, test_path[-1])


@register.inclusion_tag('admin/includes/apps.html')
def user_apps(request):
    return keen_config.get_user_apps(request)


@register.inclusion_tag('admin/includes/user_menu.html')
def user_menu(request):
    return keen_config.get_user_menu(request)


@register.simple_tag()
def app_info(request):
    return keen_config.get_app_info(request)


@register.inclusion_tag('admin/includes/header_menu.html')
def header_menu(request):
    return keen_config.get_header_menu(request)
