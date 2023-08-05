import json
from django.forms.widgets import Textarea
from .utils import jquery_plugins

class AceWidget(Textarea):

    def __init__(self, ace_options=None, attrs=None):
        ace_options = ace_options or {}
        new_attrs = {"width": "600px", "height": "400px"}
        new_attrs.update(attrs or {})
        classes = [x.strip() for x in new_attrs.get("class", "").split()]
        classes.append("django-fastadmin-ace-widget")
        new_attrs["class"] = " ".join(classes)
        new_attrs["ace-widget-options"] = json.dumps(ace_options)
        super().__init__(new_attrs)

    class Media:
        css = {
            "screen": [
                "fastadmin/widgets/ace-widget/ace-widget.css",
            ]
        }
        js = jquery_plugins([
            "ace-builds/ace.js",
            "jquery/plugins/jquery.utils.js",
            "fastadmin/widgets/ace-widget/ace-widget.js",
        ])
