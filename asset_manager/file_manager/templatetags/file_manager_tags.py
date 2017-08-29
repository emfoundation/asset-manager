from django import template

register = template.Library()

@register.filter
def show_root_level_folders_only(cl):
    """
    cl is a variable holding a Change List; the list of model instances.
    This function filters the Change List to remove non-root elements.
    """
    query_set = cl.result_list
    for folder in query_set:
        if folder.parent != None:
            query_set = query_set.exclude(pk=folder.id)
    cl.result_list = query_set
    return cl
