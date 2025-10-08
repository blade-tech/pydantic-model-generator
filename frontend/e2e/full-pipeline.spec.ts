import { test, expect } from '@playwright/test'

/**
 * Full Pipeline E2E Tests
 *
 * Tests complete workflow from business text → Pydantic models → tests
 * for 3 different business scenarios.
 */

// Increase timeout for long-running Claude generations
test.setTimeout(300000) // 5 minutes per test

/**
 * Business Prompt 1: Murabaha Audit Trail
 *
 * Islamic finance compliance tracking - validate Sharia compliance
 * for cost-plus financing transactions.
 */
test('Prompt 1: Murabaha Audit Trail - Complete Pipeline', async ({ page }) => {
  const overlayName = `e2e_murabaha_${Date.now()}`

  // Navigate directly to workflow page
  await page.goto('/workflow')
  await expect(page.locator('h1')).toContainText('Pydantic Model Generator')

  // Step 1: Enter business text
  await page.fill('textarea[placeholder*="business"]', `
We need to audit Murabaha transactions for Sharia compliance. Track:
- Purchase transactions with asset details
- Cost basis and profit markup calculations
- Payment schedules and installments
- Compliance checkpoints at each stage
- Audit findings and remediation actions

Each transaction must show full audit trail from initial purchase to final payment.
`.trim())
  await page.click('button:has-text("Start Pipeline")')

  // Wait for Step 2
  await expect(page.locator('text=Step 2')).toBeVisible({ timeout: 10000 })

  // Step 2: Ontology Research (wait for Claude)
  await page.click('button:has-text("Start Research")')

  // Wait for entities to appear (Claude thinking)
  await expect(page.locator('text=Identified Entities')).toBeVisible({ timeout: 120000 })

  // Verify at least 2 entities found
  const entityCards = page.locator('[data-testid="entity-card"], div:has(> h4.font-medium)')
  await expect(entityCards.first()).toBeVisible()

  // Approve research
  await page.click('button:has-text("Approve & Continue")')

  // Wait for Step 3
  await expect(page.locator('text=Step 3')).toBeVisible({ timeout: 10000 })

  // Step 3: OutcomeSpec Generation
  await page.click('button:has-text("Generate OutcomeSpec")')

  // Wait for OutcomeSpec to generate
  await expect(page.locator('textarea[value*="outcome"]')).toBeVisible({ timeout: 120000 })

  // Approve OutcomeSpec
  await page.click('button:has-text("Approve & Continue")')

  // Wait for Step 4
  await expect(page.locator('text=Step 4')).toBeVisible({ timeout: 10000 })

  // Step 4: LinkML Schema Generation
  await page.fill('input#overlay-name', overlayName)
  await page.click('button:has-text("Generate LinkML Schema")')

  // Wait for LinkML schema
  await expect(page.locator('text=entities')).toBeVisible({ timeout: 120000 })

  // Approve LinkML
  await page.click('button:has-text("Approve & Continue")')

  // Wait for Step 5
  await expect(page.locator('text=Step 5')).toBeVisible({ timeout: 10000 })

  // Step 5: Pydantic Generation
  await page.click('button:has-text("Generate Pydantic Models")')

  // Wait for completion
  await expect(page.locator('text=Generation complete')).toBeVisible({ timeout: 120000 })

  // Check for errors
  const hasError = await page.locator('text=Error').isVisible()
  if (hasError) {
    const errorText = await page.locator('[class*="text-red"]').textContent()
    throw new Error(`Step 5 failed: ${errorText}`)
  }

  // Approve Pydantic
  await page.click('button:has-text("Approve & Continue")')

  // Wait for Step 6
  await expect(page.locator('text=Step 6')).toBeVisible({ timeout: 10000 })

  // Step 6: Run Tests
  await page.click('button:has-text("Run Tests")')

  // Wait for test results
  await expect(page.locator('text=Total Tests')).toBeVisible({ timeout: 120000 })

  // Verify tests passed
  const passedCount = await page.locator('div:has-text("Passed") .text-2xl').textContent()
  const failedCount = await page.locator('div:has-text("Failed") .text-2xl').textContent()

  console.log(`Prompt 1 Results: ${passedCount} passed, ${failedCount} failed`)

  // Assert no failures
  expect(failedCount).toBe('0')
})

/**
 * Business Prompt 2: Customer Support Tickets
 *
 * Track support tickets, assignments, resolution, and satisfaction.
 */
