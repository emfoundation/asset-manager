from django import forms
from django.conf import settings
from . models import Asset, Folder
import re

descendant_set_as_own_parent_msg = "A Folder's Parent cannot be one of its \
sub-folders! Please choose an alternative Folder or leave blank to create a \
root level Folder"
duplicate_folder_name_msg = 'Folder "{0}" already exists within Folder "{1}" \
. Please choose another name or a different parent.'
folder_set_as_own_parent_msg = "A Folder cannot be set as its own Parent! \
Please choose an alternative Folder or leave blank to create a root level \
Folder."
invalid_name_msg = "Invalid {0}, please use only: a-z A-Z 0-9 _ and -"
duplicate_inline_folder_name = 'You are attempting to add more than one Folder \
with the same name: "{0}". Please choose unique names for each Folder.'

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['parent', 'name', 'file', 'link', 'owner', 'tags', 'locations', 'contributors', 'collections', 'description', 'copyright_info', 'duration', 'creation_date', 'enabled', 'status', ]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        pattern = re.compile('^[a-zA-Z0-9-_]+$')
        if not pattern.match(name):
            raise forms.ValidationError(invalid_name_msg.format('filename'))
        return name

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
                raise forms.ValidationError(folder_set_as_own_parent_msg)
            elif not self.instance.is_new_parent_valid(parent):
                raise forms.ValidationError(descendant_set_as_own_parent_msg)

        # Validate Folder name format
        pattern = re.compile('^[a-zA-Z0-9-_]+$')
        if name and not pattern.match(name):
            raise forms.ValidationError(invalid_name_msg.format('folder name'))

        # Check Folder name is unique within parent
        sibling_folders = Folder.objects.filter(parent=parent) \
                                            .exclude(pk=self.instance.pk)
        for sibling_folder in sibling_folders:
            if sibling_folder.name == name:
                raise forms.ValidationError(duplicate_folder_name_msg.format(name,\
                parent or 'Root'))

        return self.cleaned_data

class BaseFolderFormSet(forms.BaseInlineFormSet):
    def clean(self):
        """
        Check no two inline Folders have the same title as each other.
        """
        if any(self.errors):
            # Don't validate formset unless each form is valid itself
            return
        folder_names = []
        for form in self.forms:
            name = form.cleaned_data['name']
            if name in folder_names:
                raise forms.ValidationError(duplicate_inline_folder_name.format(name))
            folder_names.append(name)
