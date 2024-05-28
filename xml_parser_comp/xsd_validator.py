import re


from xml_parser_comp.exceptions.xsd_error import XSDError
from xml_parser_comp.model.xsd_token import XSDToken
from xml_parser_comp.model.xsd_tree import (
    XSDAttribute,
    XSDElementTypeAttribute,
    XSDTree,
)


class XSDValidator:
    """
    Class to validate if a XSD file is valid or not
    """

    def __init__(self, xsd_string):
        self.tags_atributes_allowed = {
            "xs:sequence": [],
            "xs:complexType": [],
            "xs:element": ["name", "type"],
            "xs:schema": ["xmlns:xs"],
            "xs:attribute": ["name", "type"],
        }
        self.xsd_string = xsd_string
        self.tags = self.get_all_tags()
        self.tokens: list[XSDToken] = self.generate_xsd_tokens()

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

    def generate_xsd_tokens(self) -> list[XSDToken]:
        xsd_tree = []

        for tag in self.tags:
            attributes = self.get_attributes(tag)
            # make attibutes a dictionary
            attributes = dict(attributes)

            # check if the tag is an opening tag or closing tag
            is_opening_tag = True
            is_closing_tag = False
            if tag.startswith("/"):
                is_closing_tag = True
                is_opening_tag = False
            if tag.endswith("/"):
                is_closing_tag = True

            # get the name of the tag
            tag_name = tag.split(" ")[0]
            tag_name = tag_name.replace("/", "")

            _tag = XSDToken(
                name=tag_name,
                attributes=attributes,
                is_opening_tag=is_opening_tag,
                is_closing_tag=is_closing_tag,
            )
            xsd_tree.append(_tag)

        return xsd_tree

    def check_if_all_tags_are_closed(self) -> bool:
        stack = []
        root_counter = 0
        for tag in self.tokens:
            if tag.is_opening_tag:
                stack.append(tag)
                if len(stack) == 1:
                    if tag.name != "xs:schema":
                        raise XSDError(message=f"The first tag should be a xs:schema")
                    root_counter += 1
            if tag.is_closing_tag:
                if not stack:
                    return False
                if tag.name != stack[-1].name:
                    raise XSDError(message=f"{stack[-1].name} is not closed")
                stack.pop()

        if stack:
            raise XSDError(f"Tag '{stack[-1].name}' is not closed")
        if root_counter > 1:
            raise XSDError("Multiple root elements found")
        return True

    def check_if_tags_is_allowed(self):
        for tag in self.tokens:
            if tag.name not in self.tags_atributes_allowed:
                raise XSDError(message=f"TagName {tag.name} is not allowed")
        return True

    def check_if_attributes_is_allowed(self):
        for tag in self.tokens:
            for attribute in tag.attributes:
                if attribute not in self.tags_atributes_allowed[tag.name]:
                    raise XSDError(message=f"Attribute {attribute} is not allowed")
                if tag.is_opening_tag is False:
                    raise XSDError(message=f"the closing tag cannot contain attributes")
        return True

    def validate(self):
        self.check_if_all_tags_are_closed()
        self.check_if_tags_is_allowed()
        self.check_if_attributes_is_allowed()

    def generate_xsd_tree(self):
        xsd_tree: XSDTree = None
        stack = []
        for token in self.tokens:
            if token.is_opening_tag:

                if token.name == "xs:complexType":
                    stack.append(None)

                elif token.name == "xs:sequence" and stack[-1] is None:
                    if stack[-2].type is not None:
                        raise XSDError("complexElement should not have a type")
                    stack[-2].type = XSDElementTypeAttribute.SEQUENCE

                elif token.name == "xs:sequence" and stack[-1] is not None:
                    raise XSDError("xs:sequence should be a child of xs:complexType")

                elif token.name == "xs:attribute" and stack[-1] is None:
                    attribute = XSDAttribute(
                        name=token.attributes.get("name"),
                        type=token.attributes.get("type"),
                    )
                    stack[-2].attributes.append(attribute)

                elif token.name == "xs:attribute" and stack[-1] is not None:
                    raise XSDError("xs:attribute should be a child of xs:complexType")

                elif token.name == "xs:element":
                    tag = XSDTree(
                        name=token.attributes.get("name"),
                        type=token.attributes.get("type"),
                    )
                    if not stack:
                        xsd_tree = tag
                        stack.append(tag)
                    elif stack[-1] is None:
                        stack[-2].children.append(tag)
                        stack.append(tag)
                    else:
                        stack[-1].children.append(tag)
                        stack.append(tag)

            if token.name == "xs:element" and token.is_closing_tag:
                stack.pop()
            if token.name == "xs:complexType" and token.is_closing_tag:
                stack.pop()

        return xsd_tree


if __name__ == "__main__":
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
    xsd_validator.validate()

    tree = xsd_validator.generate_xsd_tree()
    print(tree)
    for child in tree.children:
        print("  ", child)
        for sub_child in child.children:
            print("    ", sub_child)
    # tree = xsd_validator.generate_xsd_tree()
    # for tag in tree:
    #     print(tag)

    # print(xsd_validator.check_if_all_tags_are_closed())
    # print(xsd_validator.check_if_attributes_is_allowed())
    # print(xsd_validator.check_if_tags_is_allowed())
