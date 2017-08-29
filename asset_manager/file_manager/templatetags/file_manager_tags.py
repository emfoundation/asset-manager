from django import template

register = template.Library()

@register.filter
def show_root_level_folders_only(cl):
    qs = cl.result_list
    for folder in qs:
        if folder.parent != None:
            qs = qs.exclude(pk=folder.id)
    cl.result_list = qs
    return cl
