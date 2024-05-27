from xml_parser_comp.exceptions.xml_error import XMLParseError
from xml_parser_comp.model.xml_tree import XMLTree
from xml_parser_comp.model.xsd_tree import XSDElementTypeAttribute, XSDTree


class XMLWithXSDValidator:
    def __init__(self, xml_tree: XMLTree, xsd_tree: XSDTree):
        self.xml_tree: XMLTree = xml_tree
        self.xsd_tree: XSDTree = xsd_tree

    def validate(self) -> bool:
        return self.validate_tag(xml_tree, xsd_tree)

    def validate_tag(self, xml_tag: XMLTree, xsd_tag: XSDTree) -> bool:
        if xml_tag.tag != xsd_tag.name:
            raise XMLParseError(f"Tag {xml_tag.tag} is not allowed in this context")

        if xsd_tag.type is not None:
            pass

        # for attribute in xml_tag.attributes:
        #     if attribute not in xsd_tag.attributes:
        #         raise XMLParseError(f"Attribute {attribute} is not allowed in this context")

        for index in range(len(xml_tag.children)):
            child = xml_tag.children[index]
            try:
                xsd_child = xsd_tag.children[index]
            except IndexError:
                raise XMLParseError(f"Tag {child.tag} is not allowed in this context")
            self.validate_tag(child, xsd_child)
        else:
            if len(xml_tag.children) < len(xsd_tag.children):
                extra_tags = xsd_tag.children[len(xml_tag.children) :]
                raise XMLParseError(
                    f"XML has not this tags: {', '.join([tag.name for tag in extra_tags])} in {xml_tag.tag}"
                )

        return True

    def validate_type(text: str, type: XSDElementTypeAttribute):
        pass


if __name__ == "__main__":
    from xml_parser_comp.xml_base_validator import XMLBaseValidator
    from xml_parser_comp.xsd_validator import XSDValidator

    xml_parser = XMLBaseValidator(
        """
    <note>
        <to>Tove</to>
        <from>Jani</from>
        <heading>Reminder</heading>
        <body>Don't forget me this weekend!</body>
    </note>
    """
    )
    xml_parser.validate()
    xsd_parser = XSDValidator(
        """
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
    )

    xml_tree = xml_parser.generate_xml_tree()
    xsd_tree = xsd_parser.generate_xsd_tree()

    xml_with_xsd_validator = XMLWithXSDValidator(xml_tree, xsd_tree)
    xml_with_xsd_validator.validate_tag(xml_tree, xsd_tree)
    print("XML is valid")
    xml_parser.print_xml_tree(xml_tree)
