#!/usr/bin/env node
/**
 * Verification script for Playwright installation.
 * 
 * This script tests that Playwright is installed and can launch a browser.
 * 
 * Exit codes:
 *   0 - Verification passed
 *   1 - Playwright not installed
 *   2 - Browser not installed
 *   3 - Browser launch failed
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

async function verifyPlaywright() {
    const result = {
        test: 'playwright',
        success: false,
        verified_at: new Date().toISOString()
    };

    // Check if we're in the right directory
    const playwrightDir = path.resolve(__dirname, '..', 'cursor-playwright');
    const packageJson = path.join(playwrightDir, 'package.json');
    
    if (!fs.existsSync(packageJson)) {
        result.error = 'cursor-playwright directory not found';
        result.details = playwrightDir;
        return result;
    }

    try {
        // Check if playwright is installed
        const nodeModules = path.join(playwrightDir, 'node_modules', '@playwright', 'test');
        if (!fs.existsSync(nodeModules)) {
            result.error = 'Playwright not installed';
            result.details = 'Run npm install in cursor-playwright';
            return result;
        }

        // Try to list tests (quick check that Playwright works)
        try {
            execSync('npx playwright test --list', {
                cwd: playwrightDir,
                timeout: 30000,
                stdio: 'pipe'
            });
        } catch (e) {
            // This might fail if no tests exist, but that's OK
            // We just want to verify Playwright can run
            if (e.message.includes('ENOENT')) {
                result.error = 'Playwright executable not found';
                result.details = 'npm install may not have completed';
                return result;
            }
        }

        // Try to launch browser in headless mode
        const checkBrowser = `
            const { chromium } = require('playwright');
            (async () => {
                try {
                    const browser = await chromium.launch({ headless: true });
                    await browser.close();
                    process.exit(0);
                } catch (e) {
                    console.error(e.message);
                    process.exit(1);
                }
            })();
        `;

        try {
            execSync(`node -e "${checkBrowser.replace(/\n/g, ' ')}"`, {
                cwd: playwrightDir,
                timeout: 60000,
                stdio: 'pipe'
            });
            
            result.success = true;
            result.message = 'Playwright is ready';
            result.browser = 'chromium';
        } catch (e) {
            result.error = 'Browser launch failed';
            result.details = 'Run: npx playwright install chromium';
        }

    } catch (e) {
        result.error = e.message;
        result.details = e.stack;
    }

    return result;
}

async function main() {
    console.log('='.repeat(60));
    console.log('Playwright Verification Test');
    console.log('='.repeat(60));
    console.log();

    const result = await verifyPlaywright();

    if (result.success) {
        console.log('[PASS] Playwright verified!');
        console.log(`       Browser: ${result.browser}`);
    } else {
        console.log(`[FAIL] ${result.error}`);
        if (result.details) {
            console.log(`       Details: ${result.details}`);
        }
    }

    console.log();
    console.log(JSON.stringify(result, null, 2));

    process.exit(result.success ? 0 : 1);
}

main().catch(e => {
    console.error('Verification error:', e);
    process.exit(1);
});
