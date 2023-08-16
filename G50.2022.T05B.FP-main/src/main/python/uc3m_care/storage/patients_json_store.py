"""Subclass of JsonStore for managing the Patients store"""
from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class PatientsJsonStore():
    """Implmentation of the singleton pattern"""

    #pylint: disable=invalid-name
    class __PatientsJsonStore(JsonStore):
        """Subclass of JsonStore for managing the VaccinationLog"""
        _FILE_PATH = JSON_FILES_PATH + "store_patient.json"
        _ID_FIELD = "_VaccinePatientRegister__patient_sys_id"
        _ERROR_MESSAGE_INVALID_PATIENT_OBJECT = "Invalid patient object"
        _KEY_ITEM_FOUND_PATIENT_ID = "_VaccinePatientRegister__patient_id"
        _KEY_ITEM_FOUND_REGISTRATION_TYPE = "_VaccinePatientRegister__registration_type"
        _KEY_ITEM_FOUND_FULL_NAME = "_VaccinePatientRegister__full_name"
        _ERROR_MESSAGE_PATIENT_IS_REGISTERED = "patien_id is registered in store_patient"

        def add_item( self, item ):
            """Overrides the add_item to verify the item to be stored"""
            #pylint: disable=import-outside-toplevel, cyclic-import
            from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
            if not isinstance(item,VaccinePatientRegister):
                raise VaccineManagementException(self._ERROR_MESSAGE_INVALID_PATIENT_OBJECT)

            patient_found = False
            patient_records = self.find_items_list\
                (item.patient_id,self._KEY_ITEM_FOUND_PATIENT_ID)
            for patient_recorded in patient_records:
                if (patient_recorded[self._KEY_ITEM_FOUND_REGISTRATION_TYPE]
                    == item.vaccine_type) \
                        and \
                        (patient_recorded[self._KEY_ITEM_FOUND_FULL_NAME]
                            == item.full_name):
                    raise VaccineManagementException(self._ERROR_MESSAGE_PATIENT_IS_REGISTERED)

            if not patient_found:
                super().add_item(item)

    # SINGLETON
    instance = None
    def __new__ ( cls ):
        if not PatientsJsonStore.instance:
            PatientsJsonStore.instance = PatientsJsonStore.__PatientsJsonStore()
        return PatientsJsonStore.instance

    def __getattr__ ( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__ ( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
