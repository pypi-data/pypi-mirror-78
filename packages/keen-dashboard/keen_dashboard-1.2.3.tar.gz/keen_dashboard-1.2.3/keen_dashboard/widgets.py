from django.contrib.admin.widgets import ForeignKeyRawIdWidget, RelatedFieldWidgetWrapper, AutocompleteMixin
from django.forms import ClearableFileInput, Media, CheckboxInput, DateInput, TimeInput, SplitDateTimeWidget, TextInput, \
    Select, Textarea
from django.forms.widgets import TextInput as TextInputWidget
from django.utils.safestring import mark_safe


class AdminAvatarWidget(ClearableFileInput):
    template_name = 'admin/widgets/avatar_input.html'

    @property
    def media(self):
        return Media(js=('dist/assets/js/pages/components/forms/controls/avatar.js',))


class AdminSwitchWidget(CheckboxInput):
    input_type = 'checkbox'
    template_name = 'admin/widgets/switch_input.html'


class AdminSelect2(AutocompleteMixin, Select):

    def build_attrs(self, base_attrs, extra_attrs=None):
        atributos = super().build_attrs(base_attrs, extra_attrs)
        atributos['data-theme'] = 'default'
        return atributos


class AdminDate(DateInput):
    template_name = 'admin/widgets/date_input.html'

    @property
    def media(self):
        return Media(js=(
            'dist/assets/js/pages/components/forms/widgets/bootstrap-datetimepicker.js',
            'admin/js/date.picker.br.js',
        ))


class AdminDateTime(SplitDateTimeWidget):
    template_name = 'admin/widgets/datetime_input.html'

    @property
    def media(self):
        return Media(js=(
            'dist/assets/js/pages/components/forms/widgets/bootstrap-datetimepicker.js',
            'admin/js/date.picker.br.js',
        ))


class AdminTime(TimeInput):
    template_name = 'admin/widgets/time_input.html'

    @property
    def media(self):
        return Media(js=(
            'dist/assets/js/pages/components/forms/widgets/bootstrap-datetimepicker.js',
            'admin/js/date.picker.br.js',
        ))


class AdminText(TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'vTextField form-control', **(attrs or {})})


class AdminSelect(Select):
    template_name = 'admin/widgets/select_input.html'
    allow_multiple_selected = True


class AutosizedTextarea(Textarea):
    def __init__(self, attrs=None):
        new_attrs = _make_attrs(attrs, {"rows": 5}, "autosize form-control")
        super(AutosizedTextarea, self).__init__(new_attrs)

    @property
    def media(self):
        return Media(js=('admin/js/autosize.min.js',))


class ImageWidget(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super(ImageWidget, self).render(name, value, attrs, renderer)
        if not value or not hasattr(value, 'url') or not value.url:
            return html
        html = u'<div class="ImageWidget"><div class="float-xs-left">' \
               u'<a href="%s" target="_blank"><img class="rounded-lg" src="%s" width="75"></a></div>' \
               u'%s</div>' % (value.url, value.url, html)
        return mark_safe(html)


class EnclosedWidget(TextInputWidget):
    """
    Widget for bootstrap appended/prepended inputs
    """

    def __init__(self, attrs=None, prepend=None, append=None, prepend_class='prepend', append_class='append'):
        """
        :param prepend_class|append_class: CSS class applied to wrapper element. Values: addon or btn
        """
        self.prepend = prepend
        self.prepend_class = prepend_class
        self.append = append
        self.append_class = append_class
        super(EnclosedWidget, self).__init__(attrs=attrs)

    def enclose_value(self, value, wrapper_class):
        value = '<i class="%s"></i>' % value
        return '<div class="input-group-%s">' \
               '<span class="input-group-text">%s</span>' \
               '</div>' % (wrapper_class, value)

    def render(self, name, value, attrs=None, renderer=None):
        output = super(EnclosedWidget, self).render(name, value, attrs, renderer)
        div_classes = set()
        if self.prepend:
            div_classes.add('input-group')
            self.prepend = self.enclose_value(self.prepend, self.prepend_class)
            output = ''.join((self.prepend, output))
        if self.append:
            div_classes.add('input-group')
            self.append = self.enclose_value(self.append, self.append_class)
            output = ''.join((output, self.append))

        return mark_safe('<div class="%s">%s</div>' % (' '.join(div_classes), output))


def _make_attrs(attrs, defaults=None, classes=None):
    result = defaults.copy() if defaults else {}
    if attrs:
        result.update(attrs)
    if classes:
        result["class"] = " ".join((classes, result.get("class", "")))
    return result


class SearchWidget(ForeignKeyRawIdWidget):
    template_name = 'admin/widgets/search_input.html'


class TextSearchWidget(TextInputWidget):
    template_name = 'admin/widgets/text_search_input.html'

    def __init__(self, search_url=None, search=None, link_label=None, link_url=None):
        attrs = {
            'search_url': search_url,
            'link_label': link_label,
            'link_url': link_url,
            'search': search,
        }
        super().__init__(attrs)


class RelatedFieldWrapper(RelatedFieldWidgetWrapper):
    template_name = 'admin/widgets/related_wrapper.html'
