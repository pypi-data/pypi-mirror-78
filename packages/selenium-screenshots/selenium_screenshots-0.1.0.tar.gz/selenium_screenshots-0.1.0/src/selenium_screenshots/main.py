"""Main file of this python package with the class Screenshots"""
# Standard library imports
import os
import logging

# Third party imports
from local_simple_database import LocalSimpleDatabase
from char import char

# Local imports
from .exceptions import SeleniumScreenshotsError
from .additional import delete_from_file_name_forbidden_characters


LOGGER = logging.getLogger("selenium_screenshots")


class Screenshots(object):
    """Class to handle creation of many screenshots for selenium

    Raises:
        SeleniumScreenshotsError: Main Exception of this python package
    """

    @char
    def __init__(
            self,
            webdriver,
            str_path_dir_with_screenshots="screenshots",
            int_screenshots_to_delete_half=9999,
            int_max_length_of_filename=50,
    ):
        """Init object for handling screenshots

        Args:
            webdriver (selenium.webdriver): Selenium Webdriver
            str_path_dir_with_screenshots (str, optional): \
                Path to directory where to save screenshots.
            int_screenshots_to_delete_half (int, optional): Number of the \
                screenshots in the directory when delete half of them
            int_max_length_of_filename (int, optional): \
                Max length of the filename for new screenshot file
        """
        self.webdriver = webdriver
        self.str_path_dir_with_screenshots = \
            os.path.abspath(str_path_dir_with_screenshots)
        self.LSD = LocalSimpleDatabase(self.str_path_dir_with_screenshots)
        self.int_screenshots_to_delete_half = int_screenshots_to_delete_half
        self.int_max_length_of_filename = int_max_length_of_filename
        # Create directory for the screenshots
        if not os.path.exists(str_path_dir_with_screenshots):
            os.makedirs(str_path_dir_with_screenshots)
            LOGGER.info(
                "Created directory for the screenshots: %s",
                str_path_dir_with_screenshots
            )
        self.LSD["int_screenshots_in_the_dir"] = \
            self._count_number_of_screenshots_in_the_directory()

    @char
    def create_screenshot(self, str_description="", another_webdriver=None):
        """Create a new screenshot with given description

        Args:
            str_description (str): description to add in the screenshot name.
            another_webdriver (selenium.webdriver): \
                If you want to use another webdriver

        Raises:
            SeleniumScreenshotsError: Main exception of this python package
        """
        str_filename = self._create_name_for_screenshot(str_description)
        str_screenshot_path = os.path.join(
            self.str_path_dir_with_screenshots, str_filename)
        LOGGER.debug("Create screenshot in path: %s", str_screenshot_path)
        #####
        # Choose webdriver
        if another_webdriver is not None:
            webdriver_to_use = another_webdriver
        else:
            webdriver_to_use = self.webdriver
        #####
        # Try to create screenshot
        try:
            webdriver_to_use.get_screenshot_as_file(str_screenshot_path)
        except Exception as ex:
            LOGGER.error(
                "Unable to create screenshot with name: %s", str_filename)
            raise SeleniumScreenshotsError(str(ex))
        self.LSD["int_last_screenshot_num"] += 1
        self.LSD["int_screenshots_in_the_dir"] += 1
        # Delete screenshots if there are too many of them
        if self.LSD["int_screenshots_in_the_dir"] > \
        self.int_screenshots_to_delete_half:
            self._remove_old_screenshots_if_there_are_too_much()

    @char
    def _create_name_for_screenshot(self, str_description):
        """Create name for the new screenshot like "<number>_<description>"

        Args:
            str_description (str): string which to add in screenshot name

        Returns:
            str: Name for the screenshot
        """
        # Get number for new screenshot
        int_new_screenshot_num = self.LSD["int_last_screenshot_num"] + 1
        LOGGER.debug("Number for new screenshot: %d", int_new_screenshot_num)
        str_filename = "{}_{}".format(
            int_new_screenshot_num, str_description)
        # If the filename is too long then cut it
        if len(str_filename) > self.int_max_length_of_filename:
            str_filename = str_filename[:self.int_max_length_of_filename]
        # Delete forbidden characters
        str_filename_filtered = \
            delete_from_file_name_forbidden_characters(str_filename)
        LOGGER.debug(
            "Created a name for new screenshot: %s", str_filename_filtered)
        return str_filename_filtered + ".png"

    def _remove_old_screenshots_if_there_are_too_much(self):
        """Delete most old screenshots if there are too much of them
        """
        # Check if there are too much screenshots
        list_screens_names = self._get_names_of_all_screenshots()
        if len(list_screens_names) < self.int_screenshots_to_delete_half:
            self.LSD["int_screenshots_in_the_dir"] = len(list_screens_names)
            return None
        # Create dictionary {screenshot_num: screenshot_filename, ...}
        dict_screen_name_by_num = {}
        for str_screenshot_name in list_screens_names:
            try:
                int_screen_num = int(str_screenshot_name.split("_")[0])
            except ValueError:
                LOGGER.warning(
                    "Wrong filename of the screenshot: %s",
                    str_screenshot_name
                )
                continue
            dict_screen_name_by_num[int_screen_num] = str_screenshot_name
        # Create sorted list with screenshot's numbers
        list_sorted_screenshot_numbers = sorted(dict_screen_name_by_num)
        int_screens_to_delete = self.int_screenshots_to_delete_half // 2
        int_screens_deleted = 0
        # Delete old screenshots
        for int_screen_num_to_del in  \
        list_sorted_screenshot_numbers[:int_screens_to_delete]:
            str_screen_name = dict_screen_name_by_num[int_screen_num_to_del]
            str_screenshot_path = os.path.join(
                self.str_path_dir_with_screenshots, str_screen_name)
            LOGGER.debug("Delete screenshot: %s", str_screen_name)
            try:
                os.remove(str_screenshot_path)
                int_screens_deleted += 1
            except OSError:
                LOGGER.warning(
                    "Unable to delete screenshot: %s", str_screenshot_path)
        LOGGER.info("Were deleted screenshots: %d", int_screens_to_delete)
        #####
        # Save new number of screenshots in the dir
        list_screens_names = self._get_names_of_all_screenshots()
        self.LSD["int_screenshots_in_the_dir"] = len(list_screens_names)
        return None

    def _get_names_of_all_screenshots(self):
        """Get list with names of all screenshots

        Returns:
            list: Names of all screenshots
        """
        list_screenshots_names = [
            filename
            for filename in os.listdir(self.str_path_dir_with_screenshots)
            if ".png" in filename
        ]
        return list_screenshots_names

    def _count_number_of_screenshots_in_the_directory(self):
        """Count number of screenshots in the set directory

        Returns:
            int: Number of the screenshots
        """
        return len(self._get_names_of_all_screenshots())
