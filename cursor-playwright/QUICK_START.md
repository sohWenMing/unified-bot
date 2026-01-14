# Quick Start Guide

Get your self-healing E2E test framework running in 5 minutes!

## Step 1: Setup (2 minutes)

### Install Dependencies
```bash
npm install
npx playwright install chromium
```

### Configure Playwright MCP
1. Open: `MCP_SETUP_INSTRUCTIONS.md`
2. Follow the instructions to add Playwright MCP to Cursor settings
3. Restart Cursor

### Set Up Credentials
```bash
cp ../.env.example ../.env
```

Edit `.env`:
```
APP_URL=https://your-app.com
TEST_USER_EMAIL=your-test@email.com
TEST_USER_PASSWORD=your-password
```

## Step 2: Create Your First Test (2 minutes)

1. **Open Cursor Command Palette**: `Ctrl+Shift+P` (or `Cmd+Shift+P`)

2. **Run**: "Generate New E2E Test"

3. **Answer Questions**:
   - Test name: `login-flow`
   - Starting URL: `https://your-app.com/login`
   - Behavior:
     ```
     1. Navigate to login page
     2. Enter email
     3. Enter password
     4. Click login button
     5. Verify dashboard loads
     ```
   - Expected outcome: "User logged in and sees dashboard"

4. **Watch**: The AI verifies behavior, generates test, and runs it

5. **Verify**: Run "Run Test in Headed Mode" to watch it work

## Step 3: Run Tests (30 seconds)

**Run all tests**:
- Command: "Run All Tests"

**Run single test**:
- Command: "Run Single Test"

**See the browser**:
- Command: "Run Test in Headed Mode"

## Step 4: Self-Heal a Test (1 minute)

When a test fails but the feature still works:

1. **Manually verify** the feature works in your browser
2. **Run**: "Self-Heal [Test Name]" command
3. **Done**: Test is regenerated and passes

## Step 5: Save Your Work (30 seconds)

**Commit your tests**:
- Command: "Commit Changes"
- Message: "Add initial tests"

**Push to backup**:
- Command: "Push to Remote"

## Common Commands Reference

| What You Want | Command |
|--------------|---------|
| Create new test | "Generate New E2E Test" |
| Run all tests | "Run All Tests" |
| Run one test | "Run Single Test" |
| Watch test run | "Run Test in Headed Mode" |
| Fix broken test | "Self-Heal [Test Name]" |
| Save changes | "Commit Changes" |
| View history | "View Commit History" |
| Undo changes | "Rollback to Previous Commit" |
| Upload to GitHub | "Push to Remote" |

## Troubleshooting

### "Unable to verify behavior"
- Check URL is correct
- Verify credentials in `.env`
- Test manually first

### Test fails after generation
- Run in headed mode to see what's happening
- Use self-heal command

### No browser window in headed mode
```bash
npx playwright install chromium --with-deps
```

## Next Steps

📖 **Read the full README**: `README.md`
✅ **Complete the checklist**: `TESTING_CHECKLIST.md`
🎯 **Create more tests**: Use "Generate New E2E Test"

## Help

All Cursor commands have detailed instructions. Just run the command and follow the prompts!

---

**You're all set!** Start creating tests by describing behavior. The AI handles the rest. 🚀
