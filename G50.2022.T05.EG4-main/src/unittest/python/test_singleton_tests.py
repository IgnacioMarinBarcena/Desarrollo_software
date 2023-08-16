import unittest
from uc3m_care.storage.appointment_json_store import AppointmentJsonStore
from uc3m_care.storage.patient_json_store import PatientJsonStore
from uc3m_care.storage.vaccine_json_store import VaccineJsonStore
from uc3m_care.vaccine_manager import VaccineManager

class SingletonTests(unittest.TestCase):
    def test_singleton_appointment_store(self):
        my_store_appointment_1 = AppointmentJsonStore()
        my_store_appointment_2 = AppointmentJsonStore()
        my_store_appointment_3 = AppointmentJsonStore()
        my_store_appointment_4 = AppointmentJsonStore()

        self.assertEqual(my_store_appointment_1, my_store_appointment_2)
        self.assertEqual(my_store_appointment_1, my_store_appointment_3)
        self.assertEqual(my_store_appointment_1, my_store_appointment_4)

    def test_singleton_patient_store(self):
        my_store_patient_1 = PatientJsonStore()
        my_store_patient_2 = PatientJsonStore()
        my_store_patient_3 = PatientJsonStore()
        my_store_patient_4 = PatientJsonStore()

        self.assertEqual(my_store_patient_1, my_store_patient_2)
        self.assertEqual(my_store_patient_1, my_store_patient_3)
        self.assertEqual(my_store_patient_1, my_store_patient_4)

    def test_singleton_vaccine_store(self):
        my_store_vaccine_1 = VaccineJsonStore()
        my_store_vaccine_2 = VaccineJsonStore()
        my_store_vaccine_3 = VaccineJsonStore()
        my_store_vaccine_4 = VaccineJsonStore()

        self.assertEqual(my_store_vaccine_1, my_store_vaccine_2)
        self.assertEqual(my_store_vaccine_1, my_store_vaccine_3)
        self.assertEqual(my_store_vaccine_1, my_store_vaccine_4)

    def test_singleton_vaccine_manager(self):
        my_vaccine_manager_1 = VaccineManager()
        my_vaccine_manager_2 = VaccineManager()
        my_vaccine_manager_3 = VaccineManager()
        my_vaccine_manager_4 = VaccineManager()

        self.assertEqual(my_vaccine_manager_1, my_vaccine_manager_2)
        self.assertEqual(my_vaccine_manager_1, my_vaccine_manager_3)
        self.assertEqual(my_vaccine_manager_1, my_vaccine_manager_4)

if __name__ == '__main__':
    unittest.main()
