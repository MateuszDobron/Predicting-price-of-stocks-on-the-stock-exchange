# Author: Piotr Cieślak

import re
import pandas as pd
from pandas.errors import EmptyDataError
from .exceptions.wrong_file_extension_exception import WrongFileExtensionException
from .exceptions.empty_file_exception import EmptyFileException

class FileValidator:
    """This class provides methods for checking if a dataset provided by a user is valid"""

    def validate_file(self, file):
        """Check if a training dataset provided by user is valid"""

        if_valid = False
        if self.__get_file_extension(file, ".csv").__len__() != 1:
            raise WrongFileExtensionException()
        # if self.__validate_col_names(file) != True:
        #     return if_valid
        if_valid = True
        return if_valid


    def __get_file_extension(self, file, ext):
        """Checks if the file has the correct extension"""

        return re.findall(ext, file.name)


    #fixme: think if the validation of empty rows should be moved to preprocessing
    def __validate_values(self, file):
        """Validates if the values in the dataset are numerical variables."""

