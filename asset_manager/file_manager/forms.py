from django import forms
from django.conf import settings
from . models import Asset, Folder
import re

invalid_name_msg = 'Invalid {0}, please use only: a-z A-Z 0-9 _ and -'

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        readonly_fields = ['s3_key',]
        fields = ['parent', 'name', 'file', 's3_key', 'tags']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        pattern = re.compile('^[a-zA-Z0-9-_]+$')
        if not pattern.match(name):
            raise forms.ValidationError(invalid_name_msg.format('filename'))
        return self.cleaned_data['name']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        readonly_fields = ['s3_key']
        fields = ['parent', 'name', 's3_key']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        pattern = re.compile('^[a-zA-Z0-9-_]+$')
        if not pattern.match(name):
            raise forms.ValidationError(invalid_name_msg.format('folder name'))
        return self.cleaned_data['name']
