# Testing Checklist for Self-Healing E2E Framework

This checklist helps you verify the framework is set up correctly and working as expected.

## 🔧 Initial Setup Verification

### Prerequisites Check
- [ ] Node.js installed (run: `node --version`)
- [ ] Git initialized (run: `git status`)
- [ ] Dependencies installed (run: `npm list`)
- [ ] Playwright browsers installed (run: `npx playwright --version`)

### Configuration Check
- [ ] `playwright.config.ts` exists and is valid
- [ ] `tsconfig.json` exists
- [ ] `.gitignore` includes `.env` and `node_modules/`
- [ ] `.env.example` exists at bot root as a template
- [ ] `.cursorrules` file exists with framework rules

### Directory Structure Check
```bash
# Run this to verify structure:
ls -la .cursor/commands/
ls -la tests/
ls -la test-behaviors/
```

Should see:
- [ ] `.cursor/commands/` directory with command files
- [ ] `tests/` directory (empty initially)
- [ ] `test-behaviors/` directory (empty initially)

## 🎯 MCP Server Setup

### Playwright MCP Configuration
- [ ] Read `MCP_SETUP_INSTRUCTIONS.md`
- [ ] Added Playwright MCP to Cursor settings
- [ ] Restarted Cursor after configuration
- [ ] Can see Playwright MCP in available MCP servers

To verify MCP is working:
1. In Cursor, check MCP servers list
2. Should see "playwright" server with "testing" capability

## 📝 Cursor Commands Verification

Check that all commands are available in Cursor:

### Git Commands
- [ ] "Commit Changes" command exists
- [ ] "View Commit History" command exists
- [ ] "Rollback to Previous Commit" command exists
- [ ] "Create New Branch" command exists
- [ ] "Push to Remote" command exists

### Test Execution Commands
- [ ] "Run All Tests" command exists
- [ ] "Run Single Test" command exists
- [ ] "Run Test in Headed Mode" command exists
- [ ] "Analyze Test Results" command exists

### Test Generation Command
- [ ] "Generate New E2E Test" command exists

## 🚀 End-to-End Workflow Test

### Prepare Test Environment

1. **Create `.env` file**
   ```bash
   cp ../.env.example ../.env
   ```

2. **Edit `.env` with real test data**
   ```
   APP_URL=https://your-actual-app.com
   TEST_USER_EMAIL=your-test@email.com
   TEST_USER_PASSWORD=your-test-password
   ```
   - [ ] `.env` file created
   - [ ] Real application URL added
   - [ ] Valid test credentials added

3. **Verify credentials work**
   - [ ] Manually log into application with test credentials
   - [ ] Credentials are valid

### Test 1: Generate Your First Test

**Objective**: Create a simple login test

1. **Run Command**: "Generate New E2E Test"
   - [ ] Command executes without errors

2. **Provide Information**:
   - Test Name: `login-flow`
   - Starting URL: `[your-app]/login`
   - Behavior Steps:
     ```
     1. Navigate to login page
     2. Enter email address
     3. Enter password
     4. Click login button
     5. Verify dashboard is visible
     ```
   - Expected Outcome: "User is logged in and sees dashboard"
   - [ ] All information provided

3. **Verify Browser Plugin Execution**
   - [ ] Browser plugin navigates to login page
   - [ ] Browser plugin enters credentials
   - [ ] Browser plugin clicks login
   - [ ] Browser plugin verifies success
   - [ ] No errors during browser verification

4. **Verify Test File Generation**
   - [ ] `tests/login-flow.spec.ts` created
   - [ ] File contains proper imports
   - [ ] File uses `process.env` for credentials
   - [ ] File has descriptive comments
   - [ ] File uses Playwright best practices (getByRole, etc.)

5. **Verify Test Execution**
   - [ ] Test runs automatically after generation
   - [ ] Test passes on first attempt (or within 5 attempts)
   - [ ] No runtime errors

6. **Verify Supporting Files**
   - [ ] `test-behaviors/login-flow.md` created
   - [ ] Behavior doc contains all steps
   - [ ] `.cursor/commands/self-heal-login-flow.md` created
   - [ ] Self-heal command has correct test path

7. **Verify in Headed Mode**
   - [ ] Run: "Run Test in Headed Mode"
   - [ ] Select: `login-flow.spec.ts`
   - [ ] Browser window opens
   - [ ] Can see each action happening
   - [ ] Test completes successfully

### Test 2: Run Test Suite

**Objective**: Verify test execution commands work

1. **Run All Tests**
   - [ ] Command: "Run All Tests"
   - [ ] Shows test execution progress
   - [ ] Displays summary (Total, Passed, Failed)
   - [ ] HTML report generated
   - [ ] Can open report in browser

2. **Run Single Test**
   - [ ] Command: "Run Single Test"
   - [ ] Shows list of available tests
   - [ ] Can select test
   - [ ] Test runs successfully
   - [ ] Results displayed clearly

3. **Analyze Results**
   - [ ] Command: "Analyze Test Results"
   - [ ] Shows test summary
   - [ ] Lists passed tests
   - [ ] Provides guidance for any failures

### Test 3: Self-Healing Workflow

**Objective**: Verify self-healing capability

**Setup**: Manually break a test to simulate UI change

1. **Modify Test File to Force Failure**
   - Open: `tests/login-flow.spec.ts`
   - Change a locator to something that won't exist
   - Example: Change `getByRole('button', { name: 'Login' })` to `getByRole('button', { name: 'NonExistentButton' })`
   - [ ] Test file modified

