import json
from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class AppointmentJsonStore(JsonStore):

    class AppointmentStorage(JsonStore):
        _FILE_PATH = JSON_FILES_PATH + "store_date.json"
        _ID_FIELD = "_VaccinationAppoinment__date_signature"
        _ERROR_MESSAGE_WRONG_JSON_FORMAT = "JSON Decode Error - Wrong JSON Format"
        _ERROR_MESSAGE_STORE_NOT_FOUND = "Store_date not found"
        def __init__(self):
            pass

        def find_store_date_signature(self, date_signature:str) -> str:
            self.check_store()
            # search this date_signature
            return self.find_item(date_signature)

        def check_store(self) -> str:
            try:
                with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                    data_list = json.load(file)
            except json.JSONDecodeError as ex:
                raise VaccineManagementException(self._ERROR_MESSAGE_WRONG_JSON_FORMAT) from ex
            except FileNotFoundError as ex:
                raise VaccineManagementException(self._ERROR_MESSAGE_STORE_NOT_FOUND) from ex
            return data_list

    __instance = None
    def __new__(cls):
        if not AppointmentJsonStore.__instance:
            AppointmentJsonStore.__instance = AppointmentJsonStore.AppointmentStorage()
        return AppointmentJsonStore.__instance
