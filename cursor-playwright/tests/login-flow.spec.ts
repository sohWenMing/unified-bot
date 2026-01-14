import { test, expect } from '@playwright/test';
import * as dotenv from 'dotenv';
import * as path from 'path';

// Load environment variables from bot-level .env
dotenv.config({ path: path.resolve(__dirname, '..', '..', '.env') });

test.describe('Login Flow', () => {
  test('should successfully login and logout', async ({ page }) => {
    // Step 1: Navigate to the login page
    // Verified in browser: URL loads login page with Login Type dropdown
    await page.goto('https://dev-simattendance.simge.edu.sg/StudentAppBackOffice/Login');
    
    // Step 2: Locate the dropdown under the element with the text "Login Type"
    // Verified in browser: Element ref=e16 contains text "Login Type"
    const loginTypeLabel = page.getByText('Login Type');
    await expect(loginTypeLabel).toBeVisible();
    
    // Step 3: In the dropdown, select the "Local" option
    // Verified in browser: combobox [ref=e18] with id #LoginType, contains options "Local" and "Staff"
    // Selector strategy: Using ID selector verified in browser (Playwright code showed #LoginType)
    const loginTypeDropdown = page.locator('#LoginType');
    await loginTypeDropdown.selectOption({ label: 'Local' });
    
    // Wait for form fields to appear after selecting Local
    await page.waitForSelector('input[type="text"]', { state: 'visible' });
    
    // Step 4: For username, read from the Testing Configuration in the .env file
    // and enter it into the input field underneath the element with the text Username
    // Verified in browser: textbox [ref=e24] with label "Username*" [ref=e22]
    // Selector strategy: Using getByLabel for form field with visible label
    const usernameLabel = page.getByText('Username', { exact: false });
    await expect(usernameLabel).toBeVisible();
    
    const usernameField = page.getByLabel('Username', { exact: false });
    // Check for TEST_USERNAME (used in .env) or TEST_USER_EMAIL
    const testUsername = process.env.TEST_USERNAME || process.env.TEST_USER_EMAIL;
    if (!testUsername) {
      throw new Error('TEST_USERNAME or TEST_USER_EMAIL must be set in .env file');
    }
    await usernameField.fill(testUsername);
    
    // Step 5: For password, read from the Testing Configuration in the .env file
    // and enter it into the input field underneath the element with the text Password
    // Verified in browser: textbox [ref=e28] with label "Password*" [ref=e26], type="password"
    // Selector strategy: Using getByRole for password textbox to avoid matching checkbox
    const passwordLabel = page.getByText('Password', { exact: false });
    await expect(passwordLabel).toBeVisible();
    
    const passwordField = page.getByRole('textbox', { name: /Password/i });
    // Check for TEST_PASSWORD (used in .env) or TEST_USER_PASSWORD
    const testPassword = process.env.TEST_PASSWORD || process.env.TEST_USER_PASSWORD;
    if (!testPassword) {
      throw new Error('TEST_PASSWORD or TEST_USER_PASSWORD must be set in .env file');
    }
    await passwordField.fill(testPassword);
    
    // Step 6: Press the Login button
    // Verified in browser: button [ref=e43] with text "Login"
    // Selector strategy: Using getByRole for button with accessible name
    const loginButton = page.getByRole('button', { name: 'Login' });
    await loginButton.click();
    
    // Step 7: On redirect after login, wait for the page to load
    await page.waitForLoadState('networkidle');
    await page.waitForLoadState('domcontentloaded');
    
    // Step 8: Verify that there is an element in the top right corner of the page
    // with the text "StudentAppBackOffice"
    // Verified in browser: heading [ref=e13] with text "StudentAppBackOffice" (level=1)
    // Selector strategy: Using getByText and taking first match (multiple elements exist)
    const headerElement = page.getByText('StudentAppBackOffice', { exact: false }).first();
    await expect(headerElement).toBeVisible();
    
    // Verify it's in the top portion of the page (position check)
    const boundingBox = await headerElement.boundingBox();
    if (boundingBox) {
      const viewportSize = page.viewportSize();
      if (viewportSize) {
        // Check if element is in the top portion of the page (top 50% of screen)
        const isInTopPortion = boundingBox.y < viewportSize.height * 0.5;
        expect(isInTopPortion).toBeTruthy();
      }
    }
    
    // Step 9: Logout of the page by clicking on the element with the text "Student App IT Admin"
    // Note: This element will be verified after login - need to check actual page structure
    // Selector strategy: Using getByText for logout element
    const logoutElement = page.getByText('Student App IT Admin', { exact: false });
    await expect(logoutElement).toBeVisible();
    await logoutElement.click();
    
    // Wait for logout to complete
    await page.waitForLoadState('networkidle');
  });
});
