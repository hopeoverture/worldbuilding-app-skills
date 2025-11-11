#!/usr/bin/env python3
"""
Create a new Product Requirement Document (PRD).
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


def create_prd(title, prd_dir='docs/PRD', author=''):
    """Create a new PRD file."""
    prd_dir = Path(prd_dir)
    prd_dir.mkdir(parents=True, exist_ok=True)

    slug = slugify(title)
    filename = f"{slug}.md"
    filepath = prd_dir / filename

    date = datetime.now().strftime('%Y-%m-%d')

    content = f"""# Product Requirement Document: {title}

**Author:** {author or '[Your Name]'}

**Date:** {date}

**Status:** Draft

**Last Updated:** {date}

## Executive Summary

[Brief 2-3 sentence overview of what this feature is and why it matters]

## Problem Statement

### Current Situation

[Describe the current state and what pain points exist]

### User Impact

[Who is affected by this problem and how?]

### Business Impact

[What is the business cost of not solving this problem?]

## Goals and Objectives

### Primary Goals

1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

### Success Metrics

- [Metric 1]: [Target]
- [Metric 2]: [Target]
- [Metric 3]: [Target]

### Non-Goals

[What is explicitly out of scope for this feature?]

- [Non-goal 1]
- [Non-goal 2]

## User Stories

### Story 1: [User Type]

**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Story 2: [User Type]

**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Requirements

### Functional Requirements

#### Must Have (P0)

1. **[Requirement 1]**
   - Description: [Details]
   - User Impact: [High/Medium/Low]

2. **[Requirement 2]**
   - Description: [Details]
   - User Impact: [High/Medium/Low]

#### Should Have (P1)

1. **[Requirement 3]**
   - Description: [Details]
   - User Impact: [High/Medium/Low]

#### Nice to Have (P2)

1. **[Requirement 4]**
   - Description: [Details]
   - User Impact: [High/Medium/Low]

### Non-Functional Requirements

#### Performance

- [Performance requirement 1]
- [Performance requirement 2]

#### Security

- [Security requirement 1]
- [Security requirement 2]

#### Accessibility

- [Accessibility requirement 1]
- [Accessibility requirement 2]

#### Scalability

- [Scalability requirement 1]
- [Scalability requirement 2]

## Design Considerations

### User Experience

[Describe the intended user experience]

#### User Flow

1. [Step 1]
2. [Step 2]
3. [Step 3]

#### UI Components

- [Component 1]: [Description]
- [Component 2]: [Description]

### Technical Architecture

[High-level technical approach]

#### Components

- **[Component 1]**: [Purpose and responsibilities]
- **[Component 2]**: [Purpose and responsibilities]

#### Data Model

[Overview of data structures and relationships]

#### APIs

- **[Endpoint 1]**: [Purpose]
- **[Endpoint 2]**: [Purpose]

### Integration Points

- [System/Service 1]: [How it integrates]
- [System/Service 2]: [How it integrates]

## Dependencies

### Internal Dependencies

- [Dependency 1]: [Why needed]
- [Dependency 2]: [Why needed]

### External Dependencies

- [Third-party service 1]: [Purpose]
- [Third-party service 2]: [Purpose]

### Blocking Issues

- [Issue 1]: [Resolution plan]
- [Issue 2]: [Resolution plan]

## Risks and Mitigation

| Risk | Impact | Likelihood | Mitigation Strategy |
|------|--------|------------|---------------------|
| [Risk 1] | High/Medium/Low | High/Medium/Low | [Strategy] |
| [Risk 2] | High/Medium/Low | High/Medium/Low | [Strategy] |

## Timeline and Milestones

### Phase 1: [Name] ([Duration])

- [ ] [Milestone 1]
- [ ] [Milestone 2]

### Phase 2: [Name] ([Duration])

- [ ] [Milestone 3]
- [ ] [Milestone 4]

### Phase 3: [Name] ([Duration])

- [ ] [Milestone 5]
- [ ] [Milestone 6]

### Target Launch Date

[Date or timeframe]

## Testing Strategy

### Unit Testing

[Approach to unit testing]

### Integration Testing

[Approach to integration testing]

### User Acceptance Testing

[UAT plan and criteria]

### Performance Testing

[Performance testing approach]

## Launch Plan

### Pre-Launch Checklist

- [ ] [Item 1]
- [ ] [Item 2]
- [ ] [Item 3]

### Rollout Strategy

[Describe how the feature will be rolled out]

- **Audience**: [Who gets access first]
- **Timeline**: [Phased rollout schedule]
- **Monitoring**: [What metrics to watch]

### Communication Plan

- **Internal**: [How to communicate to team]
- **External**: [How to communicate to users]

### Rollback Plan

[How to rollback if issues arise]

## Post-Launch

### Monitoring

- [Metric to monitor 1]
- [Metric to monitor 2]

### Iteration Plan

[How we'll iterate based on feedback]

### Success Evaluation

[How and when we'll evaluate if we met our goals]

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]
- [ ] [Question 3]

## Stakeholders

| Name | Role | Responsibility |
|------|------|----------------|
| [Name] | [Role] | [What they're responsible for] |
| [Name] | [Role] | [What they're responsible for] |

## References

- [Link to related PRDs]
- [Link to design mockups]
- [Link to technical specs]
- [Link to user research]

## Appendix

### Terminology

- **[Term 1]**: [Definition]
- **[Term 2]**: [Definition]

### Additional Resources

- [Resource 1]
- [Resource 2]
"""

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"Created PRD: {filepath}")

    return filepath


def main():
    parser = argparse.ArgumentParser(description='Create a new Product Requirement Document')
    parser.add_argument('title', help='Title of the PRD')
    parser.add_argument('--dir', default='docs/PRD', help='PRD directory path')
    parser.add_argument('--author', help='Document author name')

    args = parser.parse_args()

    filepath = create_prd(args.title, args.dir, args.author or '')

    print("\nNext steps:")
    print(f"1. Edit {filepath} to complete all sections")
    print("2. Share with stakeholders for review")
    print("3. Refine based on feedback")
    print("4. Get final approval before implementation")


if __name__ == '__main__':
    main()
