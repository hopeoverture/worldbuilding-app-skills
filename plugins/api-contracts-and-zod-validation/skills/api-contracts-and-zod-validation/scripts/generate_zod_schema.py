#!/usr/bin/env python3
"""
Generate Zod schemas from TypeScript interfaces/types.

Usage:
    python generate_zod_schema.py --input types/entities.ts --output schemas/entities.ts
    python generate_zod_schema.py --input-string "interface User { name: string; age: number; }"
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TypeScriptToZodConverter:
    """Convert TypeScript types to Zod schemas."""

    # Type mappings from TS to Zod
    TYPE_MAP = {
        'string': 'z.string()',
        'number': 'z.number()',
        'boolean': 'z.boolean()',
        'Date': 'z.date()',
        'any': 'z.any()',
        'unknown': 'z.unknown()',
        'null': 'z.null()',
        'undefined': 'z.undefined()',
        'void': 'z.void()',
    }

    def __init__(self):
        self.interfaces: Dict[str, str] = {}
        self.types: Dict[str, str] = {}
        self.enums: Dict[str, List[str]] = {}

    def convert_type(self, ts_type: str, optional: bool = False) -> str:
        """Convert a TypeScript type to Zod schema."""
        ts_type = ts_type.strip()

        # Handle optional (?)
        if ts_type.endswith('?'):
            ts_type = ts_type[:-1].strip()
            optional = True

        # Handle union with undefined/null
        if ' | undefined' in ts_type or ' | null' in ts_type:
            optional = True
            ts_type = re.sub(r'\s*\|\s*(undefined|null)', '', ts_type).strip()

        # Simple types
        if ts_type in self.TYPE_MAP:
            zod = self.TYPE_MAP[ts_type]
        # Array types
        elif ts_type.endswith('[]'):
            inner_type = ts_type[:-2].strip()
            inner_zod = self.convert_type(inner_type)
            zod = f'z.array({inner_zod})'
        # Generic Array<T>
        elif ts_type.startswith('Array<') and ts_type.endswith('>'):
            inner_type = ts_type[6:-1].strip()
            inner_zod = self.convert_type(inner_type)
            zod = f'z.array({inner_zod})'
        # Record<K, V>
        elif ts_type.startswith('Record<'):
            match = re.match(r'Record<\s*(.+?)\s*,\s*(.+?)\s*>', ts_type)
            if match:
                value_type = match.group(2)
                value_zod = self.convert_type(value_type)
                zod = f'z.record({value_zod})'
            else:
                zod = 'z.record(z.any())'
        # Union types
        elif ' | ' in ts_type:
            union_types = [t.strip() for t in ts_type.split('|')]
            union_zods = [self.convert_type(t) for t in union_types]
            zod = f'z.union([{", ".join(union_zods)}])'
        # Literal types
        elif ts_type.startswith("'") or ts_type.startswith('"'):
            zod = f'z.literal({ts_type})'
        # Reference to another interface/type/enum
        elif ts_type in self.interfaces or ts_type in self.types or ts_type in self.enums:
            zod = f'{ts_type}Schema'
        else:
            # Unknown type - use z.any() with comment
            zod = f'z.any() /* TODO: define schema for {ts_type} */'

        # Add optional modifier
        if optional:
            zod = f'{zod}.optional()'

        return zod

    def parse_interface(self, interface_str: str) -> Tuple[str, List[Tuple[str, str, bool, Optional[str]]]]:
        """Parse a TypeScript interface and return name and fields."""
        # Extract interface name
        name_match = re.search(r'interface\s+(\w+)', interface_str)
        if not name_match:
            raise ValueError("Could not parse interface name")

        name = name_match.group(1)

        # Extract fields
        fields = []
        field_pattern = re.compile(
            r'^\s*(?:/\*\*\s*(.+?)\s*\*/\s*)?'  # Optional JSDoc comment
            r'(\w+)(\??)\s*:\s*(.+?);?\s*$',     # fieldName?: type;
            re.MULTILINE
        )

        body_match = re.search(r'\{(.+?)\}', interface_str, re.DOTALL)
        if body_match:
            body = body_match.group(1)
            for match in field_pattern.finditer(body):
                description = match.group(1)
                field_name = match.group(2)
                optional = match.group(3) == '?'
                field_type = match.group(4).strip()
                fields.append((field_name, field_type, optional, description))

        return name, fields

    def parse_type_alias(self, type_str: str) -> Tuple[str, str]:
        """Parse a TypeScript type alias."""
        match = re.search(r'type\s+(\w+)\s*=\s*(.+?);?\s*$', type_str, re.DOTALL)
        if not match:
            raise ValueError("Could not parse type alias")

        name = match.group(1)
        type_def = match.group(2).strip().rstrip(';')
        return name, type_def

    def parse_enum(self, enum_str: str) -> Tuple[str, List[str]]:
        """Parse a TypeScript enum."""
        name_match = re.search(r'enum\s+(\w+)', enum_str)
        if not name_match:
            raise ValueError("Could not parse enum name")

        name = name_match.group(1)

        # Extract enum values
        values = []
        body_match = re.search(r'\{(.+?)\}', enum_str, re.DOTALL)
        if body_match:
            body = body_match.group(1)
            value_pattern = re.compile(r'(\w+)\s*(?:=\s*["\'](.+?)["\']\s*)?', re.MULTILINE)
            for match in value_pattern.finditer(body):
                value = match.group(2) if match.group(2) else match.group(1)
                values.append(value)

        return name, values

    def interface_to_zod(self, name: str, fields: List[Tuple[str, str, bool, Optional[str]]]) -> str:
        """Convert interface fields to Zod schema."""
        schema_lines = [f'export const {name}Schema = z.object({{']

        for field_name, field_type, optional, description in fields:
            zod_type = self.convert_type(field_type, optional)

            # Add description if present
            if description:
                desc_line = f'  {field_name}: {zod_type}.describe("{description}"),'
            else:
                desc_line = f'  {field_name}: {zod_type},'

            schema_lines.append(desc_line)

        schema_lines.append('});')
        schema_lines.append('')
        schema_lines.append(f'export type {name} = z.infer<typeof {name}Schema>;')

        return '\n'.join(schema_lines)

    def type_alias_to_zod(self, name: str, type_def: str) -> str:
        """Convert type alias to Zod schema."""
        zod_type = self.convert_type(type_def)

        lines = [
            f'export const {name}Schema = {zod_type};',
            '',
            f'export type {name} = z.infer<typeof {name}Schema>;'
        ]

        return '\n'.join(lines)

    def enum_to_zod(self, name: str, values: List[str]) -> str:
        """Convert enum to Zod schema."""
        quoted_values = [f'"{v}"' for v in values]

        if len(values) == 1:
            zod_def = f'z.literal({quoted_values[0]})'
        else:
            zod_def = f'z.enum([{", ".join(quoted_values)}])'

        lines = [
            f'export const {name}Schema = {zod_def};',
            '',
            f'export type {name} = z.infer<typeof {name}Schema>;'
        ]

        return '\n'.join(lines)

    def convert_file(self, input_content: str) -> str:
        """Convert an entire TypeScript file to Zod schemas."""
        output_lines = [
            "import { z } from 'zod';",
            '',
            '// Auto-generated Zod schemas',
            ''
        ]

        # Parse all interfaces
        interface_pattern = re.compile(
            r'(?:export\s+)?interface\s+\w+\s*\{[^}]*\}',
            re.DOTALL
        )
        for match in interface_pattern.finditer(input_content):
            interface_str = match.group(0)
            try:
                name, fields = self.parse_interface(interface_str)
                self.interfaces[name] = interface_str
            except ValueError:
                pass

        # Parse all type aliases
        type_pattern = re.compile(
            r'(?:export\s+)?type\s+\w+\s*=\s*[^;]+;?',
            re.DOTALL
        )
        for match in type_pattern.finditer(input_content):
            type_str = match.group(0)
            try:
                name, type_def = self.parse_type_alias(type_str)
                self.types[name] = type_def
            except ValueError:
                pass

        # Parse all enums
        enum_pattern = re.compile(
            r'(?:export\s+)?enum\s+\w+\s*\{[^}]*\}',
            re.DOTALL
        )
        for match in enum_pattern.finditer(input_content):
            enum_str = match.group(0)
            try:
                name, values = self.parse_enum(enum_str)
                self.enums[name] = values
            except ValueError:
                pass

        # Generate Zod schemas
        # Enums first (no dependencies)
        for name, values in self.enums.items():
            output_lines.append(self.enum_to_zod(name, values))
            output_lines.append('')

        # Then type aliases
        for name, type_def in self.types.items():
            output_lines.append(self.type_alias_to_zod(name, type_def))
            output_lines.append('')

        # Finally interfaces
        for name, interface_str in self.interfaces.items():
            _, fields = self.parse_interface(interface_str)
            output_lines.append(self.interface_to_zod(name, fields))
            output_lines.append('')

        return '\n'.join(output_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Zod schemas from TypeScript interfaces/types'
    )
    parser.add_argument(
        '--input',
        help='Input TypeScript file path'
    )
    parser.add_argument(
        '--output',
        help='Output file path for Zod schemas'
    )
    parser.add_argument(
        '--input-string',
        help='Input TypeScript code as string'
    )

    args = parser.parse_args()

    # Read input
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}")
            return 1
        input_content = input_path.read_text(encoding='utf-8')
    elif args.input_string:
        input_content = args.input_string
    else:
        print("Error: Either --input or --input-string must be provided")
        return 1

    # Convert
    converter = TypeScriptToZodConverter()
    try:
        output_content = converter.convert_file(input_content)
    except Exception as e:
        print(f"Error during conversion: {e}")
        return 1

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_content, encoding='utf-8')
        print(f"Generated Zod schemas written to: {args.output}")
    else:
        print(output_content)

    return 0


if __name__ == '__main__':
    exit(main())
