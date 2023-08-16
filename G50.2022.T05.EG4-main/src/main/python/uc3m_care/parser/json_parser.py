import json
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class JsonParser():
    _key_list = []
    _key_error_message = []
    _ERROR_MESSAGE_FILE_NOT_FOUND = "File is not found"
    _ERROR_MESSAGE_WRONG_JSON_FORMAT = "JSON Decode Error - Wrong JSON Format"

    def __init__(self, input_file:str):
        self._file = input_file
        self._json_content = self._read_json_file()
        self._validate_key_labels()

    def _read_json_file(self) -> str:
        try:
            with open(self._file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise VaccineManagementException(self._ERROR_MESSAGE_FILE_NOT_FOUND) from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException(self._ERROR_MESSAGE_WRONG_JSON_FORMAT) from ex
        return data

    def _validate_key_labels(self):
        """checking the labels of the input json file"""
        i = 0
        for key in self._key_list:
            if not key in self._json_content.keys():
                raise VaccineManagementException(self._key_error_message[i])
            i = i + 1

    @property
    def json_content(self):
        return self._json_content
