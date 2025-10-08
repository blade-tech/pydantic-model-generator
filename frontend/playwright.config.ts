import { defineConfig, devices } from '@playwright/test'

/**
 * Playwright E2E Test Configuration
 *
 * Tests the full Pydantic Model Generator workflow:
 * 1. Business text input
 * 2. AI ontology research
 * 3. OutcomeSpec generation
 * 4. LinkML schema generation
 * 5. Pydantic model generation
 * 6. Test execution
 */

export default defineConfig({
  testDir: './e2e',

  // Maximum time one test can run
  timeout: 300 * 1000, // 5 minutes per test (Claude generation can be slow)

  // Maximum time for expect() assertions
  expect: {
    timeout: 10000
  },

  // Run tests in parallel
  fullyParallel: false, // Run sequentially to avoid conflicts

  // Fail the build on CI if you accidentally left test.only
  forbidOnly: !!process.env.CI,

  // Retry on CI only
  retries: process.env.CI ? 2 : 0,

  // Use single worker to avoid state conflicts
  workers: 1,

  // Reporter to use
  reporter: [
    ['html', { outputFolder: 'e2e-results/html' }],
    ['json', { outputFile: 'e2e-results/results.json' }],
    ['list']
  ],

  use: {
    // Base URL for the app
    baseURL: 'http://localhost:3000',

    // Collect trace on failure
    trace: 'on-first-retry',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Video on failure
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // Run local dev server before starting tests
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: true, // Always reuse existing server
    timeout: 120 * 1000,
  },
})
