# Skill Review Report: [Skill Name]

**Skill Path:** `skills/[category]/[skill-name]`
**Review Date:** [YYYY-MM-DD]
**Reviewer:** Claude Code (skill-reviewer-and-enhancer)
**Skill Purpose:** [Brief description of what the skill does]

---

## Executive Summary

**Overall Grade:** [A / B / C / D / F]
**Status:** [[OK] Production Ready / [WARN] Needs Minor Fixes / [ERROR] Needs Major Revision]
**Critical Issues:** [count]
**Warnings:** [count]
**Suggestions:** [count]

### Quick Assessment
[1-2 sentence summary of skill quality and readiness]

---

## 1. Structural Compliance

### Frontmatter Validation

#### Name Field
- [x] Present
- [x] Uses hyphen-case
- [ ] Issue: [Description if any]

**Current:** `[current-name]`
**Expected:** `[correct-name]` (if different)

#### Description Field
- [x] Present
- [x] Third-person voice
- [x] Includes trigger terms
- [x] Under 1024 characters ([X] chars)
- [ ] Issue: [Description if any]

**Current Length:** [X] characters
**Quality Score:** [High / Medium / Low]

#### Optional Fields
- [x] `allowed-tools` specified (if applicable)
- [ ] Missing but recommended: [field name]

### Naming Convention
- [x] Lowercase only
- [x] Uses hyphens (not underscores or spaces)
- [x] No consecutive hyphens
- [x] Doesn't start/end with hyphen

**Validation:** [[OK] PASS / [ERROR] FAIL]

---

## 2. Instruction Style Analysis

### Imperative Form Check

**Second-Person Usage Found:** [count] instances

**Examples:**
| Line | Current Text | Suggested Fix |
|------|-------------|---------------|
| [N] | "[text with 'you should']" | "[imperative version]" |
| [N] | "[text with 'you can']" | "[imperative version]" |

**Pattern Breakdown:**
- "you should" → [count] instances
- "you can" → [count] instances
- "you need to" → [count] instances
- "you will" → [count] instances

### Section Organization
- [x] Clear overview section
- [x] When to Use section (recommended)
- [x] Step-by-step implementation
- [x] Resource references
- [x] Best practices section
- [ ] Missing: [section name]

**Organization Score:** [Excellent / Good / Needs Improvement]

---

## 3. Domain-Specific Best Practices

**Skill Domain:** [Next.js / Testing / UI Components / Database / Security / Other]

### Framework/Library Versions

| Component | Current | Latest | Status |
|-----------|---------|--------|--------|
| [Framework] | [version] | [version] | [[OK] / [WARN] / [ERROR]] |
| [Library] | [version] | [version] | [[OK] / [WARN] / [ERROR]] |

### Pattern Compliance

#### Modern Patterns Used [OK]
- [x] [Pattern name and description]
- [x] [Pattern name and description]

#### Deprecated Patterns Found [ERROR]
- [ ] **Issue:** [Description of deprecated pattern]
  - **Line/Section:** [location]
  - **Recommendation:** [modern replacement]

- [ ] **Issue:** [Description of deprecated pattern]
  - **Line/Section:** [location]
  - **Recommendation:** [modern replacement]

### Domain-Specific Checklist

**For [Domain] Skills:**
- [x] [Specific requirement 1]
- [x] [Specific requirement 2]
- [ ] [Missing requirement]

**Compliance Score:** [X]% ([Y]/[Z] checks passed)

---

## 4. Resource Completeness

### Scripts Directory

**Scripts Mentioned in SKILL.md:**
| Script Name | Exists | Documented | Executable |
|-------------|--------|------------|------------|
| `[name].py` | [[OK]/[ERROR]] | [[OK]/[ERROR]] | [[OK]/[ERROR]] |

**Issues:**
- [ ] Script `[name]` mentioned but not found
- [ ] Script `[name]` missing usage documentation

### References Directory

**References Mentioned:**
| Reference Name | Exists | Size | Grep Patterns |
|----------------|--------|------|---------------|
| `[name].md` | [[OK]/[ERROR]] | [X]KB | [[OK]/[ERROR]] |

**Issues:**
- [ ] Reference `[name]` mentioned but not found
- [ ] Large reference (>10KB) without grep patterns

### Assets Directory

**Assets Mentioned:**
| Asset Name | Exists | Type | Documented |
|------------|--------|------|------------|
| `[name]` | [[OK]/[ERROR]] | [type] | [[OK]/[ERROR]] |

**Issues:**
- [ ] Asset `[name]` mentioned but not found

---

## 5. Detailed Findings

### Critical Issues (Must Fix Before Production)

#### Issue 1: [Title]
**Severity:** Critical
**Location:** [Line number or section]
**Description:** [Detailed explanation]

