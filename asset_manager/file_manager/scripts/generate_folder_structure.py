# Checks the assets currently in use, and sorts them into a folder structure that is structured based on the Content types.
from file_manager.models import Asset, Folder

# Changes the Assets parent folder to the specified folder
def move_asset(asset, folder_name):
    folder = Folder.objects.get_or_create(name=folder_name)[0]
    if asset.parent != folder:
        #print("\n    Moving Asset '%s' into '%s' Folder" % (asset.name, folder_name))
        asset.parent = folder
        asset.save()
        return True

    return False

def create_structure():
    types_dict = dict(Asset.TYPE_CHOICES)
    for code, type in types_dict.items():
        print("Checking the '%s' Content types..." % type, end='')
        assets_by_type = Asset.objects.filter(type_field=code)
        moved = 0
        for asset in assets_by_type:
            moved += int(move_asset(asset, type))

        print("%s Asset(s) moved " % moved)
def run():
    create_structure()
