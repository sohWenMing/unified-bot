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

⚠️ **CRITICAL REQUIREMENT: BROWSER VERIFICATION IS MANDATORY**

**YOU MUST complete Step 3 (Browser Verification) BEFORE proceeding to Step 4 (Test Generation).**

- **NEVER skip browser verification**
- **NEVER write test code without first verifying behavior in browser**
- **NEVER assume element structure - always verify with browser plugin**
- **ALWAYS capture element references from browser snapshots**
- **ALWAYS use browser-verified selectors in generated test code**

Failure to follow this requirement will result in unreliable tests.

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
STEP 3: VERIFY BEHAVIOR WITH BROWSER (MANDATORY)
═══════════════════════════════════════════════════════════════

⚠️ **CRITICAL: THIS STEP IS MANDATORY - DO NOT SKIP OR PROCEED WITHOUT IT**

**YOU MUST USE THE BROWSER PLUGIN TO VERIFY BEHAVIOR BEFORE WRITING ANY TEST CODE.**

```
Verifying behavior is achievable...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'm testing each step using a real browser.
Watch for the browser actions...
```

**REQUIRED WORKFLOW - Follow EXACTLY:**

For EACH step in the behavior description:

1. **Navigate to page** (first step only):
   - Use `browser_navigate` with the starting URL from Step 1.2
   - Wait for page to load: `browser_wait_for` with appropriate time

2. **Capture page structure**:
   - Use `browser_snapshot` to see the current page state
   - Analyze the snapshot to understand page structure
   - Identify all elements needed for this step

3. **Record element information**:
   - For each element you need to interact with:
     - Note the element's text, role, or other identifying characteristics
     - Record the element reference (ref) from the snapshot
     - Document what action will be performed (click, type, select, etc.)

4. **Perform the action**:
   - Use appropriate browser plugin tool:
     - `browser_click` for buttons/links
     - `browser_type` for input fields
     - `browser_select_option` for dropdowns
     - `browser_fill_form` for multiple fields
   - Use the element ref from the snapshot
   - Wait for any page changes: `browser_wait_for` if needed

5. **Verify step completion**:
   - Take another `browser_snapshot` to confirm action succeeded
   - Verify expected state change occurred
   - Record any element references that changed

6. **Document findings**:
   - Record element refs used
   - Record selectors/identifiers that worked
   - Note any timing requirements
   - Document any special handling needed

**CRITICAL RULES:**

- **NEVER write test code before completing browser verification**
- **NEVER skip browser verification even if behavior seems obvious**
- **NEVER assume element structure - always verify with browser**
- **ALWAYS capture element refs from browser snapshots**
- **ALWAYS perform actual actions in browser, not just inspect**

**If ANY step fails:**

```
✗ Unable to verify behavior

Failed at step: [description]
Error: [message]

This means I couldn't complete this step in the browser.
Please verify manually and check:
- Is the URL correct?
- Are credentials correct?
- Is the application running?
- Is VPN/network access required?

STOPPING test generation.
DO NOT proceed to test code generation.
```

**If ALL steps succeed:**

```
✓ Behavior verified successfully!

All steps completed:
✓ Navigate to login page
✓ Located Login Type dropdown
✓ Selected "Local" option
✓ Entered username
✓ Entered password
✓ Clicked login button
✓ Verified dashboard loaded
✓ Verified StudentAppBackOffice header
✓ Clicked logout

Element references captured:
- Login Type dropdown: [ref]
- Username field: [ref]
- Password field: [ref]
- Login button: [ref]
- Header element: [ref]
- Logout element: [ref]

Moving to test generation...
```

**ONLY AFTER successful browser verification, proceed to Step 4.**

═══════════════════════════════════════════════════════════════
STEP 4: GENERATE TEST SCRIPT (USING BROWSER CAPTURED DATA)
═══════════════════════════════════════════════════════════════

⚠️ **CRITICAL: Use ONLY the element references and selectors captured from Step 3 browser verification.**

**DO NOT guess or assume element structure - use what you verified in the browser.**

Use Context7 to get latest Playwright best practices for locator strategies.

Create test file: `cursor-playwright/tests/[test-name].spec.ts`

**Locator Strategy Priority (based on browser verification):**

1. **getByRole()** - Preferred for accessibility and resilience
   - Use when element has semantic role (button, textbox, combobox, etc.)
   - Example: `page.getByRole('button', { name: 'Login' })`

2. **getByLabel()** - Excellent for form fields with labels
   - Use when label text was visible in browser snapshot
   - Example: `page.getByLabel('Username')`

3. **getByText()** - For visible text content
   - Use when text was visible in browser snapshot
   - Example: `page.getByText('StudentAppBackOffice')`

4. **getByPlaceholder()** - For inputs with placeholder text
   - Use when placeholder was visible in browser snapshot

5. **locator() with CSS/XPath** - Last resort, only if above don't work
   - Use element refs from browser snapshot to construct selectors
   - Prefer stable attributes (id, data-testid) over classes

**Template (using captured browser data):**

