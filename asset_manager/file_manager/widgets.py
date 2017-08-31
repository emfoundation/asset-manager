from django import forms

class ClearableFileInputNonEdit(forms.widgets.ClearableFileInput):
    template_name = 'widgets/clearable_file_input_non_edit.html'