test('Prompt 2: Customer Support Tickets - Complete Pipeline', async ({ page }) => {
  const overlayName = `e2e_support_${Date.now()}`

  await page.goto('/workflow')

  // Step 1
  await page.fill('textarea[placeholder*="business"]', `
Customer support ticket system. Track:
- Tickets with priority, category, and status
- Agent assignments and transfers
- Resolution steps and timeline
- Customer satisfaction ratings
- SLA compliance metrics

Need full history of ticket lifecycle from creation to closure.
`.trim())
  await page.click('button:has-text("Start Pipeline")')

  // Step 2
  await expect(page.locator('text=Step 2')).toBeVisible({ timeout: 10000 })
  await page.click('button:has-text("Start Research")')
  await expect(page.locator('text=Identified Entities')).toBeVisible({ timeout: 120000 })
  await page.click('button:has-text("Approve & Continue")')

  // Step 3
  await expect(page.locator('text=Step 3')).toBeVisible({ timeout: 10000 })
  await page.click('button:has-text("Generate OutcomeSpec")')
  await expect(page.locator('textarea[value*="outcome"]')).toBeVisible({ timeout: 120000 })
  await page.click('button:has-text("Approve & Continue")')

  // Step 4
  await expect(page.locator('text=Step 4')).toBeVisible({ timeout: 10000 })
  await page.fill('input#overlay-name', overlayName)
  await page.click('button:has-text("Generate LinkML Schema")')
  await expect(page.locator('text=entities')).toBeVisible({ timeout: 120000 })
  await page.click('button:has-text("Approve & Continue")')

  // Step 5
  await expect(page.locator('text=Step 5')).toBeVisible({ timeout: 10000 })
  await page.click('button:has-text("Generate Pydantic Models")')
  await expect(page.locator('text=Generation complete')).toBeVisible({ timeout: 120000 })

  const hasError = await page.locator('text=Error').isVisible()
  if (hasError) {
    const errorText = await page.locator('[class*="text-red"]').textContent()
    throw new Error(`Step 5 failed: ${errorText}`)
  }

  await page.click('button:has-text("Approve & Continue")')

  // Step 6
  await expect(page.locator('text=Step 6')).toBeVisible({ timeout: 10000 })
  await page.click('button:has-text("Run Tests")')
  await expect(page.locator('text=Total Tests')).toBeVisible({ timeout: 120000 })

  const failedCount = await page.locator('div:has-text("Failed") .text-2xl').textContent()
  expect(failedCount).toBe('0')
})

/**
 * Business Prompt 3: Resource Allocation
 *
 * Track resource allocation across projects with capacity planning.
 */
test('Prompt 3: Resource Allocation - Complete Pipeline', async ({ page }) => {
  const overlayName = `e2e_resource_${Date.now()}`

  await page.goto('/workflow')

  // Step 1
  await page.fill('textarea[placeholder*="business"]', `
Resource allocation system for project management. Track:
- Resources (people, equipment, budget)
- Project assignments and capacity
- Allocation periods and utilization rates
- Conflicts and reallocation events
- Cost tracking per resource per project

Need visibility into current allocation and historical changes.
`.trim())
  await page.click('button:has-text("Start Pipeline")')

  // Step 2
  await expect(page.locator('text=Step 2')).toBeVisible({ timeout: 10000 })
  await page.click('button:has-text("Start Research")')
  await expect(page.locator('text=Identified Entities')).toBeVisible({ timeout: 120000 })
  await page.click('button:has-text("Approve & Continue")')

  // Step 3
  await expect(page.locator('text=Step 3')).toBeVisible({ timeout: 10000 })
  await page.click('button:has-text("Generate OutcomeSpec")')
  await expect(page.locator('textarea[value*="outcome"]')).toBeVisible({ timeout: 120000 })
  await page.click('button:has-text("Approve & Continue")')

  // Step 4
  await expect(page.locator('text=Step 4')).toBeVisible({ timeout: 10000 })
  await page.fill('input#overlay-name', overlayName)
  await page.click('button:has-text("Generate LinkML Schema")')
  await expect(page.locator('text=entities')).toBeVisible({ timeout: 120000 })
  await page.click('button:has-text("Approve & Continue")')

  // Step 5
  await expect(page.locator('text=Step 5')).toBeVisible({ timeout: 10000 })
  await page.click('button:has-text("Generate Pydantic Models")')
  await expect(page.locator('text=Generation complete')).toBeVisible({ timeout: 120000 })

  const hasError = await page.locator('text=Error').isVisible()
  if (hasError) {
    const errorText = await page.locator('[class*="text-red"]').textContent()
    throw new Error(`Step 5 failed: ${errorText}`)
  }

  await page.click('button:has-text("Approve & Continue")')

  // Step 6
  await expect(page.locator('text=Step 6')).toBeVisible({ timeout: 10000 })
  await page.click('button:has-text("Run Tests")')
  await expect(page.locator('text=Total Tests')).toBeVisible({ timeout: 120000 })

  const failedCount = await page.locator('div:has-text("Failed") .text-2xl').textContent()
  expect(failedCount).toBe('0')
})
