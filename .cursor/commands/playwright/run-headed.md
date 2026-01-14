---
name: Run Test Headed
description: Run a test with browser visible to see what's happening
---

# Run Test in Headed Mode

This command runs a test with the browser window visible, so you can watch each step execute.

## Trigger Phrases

Activate when user says:
- "Run test headed"
- "Run headed mode"
- "Show test running"
- "Watch test"
- "Debug test"
- "See test execute"

## Instructions for Cursor

### Step 1: List Available Tests

```bash
ls -1 cursor-playwright/tests/*.spec.ts 2>/dev/null || echo "none"
```

If none:
```
No tests found. Create one first with "generate test".
```

Display:
```
Available tests:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. login-flow.spec.ts
2. checkout.spec.ts
3. profile-update.spec.ts

Which test would you like to watch?
```

### Step 2: Prepare User

```
Starting test in HEADED mode...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A browser window will open and you'll see:
• Each action the test performs
• What elements it interacts with
• The final result

WATCH FOR:
✓ Does the page load correctly?
✓ Does it find the right elements?
✓ Do actions complete successfully?
✓ Is timing appropriate?

Watch the browser window...
```

### Step 3: Execute

```bash
cd cursor-playwright && npx playwright test tests/[selected].spec.ts --headed
```

### Step 4: Report Result

**If passed:**
```
✓ TEST PASSED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You saw the test execute successfully!
The feature is working as expected.
```

**If failed:**
```
✗ TEST FAILED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Did you see what went wrong?

Common issues:
• Element not found (selector changed)
• Timing issue (page slow to load)
• Navigation problem
• Authentication issue

Based on what you saw:

If the feature WORKS when you try manually:
→ This is a FALSE NEGATIVE
→ Use: "Self-Heal [test-name]"

If the feature is BROKEN:
→ This is a TRUE NEGATIVE
→ Report to dev team

Would you like to:
a) Run again (slower, with 1s delay between actions)
b) Run in debug mode (step through each action)
c) Self-heal this test
```

### Step 5: Debug Mode Option

If user wants debug mode:
```bash
cd cursor-playwright && npx playwright test tests/[selected].spec.ts --debug
```

```
DEBUG MODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The Playwright Inspector has opened.

How to use:
• Click "Play" to start
• Click "Step over" to go one action at a time
• Hover over code to see what each line does
• Click "Resume" to continue

This helps pinpoint exactly where the test fails.
```

### Step 6: Slow Motion Option

```bash
cd cursor-playwright && npx playwright test tests/[selected].spec.ts --headed --slow-mo=1000
```

```
Running with 1 second delay between actions...
This makes it easier to see what's happening.
```
