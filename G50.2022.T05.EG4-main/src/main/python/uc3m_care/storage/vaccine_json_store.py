from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH

class VaccineJsonStore(JsonStore):

    class VaccineStorage(JsonStore):
        _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"

        def __init__(self):
            pass

    __instance = None
    def __new__(cls):
        if not VaccineJsonStore.__instance:
            VaccineJsonStore.__instance = VaccineJsonStore.VaccineStorage()
        return VaccineJsonStore.__instance
