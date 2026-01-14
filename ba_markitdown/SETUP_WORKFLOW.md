# ⚠️ OBSOLETE - This document is no longer current

**This documentation is for the old standalone ba_markitdown repository.**

The bot has been unified into a meta-repository. For current documentation, see:
- `bot/README.md` - Main documentation
- `bot/.cursor/commands/help.md` - Command reference
- `bot/.cursor/commands/setup.md` - Setup instructions

The old folder structure (to_be_converted/, converted/) has been replaced with SharePoint folders → reference markdown folders.

---

# Updated Setup Workflow with Test Step (OLD)

This document describes the updated setup workflow that includes a test step at the end.

## Step 7: Setup Verification Test

After Step 6 (Completion), add a new Step 7 that runs a test conversion:

### Step 7: Run Setup Test

After the user confirms their API key is configured and setup is complete, run the test:

Tell the user:
> "Now let's run a quick test to make sure everything is working correctly. I'll convert a test file to verify your setup."

Then run:
```bash
# Automatically use venv if it exists
$(python get_python.py) setup_test.py
# OR: .venv/Scripts/python.exe setup_test.py (Windows)
# OR: .venv/bin/python setup_test.py (Unix/Mac)
```

**What the test does:**
1. Copies `test_files/test.xlsx` to `to_be_converted/`
2. Runs a conversion test
3. Verifies the output file is created
4. Cleans up both the input and output test files

**If the test succeeds:**
Tell the user:
> "Perfect! The test conversion worked successfully. Everything is set up correctly and ready to use!"

**If the test fails:**
- Check the error message
- Common issues:
  - API key not configured → Guide user back to Step 3
  - API quota exceeded → Inform user about rate limits
  - Conversion error → Check API key validity and network connection
- Provide helpful guidance based on the specific error

**After successful test:**
Update the setup status:
```bash
$(python get_python.py) setup_check.py --save
```

Tell the user:
> "You're all set up and verified! Here's what you can do now:
> - Drop files into the `to_be_converted` folder
> - Say 'convert my files' to start converting
> - Say 'help' anytime if you need guidance"

## Integration Notes

This test step should be added to `.cursor/rules/setup.mdc` as Step 7, after Step 6 (Completion).

The test ensures:
- Virtual environment is working
- Dependencies are installed correctly
- API key is valid and working
- Conversion process works end-to-end
- Cleanup works properly

This gives users confidence that their setup is complete and working.
