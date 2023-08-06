"""Some additional functions for this python package"""
# Standard library imports
import logging

# Third party imports
from char import char

# Local imports

LOGGER = logging.getLogger("selenium_screenshots")

@char
def delete_from_file_name_forbidden_characters(str_filename):
    """Delete forbidden charactars in a filename from the given string

    Args:
        str_filename (str): Name of the file

    Returns:
        str: filename with removed characters which are not allowed
    """
    list_chars_of_filtered_filenames = []
    for str_char in str_filename:
        if str_char.isalnum():
            list_chars_of_filtered_filenames.append(str_char)
        else:
            list_chars_of_filtered_filenames.append('_')
    return "".join(list_chars_of_filtered_filenames)
