---
name: Generate Test
description: Create a new automated E2E test by describing the behavior you want to test
---

# Generate New E2E Test

This command creates a new automated test based on your description. The AI will verify the behavior works, generate a robust test script, and set up self-healing capabilities.

## Trigger Phrases

Activate when user says:
- "Generate test"
- "Create test"
- "New test"
- "Generate E2E test"
- "Create automated test"
- "Add a test for..."

## Instructions for Cursor

This is a complex multi-step workflow. Follow each step carefully.

═══════════════════════════════════════════════════════════════
STEP 1: GATHER INFORMATION
═══════════════════════════════════════════════════════════════

### 1.1: Get Test Name
```
What would you like to name this test?

Suggested format: feature-name (lowercase with hyphens)
Examples: login-flow, checkout-process, search-products
```

Validate: must be lowercase with hyphens, no spaces.

### 1.2: Get Starting URL
```
What URL should this test start at?

Example: https://your-app.com/login
```

### 1.3: Get Behavior Description
```
Describe step-by-step what the test should do:

Example:
1. Navigate to login page
2. Enter email address
3. Enter password
4. Click login button
5. Verify user is redirected to dashboard
6. Verify welcome message is visible
```

### 1.4: Get Expected Outcome
```
What should happen if everything works correctly?

Example: "User should be logged in and see their dashboard"
```

═══════════════════════════════════════════════════════════════
STEP 2: CHECK ENVIRONMENT
═══════════════════════════════════════════════════════════════

### 2.1: Check and Update .env File (ADDITIVE ONLY)

```bash
test -f ../.env && echo "exists" || echo "not found"
```

**CRITICAL - ADDITIVE OPERATIONS ONLY:**

**If .env does NOT exist:**
1. Copy from template:
   ```bash
   cp ../.env.example ../.env
   ```
2. Extract base URL from starting URL (Step 1.2):
   - If full URL (e.g., `https://app.com/login`), extract base: `https://app.com`
   - If already base (e.g., `https://app.com`), use as-is
3. Add `APP_URL=[base-url]` to `.env` file (preserve all template content)
4. Prompt user for remaining credentials:
```
I've created .env and set APP_URL to [base-url] from your starting URL.

Please add these to .env (open the file and edit directly):
- TEST_USER_EMAIL: [your test email]
- TEST_USER_PASSWORD: [your test password]

⚠️ DO NOT paste credentials in chat - edit .env file directly.
```

**If .env EXISTS:**
1. Read current `.env` file to check existing values
2. Check if `APP_URL` exists and what its current value is
3. Extract base URL from starting URL (Step 1.2)
4. **If APP_URL is missing:**
   - Add `APP_URL=[base-url]` to end of `.env` file
   - Inform user: "Added APP_URL=[base-url] to .env"
5. **If APP_URL exists but is different:**
   - **REQUIRE USER CONFIRMATION BEFORE CHANGING:**
   ```
   ⚠️ APP_URL Change Required
   
   Current .env has: APP_URL=[current-value]
   Test needs: APP_URL=[new-base-url]
   
   This will update APP_URL in your .env file.
   All other values will be preserved.
   
   Proceed with updating APP_URL? (yes/no)
   ```
   - If user confirms "yes": Update only the APP_URL line, preserve all other lines
   - If user says "no": Stop and inform: "Test generation paused. Please update APP_URL manually or use a different URL."
6. **If APP_URL matches:** Inform user: "APP_URL already set correctly in .env"

**NEVER:**
- Overwrite entire .env file
- Remove existing variables
- Change values without user confirmation
- Use `cp` or `>` to replace .env

**ALWAYS:**
- Read existing .env first
- Append new variables or update specific lines only
- Preserve all existing values
- Show user what will change before changing
- Require confirmation for any value changes

═══════════════════════════════════════════════════════════════
STEP 3: VERIFY BEHAVIOR WITH BROWSER
═══════════════════════════════════════════════════════════════

```
Verifying behavior is achievable...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'm testing each step using a real browser.
Watch for the browser actions...
```

For EACH step in behavior:
1. Use browser_navigate to starting URL (first step)
2. Use browser_snapshot to see current page
3. Identify elements needed
4. Perform action (browser_click, browser_type, etc.)
5. Record element ref and action taken

If ANY step fails:
```
✗ Unable to verify behavior

Failed at step: [description]
Error: [message]

This means I couldn't complete this step in the browser.
Please verify manually and check:
- Is the URL correct?
- Are credentials correct?
- Is the application running?

STOPPING test generation.
```

