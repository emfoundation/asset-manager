from django.contrib import admin
from django.contrib.auth.models import User

from .models import Asset, Contributor, CountryTag, Tag, TagGroup


class ContributorListFilter(admin.SimpleListFilter):
    title = 'Contributor'
    parameter_name = 'contributors'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        contributor_list = []
        for contributor in Contributor.objects.all():
            if contributor.asset_set.all().exists():
                contributor_list.append(
                    (str(contributor.id), contributor.name + ' ({})'.format(len(contributor.asset_set.all())))
                )
        return sorted(contributor_list, key=lambda i: i[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(contributors=self.value())
        return queryset


class FileTypeListFilter(admin.SimpleListFilter):
    title = 'FileType'
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
        for asset in Asset.objects.all():
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


class LocationsListFilter(admin.SimpleListFilter):
    title = 'Country'
    parameter_name = 'locations'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        country_tag_list = []
        for country_tag in CountryTag.objects.all():
            if country_tag.asset_set.all().exists():
                country_tag_list.append(
                    (str(country_tag.id), country_tag.name + ' ({})'.format(len(country_tag.asset_set.all())))
                )
        return sorted(country_tag_list, key=lambda ct: ct[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(locations=self.value())
        return queryset


class OwnerListFilter(admin.SimpleListFilter):
    title = 'Owner'
    parameter_name = 'owner'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        owner_list = []
        for owner in User.objects.all():
            if owner.asset_set.all().exists():
                owner_list.append(
                    (str(owner.id), owner.username + ' ({})'.format(len(owner.asset_set.all())))
                )
        return sorted(owner_list, key=lambda i: i[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(owner=self.value())
        return queryset


class TagListFilter(admin.SimpleListFilter):

    title = 'Tag'
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        tag_list = []
        tags = Tag.objects.order_by('name')
        for tag in tags:
            if tag.asset_set.all().exists():
                tag_list.append(
                    (str(tag.id), tag.name + ' ({})'.format(len(tag.asset_set.all())))
                )
        return sorted(tag_list, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        # Only apply Tag level filter if currently selected Tag is a child
        # of the currently selected TagGroup.
        if self.value():
            # if 'tag' in request.GET and 'tag_group' in request.GET:
            #     tag = Tag.objects.get(id=request.GET['tag'])
            #     tag_group = TagGroup.objects.get(id=request.GET['tag_group'])
            #     if tag.group == tag_group:
            #         return queryset.filter(tags=self.value())
            # else:
                return queryset.filter(tags=self.value())
        return queryset


class TagGroupListFilter(admin.SimpleListFilter):

    title = 'tag group'
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_of_tag_groups = []
        tag_groups = TagGroup.objects.all()
        for tag_group in tag_groups:
            list_of_tag_groups.append(
                (str(tag_group.id), tag_group.name)
            )
        return sorted(list_of_tag_groups, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(group=self.value())
        return queryset


# class ReferencedTagGroupFilter(admin.SimpleListFilter):
#
#     # Human-readable title which will be displayed in the right admin sidebar just above the filter
#     # options.
#     title = 'tag group'
#
#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = 'tag_group'
#
#     # Custom attributes
#     # related_filter_parameter = 'tags__group__id__exact'
#
#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#
#         Limits TagGroups to those whose tags are in use.
#         """
#
#         referenced_tag_groups = []
#         all_tag_groups = TagGroup.objects.order_by('name')
#
#         for tag_group in all_tag_groups:
#             # 1. get all tags in a tag_group
#             tags = tag_group.tag_set.all()
#             if tags:
#                 # 2. check whether AT LEAST ONE tag is in use...
#                 for tag in tags:
#                     if tag.asset_set.all().exists():
#                         # 3. if so, add the parent tag_group
#                         referenced_tag_groups.append(
#                             (str(tag_group.id), tag_group.name)
#                         )
#                         break
#
#         return sorted(referenced_tag_groups, key=lambda tp: tp[1])
#
#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value
#         provided in the query string and retrievable via
#         `self.value()`.
#         """
#         # Compare the requested value to decide how to filter the queryset.
#         if self.value():
#             return queryset.filter(tags__group=self.value()).distinct()
#         return queryset