2. **Run Test to Confirm Failure**
   - [ ] Command: "Run Single Test"
   - [ ] Select: `login-flow.spec.ts`
   - [ ] Test fails as expected
   - [ ] Error message is clear

3. **Manually Verify Behavior Works**
   - [ ] Open browser manually
   - [ ] Can complete login successfully
   - [ ] Confirmed behavior still works

4. **Run Self-Heal Command**
   - [ ] Command: "Self-Heal Login Flow Test"
   - [ ] AI verifies behavior with browser plugin
   - [ ] New test file generated
   - [ ] Test passes after regeneration

5. **Verify Fixed Test**
   - [ ] Run test again
   - [ ] Test now passes
   - [ ] Test file has updated locators
   - [ ] Behavior doc updated with timestamp

### Test 4: Git Workflow

**Objective**: Verify Git commands work for non-technical users

1. **View History**
   - [ ] Command: "View Commit History"
   - [ ] Shows initial commit (if any)
   - [ ] Display is user-friendly

2. **Commit Changes**
   - [ ] Command: "Commit Changes"
   - [ ] Shows changed files (test files)
   - [ ] Prompts for commit message
   - [ ] Enter: "Add login test"
   - [ ] Commit succeeds
   - [ ] Confirmation displayed

3. **View Updated History**
   - [ ] Command: "View Commit History"
   - [ ] Shows new commit
   - [ ] Commit message visible

4. **Create Branch**
   - [ ] Command: "Create New Branch"
   - [ ] Enter: "test-experiment"
   - [ ] Branch created successfully
   - [ ] Switched to new branch

5. **Return to Main Branch**
   - [ ] Run: `git checkout main` (or use command if available)
   - [ ] Switched back successfully

6. **Test Rollback (Optional - Careful!)**
   - [ ] Command: "Rollback to Previous Commit"
   - [ ] Shows recent commits
   - [ ] Shows warning about data loss
   - [ ] Creates backup branch
   - [ ] Can successfully rollback
   - [ ] Can restore from backup if needed

### Test 5: Error Handling

**Objective**: Verify graceful error handling

1. **Test Generation with Invalid URL**
   - [ ] Run: "Generate New E2E Test"
   - [ ] Provide invalid URL
   - [ ] System detects and reports error clearly
   - [ ] Suggests next steps

2. **Test Generation with Impossible Behavior**
   - [ ] Run: "Generate New E2E Test"
   - [ ] Describe behavior that doesn't exist in app
   - [ ] Browser verification fails
   - [ ] Clear error message
   - [ ] Test generation stops (doesn't create bad test)

3. **Self-Heal Without Manual Verification**
   - [ ] Try to self-heal when behavior is actually broken
   - [ ] System attempts healing
   - [ ] Reports if unable to create working test
   - [ ] Provides clear guidance

## 📊 Success Criteria

All of the following should be true:

### Framework Setup
- ✅ All dependencies installed
- ✅ All configuration files in place
- ✅ Directory structure correct
- ✅ MCP server configured

### Test Generation
- ✅ Can generate test from behavior description
- ✅ Browser plugin verifies behavior
- ✅ Test file created with best practices
- ✅ Test passes when executed
- ✅ Supporting files created

### Test Execution
- ✅ Can run all tests
- ✅ Can run single test
- ✅ Can run in headed mode
- ✅ Can analyze results
- ✅ Reports are generated

### Self-Healing
- ✅ Can detect test failures
- ✅ Can regenerate tests
- ✅ Regenerated tests pass
- ✅ Self-heal commands work

### Git Workflow
- ✅ Can commit changes
- ✅ Can view history
- ✅ Can create branches
- ✅ Can rollback safely
- ✅ Can push to remote (if configured)

### Error Handling
- ✅ Invalid inputs handled gracefully
- ✅ Errors explained clearly
- ✅ Next steps provided
- ✅ No system crashes

### Documentation
- ✅ README is comprehensive
- ✅ Commands have clear instructions
- ✅ Examples are helpful
- ✅ Non-technical language used

## 🐛 Common Issues and Solutions

### Issue: Test generation fails at browser verification
**Solution**: 
- Check app URL is correct
- Verify app is accessible
- Check credentials in `.env`

### Issue: Generated test uses wrong locators
**Solution**:
- Regenerate using self-heal command
- Ensure Playwright MCP is configured
- Check Context7 integration

### Issue: Tests are flaky (inconsistent)
**Solution**:
- Run in headed mode to observe
- Regenerate test for better waits
- Check for dynamic content issues

### Issue: Git commands fail
**Solution**:
- Verify Git is installed
- Check you're in project directory
- Ensure no unstaged changes blocking operation

## ✅ Final Verification

Once all tests pass:

- [ ] Framework is fully functional
- [ ] Documentation is clear and helpful
- [ ] Commands work as expected
- [ ] Ready for production use
- [ ] Team members can use without programming knowledge

## 📝 Notes

Use this space to document any issues or customizations:

```
Date: ___________
Tested by: ___________

Notes:
_________________________________
_________________________________
_________________________________

Issues found:
_________________________________
_________________________________
_________________________________

Resolutions:
_________________________________
_________________________________
_________________________________
```

---

**Congratulations!** If you've completed this checklist successfully, your self-healing E2E test framework is ready to use! 🎉
