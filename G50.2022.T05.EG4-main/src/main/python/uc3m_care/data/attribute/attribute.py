import re
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class Attribute():
    def __init__(self):
        self._attr_value = ""
        self._validation_pattern = r""
        self._error_message = ""

    def _validate(self, attr_value:str) -> str:
        if not isinstance(attr_value, str):
            raise VaccineManagementException(self._error_message)
        if not re.fullmatch(self._validation_pattern, attr_value):
            raise VaccineManagementException(self._error_message)
        return attr_value

    @property
    def value(self):
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = attr_value
