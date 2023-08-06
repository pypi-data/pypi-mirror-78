from django.forms import widgets
from django.conf import settings
from django.template.loader import render_to_string


class EditorJsWidget(widgets.TextInput):
    class Media:
        js = (
            'editorjs/editor.js',
            'editorjs/checklist.js',
            'editorjs/delimiter.js',
            'editorjs/header.js',
            'editorjs/image.js',
            'editorjs/inline-code.js',
            'editorjs/link.js',
            'editorjs/list.js',
            'editorjs/paragraph.js',
            'editorjs/quote.js',
            'editorjs/raw.js',
            'editorjs/table.js',
            'editorjs/editorjs_field.js',
        )
        css = {'all': ('editorjs/editorjs_field.css',)}

    def __init__(self, *args, **kwargs):
        super(EditorJsWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, **kwargs):
        elements = {'data_ejs_checklist': kwargs.get('checklist', "true"),
                    'data_ejs_delimiter': kwargs.get('delimiter', "true"),
                    'data_ejs_header': kwargs.get('header', "true"),
                    'data_ejs_image': kwargs.get('image', "true"),
                    'data_ejs_inline-code': kwargs.get('inline-code', "true"),
                    'data_ejs_link': kwargs.get('link', "true"),
                    'data_ejs_list': kwargs.get('list', "true"),
                    'data_ejs_paragraph': kwargs.get('paragraph', "true"),
                    'data_ejs_quote': kwargs.get('quote', "true"),
                    'data_ejs_raw': kwargs.get('raw', "true"),
                    'data_ejs_table': kwargs.get('table', "true")}
        ctx = {
            'name': name,
            'id': kwargs['attrs']['id'],
            'value': value,
            'media_url': settings.MEDIA_URL,
            'attributes': elements
        }

        return render_to_string('editorjs_widget.html', ctx)
