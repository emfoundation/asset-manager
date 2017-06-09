from django.contrib import admin
from . import forms, models

class AssetAdmin(admin.ModelAdmin):
    form = forms.AssetForm

class FolderAdmin(admin.ModelAdmin):
    form = forms.FolderForm

# Register your models here.
admin.site.register(models.Folder, FolderAdmin)
admin.site.register(models.Asset, AssetAdmin)
