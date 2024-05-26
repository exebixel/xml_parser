import re

from xml_parser_comp.exceptions.xml_error import XMLParseError
from xml_parser_comp.model.xml_token import XMLToken


class XMLBaseValidator:
    def __init__(self, xml_string: str):
        self.xml_string: str = xml_string
        self.xml_tokens: list[XMLToken] = self.parse_tag()

    def parse_tag(self) -> list[XMLToken]:
        matches = re.findall(r"<(/?)([^>]+)>|([^<]+)", self.xml_string)
        result = []
        for match in matches:
            if match[0] or match[1]:  # This is a tag
                is_opening_tag = match[0] == ""
                is_closing_tag = match[0] == "/"
                tag_name = match[1]
                result.append(
                    XMLToken(
                        type="Tag",
                        is_opening_tag=is_opening_tag,
                        is_closing_tag=is_closing_tag,
                        tag_name=tag_name,
                        text=None,
                    )
                )
            else:  # This is text
                if match[2].strip().replace("\n", "") == "":
                    continue

                result.append(
                    XMLToken(
                        type="Text",
                        is_opening_tag=False,
                        is_closing_tag=False,
                        tag_name=None,
                        text=match[2],
                    )
                )
        return result

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
            raise XMLParseError(f"Tag '{stack[-1].name}' is not closed")
        if root_counter != 1:
            raise XMLParseError("There should be only one root element")
        return True

    def validate(self):
        self.parse_tag()
        self.check_if_all_tags_are_closed()


if __name__ == "__main__":
    xml_string = """
    <note>
        <to>Tove</to>
        <from>Jani</from>
        <heading>Reminder</heading>
        <body>Don't forget me this weekend!</body>
    </note>
    """
    xml_validator = XMLBaseValidator(xml_string)

    for tag in xml_validator.parse_tag():
        print(tag)
