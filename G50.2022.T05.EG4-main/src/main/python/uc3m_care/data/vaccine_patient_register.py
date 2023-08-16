"""MODULE: access_request. Contains the access request class"""
import hashlib
import json
from datetime import datetime
from freezegun import freeze_time
from uc3m_care.data.attribute.attribute_registration_type import RegistrationType
from uc3m_care.data.attribute.attribute_uuid import Uuid
from uc3m_care.data.attribute.attribute_name_surname import NameSurname
from uc3m_care.data.attribute.attribute_age import Age
from uc3m_care.data.attribute.attribute_phone import PhoneNumber
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH


class VaccinePatientRegister:
    """Class representing the register of the patient in the system"""
    #pylint: disable=too-many-arguments
    KEY_ITEM_PATIENT_SYSTEM_ID_DATA_LIST = "_VaccinePatientRegister__patient_sys_id"
    KEY_ITEM_PATIENT_ID_DATA_LIST = "_VaccinePatientRegister__patient_id"
    KEY_ITEM_FULL_NAME_DATA_LIST = "_VaccinePatientRegister__full_name"
    KEY_ITEM_REGISTRATION_TYPE_DATA_LIST = "_VaccinePatientRegister__registration_type"
    KEY_ITEM_PHONE_NUMBER_DATA_LIST = "_VaccinePatientRegister__phone_number"
    KEY_ITEM_AGE_DATA_LIST = "_VaccinePatientRegister__age"
    KEY_ITEM_TIME_STAMP_DATA_LIST = "_VaccinePatientRegister__time_stamp"
    _ERROR_MESSAGE_DATA_MANIPULATED = "Patient's data have been manipulated"
    _ERROR_MESSAGE_PATIENT_SYSTEM_ID_NOT_FOUND = "patient_system_id not found"

    def __init__( self, patient_id:str, full_name:str, registration_type:str,
                  phone_number:str, age:str):
        self.__patient_id = Uuid(patient_id).value
        self.__full_name = NameSurname(full_name).value
        self.__registration_type = RegistrationType(registration_type).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__age = Age(age).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)
        #self.__time_stamp = 1645542405.232003
        self.__patient_sys_id =  hashlib.md5(self.__str__().encode()).hexdigest()

    def __str__(self):
        return "VaccinePatientRegister:" + json.dumps(self.__dict__)

    @property
    def full_name( self ):
        """Property representing the name and the surname of
        the person who request the registration"""
        return self.__full_name

    @full_name.setter
    def full_name( self, value ):
        self.__full_name = NameSurname(value).value

    @property
    def vaccine_type( self ):
        """Property representing the type vaccine"""
        return self.__registration_type
    @vaccine_type.setter
    def vaccine_type( self, value ):
        self.__registration_type = RegistrationType(value).value

    @property
    def phone_number( self ):
        """Property representing the requester's phone number"""
        return self.__phone_number
    @phone_number.setter
    def phone_number( self, value ):
        self.__phone_number = PhoneNumber(value).value

    @property
    def patient_id( self ):
        """Property representing the requester's UUID"""
        return self.__patient_id
    @patient_id.setter
    def patient_id( self, value ):
        self.__patient_id = Uuid(value).value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def patient_system_id( self ):
        """Returns the md5 signature"""
        return self.__patient_sys_id

    @property
    def patient_age( self ):
        """Returns the patient's age"""
        return self.__age

    @property
    def patient_sys_id(self):
        """Property representing the md5 generated"""
        return self.__patient_sys_id

    @classmethod
    def create_patient_from_sys_id(cls, patient_system_id:str) -> str:
        file_store = JSON_FILES_PATH + "store_patient.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item[cls.KEY_ITEM_PATIENT_SYSTEM_ID_DATA_LIST] == patient_system_id:
                found = True
                # retrieve the patients data
                guid = item[cls.KEY_ITEM_PATIENT_ID_DATA_LIST]
                name = item[cls.KEY_ITEM_FULL_NAME_DATA_LIST]
                reg_type = item[cls.KEY_ITEM_REGISTRATION_TYPE_DATA_LIST]
                phone = item[cls.KEY_ITEM_PHONE_NUMBER_DATA_LIST]
                age = item[cls.KEY_ITEM_AGE_DATA_LIST]
                # set the date when the patient was registered for checking the md5
                patient_timestamp = item[cls.KEY_ITEM_TIME_STAMP_DATA_LIST]
                freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
                freezer.start()
                patient = cls(guid, name, reg_type, phone, age)
                freezer.stop()
                if patient.patient_system_id != patient_system_id:
                    raise VaccineManagementException(cls._ERROR_MESSAGE_DATA_MANIPULATED)
        if not found:
            raise VaccineManagementException(cls._ERROR_MESSAGE_PATIENT_SYSTEM_ID_NOT_FOUND)
        return guid
