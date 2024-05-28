import click
from traitlets import default
from xml_parser_comp.exceptions.xml_error import XMLParseError
from xml_parser_comp.exceptions.xsd_error import XSDError
from xml_parser_comp.xml_base_validator import XMLBaseValidator
from xml_parser_comp.xml_with_xsd_validator import XMLWithXSDValidator
from xml_parser_comp.xsd_validator import XSDValidator


@click.command()
@click.option("xsd_file_path", "--xsd", type=click.Path(exists=True), help="XSD file path" , default="./tests/test.xsd")
@click.option("xml_file_path", "--xml", type=click.Path(exists=True), help="XML file path", default="./tests/test.xml")
def main(xsd_file_path: str, xml_file_path: str):

    with open(xsd_file_path, "r") as file:
        xsd_string = file.read()
    try:
        xsd = XSDValidator(xsd_string)
        xsd.validate()
        xsd_tree = xsd.generate_xsd_tree()
    except XSDError as e:
        print(f"XSD Error: {e}")
        return

    with open(xml_file_path, "r") as file:
        xml_string = file.read()
    try:
        xml = XMLBaseValidator(xml_string)
        xml.validate()
        xml_tree = xml.generate_xml_tree()
    except XMLParseError as e:
        print(f"XML Error: {e}")
        return


    try: 
        xml_with_xsd_validator = XMLWithXSDValidator(xml_tree, xsd_tree)
        xml_with_xsd_validator.validate()
    except XMLParseError as e:
        print(f"XML Error: {e}")
        return
    
    print("XML is valid according to the XSD")
    xml.print_xml_tree(xml_tree)


if __name__ == "__main__":
    main()