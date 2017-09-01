from django.contrib import admin

from .models import Asset, TagGroup, Tag

class TagGroupListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'TagGroup'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'group'

    default_value = None

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
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(group=self.value())
        return queryset

    def value(self):
        """
        Overriding this method will allow us to always have a default value.
        """
        value = super(TagGroupListFilter, self).value()
        if value is None:
            if self.default_value is None:
                # If there is at least one TagGroup, return the first by name. Otherwise, None.
                first_tag_group = TagGroup.objects.order_by('name').first()
                value = None if first_tag_group is None else first_tag_group.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)

class ReferencedTagGroupFilter(admin.SimpleListFilter):

    # Human-readable title which will be displayed in the right admin sidebar just above the filter
    # options.
    title = 'tag group'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'tag_group'

    # Custom attributes
    # related_filter_parameter = 'tags__group__id__exact'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.

        Limits TagGroups to those whose tags are in use.
        """
        referenced_tag_groups = []
        all_tag_groups = TagGroup.objects.order_by('name')

        for tag_group in all_tag_groups:
            # 1. get all tags in a tag_group
            tags = tag_group.tag_set.all()
            if tags:
                # 2. check whether AT LEAST ONE tag is in use...
                for tag in tags:
                    if tag.asset_set.all().exists():
                        # 3. if so, add the parent tag_group
                        referenced_tag_groups.append(
                            (str(tag_group.id), tag_group.name)
                        )
                        break

        return sorted(referenced_tag_groups, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(tags__group=self.value()).distinct()
        return queryset

class TagListFilter(admin.SimpleListFilter):

    # Human-readable title which will be displayed in the right admin sidebar just above the filter
    # options.
    title = 'tag'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'tag'

    # Custom attributes
    related_filter_parameter = 'tag_group'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_of_tags = []
        tags = Tag.objects.order_by('name')
        print(request.GET)
        if self.related_filter_parameter in request.GET:
            tags = tags.filter(group=request.GET[self.related_filter_parameter])
        for tag in tags:
            if tag.asset_set.all().exists():
                list_of_tags.append(
                    (str(tag.id), tag.name)
                )
        return sorted(list_of_tags, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(tags=self.value())
        return queryset
