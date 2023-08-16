import hashlib
import os
import time
import unittest
from pathlib import Path
import json
from uc3m_care.vaccine_manager import VaccineManager
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from freezegun import freeze_time
from uc3m_care.storage.cancel_appointment_json_store import CancelationJsonStore
from datetime import datetime

@freeze_time("2022-03-08")
class MyTestCase(unittest.TestCase):
# PRUEBAS DEL ÁRBOL DE DERIVACIÓN

    def test_cancel_appointment_ok(self):
        # Camino del fichero de salida y de lectura
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"
        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Camino fichero de entrada
        file_test = json_files_rf4_path + "test_ok.json"
        my_manager = VaccineManager()

        # añadimos un paciente extra para ver que no de error

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family","+34333456789", "7")

        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-05-09")

        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "7a3b9278198d172a4f5ff0234c588c7383feb276febad1017bd947cccab96ce0")

        with open(file_store_cancel,"r",encoding="utf-8",newline="") as file:
            data_list = json.load(file)

        found = False
        for item in data_list:
            if item["_CancelAppointment__date_signature"] == value:
                found = True
        self.assertTrue(found)

    def test_cancel_appointment_nok1(self):
        # No se encuentra el fichero de entrada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        #Abrimos el fichero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        file_test = json_files_rf4_path + "erroneo_test.json"

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("File is not found", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok2(self):
        # El fichero de entrada se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test.json"

        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok3(self):
        # No se encuentra el inicio objeto
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test2.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok4(self):
        # El inicio objeto se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        date = my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test3.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok5(self):
        # No se encuentran los datos
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test4.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label date_signature", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok6(self):
        # Los datos se encuentran duplicados
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test5.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok7(self):
        # No se encuentra el fin_objeto
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test6.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok8(self):
        # El fin_objeto se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test7.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok9(self):
        # No se encuentra el campo 1
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test8.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label date_signature", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok10(self):
        # El campo 1 se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test9.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok11(self):
        # No se encuentra el separador
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test10.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok12(self):
        # el separador se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test11.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok13(self):
        # No se encuentra el campo 2
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test12.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label cancelation_type", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok14(self):
        # El campo 2 se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test13.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok15(self):
        # No se encuentra el campo 3
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test14.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok16(self):
        # El campo 3 se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test15.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok17(self):
        # No se encuentra la etiqueta
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test16.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok18(self):
        # la etiqueta se encuentra duplicada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test17.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok19(self):
        # No se encuentra el separador
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel_appointment.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test18.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok20(self):
        # El separador se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test19.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok21(self):
        # No se encuentra el valor
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test20.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok22(self):
        # El valor se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test21.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok23(self):
        # No se encuentra las comillas iniciales
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test22.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok24(self):
        # Las comillas iniciales se encuentran duplicadas
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test23.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok25(self):
        # No se encuentra las comillas finales
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test24.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok26(self):
        # Las comillas finales se encuentran duplicadas
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test25.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok27(self):
        # El valor_etiqueta1 no se encuentra
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test26.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label date_signature", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok28(self):
        # El valor_etiqueta1 se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test27.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label date_signature", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok29(self):
        # El valor1 no se encuentra
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test28.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("date_signature format is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok30(self):
        # El valor1 se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test29.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("date_signature format is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok31(self):
        # El valor_etiqueta2 no se encuentra
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test30.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label cancelation_type", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok32(self):
        # El valor_etiqueta2 se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test31.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label cancelation_type", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok33(self):
        # El valor2 no se encuentra
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test32.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("cancelation_type is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok34(self):
        # El valor2 se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test33.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("cancelation_type is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok35(self):
        # El valor_etiqueta3 no se encuentra
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test34.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label reason", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok36(self):
        # El valor_etiqueta3 se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test35.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label reason", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok37(self):
        # El valor3 no se encuentra
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test36.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("reason is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok38(self):
        # El valor3 se encuentra duplicado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test37.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("reason is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok39(self):
        # La llave inicial se encuentra modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test38.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok40(self):
        # La llave final se encuentra modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test39.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok41(self):
        # El primer separador se encuentra modificado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test40.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok42(self):
        # El segundo separador se encuentra modificado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test41.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok43(self):
        # La primera igualdad se encuentra modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test42.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok44(self):
        # La segunda igualdad se encuentra modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test43.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok45(self):
        # La tercera igualdad se encuentra modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test44.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok46(self):
        # La comilla inicial de la primera etiqueta esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test45.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok47(self):
        # La comilla final de la primera etiqueta esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test46.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok48(self):
        # La comilla inicial del primer valor esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test47.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok49(self):
        # La comilla final del primer valor esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test48.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok50(self):
        # La comilla inicial de la segunda etiqueta esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test49.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok51(self):
        # La comilla final de la segunda etiqueta esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test50.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok52(self):
        # La comilla inicial del segundo valor esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test51.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok53(self):
        # La comilla final del segundo valor esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test52.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok54(self):
        # La comilla inicial de la tercera etiqueta esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test53.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok55(self):
        # La comilla final de la tercera etiqueta esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test54.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok56(self):
        # La comilla inicial del tercer valor esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test55.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok57(self):
        # La comilla final del tercer valor esta modificada
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test56.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("JSON Decode Error - Wrong JSON Format", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok58(self):
        # Valor_etiqueta1 modificado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test57.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label date_signature", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok59(self):
        # Valor1 modificado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test58.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("date_signature format is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok60(self):
        # Valor_etiqueta2 modificado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test59.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label cancelation_type", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok61(self):
        # Valor2 modificado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test60.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("cancelation_type is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok62(self):
        # Valor_etiqueta3 modificado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test61.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("Bad label reason", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_nok63(self):
        # Valor3 modificado
        # Cargamos los ficheros necesarios
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "invalid_test62.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("reason is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    # Pruebas diagrama de flujo de control
    def setup(self):
        # Para pasar dos veces por el primer for y 1 vez por el segundo y 1 vez por el tercero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()

        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("a729d963-e0dd-47d0-8bc6-b6c595ad0098",
                                          "m m", "Regular","+44333456789", "124", )

        file_test = json_files_rf4_path + "test_ok4.json"
        file_test_2 = json_files_rf2_path + "test_ok.json"
        file_test_3 = json_files_rf2_path + "test_ok_3.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)
        my_manager.cancel_appointment(file_test)

    def setup_1(self):
        # Para pasar 1 vez por el primer for 1 una vez por el segundo
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()

        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        date_signature = my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

    def setup_2(self):
        # Para pasar 2 veces por el primer for 2 veces por el segundo
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()

        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("a729d963-e0dd-47d0-8bc6-b6c595ad0098",
                                          "m m", "Regular","+44333456789", "124", )

        file_test_2 = json_files_rf2_path + "test_ok.json"
        file_test_3 = json_files_rf2_path + "test_ok_3.json"
        date_signature = my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        date_signature_2 = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)
        my_manager.vaccine_patient(date_signature_2)

    def setup_3(self):
        # Para pasar 1 vez por el primer for 0 veces por el segundo y 1 por el tercero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()

        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("a729d963-e0dd-47d0-8bc6-b6c595ad0098",
                                          "m m", "Regular", "+44333456789", "124", )

        file_test = json_files_rf4_path + "test_ok4.json"
        file_test_2 = json_files_rf2_path + "test_ok.json"
        file_test_3 = json_files_rf2_path + "test_ok_3.json"
        date_signature_2 = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature_2)
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        my_manager.cancel_appointment(file_test)

    def setup_4(self):
        # Para revisar si una cita ya ha pasado
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()

        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("a729d963-e0dd-47d0-8bc6-b6c595ad0098",
                                          "m m", "Regular","+44333456789", "124", )

        file_test_2 = json_files_rf2_path + "test_ok.json"
        file_test_3 = json_files_rf2_path + "test_ok_3.json"
        my_manager.get_vaccine_date(file_test_2, "2022-03-09")
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-03-09")
        my_manager.vaccine_patient(date_signature)

    def test_cancel_appointment_no_appointment(self):
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"


        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        my_test = MyTestCase()
        my_manager = VaccineManager()

        my_test.setup()
        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        file_test = json_files_rf4_path + "test_ok2.json"
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("el paciente no tiene citas pendientes", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_no_appointment_2(self):
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        try:
            with open(file_store_cancel, "r", encoding="utf-8", newline="") as file:
                cancel_store = json.load(file)
        except FileNotFoundError:
            cancel_store = []
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

        my_test = MyTestCase()
        my_manager = VaccineManager()

        my_test.setup_1()
        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        file_test = json_files_rf4_path + "test_ok2.json"
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("el paciente no tiene citas pendientes", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_vaccinated(self):
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        try:
            with open(file_store_cancel, "r", encoding="utf-8", newline="") as file:
                cancel_store = json.load(file)
        except FileNotFoundError:
            cancel_store = []
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

        my_test = MyTestCase()
        my_manager = VaccineManager()

        my_test.setup_1()
        file_test = json_files_rf4_path + "test_ok4.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("el paciente ya se ha vacunado", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_vaccinated_2(self):
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        try:
            with open(file_store_cancel, "r", encoding="utf-8", newline="") as file:
                cancel_store = json.load(file)
        except FileNotFoundError:
            cancel_store = []
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

        my_test = MyTestCase()
        my_manager = VaccineManager()

        my_test.setup_2()
        file_test = json_files_rf4_path + "test_ok3.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("el paciente ya se ha vacunado", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_cancel(self):
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        try:
            with open(file_store_cancel, "r", encoding="utf-8", newline="") as file:
                cancel_store = json.load(file)
        except FileNotFoundError:
            cancel_store = []
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

        my_test = MyTestCase()
        my_manager = VaccineManager()

        my_test.setup_3()
        file_test = json_files_rf4_path + "test_ok4.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("la cita ya fue cancelada anteriormente", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_date_expired(self):
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"

        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        try:
            with open(file_store_cancel, "r", encoding="utf-8", newline="") as file:
                cancel_store = json.load(file)
        except FileNotFoundError:
            cancel_store = []
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("a729d963-e0dd-47d0-8bc6-b6c595ad0098",
                                          "m m", "Regular", "+44333456789", "124", )

        file_test_2 = json_files_rf2_path + "test_ok.json"
        file_test_3 = json_files_rf2_path + "test_ok_3.json"
        my_manager.get_vaccine_date(file_test_2, "2022-03-08")
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-03-09")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "test_ok5.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("la cita ya ha pasado", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    # Test valores limite y clases de equivalencia
    def test_cancel_appointment_1(self):
        # date_signature de longitud 65
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"
        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "test_no_valido_1.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("date_signature format is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_2(self):
        # cancelation_type "Final"
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"
        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        date_signature = my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "test_valido_1.json"

        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "e7f14e852e393981d15accc497094f8d3eee80cc4b24b50fd26a7ffaf77b5655")

        with open(file_store_cancel, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)

        found = False
        for item in data_list:
            if item["_CancelAppointment__date_signature"] == value:
                found = True
        self.assertTrue(found)

    def test_cancel_appointment_3(self):
        # reason longitud 1
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"
        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "test_no_valido_2.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("reason is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_4(self):
        # reason longitud 101
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"
        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        date_signature = my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "test_no_valido_3.json"

        # Abrimos el fihcero de salida y lo guardamos en una variable
        file_store_cancel = CancelationJsonStore()
        hash_original = file_store_cancel.data_hash()

        # Comprobamos el método
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual("reason is not valid", c_m.exception.message)

        hash_new = file_store_cancel.data_hash()

        # Comparamos que no se modifico el fichero de salida
        self.assertEqual(hash_new, hash_original)

    def test_cancel_appointment_5(self):
        # reason longitud 2
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"
        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        date_signature = my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "test_valido_2.json"

        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "e7f14e852e393981d15accc497094f8d3eee80cc4b24b50fd26a7ffaf77b5655")

        with open(file_store_cancel, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)

        found = False
        for item in data_list:
            if item["_CancelAppointment__date_signature"] == value:
                found = True
        self.assertTrue(found)

    def test_cancel_appointment_6(self):
        # reason longitud 3
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/"
        json_files_rf2_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF2/"
        json_files_rf4_path = str(Path.home()) + "/PycharmProjects/G50.2022.T05B.FP/src/JsonFiles/RF4/"

        file_store_cancel = json_files_path + "store_cancel.json"
        if os.path.isfile(file_store_cancel):
            os.remove(file_store_cancel)

        file_store_patient = json_files_path + "store_patient.json"
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)

        file_store_date = json_files_path + "store_date.json"
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        file_store_vaccine = json_files_path + "store_vaccine.json"
        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Añadimos clientes en forma de setup
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax",
                                          "Family", "+34333456789", "7")

        file_test_2 = json_files_rf2_path + "test_ok.json"
        date_signature = my_manager.get_vaccine_date(file_test_2, "2022-10-14")
        file_test_3 = json_files_rf2_path + "test_ok_2.json"
        my_manager.get_vaccine_date(file_test_3, "2022-10-14")
        my_manager.vaccine_patient(date_signature)

        file_test = json_files_rf4_path + "test_valido_3.json"

        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "e7f14e852e393981d15accc497094f8d3eee80cc4b24b50fd26a7ffaf77b5655")

        with open(file_store_cancel, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)

        found = False
        for item in data_list:
            if item["_CancelAppointment__date_signature"] == value:
                found = True
        self.assertTrue(found)

if __name__ == '__main__':
    unittest.main()
