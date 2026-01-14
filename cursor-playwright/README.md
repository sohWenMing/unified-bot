# Self-Healing E2E Test Framework

Welcome! This project helps you create and maintain automated tests for your web application without needing to be a programmer. The system can even fix broken tests automatically!

## 🎯 What This Does

This framework lets you:
- **Create tests by describing behavior** - Just explain what you want to test in plain English
- **Run tests automatically** - Check if your app is working correctly
- **Self-heal broken tests** - When your app's UI changes, tests can be regenerated automatically
- **Track changes with Git** - Save versions of your tests without knowing Git commands

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Your First Test](#your-first-test)
- [Running Tests](#running-tests)
- [When Tests Fail](#when-tests-fail)
- [Git Workflow (Version Control)](#git-workflow)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)
- [Understanding the Files](#understanding-the-files)

## 🚀 Getting Started

### Prerequisites

Before you begin, make sure you have:
- [ ] Node.js installed (version 16 or higher)
- [ ] Access to the web application you want to test
- [ ] Test user credentials (email/password)

### Initial Setup

1. **Open this project in Cursor**
   - The project is already set up with all necessary tools

2. **Configure Playwright MCP Server** (Required for test generation)
   - Open the file: `MCP_SETUP_INSTRUCTIONS.md`
   - Follow the instructions to enable the Playwright MCP server
   - This enables AI-powered test generation

3. **Install Dependencies**
   ```bash
   npm install
   ```

4. **Install Playwright Browsers**
   ```bash
   npx playwright install chromium
   ```

5. **Set Up Environment Variables**
   - Copy `.env.example` from the bot root to `.env` at the bot root
   - Edit `.env` and add your test credentials:
     ```
     APP_URL=https://your-app.com
     TEST_USER_EMAIL=test@example.com
     TEST_USER_PASSWORD=your_password
     ```
   - ⚠️ **Important**: Never share your `.env` file! It's automatically ignored by Git.

### Verification

Run this command to verify everything is set up:
```bash
npx playwright --version
```

You should see the Playwright version number.

## ✨ Your First Test

Let's create your first automated test! We'll use Cursor commands (no coding required).

### Step 1: Describe What You Want to Test

Think about a simple user journey, like:
- Logging in
- Searching for something
- Adding an item to cart
- Updating profile information

### Step 2: Run the Test Generation Command

In Cursor:
1. Open the command palette (Ctrl+Shift+P or Cmd+Shift+P)
2. Type: "Generate New E2E Test"
3. Select the command

### Step 3: Answer the Questions

The AI will ask you:

**Test Name**: Give it a descriptive name
- Good: `login-flow`, `checkout-process`, `search-products`
- Bad: `test1`, `my-test`, `asdf`

**Starting URL**: Where should the test begin?
- Example: `https://your-app.com/login`

**Behavior Description**: Describe step-by-step what should happen
```
Example:
1. Navigate to login page
2. Enter email address
3. Enter password
4. Click the "Log In" button
5. Verify the dashboard page loads
6. Verify welcome message is visible
```

**Expected Outcome**: What should happen if everything works?
- Example: "User should be logged in and see their dashboard"

### Step 4: Watch the Magic

The AI will:
1. ✅ Test your behavior in a real browser to verify it works
2. ✅ Generate a test script with robust selectors
3. ✅ Run the test to make sure it passes
4. ✅ Create a self-heal command for this test
5. ✅ Create documentation

### Step 5: Verify in Headed Mode

After generation, you'll be prompted to run the test in "headed mode" (where you can see the browser).

This is important! It confirms the test works correctly.

## 🏃 Running Tests

You have several options for running tests:

### Run All Tests

Use Cursor command: **"Run All Tests"**

This will:
- Run all tests in the background (headless)
- Generate a report
- Show you which tests passed and failed

### Run a Single Test

Use Cursor command: **"Run Single Test"**

Choose which test to run from the list.

### Run Test in Headed Mode (See the Browser)

Use Cursor command: **"Run Test in Headed Mode"**

This opens a browser window so you can watch the test execute.

Great for:
- Verifying new tests
- Debugging failures
- Understanding what the test does

### View Test Results

Use Cursor command: **"Analyze Test Results"**

This shows detailed results from your last test run and helps you understand what to do next.

## 🔧 When Tests Fail

When a test fails, there are two possibilities:

### False Negative (Test Needs Fixing)

**Situation**: The feature works when you test manually, but the automated test fails.

**Why**: The app's UI changed, but the feature still works.

**Solution**: Self-heal the test!

1. Manually verify the feature works in your browser
2. Use Cursor command: **"Self-Heal [Test Name]"**
   - Example: "Self-Heal Login Test"
3. The AI will regenerate the test to match current behavior
4. Verify the fixed test passes

### True Negative (Real Bug)

**Situation**: The feature doesn't work when you test manually.

**Why**: There's an actual bug in the application.

**Solution**: Report to development team!

1. Do NOT self-heal the test
2. Note down:
   - Test name
   - Error message
   - Screenshot (automatically saved on failure)
3. Contact development team
4. Wait for bug fix
5. Re-run test after fix

### Not Sure?

Use Cursor command: **"Run Test in Headed Mode"**
- Watch what happens
- See where it fails
- Decide: Is it the test or the app?

## 📝 Git Workflow (Version Control)

Git saves versions of your work. Here's how to use it without knowing Git commands:

### Save Your Changes (Commit)

**When**: After creating or fixing tests

**Command**: "Commit Changes"

Steps:
1. Run the command
2. You'll see what files changed
3. Provide a description:
   - Good: "Add login test", "Fix checkout test selectors"
   - Bad: "changes", "update", "test"
4. Changes are saved!

### View History

**Command**: "View Commit History"

See all previous versions of your work.

### Go Back to a Previous Version (Rollback)

⚠️ **Careful**: This undoes recent changes!

**Command**: "Rollback to Previous Commit"

Use when:
- You made a mistake
- Tests were working before
- Want to undo recent changes

The system creates a backup before rollback, so you can't lose work permanently.

### Create a New Branch (Separate Workspace)

**Command**: "Create New Branch"

Use when:
- Trying experimental tests
- Working on multiple features
- Don't want to affect main tests

Think of it as creating a copy where you can experiment safely.

### Upload to GitHub/GitLab (Push)

**Command**: "Push to Remote"

Use when:
- Want to backup tests online
- Share tests with team
- Deploy to server

## 🎯 Common Tasks

### Add a New Test

1. Command: "Generate New E2E Test"
2. Describe the behavior
3. Verify in headed mode
4. Command: "Commit Changes"

### Update an Existing Test

1. Verify behavior works manually
2. Command: "Self-Heal [Test Name]"
3. Verify regenerated test passes
4. Command: "Commit Changes"

### Check If Everything Works

1. Command: "Run All Tests"
2. Review results
3. Self-heal false negatives
4. Report true negatives

### Before Deploying New Code

1. Command: "Run All Tests"
2. All tests should pass
3. If failures, investigate
4. Don't deploy with failing tests

### Regular Regression Testing

Weekly or after major changes:
1. Command: "Run All Tests"
2. Command: "Analyze Test Results"
3. Fix or report issues
4. Commit any test updates

## 🔍 Troubleshooting

### Test Generation Fails

**Problem**: "Unable to verify behavior"

**Solutions**:
- Check the URL is correct
- Verify you can do it manually
- Check credentials in `.env` file
- Make sure app is running/accessible

### All Tests Suddenly Failing

**Problem**: Tests that worked before all fail now

**Possible Causes**:
- App is down
- Environment variables wrong
- Major UI redesign

**Solutions**:
- Check if app is accessible
- Verify `.env` file
- Contact development team

### Browser Doesn't Open in Headed Mode

**Problem**: Test runs but no browser window

**Solutions**:
```bash
npx playwright install chromium
```

Or reinstall browsers:
```bash
npx playwright install --with-deps
```

### Test is Flaky (Sometimes Passes, Sometimes Fails)

**Problem**: Inconsistent test results

**Likely Cause**: Timing issues

**Solution**:
1. Run in headed mode to observe
2. Regenerate test (self-heal command)
3. The new version may have better waits

### Permission Errors

**Problem**: Can't write files or run commands

**Solutions**:
- Check file permissions
- Don't run tests as admin/root
- Check disk space

### Git Errors

**Problem**: Git commands fail

**Solutions**:
- Make sure Git is installed
- Check you're in the project folder
- If stuck, create a new branch: "Create New Branch"

## 📂 Understanding the Files

Here's what each folder and file does:

```
project/
├── .cursor/
│   └── commands/           # Cursor commands (AI instructions)
│       ├── generate-test.md
│       ├── git-*.md
│       ├── test-*.md
│       └── self-heal-*.md  # Generated for each test
│
├── tests/                  # Your test scripts
│   ├── login-flow.spec.ts
│   └── *.spec.ts
│
├── test-behaviors/         # Human-readable test descriptions
│   └── *.md
│
├── test-results/           # Test execution results
│   └── results.json
│
├── playwright-report/      # HTML reports (auto-generated)
│
├── .env                    # Your credentials (SECRET - not in Git, at bot root)
├── .env.example            # Template for .env (at bot root)
├── .gitignore             # Tells Git what NOT to save
├── playwright.config.ts   # Test configuration
├── package.json           # Project dependencies
└── README.md              # This file!
```

### Files You'll Edit

- **`.env`**: Your credentials (after initial setup)

### Files Created Automatically

- **`tests/*.spec.ts`**: Test scripts (by "Generate New E2E Test")
- **`test-behaviors/*.md`**: Test documentation (auto-generated)
- **`.cursor/commands/self-heal-*.md`**: Self-heal commands (auto-generated)
- **`test-results/`**: Test results (after running tests)
- **`playwright-report/`**: Pretty HTML reports (after running tests)

### Files You Shouldn't Change

- **`playwright.config.ts`**: Test settings (pre-configured)
- **`package.json`**: Dependencies list
- **`.gitignore`**: Git ignore rules
- **`.cursorrules`**: AI behavior rules

## 🎓 Best Practices

### Test Creation

✅ **DO**:
- Give tests descriptive names
- Test one feature per test file
- Verify tests in headed mode after creation
- Commit tests after they work

❌ **DON'T**:
- Create tests for behaviors that don't work
- Skip manual verification
- Edit test files manually (unless you know TypeScript)
- Share your `.env` file

### Test Maintenance

✅ **DO**:
- Run all tests before deploying
- Self-heal tests when UI changes
- Keep test descriptions updated
- Commit test changes

❌ **DON'T**:
- Self-heal tests without verifying behavior works
- Ignore test failures
- Delete tests without understanding why
- Force push to main branch

### Version Control

✅ **DO**:
- Commit after each test creation/fix
- Use descriptive commit messages
- Create branches for experiments
- Push to backup regularly

❌ **DON'T**:
- Commit broken tests
- Use vague commit messages
- Rollback without creating backup branch
- Force push without understanding consequences

## 📞 Getting Help

### Built-in Help

Each Cursor command has detailed instructions. Just run the command and follow the prompts.

### Common Questions

**Q: Do I need to know programming?**
A: No! The AI generates all code for you.

**Q: What if I break something?**
A: Git saves all versions. Use "Rollback to Previous Commit" to undo changes.

**Q: Can I edit the test files manually?**
A: You can, but it's easier to regenerate using self-heal commands.

**Q: How often should I run tests?**
A: After any significant changes, before deployments, and weekly for regression.

**Q: What browsers are supported?**
A: Chromium (Chrome-like) by default. Can be configured for Firefox and WebKit.

## 🎉 Success Tips

1. **Start Small**: Create one simple test first (like login)
2. **Verify Everything**: Always run tests in headed mode after creation
3. **Commit Often**: Save your work frequently
4. **Document Issues**: Note down test failures for team
5. **Self-Heal Proactively**: Fix tests as soon as UI changes
6. **Run Regularly**: Schedule weekly test runs

## 📚 Additional Resources

- [Playwright Documentation](https://playwright.dev) - For advanced users
- [Context7 Playwright Docs](https://context7.com) - Latest best practices
- `MCP_SETUP_INSTRUCTIONS.md` - MCP server setup guide
- `.cursorrules` - Framework behavior rules (for reference)

## 🤝 Contributing

If you discover ways to improve this framework:
1. Document the issue or enhancement
2. Share with the team
3. Consider updating this README

---

**Remember**: This framework is designed to make testing easy and maintainable. If something feels too complicated, there's probably a simpler way. Use the Cursor commands and let the AI do the heavy lifting!

Happy Testing! 🚀
