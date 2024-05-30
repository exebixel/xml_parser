import unittest

from xml_parser_comp.exceptions.xsd_error import XSDError
from xml_parser_comp.model.xsd_tree import XSDAttribute, XSDTree
from xml_parser_comp.xsd_validator import XSDValidator


class TestXSDGenerateTree(unittest.TestCase):

    def test_generate_xsd_tree(self):
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
        xsd_tree = xsd_validator.generate_xsd_tree()
        self.assertEqual(
            xsd_tree,
            XSDTree(
                name="note",
                type="xs:sequence",
                children=[
                    XSDTree(name="to", type="xs:string"),
                    XSDTree(name="from", type="xs:string"),
                    XSDTree(name="heading", type="xs:string"),
                    XSDTree(name="body", type="xs:string"),
                ],
            ),
        )

    def test_multi_complex_type(self):
        xsd_string = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="note">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="to" type="xs:string"/>
                        <xs:element name="from" type="xs:string"/>
                        <xs:element name="heading">
                            <xs:complexType>
                                <xs:sequence>
                                    <xs:element name="magia" type="xs:string"/>
                                </xs:sequence>
                                <xs:attribute name="valor" type="xs:string"/>
                            </xs:complexType>
                        </xs:element>
                        <xs:element name="body">
                            <xs:complexType>
                                <xs:sequence>
                                    <xs:element name="magia" type="xs:string"/>
                                </xs:sequence>
                                <xs:attribute name="valor" type="xs:string"/>
                            </xs:complexType>
                        </xs:element>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
        </xs:schema>
        """
        xsd_validator = XSDValidator(xsd_string)
        xsd_tree = xsd_validator.generate_xsd_tree()
        self.assertEqual(
            xsd_tree,
            XSDTree(
                name="note",
                type="xs:sequence",
                children=[
                    XSDTree(name="to", type="xs:string"),
                    XSDTree(name="from", type="xs:string"),
                    XSDTree(
                        name="heading",
                        type="xs:sequence",
                        children=[
                            XSDTree(name="magia", type="xs:string"),
                        ],
                        attributes=[
                            XSDAttribute(name="valor", type="xs:string"),
                        ],
                    ),
                    XSDTree(
                        name="body",
                        type="xs:sequence",
                        children=[
                            XSDTree(name="magia", type="xs:string"),
                        ],
                        attributes=[
                            XSDAttribute(name="valor", type="xs:string"),
                        ],
                    ),
                ],
            ),
        )
