"""Contains the class Vaccination Appoinment"""
import re
from datetime import datetime
import hashlib
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemID
from uc3m_care.data.attribute.attribute_phone import PhoneNumber

#pylint: disable=too-many-instance-attributes
class VaccinationAppoinment():
    """Class representing an appoinment  for the vaccination of a patient"""
    KEY_LABEL_PATIENT_SYSTEM_ID = "PatientSystemID"
    KEY_LABEL_PHONE_NUMBER = "ContactPhoneNumber"
    _ERROR_VALIDATE_PATIENT_SYSTEM_ID = "patient system id is not valid"
    _ERROR_VALIDATE_PHONE = "phone number is not valid"
    _DAYS_DATE = 10

    def __init__(self, input_file:str):

        my_data = AppointmentJsonParser(input_file)
        data = my_data.json_content

        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_sys_id = PatientSystemID(data[self.KEY_LABEL_PATIENT_SYSTEM_ID]).value
        self.__phone_number = PhoneNumber(data[self.KEY_LABEL_PHONE_NUMBER]).value

        self.__patient_id = VaccinePatientRegister.create_patient_from_sys_id(self.__patient_sys_id)
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        days = self._DAYS_DATE
        if days == 0:
            self.__appoinment_date = 0
        else:
            #timestamp is represneted in seconds.microseconds
            #age must be expressed in senconds to be added to the timestap
            self.__appoinment_date = self.__issued_at + (days * 24 * 60 * 60)
        self.__date_signature = self.vaccination_signature


    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg +",typ:" + self.__type +",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appoinment_date.__str__() + "}"

    @property
    def patient_id( self ):
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id( self, value ):
        self.__patient_id = value

    @property
    def patient_sys_id(self):
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id

    @patient_sys_id.setter
    def patient_sys_id(self, value):
        self.__patient_sys_id = value

    @property
    def phone_number( self ):
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number( self, value ):
        self.__phone_number = value

    @property
    def vaccination_signature( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at( self, value ):
        self.__issued_at = value

    @property
    def appoinment_date( self ):
        """Returns the vaccination date"""
        return self.__appoinment_date

    @property
    def date_signature(self):
        """Returns the SHA256 """
        return self.__date_signature

    def validate_patient_system_id(self, value: str) -> str:
        patient_system_id_pattern = re.compile(r"[0-9a-fA-F]{32}$")
        result = patient_system_id_pattern.fullmatch(value)
        if not result:
            raise VaccineManagementException(self._ERROR_VALIDATE_PATIENT_SYSTEM_ID)
        return value

    def validate_phone(self, phone_number: str) -> str:
        phone_pattern = re.compile(r"^(\+)[0-9]{11}")
        result = phone_pattern.fullmatch(phone_number)
        if not result:
            raise VaccineManagementException(self._ERROR_VALIDATE_PHONE)
        return phone_number
