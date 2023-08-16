"""Classs for the attribute Reason"""
from uc3m_care.data.attribute.attribute import Attribute

#pylint: disable=too-few-public-methods
class Reason(Attribute):
    """Classs for the attribute Reason"""
    _validation_pattern = r"^(?=^.{2,100}$)(([a-zA-Z0-9]+\s{0,1})+[a-zA-Z0-9]+)$"
    _validation_error_message = "reason is not valid"
