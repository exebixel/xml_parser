import click
from traitlets import default
from compiler.xsd_validator import XSDValidator
from compiler.exceptions.xsd_error import XSDError
from compiler.exceptions.xml_error import XMLParseError
from compiler.xml_base_validator import XMLBaseValidator
from compiler.xml_with_xsd_validator import XMLWithXSDValidator


@click.command()
@click.option("xml_file_path", "--xml", type=click.Path(exists=True), help="XML file path", required=True)
def main(xml_file_path: str):

    with open(xml_file_path, "r") as file:
        xml_string = file.read()
    try:
        xml = XMLBaseValidator(xml_string)
        xml.validate()
        xsd_file_path = xml.get_schema_location()
        xml_tree = xml.generate_xml_tree()
    except XMLParseError as e:
        print(f"XML Error: {e}")
        return

    with open(xsd_file_path, "r") as file:
        xsd_string = file.read()
    try:
        xsd = XSDValidator(xsd_string)
        xsd.validate()
        xsd_tree = xsd.generate_xsd_tree()
    except XSDError as e:
        print(f"XSD Error: {e}")
        return

    try: 
        xml_with_xsd_validator = XMLWithXSDValidator(xml_tree, xsd_tree)
        xml_with_xsd_validator.validate()
    except XMLParseError as e:
        print(f"XML Error: {e}")
        return
    
    print("XML is valid according to the XSD")