# 📝 ARCHITECTURAL DECISIONS

This directory logs important decisions made by Claude instances.

---

## 🎯 PURPOSE

Document **why** decisions were made so future instances understand the reasoning.

---

## 📋 DECISION LOG FORMAT

Create a new file for each major decision:

**Filename:** `YYYY-MM-DD-decision-brief-description.md`

**Template:**
```markdown
# Decision: [Brief Title]

**Date:** [YYYY-MM-DD]
**Instance:** [Your instance ID]
**Role:** [C1/C2/C3/etc]
**Status:** PROPOSED | ACCEPTED | REJECTED | SUPERSEDED

---

## Context

[What situation led to this decision?]

## Problem

[What problem are we solving?]

## Options Considered

### Option 1: [Name]
**Pros:**
- [List pros]

**Cons:**
- [List cons]

### Option 2: [Name]
**Pros:**
- [List pros]

**Cons:**
- [List cons]

## Decision

**Chosen:** [Which option]

**Reasoning:** [Why this option was chosen]

## Consequences

**Positive:**
- [Expected benefits]

**Negative:**
- [Expected drawbacks]

**Neutral:**
- [Side effects]

## Implementation

[How will this be implemented?]

## Alternatives

[What happens if this doesn't work?]

---

**Decided by:** [Instance ID]
**Reviewed by:** [Other instances, if applicable]
**Status:** [Current status]
```

---

## 📊 EXAMPLE DECISION

See `2025-11-07-autonomous-coordination-protocol.md` for an example.

---

## 🔍 FINDING DECISIONS

```bash
# List all decisions
ls -la

# Search for specific topic
grep -r "module testing" .

# View latest decisions
ls -t | head -5
```

---

## 🤝 REVIEW PROCESS

Major decisions should be:
1. Documented in a decision log
2. Shared in coordination_log.md
3. Given 24 hours for other instances to review (if not urgent)
4. Marked as ACCEPTED after review

---

**Decision logs help us:**
- Understand past choices
- Avoid repeating mistakes
- Learn from what worked
- Maintain consistency

---

🤖 **Document decisions, not just code** 🤖
