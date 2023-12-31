from uc3m_care.data.attribute.attribute import Attribute

class PatientSystemID(Attribute):
    def __init__(self, attr_value:str):
        self._validation_pattern = r"[0-9a-fA-F]{32}$"
        self._error_message = "patient system id is not valid"
        self._attr_value = self._validate(attr_value)
