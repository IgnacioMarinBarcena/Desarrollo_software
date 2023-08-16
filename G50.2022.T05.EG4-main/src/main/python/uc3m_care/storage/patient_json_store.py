from uc3m_care.storage.json_store import JsonStore
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class PatientJsonStore(JsonStore):

    class PatientStorage(JsonStore):
        _FILE_PATH = JSON_FILES_PATH + "store_patient.json"
        _ID_FIELD = "_VaccinePatientRegister__patient_id"
        _ERROR_MESSAGE_INVALID_PATIENT_OBJECT = "Invalid patient object"
        _KEY_ITEM_FOUND_REGISTRATION_TYPE = "_VaccinePatientRegister__registration_type"
        _KEY_ITEM_FOUND_FULL_NAME = "_VaccinePatientRegister__full_name"
        _ERROR_MESSAGE_PATIENT_IS_REGISTERED = "patien_id is registered in store_patient"

        def __init__(self):
            pass

        def save_store( self, data:VaccinePatientRegister )->True:
            """Medthod for savint the patients store"""
            #first read the file
            if not isinstance(data, VaccinePatientRegister):
                raise VaccineManagementException(self._ERROR_MESSAGE_INVALID_PATIENT_OBJECT)

            data_list = self.load_store()

            found = False
            item_found = self.find_item(data.patient_id)
            if item_found is not None:
                if (item_found[self._KEY_ITEM_FOUND_REGISTRATION_TYPE] == data.vaccine_type) and \
                        (item_found[self._KEY_ITEM_FOUND_FULL_NAME] == data.full_name):
                    found = True

            if found is False:
                data_list.append(data.__dict__)

            self.save(data_list)

            if found is True:
                raise VaccineManagementException(self._ERROR_MESSAGE_PATIENT_IS_REGISTERED)
            return True

    __instance = None
    def __new__(cls):
        if not PatientJsonStore.__instance:
            PatientJsonStore.__instance = PatientJsonStore.PatientStorage()
        return PatientJsonStore.__instance
