from compiler.model.xml_tree import XMLTree
from compiler.exceptions.xml_error import XMLParseError
from compiler.element_type_validator import ElementTypeValidator
from compiler.model.xsd_tree import XSDElementTypeAttribute, XSDTree


class XMLWithXSDValidator:
    def __init__(self, xml_tree: XMLTree, xsd_tree: XSDTree):
        self.xml_tree: XMLTree = xml_tree
        self.xsd_tree: XSDTree = xsd_tree

    def validate(self) -> bool:
        return self.validate_tag(self.xml_tree, self.xsd_tree)

    def validate_tag(self, xml_tag: XMLTree, xsd_tag: XSDTree) -> bool:
        if xml_tag.tag != xsd_tag.name:
            raise XMLParseError(f"Tag {xml_tag.tag} is not allowed in this context")

        if xsd_tag.type is not None:
            if not ElementTypeValidator.validate_type(xml_tag.text, xsd_tag.type):
                raise XMLParseError(f"Tag {xml_tag.tag} has the wrong type")

        for xsd_attribute in xsd_tag.attributes:
            if xsd_attribute.name not in xml_tag.attributes:
                raise XMLParseError(
                    f"Tag {xml_tag.tag} has not the attribute {xsd_attribute.name}"
                )
            if not ElementTypeValidator.validate_type(
                xml_tag.attributes[xsd_attribute.name], xsd_attribute.type
            ):
                raise XMLParseError(
                    f"Tag {xml_tag.tag} has the wrong type for the attribute {xsd_attribute.name}"
                )
        else:
            if len(xml_tag.attributes) > len(xsd_tag.attributes):
                extra_attributes = list(xml_tag.attributes)[len(xsd_tag.attributes) :]
                raise XMLParseError(
                    f"XML has not this attribute: {extra_attributes[0]} in {xml_tag.tag}"
                )

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
                    f"XML has not this tags: {extra_tags[0]} in {xml_tag.tag}"
                )

        return True
