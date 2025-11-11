#!/usr/bin/env python3
"""
Create a new Architectural Decision Record (ADR).
"""

import argparse
import re
from datetime import datetime
from pathlib import Path


def slugify(text):
    """Convert text to lowercase slug format."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def get_next_adr_number(adr_dir):
    """Get the next ADR number in sequence."""
    if not adr_dir.exists():
        return 1

    existing = list(adr_dir.glob('*.md'))
    if not existing:
        return 1

    numbers = []
    for path in existing:
        match = re.match(r'^(\d+)', path.name)
        if match:
            numbers.append(int(match.group(1)))

    return max(numbers) + 1 if numbers else 1


def create_adr(title, adr_dir='docs/ADR', status='Proposed'):
    """Create a new ADR file."""
    adr_dir = Path(adr_dir)
    adr_dir.mkdir(parents=True, exist_ok=True)

    number = get_next_adr_number(adr_dir)
    slug = slugify(title)
    filename = f"{number:04d}-{slug}.md"
    filepath = adr_dir / filename

    date = datetime.now().strftime('%Y-%m-%d')

    content = f"""# ADR {number:04d}: {title}

**Status:** {status}

**Date:** {date}

**Deciders:** [List key decision makers]

## Context

[Describe the context and problem statement. What forces are at play? What are the constraints?]

### Problem

[What specific problem are we trying to solve?]

### Constraints

- [Constraint 1]
- [Constraint 2]

## Decision

[Describe the decision we made and why we made it.]

### Rationale

[Explain the reasoning behind the decision. What factors influenced this choice?]

## Consequences

### Positive

- [Positive consequence 1]
- [Positive consequence 2]

### Negative

- [Negative consequence 1]
- [Negative consequence 2]

### Neutral

- [Neutral consequence 1]

## Alternatives Considered

### Alternative 1: [Name]

**Description:** [Brief description]

**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

**Decision:** Rejected because [reason]

### Alternative 2: [Name]

**Description:** [Brief description]

**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

**Decision:** Rejected because [reason]

## Implementation

[How will this decision be implemented? What are the next steps?]

- [ ] Task 1
- [ ] Task 2

## Related Decisions

- [Link to related ADR if applicable]

## References

- [Link to relevant documentation]
- [Link to discussions or RFCs]

## Notes

[Any additional notes or context]
"""

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"Created ADR: {filepath}")
    print(f"Number: {number:04d}")
    print(f"Status: {status}")

    return filepath


def main():
    parser = argparse.ArgumentParser(description='Create a new Architectural Decision Record')
    parser.add_argument('title', help='Title of the ADR')
    parser.add_argument('--dir', default='docs/ADR', help='ADR directory path')
    parser.add_argument('--status', default='Proposed',
                       choices=['Proposed', 'Accepted', 'Rejected', 'Deprecated', 'Superseded'],
                       help='Initial status of the ADR')

    args = parser.parse_args()

    filepath = create_adr(args.title, args.dir, args.status)

    print("\nNext steps:")
    print(f"1. Edit {filepath} to complete all sections")
    print("2. Review with the team")
    print("3. Update status to 'Accepted' when finalized")
    print("4. Link from architecture documentation")


if __name__ == '__main__':
    main()
