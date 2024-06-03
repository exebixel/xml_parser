import re

from xml_parser_comp.exceptions.xml_error import XMLParseError
from xml_parser_comp.model.xml_token import XMLToken
from xml_parser_comp.model.xml_tree import XMLTree


class XMLBaseValidator:
    def __init__(self, xml_string: str):
        self.xml_string: str = xml_string
        self.xml_tokens: list[XMLToken] = []
        self.__path_to_schema: str = None

    def generate_tokens(self) -> list[XMLToken]:
        matches = re.findall(r"<(/?)([^>]+)>|([^<]+)", self.xml_string)
        result = []
        for match in matches:
            if match[0] or match[1]:  # This is a tag
                is_opening_tag = match[0] == ""
                is_closing_tag = match[0] == "/"
                tag = match[1]
                attributes = self.get_attributes(tag)
                tag_name = tag.split(" ")[0]
                result.append(
                    XMLToken(
                        type="Tag",
                        is_opening_tag=is_opening_tag,
                        is_closing_tag=is_closing_tag,
                        tag_name=tag_name,
                        text=None,
                        attributes=dict(attributes),
                    )
                )
            else:  # This is text
                text = match[2].strip().replace("\n", "")
                if text == "":
                    continue

                result.append(
                    XMLToken(
                        type="Text",
                        is_opening_tag=False,
                        is_closing_tag=False,
                        tag_name=None,
                        text=text,
                    )
                )
        return result

    def get_all_tags(self):
        xsd_tags = []
        xsd_tags_init: list[str] = re.findall(r"<([^>]+)>", self.xsd_string)
        for tag in xsd_tags_init:
            if tag.startswith("!-") is False:
                xsd_tags.append(tag)
        return xsd_tags

    def get_attributes(self, tag: str) -> list[tuple[str, str]]:
        attributes = re.findall(r'([\w:]+)="([^"]+)"', tag)
        return attributes

    def check_if_all_tags_are_closed(self) -> bool:
        stack: list[XMLToken] = []
        root_counter = 0
        for tag in self.xml_tokens:
            if tag.is_opening_tag:
                stack.append(tag)
                if len(stack) == 1:
                    root_counter += 1
            if tag.is_closing_tag:
                if not stack:
                    raise XMLParseError(f"Tag '{tag.tag_name}' is not opened")
                if tag.tag_name != stack[-1].tag_name:
                    raise XMLParseError(f"{stack[-1].tag_name} is not closed")
                stack.pop()

        if stack:
            raise XMLParseError(f"Tag '{stack[-1].tag_name}' is not closed")
        if root_counter != 1:
            raise XMLParseError("There should be only one root element")
        return True

    def check_first_tags(self):
        if self.xml_tokens[0].tag_name != "?xml" and self.xml_tokens[
            0
        ].attributes not in ["version"]:
            raise XMLParseError("First tag should be <?xml version='1.0'?>")
        if self.xml_tokens[0].attributes.get("version") != "1.0":
            raise XMLParseError("XML Version should be 1.0")
        self.xml_tokens = self.xml_tokens[1:]

        for attribute in self.xml_tokens[0].attributes.keys():
            if attribute in ["xsi:schemaLocation", "xsi:noNamespaceSchemaLocation"]:
                break
        else:
            raise XMLParseError("Root tag should have the schema location")

        return True

    def validate(self):
        self.xml_tokens = self.generate_tokens()
        self.check_first_tags()
        self.__path_to_schema = self.validate_schema_location()
        self.check_if_all_tags_are_closed()

    def validate_schema_location(self) -> str:
        if not self.xml_tokens:
            raise XMLParseError("There are no tokens to validate")
        if self.__path_to_schema:
            return self.__path_to_schema

        token = self.xml_tokens[0]
        if "xsi:schemaLocation" in token.attributes.keys():
            if len(token.attributes.get("xsi:schemaLocation").split(" ")) == 2:
                schema_path = token.attributes.get("xsi:schemaLocation").split(" ")[1]
                token.attributes.pop("xsi:schemaLocation", None)
                token.attributes.pop("xmlns", None)
                token.attributes.pop("xmlns:xsi", None)
                token.attributes.pop("xsi:noNamespaceSchemaLocation", None)
                return schema_path
            raise XMLParseError("Schema location should have two values")

        if "xsi:noNamespaceSchemaLocation" in token.attributes.keys():
            schema_path = token.attributes.get("xsi:noNamespaceSchemaLocation")
            token.attributes.pop("xsi:schemaLocation", None)
            token.attributes.pop("xmlns", None)
            token.attributes.pop("xmlns:xsi", None)
            token.attributes.pop("xsi:noNamespaceSchemaLocation", None)
            return schema_path

        raise XMLParseError("Root tag should be the schema location")

    def get_schema_location(self) -> str:
        if not self.__path_to_schema:
            raise XMLParseError("Schema location was not validated")
        return self.__path_to_schema

    def generate_xml_tree(self):
        stack = []
        xml_tree = None
        for token in self.xml_tokens:
            if token.is_opening_tag:
                if not stack:
                    xml_tree = XMLTree(tag=token.tag_name, attributes=token.attributes)
                    stack.append(xml_tree)
                else:
                    tag = XMLTree(tag=token.tag_name, attributes=token.attributes)
                    stack[-1].children.append(tag)
                    stack.append(tag)
            elif token.is_closing_tag:
                stack.pop()
            else:
                stack[-1].text = (
                    stack[-1].text + " " + token.text if stack[-1].text else token.text
                )

        return xml_tree

    def print_xml_tree(self, xml_tree: XMLTree, level=0):
        print("  " * level, f"Tag: {xml_tree.tag}", end="")
        print(
            f", Attributes: {xml_tree.attributes}" if xml_tree.attributes else "",
            end="",
        )
        print(f", Text: {xml_tree.text}" if xml_tree.text else "")
        for child in xml_tree.children:
            self.print_xml_tree(child, level + 1)


if __name__ == "__main__":
    xml_string = """
    <?xml version="1.0"?>
    <note xsi:schemaLocation="www.test.com test.xsd">
        <to>Tove</to>
        <from>Jani</from>
        <from>Jani</from>
        <heading>Reminder</heading>
        <body>Don't forget me this weekend!
            <magia>hola</magia>
            Haha
        </body>
    </note>
    """
    xml_validator = XMLBaseValidator(xml_string)
    xml_validator.xml_tokens = xml_validator.generate_tokens()
    xml_validator.check_first_tags()
    print(xml_validator.validate_schema_location())
    # xml_validator.validate()

    # xml_tree = xml_validator.generate_xml_tree()
    # xml_validator.print_xml_tree(xml_tree)
