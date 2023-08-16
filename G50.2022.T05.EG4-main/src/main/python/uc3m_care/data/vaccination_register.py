from datetime import datetime
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.appointment_json_store import AppointmentJsonStore


class VaccinationRegister():
    #Class representing a vaccine and date of a patient"""
    __CHECK_DATE_ITEM = "_VaccinationAppoinment__appoinment_date"
    __ERROR_MESSAGE_CHECK_DATE_SIGNATURE_NOT_FOUND = "date_signature is not found"
    __ERROR_MESSAGE_IS_THE_DATE_NOT_DATE = "Today is not the date"


    def __init__(self, date_signature:str):
        self.__date_signature = DateSignature(date_signature).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)

    @property
    def date_signature(self):
        return self.__date_signature

    @date_signature.setter
    def date_signature(self,value):
        self.__date_signature = DateSignature(value).value

    @property
    def time_stamp(self):
        return self.__time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        self.__time_stamp = value

    def check_date(self):
        item = self.check_the_date_signature()
        date_time = item[self.__CHECK_DATE_ITEM]
        self.is_the_date(date_time)

    def check_the_date_signature(self) -> str:
        # check if this date is in store_date
        my_store_date = AppointmentJsonStore()
        item = my_store_date.find_store_date_signature(self.__date_signature)
        if item is None:
            raise VaccineManagementException(self.__ERROR_MESSAGE_CHECK_DATE_SIGNATURE_NOT_FOUND)
        return item

    def is_the_date(self, date_time:str) -> None:
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(date_time).date()
        if date_patient != today:
            raise VaccineManagementException(self.__ERROR_MESSAGE_IS_THE_DATE_NOT_DATE)
