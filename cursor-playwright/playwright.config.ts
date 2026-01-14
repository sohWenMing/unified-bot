import { defineConfig, devices } from '@playwright/test';
import * as dotenv from 'dotenv';
import * as path from 'path';

// Load environment variables from bot-level .env
// This allows unified configuration across all bot components
dotenv.config({ path: path.resolve(__dirname, '..', '.env') });

/**
 * Playwright configuration for self-healing automated E2E tests
 * See https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './tests',
  
  /* Run tests in files in parallel */
  fullyParallel: true,
  
  /* Fail the build on CI if you accidentally left test.only in the source code */
  forbidOnly: !!process.env.CI,
  
  /* Retry on CI only - we handle self-healing differently */
  retries: 0,
  
  /* Opt out of parallel tests on CI */
  workers: process.env.CI ? 1 : undefined,
  
  /* Reporter configuration - HTML for visual review, JSON for programmatic parsing */
  reporter: [
    ['html', { open: 'never', outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list']
  ],
  
  /* Shared settings for all the projects below */
  use: {
    /* Base URL from environment variables */
    baseURL: process.env.APP_URL,
    
    /* Collect trace on failure for debugging */
    trace: 'on-first-retry',
    
    /* Screenshot on failure only */
    screenshot: 'only-on-failure',
    
    /* Video on failure only */
    video: 'retain-on-failure',
    
    /* Timeout for each action (e.g., click, fill) */
    actionTimeout: 10000,
    
    /* Navigation timeout */
    navigationTimeout: 30000,
  },
  
  /* Global timeout for each test */
  timeout: 60000,
  
  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  
  /* Run your local dev server before starting the tests */
  // webServer: {
  //   command: 'npm run start',
  //   url: 'http://127.0.0.1:3000',
  //   reuseExistingServer: !process.env.CI,
  // },
});
