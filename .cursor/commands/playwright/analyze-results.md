---
name: Analyze Test Results
description: Review the last test run and get guidance on what to do next
---

# Analyze Test Results

This command reviews the most recent test execution and helps you understand what to do next.

## Trigger Phrases

Activate when user says:
- "Analyze results"
- "Show test results"
- "What failed"
- "Test report"
- "Explain results"

## Instructions for Cursor

### Step 1: Check for Results

```bash
test -f cursor-playwright/test-results/results.json && echo "found" || echo "not found"
```

If not found:
```
No test results found.
Run tests first with "run all tests".
```

### Step 2: Parse Results

Read and parse `cursor-playwright/test-results/results.json`

### Step 3: Display Summary

```
═══════════════════════════════════════════════════════════════
       TEST RESULTS ANALYSIS
═══════════════════════════════════════════════════════════════

Last Run: [timestamp]
Duration: [time]

Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Passed: [Y] tests
✗ Failed: [Z] tests
⊘ Skipped: [W] tests

Overall: [Healthy/Needs Attention/Critical]
```

### Step 4: Detail Each Test

**Passed tests:**
```
PASSED TESTS ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ login-flow.spec.ts (2.3s)
✓ profile-update.spec.ts (1.8s)

These features are working correctly!
```

**Failed tests with guidance:**
```
FAILED TESTS ✗
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test: checkout.spec.ts
Duration: 5.2s
Error: Timeout waiting for element

DECISION GUIDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ask yourself:
"Can I complete checkout manually in my browser?"

→ YES, checkout works:
  This is a FALSE NEGATIVE (test script issue)
  Action: Say "Self-Heal Checkout Test"

→ NO, checkout is broken:
  This is a TRUE NEGATIVE (real bug)
  Action: Report to development team

→ UNSURE:
  Action: Say "Run test headed"
  Watch what happens and decide

════════════════════════════════════════
```

### Step 5: Recommendations

```
RECOMMENDED ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For FALSE NEGATIVES:
- Self-heal the failing tests
- Commands: "Self-Heal [Test Name]"

For TRUE NEGATIVES:
- Report to development team
- Include: test name, error, screenshot

For UNSURE:
- Run in headed mode to see
- Command: "Run test headed"

Quick Actions:
a) Self-heal all failing tests
b) Run failing tests in headed mode
c) Open HTML report
d) Export bug report info
```
