import re

from pydantic import BaseModel

from xml_parser_comp.exception import XSDError

class Tag(BaseModel):
    name: str
    attributes: dict
    is_opening_tag: bool
    is_closing_tag: bool

class XSDValidator():
    """
    Class to validate if a XSD file is valid or not
    """
    def __init__(self, xsd_string):
        self.xsd_string = xsd_string
        self.tags = self.get_all_tags()
        self.tree = self.generate_xsd_tree()

    def get_all_tags(self):
        xsd_tags = re.findall(r'<([^>]+)>', self.xsd_string)
        return xsd_tags

    def get_attributes(self, tag: str) -> list[tuple[str, str]]:
        attributes = re.findall(r'([\w:]+)="([^"]+)"', tag)
        return attributes 

    def generate_xsd_tree(self) -> list[Tag]:
        xsd_tree = []

        for tag in self.tags:
            attributes = self.get_attributes(tag)
            # make attibutes a dictionary
            attributes = dict(attributes)

            # check if the tag is an opening tag or closing tag
            is_opening_tag = True
            is_closing_tag = False
            if tag.startswith('/'):
                is_closing_tag = True
                is_opening_tag = False
            if tag.endswith('/'):
                is_closing_tag = True

            # get the name of the tag
            tag_name = tag.split(' ')[0]
            tag_name = tag_name.replace('/', '')
            
            _tag = Tag(name=tag_name, attributes=attributes, is_opening_tag=is_opening_tag, is_closing_tag=is_closing_tag)
            xsd_tree.append(_tag)

        return xsd_tree

    def check_if_all_tags_are_closed(self) -> bool:
        stack = []
        root_counter = 0
        for tag in self.tree:
            if tag.is_opening_tag:
                stack.append(tag)
                if len(stack) == 1:
                    root_counter += 1
            if tag.is_closing_tag:
                if not stack:
                    return False
                stack.pop()
        
        if stack:
            raise XSDError(f"Tag '{stack[-1].name}' is not closed")
        if root_counter > 1:
            raise XSDError("Multiple root elements found")
        return True




if __name__ == '__main__':
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
    tree = xsd_validator.generate_xsd_tree()
    for tag in tree:
        print(tag)

    print(xsd_validator.check_if_all_tags_are_closed())