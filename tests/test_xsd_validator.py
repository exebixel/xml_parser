import unittest


from xml_parser_comp.xsd_validator import XSDValidator
from xml_parser_comp.exception import XSDError


class TestXSDValidator(unittest.TestCase):

    def test_get_all_tags(self):
        xsd_string = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="note">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="to" type="xs:string"/>
                        <xs:element name="from" type="xs:string"/>
                        <xs:element name="heading" type="xs:string"/>
                        <xs:element name="body" type="xs:string"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
        </xs:schema>
        """
        xsd_validator = XSDValidator(xsd_string)
        self.assertEqual(
            xsd_validator.tags,
            [
                'xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"',
                'xs:element name="note"',
                "xs:complexType",
                "xs:sequence",
                'xs:element name="to" type="xs:string"/',
                'xs:element name="from" type="xs:string"/',
                'xs:element name="heading" type="xs:string"/',
                'xs:element name="body" type="xs:string"/',
                '/xs:sequence',
                '/xs:complexType',
                '/xs:element',
                '/xs:schema'
            ],
        )

    def test_check_if_all_tags_are_closed(self):
        xsd_string = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="note">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="to" type="xs:string"/>
                        <xs:element name="from" type="xs:string"/>
                        <xs:element name="heading" type="xs:string"/>
                        <xs:element name="body" type="xs:string"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
        </xs:schema>
        """
        xsd_validator = XSDValidator(xsd_string)
        self.assertTrue(xsd_validator.check_if_all_tags_are_closed())

    def test_check_if_all_tags_are_closed_with_error(self):
        xsd_string = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="note">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="to" type="xs:string"/>
                        <xs:element name="from" type="xs:string"/>
                        <xs:element name="heading" type="xs:string"/>
                        <xs:element name="body" type="xs:string"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
        </xs:schema
        """
        xsd_validator = XSDValidator(xsd_string)
        with self.assertRaises(XSDError) as context:
            xsd_validator.check_if_all_tags_are_closed()
        self.assertEqual(str(context.exception), "Tag 'xs:schema' is not closed")

    def test_check_if_tags_is_allowed(self):
        xsd_string = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="note">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="to" type="xs:string"/>
                        <xs:element name="from" type="xs:string"/>
                        <xs:element name="heading" type="xs:string"/>
                        <xs:element name="body" type="xs:string"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
        </xs:schema>
        """
        xsd_validator = XSDValidator(xsd_string)
        self.assertTrue(xsd_validator.check_if_tags_is_allowed())

    def test_check_if_tags_is_allowed_with_error(self):
        xsd_string = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="note">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="to" type="xs:string"/>
                        <xs:element name="from" type="xs:string"/>
                        <xs:element name="heading" type="xs:string"/>
                        <xs:element name="body" type="xs:string"/>
                        <xs:element name="error" type="xs:string"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
            <erro></erro>
        </xs:schema>
        """
        xsd_validator = XSDValidator(xsd_string)
        with self.assertRaises(XSDError) as context:
            xsd_validator.check_if_tags_is_allowed()
        self.assertEqual(str(context.exception), "TagName erro is not allowed")

    def test_check_if_attributes_is_allowed(self):
        xsd_string = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="note">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="to" type="xs:string"/>
                        <xs:element name="from" type="xs:string"/>
                        <xs:element name="heading" type="xs:string"/>
                        <xs:element name="body" type="xs:string"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
        </xs:schema>
        """
        xsd_validator = XSDValidator(xsd_string)
        self.assertTrue(xsd_validator.check_if_attributes_is_allowed())

    def test_check_if_attributes_is_allowed_with_error(self):
        xsd_string = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="note">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="to" type="xs:string"/>
                        <xs:element name="from" type="xs:string"/>
                        <xs:element name="heading" type="xs:string"/>
                        <xs:element name="body" type="xs:string" error="true"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
        </xs:schema>
        """
        xsd_validator = XSDValidator(xsd_string)
        with self.assertRaises(XSDError) as context:
            xsd_validator.check_if_attributes_is_allowed()
        self.assertEqual(str(context.exception), "Attribute error is not allowed")

    def test_check_if_attributes_is_allowed_with_error_2(self):
        xsd_string = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="note">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="to" type="xs:string" error="true"/>
                        <xs:element name="from" type="xs:string"/>
                        <xs:element name="heading" type="xs:string"/>
                        <xs:element name="body" type="xs:string"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
        </xs:schema>
        """
        xsd_validator = XSDValidator(xsd_string)
        with self.assertRaises(XSDError) as context:
            xsd_validator.check_if_attributes_is_allowed()
        self.assertEqual(str(context.exception), "Attribute error is not allowed")

    def test_check_if_attributes_is_allowed_with_error_3(self):
        xsd_string = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="note">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="to" type="xs:string"/>
                        <xs:element name="from" type="xs:string"/>
                        <xs:element name="heading" type="xs:string"/>
                        <xs:element name="body" type="xs:string"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
            <xs:element name="error" type="xs:string" error="true"/>
        </xs:schema>
        """
        xsd_validator = XSDValidator(xsd_string)
        with self.assertRaises(XSDError) as context:
            xsd_validator.check_if_attributes_is_allowed()
        self.assertEqual(str(context.exception), "Attribute error is not allowed")
