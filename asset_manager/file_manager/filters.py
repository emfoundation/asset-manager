from abc import abstractmethod

from django.contrib import admin
from django.contrib.auth.models import User

from . import models

class BaseListFilter(admin.SimpleListFilter):
    """
    Provides a base class for filtering Assets
    """

    title = ''
    parameter_name = ''
    model = ''

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        item_list = []
        for item in self.model.objects.all():
            if item.asset_set.all().exists():
                item_list.append(
                    (str(item.id), item.name + ' ({})'.format(len(item.asset_set.all())))
                )
        return sorted(item_list, key=lambda i: i[1])

    @abstractmethod
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        pass

class CollectionListFilter(BaseListFilter):

    title = 'Collection'
    parameter_name = 'collections'
    model = models.Collection

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(collections=self.value())
        return queryset


class ContributorListFilter(BaseListFilter):

    title = 'Contributor'
    parameter_name = 'contributors'
    model = models.Contributor

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(contributors=self.value())
        return queryset


class LocationListFilter(BaseListFilter):

    title = 'Country'
    parameter_name = 'locations'
    model = models.CountryTag

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(locations=self.value())
        return queryset


class TagListFilter(BaseListFilter):

    title = 'Tag'
    parameter_name = 'tag'
    model = models.Tag

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags=self.value())
        return queryset


class OwnerListFilter(admin.SimpleListFilter):
    """
    Provides a class for filtering Assets by Owner
    """

    title = 'Owner'
    parameter_name = 'owner'
    model = models.User

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        item_list = []
        for item in User.objects.all():
            if item.asset_set.all().exists():
                item_list.append(
                    (str(item.id), item.username + ' ({})'.format(len(item.asset_set.all())))
                )
        return sorted(item_list, key=lambda i: i[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(owner=self.value())
        return queryset


class FileTypeListFilter(admin.SimpleListFilter):
    """
    Provides a class for filtering Assets by FileType
    """

    title = 'File Type'
    parameter_name = 'filetype'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        filetype_list_count = {}
        filetype_list = []
        for asset in models.Asset.objects.all():
            filetype = asset.filetype
            if(filetype):
                if filetype in filetype_list_count:
                    filetype_list_count[filetype] += 1
                else:
                    filetype_list_count[filetype] = 1

        for key, val in filetype_list_count.items():
            filetype_list.append((key, key + ' ({})'.format(str(val))))

        return sorted(filetype_list, key=lambda i: i[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(filetype=self.value())
        return queryset


class TagGroupListFilter(admin.SimpleListFilter):
    """
    Provides a class for filtering Tags by TagGroup
    """

    title = 'Tag Group'
    parameter_name = 'taggroup'
    model = models.TagGroup

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        item_list = []
        for item in self.model.objects.all():
            if item.tag_set.all().exists():
                item_list.append(
                    (str(item.id), item.name + ' ({})'.format(len(item.tag_set.all())))
                )
        return sorted(item_list, key=lambda i: i[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(group=self.value())
        return queryset
