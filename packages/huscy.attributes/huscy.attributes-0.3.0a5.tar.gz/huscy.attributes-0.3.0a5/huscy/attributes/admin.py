from django import forms
from django.contrib import admin

from prettyjson import PrettyJSONWidget

from huscy.attributes import models


class AttributeSchemaAdminForm(forms.ModelForm):
    class Meta:
        model = models.AttributeSchema
        fields = '__all__'
        widgets = {
            'schema': PrettyJSONWidget(),
        }


class AttributeSchemaAdmin(admin.ModelAdmin):
    form = AttributeSchemaAdminForm

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.AttributeSchema, AttributeSchemaAdmin)
