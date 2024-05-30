from xml_parser_comp.exceptions.xsd_error import XSDError
from xml_parser_comp.model.xml_tree import XMLTree
from xml_parser_comp.model.xsd_tree import XSDTree
from xml_parser_comp.xml_base_validator import XMLBaseValidator
from xml_parser_comp.xsd_validator import XSDValidator


class Main:

    def __init__(self, xsd_tree, xml_tree) -> None:
        self.xsd_tree = xsd_tree
        self.xml_tree = xml_tree

    def initialize_xsd_tree(self) -> XSDTree:
        xsd_validator = XSDValidator(xsd_string)
        xsd_validator.check_if_all_tags_are_closed()
        xsd_validator.check_if_attributes_is_allowed()
        xsd_validator.check_if_tags_is_allowed()
        return xsd_validator.generate_xsd_token()
    
    def initialize_xml_tree(self) -> XMLTree:
        xml_validator = XMLBaseValidator(xml_string)
        xml_validator.validate()
        xml_tree = xml_validator.generate_xml_tree()
        return xml_tree
    
def check_xml_and_xsd_tags(xsd_list: list[XSDTree], xml: XMLTree) -> bool:
    for xsd in xsd_list:
        if xsd.tag == xml.tag:
            return True
    return False

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
    xml_string = """
    <note>
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
    main_validator = Main(xsd_tree=xsd_string, xml_tree=xml_string)
    xsd_tree = main_validator.initialize_xsd_tree()
    xml_tree = main_validator.initialize_xml_tree()
    if xsd_tree.tag == "note" and xml_tree.tag == "note":
        xsd_tree_children = xsd_tree.children
        xml_tree_children = xml_tree.children
        for xml in xml_tree_children: # verifica se o xml tem uma tag a mais ou a qual não está contida no xsd.
            if check_xml_and_xsd_tags(xsd_tree_children, xml) is False:
                raise XSDError(message="XML is invalid")
        for index in range(0, len(xsd_tree_children)):
            indexes_of_pass_items = []
            first_index_of_current_item = None
            current_item = xsd_tree_children[index].tag
            for i, xml in enumerate(xml_tree_children):
                if xml.tag != current_item:
                    indexes_of_pass_items.append(i)
                else:
                    first_index_of_current_item = i;
                    break   
            print(indexes_of_pass_items)
            print(first_index_of_current_item)
            for i in indexes_of_pass_items:
                if i >= first_index_of_current_item:
                    raise XSDError(message="invalid xml structure")
                
    else:
        raise XSDError(message="Tag note not found")


