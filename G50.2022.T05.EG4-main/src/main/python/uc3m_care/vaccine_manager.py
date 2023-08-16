"""Module """
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.vaccination_appoinment import VaccinationAppoinment
from uc3m_care.storage.patient_json_store import PatientJsonStore
from uc3m_care.data.vaccination_register import VaccinationRegister
from uc3m_care.storage.vaccine_json_store import VaccineJsonStore
from uc3m_care.storage.appointment_json_store import AppointmentJsonStore

class VaccineManager:

    class SingletonVaccineManager:
        """Class for providing the methods for managing the vaccination process"""
        def __init__(self):
            pass

        #pylint: disable=too-many-arguments
        def request_vaccination_id (self, patient_id:str,
                                    name_surname:str,
                                    registration_type:str,
                                    phone_number:str,
                                    age:str)->str:

            """Register the patinent into the patients file"""
            my_patient = VaccinePatientRegister(patient_id,
                                                name_surname,
                                                registration_type,
                                                phone_number,
                                                age)

            my_store = PatientJsonStore()
            my_store.save_store(my_patient)

            return my_patient.patient_sys_id

        def get_vaccine_date(self, input_file: str) -> str:
            """Gets an appoinment for a registered patient"""
            my_sign = VaccinationAppoinment(input_file)

            # save the date in store_date.json
            my_store_date = AppointmentJsonStore()
            my_store_date.add_item(my_sign)

            return my_sign.date_signature

        def vaccine_patient(self, date_signature:str)->True:
            """Register the vaccination of the patient"""
            my_vaccine_log = VaccinationRegister(date_signature)
            my_vaccine_log.check_date()
            my_store_vaccine = VaccineJsonStore()
            my_store_vaccine.add_item(my_vaccine_log)

            return True

    __instance = None
    def __new__(cls):
        if not VaccineManager.__instance:
            VaccineManager.__instance = VaccineManager.SingletonVaccineManager()
        return VaccineManager.__instance
