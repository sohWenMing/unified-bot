---
name: Run Single Test
description: Run one specific test to check if it passes
---

# Run Single Test

This command runs just one test file without the visual browser window.

## Trigger Phrases

Activate when user says:
- "Run single test"
- "Run one test"
- "Test [specific name]"
- "Run [test-name]"
- "Check [feature] test"

## Instructions for Cursor

### Step 1: List or Identify Test

If user didn't specify which test:
```bash
ls -1 cursor-playwright/tests/*.spec.ts
```

```
Which test would you like to run?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. login-flow.spec.ts
2. checkout.spec.ts
3. profile-update.spec.ts

Enter number or filename:
```

### Step 2: Execute Test

```bash
cd cursor-playwright && npx playwright test tests/[selected].spec.ts
```

### Step 3: Display Results

**If passed:**
```
✓ TEST PASSED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test: [test-name]
Duration: [time]

All checks passed! The feature is working.
```

**If failed:**
```
✗ TEST FAILED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test: [test-name]
Duration: [time]
Error: [error message]

NEXT STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. First, check if the feature works manually:
   Open your browser and try the same steps.

2. If feature WORKS manually:
   → FALSE NEGATIVE (test script issue)
   → Say: "Self-Heal [test-name]"

3. If feature DOESN'T WORK manually:
   → TRUE NEGATIVE (real bug)
   → Report to development team

4. If UNSURE:
   → Say: "Run test headed"
   → Watch what happens

What would you like to do?
a) Run in headed mode
b) Self-heal this test
c) Run all tests
d) Exit
```

### Step 4: Follow-up Actions

Based on user choice, trigger appropriate command.
