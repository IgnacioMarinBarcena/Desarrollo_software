"""Classs for the attribute Cancelation_type"""
from uc3m_care.data.attribute.attribute import Attribute

#pylint: disable=too-few-public-methods
class CancelationType(Attribute):
    """Classs for the attribute Cancelation_type"""
    _validation_pattern = r"(Temporal|Final)"
    _validation_error_message = "cancelation_type is not valid"
