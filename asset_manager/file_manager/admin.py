from django.conf import settings
from django.contrib import admin
from . import forms, models

from datetime import datetime
from pytz import timezone

class AssetAdmin(admin.ModelAdmin):
    form = forms.AssetForm
    filter_horizontal = ('contributors', 'locations', 'tags', )
    list_display = ['name', 'get_path', 'file', 'uploaded_by', 'uploaded_at']
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
            obj.uploaded_at = datetime.now(timezone(settings.TIME_ZONE))
        super(AssetAdmin, self).save_model(request, obj, form, change)

class FolderAdmin(admin.ModelAdmin):
    form = forms.FolderForm

# Register your models here.

admin.site.register(models.TagGroup)
admin.site.register(models.Tag)
admin.site.register(models.Contributor)
admin.site.register(models.ContinentTagGroup)
admin.site.register(models.CountryTag)
admin.site.register(models.Folder, FolderAdmin)
admin.site.register(models.Asset, AssetAdmin)
