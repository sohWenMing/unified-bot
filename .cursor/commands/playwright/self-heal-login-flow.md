---
name: Self-Heal Login Flow
description: Regenerate the login-flow test when it fails but behavior still works
---

# Self-Heal Login Flow Test

⚠️ Only use this if you verified the behavior WORKS manually
but the automated test is FAILING.

## Behavior Reference
Read from: `cursor-playwright/test-behaviors/login-flow.md`

## Test File
`cursor-playwright/tests/login-flow.spec.ts`

## Instructions for Cursor

1. **Read behavior steps** from `cursor-playwright/test-behaviors/login-flow.md`

2. **Verify behavior works manually**:
   - User must confirm: "I verified the login flow works when I test it manually"
   - If user cannot confirm, STOP and ask them to verify first

3. **Use browser plugin to verify each step**:
   - Navigate to: `https://dev-simattendance.simge.edu.sg/StudentAppBackOffice/Login`
   - Use `browser_snapshot` to capture page structure
   - Perform each step and capture element references
   - Record what selectors work

4. **Generate updated test script**:
   - Use browser-verified selectors only
   - Update `cursor-playwright/tests/login-flow.spec.ts`
   - Use same environment variables: `TEST_USERNAME`/`TEST_USER_EMAIL` and `TEST_PASSWORD`/`TEST_USER_PASSWORD`

5. **MUST run test to verify it passes** (exit code 0):
   ```bash
   cd cursor-playwright && npx playwright test tests/login-flow.spec.ts
   ```
   - If fails: Analyze error, fix, and retry (max 5 attempts)
   - **DO NOT consider self-heal complete unless test passes**

6. **Maximum 5 attempts**:
   - Attempt 1: Initial regeneration
   - Attempts 2-5: Fix and retry based on errors

7. **If test passes**:
   - Update "Last Verified" timestamp in behavior file
   - Inform user: "✓ Test regenerated and passing"

8. **If all 5 attempts fail**:
   - Report to user for manual intervention
   - Test file saved for manual adjustment

## Original Behavior Steps

1. Navigate to the login page
2. Locate the dropdown under the element with the text "Login Type"
3. In the dropdown, select the "Local" option
4. For username, read from the Testing Configuration in the .env file and enter it into the input field underneath the element with the text Username
5. For password, read from the Testing Configuration in the .env file and enter it into the input field underneath the element with the text Password
6. Press the Login button
7. On redirect after login, wait for the page to load
8. Verify that there is an element in the top right corner of the page with the text "StudentAppBackOffice"
9. Logout of the page by clicking on the element with the text "Student App IT Admin"

## Environment Variables

- `TEST_USERNAME` or `TEST_USER_EMAIL` - Test user credentials
- `TEST_PASSWORD` or `TEST_USER_PASSWORD` - Test user password

## Generated

Generated on: 2026-01-14
