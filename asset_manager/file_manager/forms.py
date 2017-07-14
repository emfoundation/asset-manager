from django import forms
from django.conf import settings
from . models import Asset, Folder
import re

invalid_name_msg = 'Invalid {0}, please use only: a-z A-Z 0-9 _ and -'
folder_set_as_own_parent_msg = 'A Folder cannot be set as its own Parent! Please choose an alternative Folder or leave blank to create a root level Folder.'

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['parent', 'name', 'file', 'link', 'owner', 'tags', 'locations', 'contributors', 'collections', 'description', 'copyright_info', 'duration', 'creation_date', 'enabled', 'status', ]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        pattern = re.compile('^[a-zA-Z0-9-_]+$')
        if not pattern.match(name):
            raise forms.ValidationError(invalid_name_msg.format('filename'))
        return self.cleaned_data['name']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['parent', 'name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        pattern = re.compile('^[a-zA-Z0-9-_]+$')
        if not pattern.match(name):
            raise forms.ValidationError(invalid_name_msg.format('folder name'))
        return self.cleaned_data['name']

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if parent == self.instance:
            raise forms.ValidationError(folder_set_as_own_parent_msg)
        return self.cleaned_data['parent']
