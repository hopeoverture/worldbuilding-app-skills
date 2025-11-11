#!/usr/bin/env python3
"""Generate Playwright test scripts from natural language flow descriptions."""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class FlowStep:
    """Represents a single step in a user flow."""

    def __init__(self, action: str, target: str, value: str = "", assertion: bool = False):
        self.action = action
        self.target = target
        self.value = value
        self.assertion = assertion


class FlowParser:
    """Parse natural language flow descriptions into structured steps."""

    # Action patterns
    ACTIONS = {
        r'navigate[s]? to (.+)': ('navigate', 'page'),
        r'click[s]? (?:on )?(?:the )?(.+?)(?:\s+button|\s+link)?$': ('click', 'button'),
        r'fill[s]? (?:in )?(?:the )?(.+?)(?: (?:with|field))? (.+)': ('fill', 'input'),
        r'enter[s]? (.+) in (?:the )?(.+)': ('fill', 'input'),
        r'type[s]? (.+) in (?:the )?(.+)': ('fill', 'input'),
        r'select[s]? (.+) from (?:the )?(.+)': ('select', 'select'),
        r'choose[s]? (.+)': ('select', 'select'),
        r'check[s]? (?:the )?(.+)': ('check', 'checkbox'),
        r'uncheck[s]? (?:the )?(.+)': ('uncheck', 'checkbox'),
        r'upload[s]? (.+)': ('upload', 'file'),
    }

    # Assertion patterns
    ASSERTIONS = {
        r'see[s]? (.+)': 'visible',
        r'(?:is|are) redirected to (.+)': 'url',
        r'(.+) displays? (.+)': 'contains',
        r'(?:page|screen) (?:shows?|displays?) (.+)': 'visible',
        r'verif(?:y|ies) (.+)': 'visible',
    }

    def parse(self, description: str) -> List[FlowStep]:
        """Parse flow description into structured steps."""
        steps = []

        # Split into lines
        lines = [line.strip() for line in description.split('\n') if line.strip()]

        for line in lines:
            # Remove numbering (1., 2., etc.)
            line = re.sub(r'^\d+\.\s*', '', line)

            # Remove Given/When/Then/And prefixes
            line = re.sub(r'^(?:Given|When|Then|And):\s*', '', line, flags=re.IGNORECASE)

            # Try to match assertion patterns first
            matched = False
            for pattern, assertion_type in self.ASSERTIONS.items():
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    steps.append(self._create_assertion_step(assertion_type, match))
                    matched = True
                    break

            if matched:
                continue

            # Try to match action patterns
            for pattern, (action, element_type) in self.ACTIONS.items():
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    steps.append(self._create_action_step(action, element_type, match))
                    matched = True
                    break

            if not matched:
                print(f"Warning: Could not parse line: {line}", file=sys.stderr)

        return steps

    def _create_action_step(self, action: str, element_type: str, match: re.Match) -> FlowStep:
        """Create action step from regex match."""
        if action == 'navigate':
            return FlowStep('navigate', match.group(1))
        elif action == 'click':
            return FlowStep('click', match.group(1), element_type)
        elif action == 'fill':
            if len(match.groups()) >= 2:
                target = match.group(2)
                value = match.group(1)
            else:
                target = match.group(1)
                value = ""
            return FlowStep('fill', target, value)
        elif action == 'select':
            target = match.group(2) if len(match.groups()) >= 2 else match.group(1)
            value = match.group(1) if len(match.groups()) >= 2 else ""
            return FlowStep('select', target, value)
        elif action in ['check', 'uncheck']:
            return FlowStep(action, match.group(1))
        elif action == 'upload':
            return FlowStep('upload', match.group(1))

        return FlowStep(action, match.group(1))

    def _create_assertion_step(self, assertion_type: str, match: re.Match) -> FlowStep:
        """Create assertion step from regex match."""
        if assertion_type == 'url':
            return FlowStep('assertUrl', match.group(1), assertion=True)
        elif assertion_type == 'contains':
            return FlowStep('assertContains', match.group(1), match.group(2), assertion=True)
        else:  # visible
            return FlowStep('assertVisible', match.group(1), assertion=True)


