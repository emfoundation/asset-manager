from django import forms
from django.conf import settings
from . models import Asset, Folder
from . import strings, widgets
import re


def validate_model_name(form, name, parent):
    """
    Check a model name is unique and valid.
    """
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

def clean_white_space(input_string):
    """
    Remove multiple spaces from input_string. Does not handle other white space chars.
    """
    return re.sub(' +', ' ', input_string)


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        widgets = {
            'file': widgets.ClearableFileInputNonEdit,
        }
        fields = ['parent', 'name', 'file', 'link', 'owner', 'tags', 'locations', 'contributors', 'collections', 'description', 'copyright_info', 'duration', 'creation_date', 'enabled', 'status', 'type_field', ]

    def clean(self):
        cleaned_data = super(AssetForm, self).clean()
        name = cleaned_data.get('name')
        parent = cleaned_data.get('parent')
        # Validate that a parent folder has been selected
        if parent is None:
            raise forms.ValidationError(strings.missing_parent_msg)

        file = cleaned_data.get('file')

        # if a name has been entered, strip extra white space and validate
        if name:
            name = clean_white_space(name)
            cleaned_data['name'] = name
            validate_model_name(self, name, parent)

        #### VALIDATE FILENAME ####
        # Pre-save filename is that of the file. Post-save filename has <parent_id>/
        # appended to it. as such it fails validation on subsequent saves due to the '/'
        # Only validating filename on initial upload is good enough for now.
        # @TODO When we allow filename to be changed after upload, or a new file
        # to be uploaded "over" an existing one, this validation will need reviewing.
        if(file and not self.instance.tracker.previous('file')):
            pattern = re.compile(strings.VALID_FILE_NAME_FORMAT)
            if not pattern.match(file.name):
                raise forms.ValidationError(strings.invalid_name_msg.format('file'))

            # Check file name is unique within parent Folder. Note that new
            # files do not yet have their parent's id appended to their name yet.
            # This will need appending to check for equality.
            assets = Asset.objects.filter(parent=parent).exclude(pk=self.instance.pk)
            filenames = []
            for asset in assets:
                filenames.append(asset.file.name)
            s3_key = str(parent.id) + '/' + file.name
            if s3_key in filenames:
                raise forms.ValidationError(strings.duplicate_file_name_msg.format(file.name, parent, name))

        #### VALIDATE FILE SIZE ####
        # Catches files that are larger than nginx's max upload size from being uploaded.
        # This should be combined with altering nginx conf file to set a limit that is higher
        # than the one set in Django.
        MAX_FILE_SIZE = 104857600 # 100MB
        readable_size = int(MAX_FILE_SIZE / (1024*1024))
        if (file._size > MAX_FILE_SIZE):
            raise forms.ValidationError(strings.file_size_exceeded.format(str(readable_size) + "MB"))

        return cleaned_data


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['parent', 'name']

    def clean(self):
        cleaned_data = super(FolderForm, self).clean()
        parent = cleaned_data.get('parent')
        name = cleaned_data.get('name')

        # Check Folder parent is correctly set
        if parent != None:
            if parent == self.instance:
                raise forms.ValidationError(strings.folder_set_as_own_parent_msg)
            elif not self.instance.is_new_parent_valid(parent):
                raise forms.ValidationError(strings.descendant_set_as_own_parent_msg)

        # if a name has been entered, strip extra white space and validate
        if name:
            name = clean_white_space(name)
            cleaned_data['name'] = name
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
            # validation must take place on the clean_white_space version of the name
            # this is not being set in the formset, so we must check against it here.
            name = form.cleaned_data.get('name')
            if name:
                name = clean_white_space(name)
                if name in model_names:
                    raise forms.ValidationError(strings.duplicate_inline_model_name.format(form._meta.model.__name__, name))
                model_names.append(name)

        return self.cleaned_data
