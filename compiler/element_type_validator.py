
from datetime import datetime

from compiler.model.xsd_tree import XSDElementTypeAttribute


class ElementTypeValidator():

    def __init__(self) -> None:
        raise NotImplementedError("This class is not meant to be instantiated")

    @staticmethod
    def validate_string(text: str) -> bool:
        return str(text).strip() != ""

    @staticmethod
    def validate_int(text: str) -> bool:
        try:
            int(text)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_float(text: str) -> bool:
        try:
            float(text)
            return True
        except ValueError:
            return False
        
    @staticmethod
    def validate_boolean(text: str) -> bool:
        return text.lower() in ['true', 'false', '0', '1']

    @staticmethod
    def validate_date(text: str) -> bool:
        try:
            datetime.strptime(text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_time(text: str) -> bool:
        try:
            datetime.strptime(text, '%H:%M:%S')
            return True
        except ValueError:
            return False
        
    @staticmethod
    def validate_type(text: str, type: XSDElementTypeAttribute) -> bool:
        if type == XSDElementTypeAttribute.STRING:
            return ElementTypeValidator.validate_string(text)
        elif type == XSDElementTypeAttribute.INTEGER:
            return ElementTypeValidator.validate_int(text)
        elif type == XSDElementTypeAttribute.DECIMAL:
            return ElementTypeValidator.validate_float(text)
        elif type == XSDElementTypeAttribute.BOLLEAN:
            return ElementTypeValidator.validate_boolean(text)
        elif type == XSDElementTypeAttribute.DATE:
            return ElementTypeValidator.validate_date(text)
        elif type == XSDElementTypeAttribute.TIME:
            return ElementTypeValidator.validate_time(text)
        elif type == XSDElementTypeAttribute.SEQUENCE:
            return True
        else:
            return False