from django.conf import settings
from django.contrib import admin
from . import forms, models

class AssetAdmin(admin.ModelAdmin):
    form = forms.AssetForm

class FolderAdmin(admin.ModelAdmin):
    form = forms.FolderForm

# Register your models here.

admin.site.register(models.TagGroup)
admin.site.register(models.Tag)
admin.site.register(models.Folder, FolderAdmin)
admin.site.register(models.Asset, AssetAdmin)

admin.site.site_header = 'EMF Digital Asset Management System {}'.format('(' + settings.ENVIRONMENT + ')')
admin.site.site_title = 'EMF DAMS Admin {}'.format('(' + settings.ENVIRONMENT + ')')
admin.site.index_title = 'Admin Interface'