**Current State:**
```[language]
[Code or text showing the problem]
```

**Required Fix:**
```[language]
[Code or text showing the solution]
```

**Impact:** [How this affects skill functionality or user experience]

---

### Warnings (Should Fix)

#### Warning 1: [Title]
**Severity:** Medium
**Location:** [Line number or section]
**Description:** [Detailed explanation]

**Recommendation:** [Suggested improvement]

---

### Suggestions (Nice to Have)

#### Suggestion 1: [Title]
**Priority:** Low
**Description:** [Enhancement opportunity]

**Benefit:** [How this would improve the skill]

---

## 6. Code Quality Assessment

### Examples Provided
- [x] Clear code examples
- [x] Examples follow best practices
- [x] Examples are complete and runnable
- [ ] Issue: [Description]

### Error Handling
- [x] Includes troubleshooting section
- [x] Common errors documented
- [x] Solutions provided
- [ ] Missing: [What's missing]

### Completeness
- [x] Prerequisites listed
- [x] Dependencies documented
- [x] Configuration steps clear
- [x] Edge cases covered

---

## 7. Modernization Opportunities

### Framework Updates Needed
1. **[Framework name]**: Update from [old] to [new]
   - Impact: [High / Medium / Low]
   - Effort: [High / Medium / Low]
   - Benefits: [List benefits]

### Pattern Modernization
1. **[Pattern name]**: Replace [old pattern] with [new pattern]
   - Affected sections: [List sections]
   - Migration path: [Brief steps]

### Tooling Updates
1. **[Tool name]**: Replace [old tool] with [new tool]
   - Rationale: [Why update]
   - Changes required: [List changes]

---

## 8. Automated Fixes Available

The following fixes can be applied automatically:

- [ ] Convert second-person to imperative form ([count] instances)
- [ ] Update frontmatter format
- [ ] Fix name hyphenation
- [ ] Add missing `allowed-tools` field
- [ ] Update framework version references
- [ ] Replace deprecated API patterns

**Estimated Time:** [X] minutes
**Apply fixes?** [Yes / No / Review First]

---

## 9. Manual Improvements Required

The following require manual review:

1. **[Improvement title]**
   - Complexity: [High / Medium / Low]
   - Estimated effort: [time]
   - Priority: [High / Medium / Low]

---

## 10. Comparison to Best-in-Class

### Strengths
- [OK] [Strength 1]
- [OK] [Strength 2]

### Areas for Improvement
- [TIP] [Improvement area 1]
- [TIP] [Improvement area 2]

### Benchmarking
Compared to similar skills in the repository:
- **Structure:** [Better / Similar / Worse]
- **Documentation:** [Better / Similar / Worse]
- **Best Practices:** [Better / Similar / Worse]
- **Resource Completeness:** [Better / Similar / Worse]

---

## 11. Action Plan

### Immediate Actions (This Week)
1. [ ] [Action item with high priority]
2. [ ] [Action item with high priority]

### Short-Term Actions (This Month)
1. [ ] [Action item with medium priority]
2. [ ] [Action item with medium priority]

### Long-Term Improvements (This Quarter)
1. [ ] [Action item with low priority but high value]
2. [ ] [Action item with low priority but high value]

---

## 12. Testing & Validation

### Pre-Enhancement Validation
```bash
python scripts/quick_validate.py skills/[category]/[skill-name]
```
**Result:** [PASS / FAIL]

### Post-Enhancement Validation
After applying fixes:
- [ ] Run validation script
- [ ] Test resource references
- [ ] Verify code examples
- [ ] Check resource file paths
- [ ] Test scripts (if applicable)

---

## 13. Approval & Sign-Off

**Recommended Next Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Skill Ready for:**
- [ ] Immediate deployment (Grade A, no critical issues)
- [ ] Deployment after minor fixes (Grade B)
- [ ] Significant revision needed (Grade C or below)

**Reviewer Notes:**
[Any additional context or recommendations]

---

## Appendix: Detailed Metrics

### Skill Statistics
- **Total Lines:** [count]
- **Code Examples:** [count]
- **Resource References:** [count]
- **Second-Person Instances:** [count]
- **External Links:** [count]

### Readability
- **Estimated Reading Time:** [X] minutes
- **Complexity Level:** [Beginner / Intermediate / Advanced]
- **Target Audience:** [Description]

### Maintenance
- **Last Updated:** [Date if available]
- **Update Frequency Required:** [How often skill needs updates]
- **Maintenance Burden:** [Low / Medium / High]

---

**End of Report**

*Generated by skill-reviewer-and-enhancer*
*For questions or clarifications, review the skill at `[skill-path]`*
