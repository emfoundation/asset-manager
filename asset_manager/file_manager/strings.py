# strings.py

# Validation messages for use in forms
descendant_set_as_own_parent_msg = "A Folder's Parent cannot be one of its \
sub-folders! Please choose an alternative Folder or leave blank to create a \
root level Folder"

folder_set_as_own_parent_msg = "A Folder cannot be set as its own Parent! \
Please choose an alternative Folder or leave blank to create a root level \
Folder."

invalid_name_msg = "Invalid {0} name, please use only: a-z A-Z 0-9 and these characters: _ - ' \" & , . ( )"

invalid_file_name_msg = "The file you are trying to upload has an invalid name. Please rename it, prior to uploading, using only the following characters: a-z A-Z 0-9 . - _"

duplicate_file_name_msg = 'A file with the name "{0}" already exists in this \
Folder: {1}, attached to Asset {2}. Please rename the file.'

duplicate_model_name_msg = '{0} "{1}" already exists within Folder "{2}" \
. Please choose another name or a different parent.'

duplicate_inline_model_name = 'You are attempting to add more than one {0} \
with the same name: "{1}". Please choose unique names for each {0}.'

missing_parent_msg = 'No Parent Folder has been selected. Please choose a Parent Folder.'

file_size_exceeded = 'The file you have chosen is too large, please select a file that is less than {0}'


# Helper text for use in forms
ASSET_PARENT_HELPER = 'Please select a parent Folder for the Asset'
ASSET_NAME_HELPER = 'Valid Asset name includes letters (lower and upper case) and the following characters _ - \' \" & , . ( )'
ASSET_FILE_NAME_HELPER = 'Valid file names include letters (lower and upper case), hyphen and underscore (- and _). Max uplod size 100mb.'


# string constants
VALID_NAME_FORMAT = '^[a-zA-Z0-9-_\'"&,.() ]+$'
VALID_FILE_NAME_FORMAT = '^[a-zA-Z0-9!-_.\'()]+$'