class TestGenerator:
    """Generate Playwright test code from flow steps."""

    def __init__(self, steps: List[FlowStep], flow_name: str):
        self.steps = steps
        self.flow_name = flow_name

    def generate(self) -> str:
        """Generate complete test file."""
        test_name = self._to_snake_case(self.flow_name)
        test_description = self.flow_name

        imports = "import { test, expect } from '@playwright/test'\n\n"

        test_code = f"test.describe('{self.flow_name}', () => {{\n"
        test_code += f"  test('{test_description}', async ({{ page }}) => {{\n"

        for step in self.steps:
            test_code += self._generate_step_code(step)

        test_code += "  })\n"
        test_code += "})\n"

        return imports + test_code

    def _generate_step_code(self, step: FlowStep) -> str:
        """Generate code for a single step."""
        indent = "    "

        if step.action == 'navigate':
            url = step.target if step.target.startswith('/') else f'/{step.target}'
            return f"{indent}// Navigate to {step.target}\n{indent}await page.goto('{url}')\n\n"

        elif step.action == 'click':
            element_name = self._normalize_text(step.target)
            return f"{indent}// Click {step.target}\n{indent}await page.getByRole('button', {{ name: /{element_name}/i }}).click()\n\n"

        elif step.action == 'fill':
            label_name = self._normalize_text(step.target)
            value = step.value or 'test_value'
            return f"{indent}// Fill {step.target}\n{indent}await page.getByLabel(/{label_name}/i).fill('{value}')\n\n"

        elif step.action == 'select':
            label_name = self._normalize_text(step.target)
            value = self._to_snake_case(step.value) if step.value else 'option'
            return f"{indent}// Select {step.value} from {step.target}\n{indent}await page.getByLabel(/{label_name}/i).selectOption('{value}')\n\n"

        elif step.action == 'check':
            label_name = self._normalize_text(step.target)
            return f"{indent}// Check {step.target}\n{indent}await page.getByLabel(/{label_name}/i).check()\n\n"

        elif step.action == 'uncheck':
            label_name = self._normalize_text(step.target)
            return f"{indent}// Uncheck {step.target}\n{indent}await page.getByLabel(/{label_name}/i).uncheck()\n\n"

        elif step.assertion:
            return self._generate_assertion_code(step, indent)

        return f"{indent}// TODO: {step.action} {step.target}\n\n"

    def _generate_assertion_code(self, step: FlowStep, indent: str) -> str:
        """Generate assertion code."""
        if step.action == 'assertVisible':
            text = self._normalize_text(step.target)
            return f"{indent}// Verify {step.target} is visible\n{indent}await expect(page.getByText(/{text}/i)).toBeVisible()\n\n"

        elif step.action == 'assertUrl':
            url = step.target if step.target.startswith('/') else f'/{step.target}'
            return f"{indent}// Verify redirect to {step.target}\n{indent}await expect(page).toHaveURL(/{url}/)\n\n"

        elif step.action == 'assertContains':
            element = self._normalize_text(step.target)
            text = self._normalize_text(step.value)
            return f"{indent}// Verify {step.target} contains {step.value}\n{indent}await expect(page.getByRole('{element}')).toContainText(/{text}/i)\n\n"

        return f"{indent}// TODO: Assert {step.target}\n\n"

    def _normalize_text(self, text: str) -> str:
        """Normalize text for regex patterns."""
        # Remove articles and common words
        text = re.sub(r'\b(the|a|an)\b', '', text, flags=re.IGNORECASE)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()

    def _to_snake_case(self, text: str) -> str:
        """Convert text to snake_case."""
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', '_', text)
        return text.lower()


def main():
    parser = argparse.ArgumentParser(
        description="Generate Playwright test from natural language flow description"
    )
    parser.add_argument(
        '--description',
        help='Flow description as string'
    )
    parser.add_argument(
        '--input',
        help='File containing flow description'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )
    parser.add_argument(
        '--name',
        default='User Flow',
        help='Test name/description'
    )

    args = parser.parse_args()

    # Get flow description
    if args.description:
        description = args.description
    elif args.input:
        with open(args.input, 'r') as f:
            description = f.read()
    else:
        print("Error: Must provide --description or --input", file=sys.stderr)
        sys.exit(1)

    # Parse flow
    flow_parser = FlowParser()
    steps = flow_parser.parse(description)

    if not steps:
        print("Error: No steps parsed from description", file=sys.stderr)
        sys.exit(1)

    # Generate test
    test_generator = TestGenerator(steps, args.name)
    test_code = test_generator.generate()

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(test_code)
        print(f"Test generated: {output_path}")
    else:
        print(test_code)


if __name__ == '__main__':
    main()
