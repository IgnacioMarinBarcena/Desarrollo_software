import json
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class JsonStore():
    _FILE_PATH = ""
    _ID_FIELD = ""
    _ERROR_MESSAGE_WRONG_FILE = "Wrong file or file path"
    _ERROR_MESSAGE_WRONG_JSON_FORMAT = "JSON Decode Error - Wrong JSON Format"

    def __init__(self):
        pass

    def save(self, data_list:str):
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise VaccineManagementException(self._ERROR_MESSAGE_WRONG_FILE) from ex

    def load_store(self) -> str:
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as ex:
            raise VaccineManagementException(self._ERROR_MESSAGE_WRONG_JSON_FORMAT) from ex
        return data_list

    def add_item(self, item):
        data_list = self.load_store()
        # append the date
        data_list.append(item.__dict__)
        self.save(data_list)

    def find_item(self, value_to_find:str, id_field=None) -> str:
        data_list = self.load_store()
        if not id_field:
            id_field = self._ID_FIELD
        for item in data_list:
            if item[id_field] == value_to_find:
                return item
        return None
