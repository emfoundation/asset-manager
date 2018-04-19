from django.conf import settings
from django.contrib import admin

from . import filters, forms, models
from .models import Contributor

from datetime import datetime
from pytz import timezone

def set_asset_user_metadata(instance, user):
    """
    Sets Asset uploaded_by, uploaded_at, last_edit_by, last_edit_at and owner.
    Called on save by AssetAdmin and FolderAdmin (for AssetInlines).
    """
    # on first save...
    if not instance.pk:
        instance.uploaded_by = user
        instance.uploaded_at = datetime.now(timezone(settings.TIME_ZONE))
    # on subsequent saves...
    else:
        instance.last_edit_by = user
        instance.last_edit_at = datetime.now(timezone(settings.TIME_ZONE))

    # owner cannot be empty...
    if not instance.owner:
        instance.owner = user

class AssetAdmin(admin.ModelAdmin):

    form = forms.AssetForm
    filter_horizontal = ('collections', 'contributors', 'locations', 'tags', )
    list_display = ['name', 'parent', 'get_path', 'file', 'filetype', 'uploaded_by', 'uploaded_at', 'last_edit_by', 'last_edit_at', 'owner', ]
    search_fields = ('name', 'file', )
    list_filter = (
        filters.TagListFilter,
        filters.LocationListFilter,
        filters.CollectionListFilter,
        filters.ContributorListFilter,
        filters.OwnerListFilter,
        filters.FileTypeListFilter,
    )
    ordering = ['name', ]

    def save_model(self, request, obj, form, change):
        set_asset_user_metadata(obj, request.user)
        super(AssetAdmin, self).save_model(request, obj, form, change)

    class Media:
        js = [
        'file_manager/js/file_size.js',
        'file_manager/js/filter.js'
        ]

        css = {
        'all':('file_manager/css/filter.css',)
        }


class AssetInline(admin.TabularInline):
    model = models.Asset
    form = forms.AssetForm
    formset = forms.InlineModelFormSet
    extra = 0
    ordering = ['name', ]
    fields = ['name', ]
    show_change_link = True
    template = "admin/file_manager/asset/tabular.html"
    ### Adds the ability to collapse the asset block within the parent folder ###
    # classes = ['collapse', ]


class FolderInline(admin.TabularInline):
    model = models.Folder
    form = forms.FolderForm
    formset = forms.InlineModelFormSet
    extra = 0
    ordering = ['name', ]
    show_change_link = True
    template = "admin/file_manager/folder/tabular.html"
    ### Adds the ability to collaspe the folder structure ###
    # classes = ['collapse', ]


class FolderAdmin(admin.ModelAdmin):
    form = forms.FolderForm
    inlines = [FolderInline, AssetInline, ]
    ordering = ['name', ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if type(instance) == models.Asset:
                set_asset_user_metadata(instance, request.user)
            instance.save()


class TagGroupAdmin(admin.ModelAdmin):
    model = models.TagGroup
    ordering = ['name', ]


class TagAdmin(admin.ModelAdmin):
    model = models.Tag
    ordering = ['group', 'name', ]
    list_filter = (
        filters.TagGroupListFilter,
    )

    class Media:
        js = [
        'file_manager/js/filter.js'
        ]

        css = {
        'all':('file_manager/css/filter.css',)
        }


class ContinentTagGroupAdmin(admin.ModelAdmin):
    model = models.ContinentTagGroup
    ordering = ['name', ]


class CountryTagAdmin(admin.ModelAdmin):
    model = models.CountryTag
    ordering = ['continent', 'name', ]


# Register your models here.

admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.AssetLearnerJourney)
admin.site.register(models.Collection)
admin.site.register(models.ContinentTagGroup, ContinentTagGroupAdmin)
admin.site.register(models.Contributor)
admin.site.register(models.CountryTag, CountryTagAdmin)
admin.site.register(models.Folder, FolderAdmin)
admin.site.register(models.LearnerJourney)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.TagGroup, TagGroupAdmin)

admin.site.site_header = 'EMF Digital Asset Management System'
admin.site.site_title = 'EMF DAMS Admin'
admin.site.index_title = 'Admin Interface'

# Concatenate environment onto Django Admin header/title to indicate dev/staging
if settings.ENVIRONMENT == 'development' or settings.ENVIRONMENT == 'staging':
    admin.site.site_header += ' - ' + settings.ENVIRONMENT.capitalize()
    admin.site.site_title += ' - ' + settings.ENVIRONMENT.capitalize()