```typescript
import { test, expect } from '@playwright/test';
import * as dotenv from 'dotenv';
import * as path from 'path';

dotenv.config({ path: path.resolve(__dirname, '..', '..', '.env') });

test.describe('[Test Name]', () => {
  test('[behavior description]', async ({ page }) => {
    // Step 1: Navigate to [description]
    // URL verified in browser: [actual URL used]
    await page.goto('[starting URL from Step 1.2]');
    
    // Step 2: [description]
    // Element verified in browser: [element ref/description]
    // Selector strategy: [getByRole/getByLabel/etc based on browser snapshot]
    await page.getByRole('combobox', { name: 'Login Type' }).selectOption('Local');
    
    // Step 3: [description]
    // Element verified in browser: [element ref/description]
    const usernameField = page.getByLabel('Username'); // or getByRole based on browser verification
    await usernameField.fill(process.env.TEST_USER_EMAIL!);
    
    // Continue for each step using browser-verified selectors...
    
    // Verify: [expected outcome]
    // Element verified in browser: [element ref/description]
    await expect(page.getByText('StudentAppBackOffice')).toBeVisible();
  });
});
```

**Key requirements:**

- **USE BROWSER-VERIFIED SELECTORS**: Only use locators you verified work in Step 3
- Use dotenv with correct path to bot/.env
- Use process.env for ALL credentials (TEST_USER_EMAIL, TEST_USER_PASSWORD)
- Match locator strategy to what worked in browser verification
- Add comments referencing browser verification for each step
- Include proper assertions based on browser-verified outcomes
- Add appropriate waits based on timing observed in browser

**For each step, include comment:**
```typescript
// Verified in browser: [what you saw/clicked/typed]
// Element ref: [if available from snapshot]
// Selector: [why you chose this locator strategy]
```

═══════════════════════════════════════════════════════════════
STEP 5: VERIFY TEST PASSES (MANDATORY - TEST MUST PASS)
═══════════════════════════════════════════════════════════════

⚠️ **CRITICAL: THE TEST SCRIPT MUST RUN AND PASS BEFORE PROCEEDING TO STEP 6.**

**DO NOT proceed to Step 6 (Create Supporting Files) unless the test passes.**

```
Running generated test to verify...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**REQUIRED WORKFLOW:**

1. **Run the test script:**
   ```bash
   cd cursor-playwright && npx playwright test tests/[test-name].spec.ts
   ```

2. **Check exit code:**
   - Exit code 0 = Test passed ✓
   - Exit code non-zero = Test failed ✗

3. **If test PASSES (exit code 0):**
   ```
   ✓ Test passed successfully!
   
   Test execution summary:
   - Tests run: 1
   - Passed: 1
   - Failed: 0
   
   Proceeding to Step 6...
   ```
   **ONLY THEN proceed to Step 6.**

4. **If test FAILS (exit code non-zero):**
   - Analyze the error output
   - Check what failed (locator, timing, assertion, etc.)
   - Adjust the test script:
     - Fix locators based on error
     - Add/adjust waits if timing issue
     - Fix assertions if verification failed
     - Update selectors if elements not found
   - Regenerate test file with fixes
   - Run test again

5. **Maximum 5 attempts:**
   - Attempt 1: Initial test run
   - Attempt 2-5: Fix and retry
   - After each failure, analyze and fix before retrying

6. **If test passes within 5 attempts:**
   ```
   ✓ Test passed on attempt [N]!
   
   Proceeding to Step 6...
   ```

7. **If all 5 attempts fail:**
   ```
   ✗ CRITICAL: Couldn't generate a passing test after 5 attempts.
   
   Test generation FAILED.
   The test script does not pass and cannot be considered complete.
   
   Last error: [error message from last attempt]
   
   Location: cursor-playwright/tests/[test-name].spec.ts
   
   OPTIONS:
   1. Review the test file manually and fix issues
   2. Verify the behavior still works in browser
   3. Check if .env credentials are correct
   4. Try generating test again with more specific behavior description
   
   STOPPING test generation.
   DO NOT proceed to Step 6.
   DO NOT create supporting files.
   ```
   
   **STOP HERE. Do NOT proceed to Step 6.**
   **Test generation is INCOMPLETE until test passes.**

**VERIFICATION REQUIREMENTS:**

- ✓ Test file exists
- ✓ Test file compiles without syntax errors
- ✓ Test executes without runtime errors
- ✓ Test passes (exit code 0)
- ✓ All assertions pass
- ✓ All steps complete successfully

**ONLY when ALL requirements are met, proceed to Step 6.**

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
STEP 7: FINAL CONFIRMATION (ONLY IF TEST PASSED)
═══════════════════════════════════════════════════════════════

⚠️ **ONLY show this confirmation if Step 5 test execution PASSED.**

**DO NOT show success message if test did not pass.**

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

Verification Status:
✓ Behavior verified in browser (Step 3)
✓ Test script generated (Step 4)
✓ Test executed successfully (Step 5)
✓ Test passed (exit code 0)
✓ All assertions passed
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
