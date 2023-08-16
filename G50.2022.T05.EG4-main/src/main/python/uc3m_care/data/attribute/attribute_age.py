from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class Age(Attribute):
    _ERROR_MESSAGE_AGE = "age is not valid"
    def __init__(self, attr_value:str):
        self._error_message = self._ERROR_MESSAGE_AGE
        self._attr_value = self._validate(attr_value)

    def _validate(self,age:str)->str:
        "Method for validating age"
        if age.isnumeric():
            if (int(age) < 6 or int(age) > 125):
                raise VaccineManagementException(self._error_message)
        else:
            raise VaccineManagementException(self._error_message)
        return age
