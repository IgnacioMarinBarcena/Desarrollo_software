import time
from datetime import datetime
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.attribute.attribute_cancelation_type import CancelationType
from uc3m_care.data.attribute.attribute_reason import Reason
from uc3m_care.parser.cancel_appointment_json_parser import CancelAppointmentJsonParser
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore
from uc3m_care.storage.cancel_appointment_json_store import CancelationJsonStore

#pylint: disable=too-many-instance-attributes
class CancelAppointment():
    """Class representing a cancelation for the  patient"""
    _KEY_APPOINTMENT_DATE = "_VaccinationAppointment__appointment_date"
    _ERROR_NO_APPOINTMENT = "el paciente no tiene citas pendientes"
    _ERROR_APPOITMENT_EXPIRED = "la cita ya ha pasado"
    _ERROR_PATIENT_VACCINATED = "el paciente ya se ha vacunado"
    _ERROR_APPOINTMENT_CANCEL = "la cita ya fue cancelada anteriormente"

    def __init__( self, input_file:str):

        my_data = CancelAppointmentJsonParser(input_file)
        data = my_data.json_content

        self.__date_signature = DateSignature(data["date_signature"]).value
        self.__cancelation_type = CancelationType(data["cancelation_type"]).value
        self.__reason = Reason(data["reason"]).value

    @property
    def date_signature(self):
        """Returns the SHA256 """
        return self.__date_signature

    @property
    def cancelation_type( self ):
        """Property representing the cancelation type"""
        return self.__cancelation_type

    @cancelation_type.setter
    def cancelation_type( self, value ):
        self.__cancelation_type = CancelationType(value)

    @property
    def reason( self ):
        """Property representing the reason"""
        return self.__reason

    @reason.setter
    def reason( self, value ):
        self.__reason = Reason(value)

    def check_date(self):
        item = self.check_the_date_signature()
        date = item[self._KEY_APPOINTMENT_DATE]
        self.is_the_date(date)

    def check_the_date_signature(self) -> str:
        # check if this date is in store_date
        my_store_date = AppointmentsJsonStore()
        item = my_store_date.find_item(self.__date_signature)
        if item is None:
            raise VaccineManagementException(self._ERROR_NO_APPOINTMENT)
        return item

    def is_the_date(self, date:str) -> None:
        today = datetime.fromtimestamp(time.time())
        date_patient = datetime.fromisoformat(date)
        if date_patient <= today:
            raise VaccineManagementException(self._ERROR_APPOITMENT_EXPIRED)

    def check_vaccination(self) -> str:
        my_vaccine_store = VaccinationJsonStore()
        item = my_vaccine_store.find_item(self.__date_signature)
        if item is not None:
            raise VaccineManagementException(self._ERROR_PATIENT_VACCINATED)
        return item

    def check_cancelation(self):
        my_cancel_store = CancelationJsonStore()
        item = my_cancel_store.find_item(self.__date_signature)
        if item is not None:
            raise VaccineManagementException(self._ERROR_APPOINTMENT_CANCEL)
        return item
