"""Module """
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.vaccination_appointment import VaccinationAppointment
from uc3m_care.data.cancel_appointment import CancelAppointment
from uc3m_care.storage.cancel_appointment_json_store import CancelationJsonStore

class VaccineManager():
    """Implmentation of the singleton pattern"""

    # pylint: disable=invalid-name
    class __VaccineManager():
        """Class for providing the methods for managing the vaccination process"""
        def __init__(self):
            pass

        #pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        def request_vaccination_id (self, patient_id:str,
                                    name_surname:str,
                                    registration_type:str,
                                    phone_number:str,
                                    age:str) -> str:
            """Register the patinent into the patients file"""
            my_patient = VaccinePatientRegister(patient_id,
                                                    name_surname,
                                                    registration_type,
                                                    phone_number,
                                                    age)

            my_patient.save_patient()
            return my_patient.patient_sys_id

        def get_vaccine_date (self, input_file:str, date:str) -> str:
            """Gets an appointment for a registered patient"""
            my_sign= VaccinationAppointment.create_appointment_from_json_file(input_file, date)
            #save the date in store_date.json
            my_sign.save_appointment()
            return my_sign.date_signature

        def vaccine_patient(self, date_signature:str) -> str:
            """Register the vaccination of the patient"""
            appointment = VaccinationAppointment.get_appointment_from_date_signature(date_signature)
            return appointment.register_vaccination()

        def cancel_appointment(self, input_file:str) -> str:
            """Cancela la cita de vacunación del paciente"""
            my_store_cancel = CancelAppointment(input_file)
            my_store_cancel.check_date()
            my_store_cancel.check_vaccination()
            my_store_cancel.check_cancelation()
            my_cancel_store = CancelationJsonStore()
            my_cancel_store.add_item(my_store_cancel)
            return my_store_cancel.date_signature

    # SINGLETON
    instance = None
    def __new__ ( cls ):
        if not VaccineManager.instance:
            VaccineManager.instance = VaccineManager.__VaccineManager()
        return VaccineManager.instance

    def __getattr__ ( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__ ( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
