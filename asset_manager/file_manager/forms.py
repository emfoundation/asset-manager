from django import forms
from django.conf import settings
from . models import Asset, Folder
from . import strings
import re


def validate_model_name(form, name, parent):
    model = form._meta.model

    # Validate model name format
    pattern = re.compile(strings.VALID_NAME_FORMAT)
    if not pattern.match(name):
        raise forms.ValidationError(strings.invalid_name_msg.format(model.__name__))

    # Check model name is unique within parent
    siblings = model.objects.filter(parent=parent).exclude(pk=form.instance.pk)
    for sibling in siblings:
        if sibling.name == name:
            raise forms.ValidationError(strings.duplicate_model_name_msg.format(
            model.__name__, name, parent or 'Root'))


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['parent', 'name', 'file', 'link', 'owner', 'tags', 'locations', 'contributors', 'collections', 'description', 'copyright_info', 'duration', 'creation_date', 'enabled', 'status', ]

    def clean(self):
        cleaned_data = super(AssetForm, self).clean()
        name = cleaned_data.get('name')
        parent = cleaned_data.get('parent')

        validate_model_name(self, name, parent)

        return cleaned_data


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['parent', 'name']

    def clean(self):
        cleaned_data = super(FolderForm, self).clean()
        name = cleaned_data.get('name')
        parent = cleaned_data.get('parent')

        # Check Folder parent is correctly set
        if parent != None:
            if parent == self.instance:
                raise forms.ValidationError(strings.folder_set_as_own_parent_msg)
            elif not self.instance.is_new_parent_valid(parent):
                raise forms.ValidationError(strings.descendant_set_as_own_parent_msg)

        validate_model_name(self, name, parent)

        return cleaned_data


class InlineModelFormSet(forms.BaseInlineFormSet):
    def clean(self):
        """
        Check no two inline models have the same title as each other.
        """
        if any(self.errors):
            # Don't validate formset unless each form is valid itself
            return
        model_names = []
        for form in self.forms:
            name = form.cleaned_data.get('name')
            if name in model_names:
                raise forms.ValidationError(strings.duplicate_inline_model_name.format(form._meta.model.__name__, name))
            model_names.append(name)

        return self.cleaned_data
