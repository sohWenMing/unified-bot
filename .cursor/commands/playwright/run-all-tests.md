---
name: Run All Tests
description: Run all automated tests and see the results
---

# Run All Tests

This command runs all your Playwright tests and shows you a summary of results.

## Trigger Phrases

Activate when user says:
- "Run all tests"
- "Run tests"
- "Execute tests"
- "Check all tests"
- "Run regression tests"

## Instructions for Cursor

### Step 1: Inform User

```
═══════════════════════════════════════════════════════════════
       RUNNING ALL TESTS
═══════════════════════════════════════════════════════════════

Starting test execution in headless mode...
This runs tests in the background (no browser window).
```

### Step 2: Execute Tests

```bash
cd cursor-playwright && npm run test
```

### Step 3: Parse and Display Results

Read: `cursor-playwright/test-results/results.json`

```
═══════════════════════════════════════════════════════════════
       TEST RESULTS
═══════════════════════════════════════════════════════════════

Total Tests: [X]
Duration: [time]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Passed: [Y]
✗ Failed: [Z]
⊘ Skipped: [W]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4: If All Pass

```
✓ ALL TESTS PASSED!

Great job! Your application is working as expected.

All tested features:
✓ Login flow
✓ Checkout process
✓ Profile update
...
```

### Step 5: If Some Fail

```
FAILED TESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. tests/checkout.spec.ts
   Error: [brief error]

2. tests/login-flow.spec.ts
   Error: [brief error]

WHAT TO DO NEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For each failed test, determine:

A) FALSE NEGATIVE (Feature works, test fails)
   → Test script needs updating
   → Use: "Self-Heal [Test Name]"

B) TRUE NEGATIVE (Feature is actually broken)
   → Real bug in application
   → Report to development team
   → Do NOT self-heal

TIP: Not sure? Run in headed mode to see what's happening.

What would you like to do?
a) Run failed tests in headed mode
b) Self-heal failed tests
c) Open detailed HTML report
d) Exit
```

### Step 6: Open HTML Report

```bash
cd cursor-playwright && npm run test:report
```

```
Opening detailed report in your browser...

The report shows:
- Screenshots of failures
- Step-by-step execution
- Error details
- Timing information
```

## Error Handling

### If no tests exist:
```
No tests found in cursor-playwright/tests/

Would you like to create your first test?
Say "generate test" to get started.
```

### If playwright not installed:
```
Playwright isn't set up yet.
Say "setup" to configure everything.
```