If ALL steps succeed:
```
✓ Behavior verified successfully!

All steps completed:
✓ Navigate to login page
✓ Enter email address
✓ Enter password
✓ Click login button
✓ Verify dashboard

Moving to test generation...
```

═══════════════════════════════════════════════════════════════
STEP 4: GENERATE TEST SCRIPT
═══════════════════════════════════════════════════════════════

Use Context7 to get latest Playwright best practices.

Create test file: `cursor-playwright/tests/[test-name].spec.ts`

Template:
```typescript
import { test, expect } from '@playwright/test';
import * as dotenv from 'dotenv';
import * as path from 'path';

dotenv.config({ path: path.resolve(__dirname, '..', '..', '.env') });

test.describe('[Test Name]', () => {
  test('[behavior description]', async ({ page }) => {
    // Step 1: [description]
    await page.goto(process.env.APP_URL + '[path]');
    
    // Step 2: [description]
    await page.getByRole('textbox', { name: 'Email' }).fill(process.env.TEST_USER_EMAIL!);
    
    // Continue for each step...
    
    // Verify: [expected outcome]
    await expect(page.getByText('Welcome')).toBeVisible();
  });
});
```

Key requirements:
- Use dotenv with correct path to bot/.env
- Use process.env for ALL credentials
- Use robust locators (getByRole, getByLabel, getByText)
- Add comments for each step
- Include proper assertions

═══════════════════════════════════════════════════════════════
STEP 5: VERIFY TEST PASSES
═══════════════════════════════════════════════════════════════

```
Running generated test to verify...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```bash
cd cursor-playwright && npx playwright test tests/[test-name].spec.ts
```

Maximum 5 attempts. If fails:
- Analyze error
- Adjust locators/timing
- Regenerate and retry

If all 5 attempts fail:
```
✗ Couldn't generate a passing test after 5 attempts.

The behavior works but I couldn't create a reliable script.
The test file is saved for manual adjustment.

Location: cursor-playwright/tests/[test-name].spec.ts
```

═══════════════════════════════════════════════════════════════
STEP 6: CREATE SUPPORTING FILES
═══════════════════════════════════════════════════════════════

### 6.1: Create Behavior Documentation

File: `cursor-playwright/test-behaviors/[test-name].md`

```markdown
# [Test Name] - Expected Behavior

## Test File
`tests/[test-name].spec.ts`

## Purpose
[purpose description]

## Starting Point
- URL: [url]
- Prerequisites: Valid test credentials in .env

## Steps
1. [step 1]
2. [step 2]
...

## Expected Outcome
[outcome]

## Test Created
[timestamp]

## Last Verified
[timestamp]

## Notes
- Credentials read from .env file
- Never hardcode credentials
```

### 6.2: Create Self-Heal Command

File: `.cursor/commands/playwright/self-heal-[test-name].md`

```markdown
---
name: Self-Heal [Test Name]
description: Regenerate the [test-name] test when it fails but behavior still works
---

# Self-Heal [Test Name] Test

⚠️ Only use this if you verified the behavior WORKS manually
but the automated test is FAILING.

## Behavior Reference
Read from: `cursor-playwright/test-behaviors/[test-name].md`

## Test File
`cursor-playwright/tests/[test-name].spec.ts`

## Instructions for Cursor

1. Read behavior steps from behavior file
2. Use browser plugin to verify each step
3. Capture new element refs
4. Generate updated test script
5. Verify test passes
6. Maximum 5 attempts
7. Update "Last Verified" timestamp
```

═══════════════════════════════════════════════════════════════
STEP 7: FINAL CONFIRMATION
═══════════════════════════════════════════════════════════════

```
═══════════════════════════════════════════════════════════════
       TEST GENERATED SUCCESSFULLY! ✓
═══════════════════════════════════════════════════════════════

Test: [test-name]
File: cursor-playwright/tests/[test-name].spec.ts

Created:
✓ Test script
✓ Behavior documentation
✓ Self-heal command

Test Status:
✓ Behavior verified
✓ Script passes
✓ Ready for regression testing

NEXT STEP (Recommended):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run in headed mode to visually confirm:
Say "run test headed" and select [test-name]

Then save your work:
Say "save my work"

Would you like to run it in headed mode now?
```

═══════════════════════════════════════════════════════════════
SECURITY RULES
═══════════════════════════════════════════════════════════════

**NEVER:**
- Hardcode credentials in test files
- Include credentials in behavior docs
- Echo credentials in chat

**ALWAYS:**
- Read from process.env
- Reference .env file for credentials
- Remind user to use .env file
