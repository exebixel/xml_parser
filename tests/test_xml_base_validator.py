import unittest

from xml_parser_comp.exceptions.xml_error import XMLParseError
from xml_parser_comp.model.xml_token import XMLToken
from xml_parser_comp.xml_base_validator import XMLBaseValidator


class TestXMLBaseValidator(unittest.TestCase):

    def test_parse_tag(self):
        xml_string = """
        <note>
            <to>Tove</to>
            <from>Jani</from>
            <heading>Reminder</heading>
            <body>Don't forget me this weekend!</body>
        </note>
        """
        xml_validator = XMLBaseValidator(xml_string)
        self.assertEqual(
            xml_validator.parse_tag(),
            [
                XMLToken(
                    type="Tag",
                    is_opening_tag=True,
                    is_closing_tag=False,
                    tag_name="note",
                    text=None,
                ),
                XMLToken(
                    type="Tag",
                    is_opening_tag=True,
                    is_closing_tag=False,
                    tag_name="to",
                    text=None,
                ),
                XMLToken(
                    type="Text",
                    is_opening_tag=False,
                    is_closing_tag=False,
                    tag_name=None,
                    text="Tove",
                ),
                XMLToken(
                    type="Tag",
                    is_opening_tag=False,
                    is_closing_tag=True,
                    tag_name="to",
                    text=None,
                ),
                XMLToken(
                    type="Tag",
                    is_opening_tag=True,
                    is_closing_tag=False,
                    tag_name="from",
                    text=None,
                ),
                XMLToken(
                    type="Text",
                    is_opening_tag=False,
                    is_closing_tag=False,
                    tag_name=None,
                    text="Jani",
                ),
                XMLToken(
                    type="Tag",
                    is_opening_tag=False,
                    is_closing_tag=True,
                    tag_name="from",
                    text=None,
                ),
                XMLToken(
                    type="Tag",
                    is_opening_tag=True,
                    is_closing_tag=False,
                    tag_name="heading",
                    text=None,
                ),
                XMLToken(
                    type="Text",
                    is_opening_tag=False,
                    is_closing_tag=False,
                    tag_name=None,
                    text="Reminder",
                ),
                XMLToken(
                    type="Tag",
                    is_opening_tag=False,
                    is_closing_tag=True,
                    tag_name="heading",
                    text=None,
                ),
                XMLToken(
                    type="Tag",
                    is_opening_tag=True,
                    is_closing_tag=False,
                    tag_name="body",
                    text=None,
                ),
                XMLToken(
                    type="Text",
                    is_opening_tag=False,
                    is_closing_tag=False,
                    tag_name=None,
                    text="Don't forget me this weekend!",
                ),
                XMLToken(
                    type="Tag",
                    is_opening_tag=False,
                    is_closing_tag=True,
                    tag_name="body",
                    text=None,
                ),
                XMLToken(
                    type="Tag",
                    is_opening_tag=False,
                    is_closing_tag=True,
                    tag_name="note",
                    text=None,
                ),
            ],
        )


    def test_check_if_all_tags_are_closed_with_exception(self):
        xml_string = """
        <note>
            <to>Tove</to>
            <from>Jani</from>
            <heading>Reminder</heading>
            <body>Don't forget me this weekend!</body>
        </note>
        """
        xml_validator = XMLBaseValidator(xml_string)
        xml_validator.parse_tag()
        self.assertTrue(xml_validator.check_if_all_tags_are_closed())

        xml_string = """
        <note>
            <to>Tove</to>
            <from>Jani</from>
            <heading>Reminder</heading>
            <body>Don't forget me this weekend!
        </note>
        """
        xml_validator = XMLBaseValidator(xml_string)
        with self.assertRaises(XMLParseError):
            xml_validator.check_if_all_tags_are_closed()

    def test_check_if_all_tags_are_closed(self):
        xml_string = """
        <note>
            <to>Tove</to>
            <from>Jani</from>
            <heading>Reminder</heading>
            <body>Don't forget me this weekend!</body>
        </note>
        """
        xml_validator = XMLBaseValidator(xml_string)
        xml_validator.parse_tag()
        self.assertTrue(xml_validator.check_if_all_tags_are_closed())

    
    def test_check_if_all_tags_are_closed_with_exception_1(self):
        xml_string = """
        <note>
            <to>Tove</to>
            <from>Jani</from>
            <heading>Reminder</heading>
            <body>Don't forget me this weekend!</body>
        </note>
        <error>
        </error>
        """
        xml_validator = XMLBaseValidator(xml_string)
        with self.assertRaises(XMLParseError):
            xml_validator.check_if_all_tags_are_closed()

    def test_check_if_all_tags_are_closed_exception_2(self):
        xml_string = """
        <note>
            </error>
            <to>Tove</to>
            <from>Jani</from>
            <heading>Reminder</heading>
            <body>Don't forget me this weekend!</body>
        <note>
        """
        xml_validator = XMLBaseValidator(xml_string)
        with self.assertRaises(XMLParseError):
            xml_validator.check_if_all_tags_are_closed()