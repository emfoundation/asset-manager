# Checks the assets currently in use, and sorts them into a folder structure that is structured based on the Content types.
from file_manager.models import Asset, Folder

# Changes the Assets parent folder to the specified folder
def move_asset(asset, folder):
    if asset.parent != folder:
        # Display the asset that is being moved in the console
        # print("\n    Moving Asset '%s' into '%s' Folder" % (asset.name, folder_name))
        asset.parent = folder
        asset.save()
        return True

    return False

# Creates the folder structrue based on the type_choices that are defined in the Asset model.
# Creates a folder for every type, and changes the parent folder of the asset to the respective type folder.
def create_structure():
    types_dict = dict(Asset.TYPE_CHOICES)
    for code, type in types_dict.items():
        print("Checking the '%s' Content types..." % type, end='')
        folder = Folder.objects.get_or_create(name=type)[0]
        assets_by_type = Asset.objects.filter(type_field=code)
        moved = 0
        for asset in assets_by_type:
            moved += int(move_asset(asset, folder))

        print("%s Asset(s) moved " % moved)

def run():
    create_structure()
