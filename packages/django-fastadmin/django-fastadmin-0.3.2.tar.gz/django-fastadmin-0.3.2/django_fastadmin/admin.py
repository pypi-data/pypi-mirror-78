import uuid

from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from .utils import jquery_plugins

class UuidFieldSearchableAdmin(admin.ModelAdmin):
    """Enable search by uuid string with dashes.
    """
    def get_search_results(self, request, queryset, search_term):
        try:
            search_term_new = search_term
            if isinstance(search_term_new, str):
                search_term_new = search_term_new.strip()
            search_term_new = uuid.UUID(search_term_new).hex
        except ValueError:
            search_term_new = search_term
        result = super().get_search_results(request, queryset, search_term_new)
        return result



class InlineBooleanFieldsAllowOnlyOneCheckedMixin(InlineModelAdmin):
    """Admin inline formset has a boolean field, so that there are many checkboxes of that field, make sure that only one checkbox is checked.
    """

    special_class_name = "inline-boolean-fields-allow-only-one-checked"
    field_name_prefix = special_class_name + "-"

    class Media:
        js = jquery_plugins([
            "jquery/plugins/jquery.utils.js",
            "fastadmin/admins/inline-boolean-fields-allow-only-one-checked.js",
        ])


class WithInlineUniqueChoiceFieldsMixin(InlineModelAdmin):
    """ @todo
    """
    special_class_name = "with-inline-unique-choice-fields"
    field_name_prefix = special_class_name + "-"

    class Media:
        js = jquery_plugins([
            "jquery/plugins/jquery.utils.js",
            "fastadmin/admins/with-inline-unique-choice-fields.js",
        ])
