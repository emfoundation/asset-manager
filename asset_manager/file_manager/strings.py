# strings.py

# Validation messages for use in forms
descendant_set_as_own_parent_msg = "A Folder's Parent cannot be one of its \
sub-folders! Please choose an alternative Folder or leave blank to create a \
root level Folder"

folder_set_as_own_parent_msg = "A Folder cannot be set as its own Parent! \
Please choose an alternative Folder or leave blank to create a root level \
Folder."

invalid_name_msg = "Invalid {0} name, please use only: a-z A-Z 0-9 _ and -"

duplicate_model_name_msg = '{0} "{1}" already exists within Folder "{2}" \
. Please choose another name or a different parent.'

duplicate_inline_model_name = 'You are attempting to add more than one {0} \
with the same name: "{1}". Please choose unique names for each {0}.'

# string constants
VALID_NAME_FORMAT = '^[a-zA-Z0-9-_]+$'
VALID_FILE_NAME_FORMAT = '^[a-zA-Z0-9-_.]+$'
