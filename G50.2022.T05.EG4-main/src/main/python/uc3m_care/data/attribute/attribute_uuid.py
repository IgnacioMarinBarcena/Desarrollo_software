import uuid
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class Uuid(Attribute):
    _ERROR_MESSAGE_UUID_INVALID = "UUID invalid"
    _ERROR_MESSAGE_UUID_IS_NOT_UUID = "Id received is not a UUID"

    def __init__(self, attr_value:str):
        self._validation_pattern = r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]" \
                                   r"{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
        self._error_message = self._ERROR_MESSAGE_UUID_INVALID
        self.__uuid_error_message = self._ERROR_MESSAGE_UUID_IS_NOT_UUID
        self._attr_value = self._validate(attr_value)

    def _validate(self,attr_value:str)->str:
        "Method for validating uuid  v4"
        try:
            uuid.UUID(attr_value)
            super()._validate(attr_value)
        except ValueError as val_er:
            raise VaccineManagementException (self.__uuid_error_message) from val_er
        return attr_value
