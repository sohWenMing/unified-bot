# Login Flow Test

## Test Name
`login-flow`

## Purpose
This test verifies the complete login and logout flow for the StudentAppBackOffice application.

## Starting URL
`https://dev-simattendance.simge.edu.sg/StudentAppBackOffice/Login`

## Test Steps

1. **Navigate to the login page**
   - Opens the StudentAppBackOffice login page

2. **Locate Login Type dropdown**
   - Finds the dropdown element associated with the "Login Type" label

3. **Select "Local" option**
   - Selects "Local" from the Login Type dropdown

4. **Enter username**
   - Reads `TEST_USER_EMAIL` from `.env` file
   - Enters the username into the input field below the "Username" label

5. **Enter password**
   - Reads `TEST_USER_PASSWORD` from `.env` file
   - Enters the password into the input field below the "Password" label

6. **Click Login button**
   - Clicks the Login button to submit credentials

7. **Wait for page load**
   - Waits for the page to fully load after login redirect
   - Ensures network requests are complete

8. **Verify StudentAppBackOffice header**
   - Verifies that an element with text "StudentAppBackOffice" is visible
   - Confirms it appears in the top right corner of the page

9. **Logout**
   - Clicks on the element with text "Student App IT Admin" to logout
   - Waits for logout to complete

## Expected Outcome
- User successfully logs in with Local login type
- Page redirects and loads correctly
- "StudentAppBackOffice" header is visible in the top right corner
- User can successfully logout by clicking "Student App IT Admin"

## Environment Variables Required
- `TEST_USERNAME` or `TEST_USER_EMAIL` - Test user username/email address
- `TEST_PASSWORD` or `TEST_USER_PASSWORD` - Test user password

## Self-Heal Command
To regenerate this test if the UI changes:
```
Self-Heal login-flow
```

## Generated
Generated on: 2026-01-14
