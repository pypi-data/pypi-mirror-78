"""Convert JSON Schema to Markdown documentation."""


import json
from typing import Dict, Optional, Sequence

import click


class Parser:
    """
    JSON Schema to Markdown parser.

    Examples
    --------
    >>> parser = Parser()
    >>> md_lines = parser.parse_schema(json.load(input_json))
    """

    tab_size = 2

    def _construct_description_line(self, obj: Dict) -> Sequence[str]:
        """Construct description line of property or definition."""
        description_line = [": "]

        if "description" in obj:
            ending = "" if obj["description"].endswith(".") else "."
            description_line.append(f"{obj['description']}{ending}")
        if "enum" in obj:
            description_line.append(f"Must be one of: `{obj['enum']}`.")
        if "additionalProperties" in obj:
            if obj["additionalProperties"]:
                description_line.append("Can contain additional properties.")
            else:
                description_line.append("Cannot contain additional properties.")
        if "$ref" in obj:
            description_line.append(f"Refer to *{obj['$ref']}*.")
        if "default" in obj:
            description_line.append(f"Default: `{obj['default']}`.")
        if "items" in obj:
            # Add description for items recursively
            description_line.append(
                "Items" + " ".join(self._construct_description_line(obj["items"]))
            )

        return description_line

    def _parse_definitions(
        self,
        obj,
        output_lines=None,
        indent_level: int = 0,
        add_title: bool = True
    ) -> Sequence[str]:
        """Parse JSON object definitions recursively."""
        if not output_lines:
            output_lines = []

        if add_title:
            indentation = " " * self.tab_size * indent_level
            output_lines.append(f"{indentation}- Definitions:\n")

        for def_name, def_obj in obj.items():
            output_lines = self._parse_object(
                def_obj,
                def_name,
                output_lines=output_lines,
                indent_level=indent_level + 1 if add_title else indent_level,
            )

        return output_lines

    def _parse_object(
        self,
        obj: Dict,
        name: str,
        output_lines: Optional[str] = None,
        indent_level: int = 0,
    ) -> Sequence[str]:
        """Parse JSON object and its properties recursively."""
        if not isinstance(obj, dict):
            raise TypeError(
                f"Non-object type found in properties list: `{name}: {obj}`."
            )

        if not output_lines:
            output_lines = []

        # Construct full description line
        description_line = self._construct_description_line(obj)

        # Add full line to output
        description_line = " ".join(description_line)
        indentation = " " * self.tab_size * indent_level
        obj_type = f" *({obj['type']})*" if "type" in obj else ""
        output_lines.append(
            f"{indentation}- **`{name}`**{obj_type}{description_line}\n"
        )

        # Recursively add definitions
        if "definitions" in obj:
            output_lines = self._parse_definitions(
                obj["definitions"],
                output_lines=output_lines,
                indent_level=indent_level + 1,
            )

        # Recursively add child properties
        if "properties" in obj:
            for property_name, property_obj in obj["properties"].items():
                output_lines = self._parse_object(
                    property_obj,
                    property_name,
                    output_lines=output_lines,
                    indent_level=indent_level + 1,
                )

        return output_lines

    def parse_schema(self, schema_object: Dict) -> Sequence[str]:
        """Parse JSON Schema object to markdown text."""
        output_lines = []

        if "title" in schema_object:
            output_lines.append(f"# {schema_object['title']}\n\n")
        else:
            output_lines.append("JSON Schema\n\n")
        if "description" in schema_object:
            output_lines.append(f"*{schema_object['description']}*\n\n")

        output_lines.append("## Properties\n\n")
        for property_name, property_obj in schema_object["properties"].items():
            output_lines.extend(self._parse_object(property_obj, property_name))

        output_lines.append("## Definitions\n\n")
        if "definitions" in schema_object:
            output_lines.extend(self._parse_definitions(
                schema_object["definitions"],
                add_title=False
            ))

        return output_lines


@click.command()
@click.argument("input-json", type=click.File("rt"))
@click.argument("output-markdown", type=click.File("wt"))
def main(input_json, output_markdown):
    """Command line interface."""
    parser = Parser()
    output_markdown.writelines(parser.parse_schema(json.load(input_json)))


if __name__ == "__main__":
    main()
