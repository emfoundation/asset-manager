from django.conf import settings
from django.contrib import admin
from . import forms, models

from datetime import datetime
from pytz import timezone

class AssetAdmin(admin.ModelAdmin):
    form = forms.AssetForm
    filter_horizontal = ('collections', 'contributors', 'locations', 'tags', )
    list_display = ['name', 'get_path', 'file', 'filetype', 'uploaded_by', 'uploaded_at', 'last_edit_by', 'last_edit_at', 'owner', ]

    def save_model(self, request, obj, form, change):
        # on first save...
        if not change:
            obj.uploaded_by = request.user
            obj.uploaded_at = datetime.now(timezone(settings.TIME_ZONE))
        # on subsequent saves...
        else:
            obj.last_edit_by = request.user
            obj.last_edit_at = datetime.now(timezone(settings.TIME_ZONE))
            
        # owner cannot be empty...
        if not obj.owner:
            obj.owner = request.user

        super(AssetAdmin, self).save_model(request, obj, form, change)

class FolderAdmin(admin.ModelAdmin):
    form = forms.FolderForm

# Register your models here.

admin.site.register(models.TagGroup)
admin.site.register(models.Tag)
admin.site.register(models.Contributor)
admin.site.register(models.ContinentTagGroup)
admin.site.register(models.CountryTag)
admin.site.register(models.Collection)
admin.site.register(models.Folder, FolderAdmin)
admin.site.register(models.Asset, AssetAdmin)
