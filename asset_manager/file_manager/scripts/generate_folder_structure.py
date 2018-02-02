# Checks the assets currently in use, and sorts them into a folder structure that is structured based on the Content types.
from file_manager.models import Asset, Folder
# Moves an Asset into a Folder
def move_asset(asset, folder_name):
    folder = Folder.objects.get_or_create(name=folder_name)[0]
    if asset.parent != folder:
        print("Moving Asset '%s' into '%s' Folder \n" % (asset, type))
        asset.parent = folder

    asset.save()


def create_structure():
    types_dict = dict(Asset.TYPE_CHOICES)
    for code, type in types_dict.items():
        print("Checking all '%s'|'%s' Assets" % (code, type))
        assets_by_type = Asset.objects.filter(type_field=code)
        for asset in assets_by_type:
            move_asset(asset, type)

def run():
    create_structure()
