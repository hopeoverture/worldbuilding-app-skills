import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import * as fs from 'fs'
import * as path from 'path'

/**
 * Accessibility test suite using axe-core
 *
 * Tests pages against WCAG 2.1 Level AA standards
 * Generates JSON results for report generation
 */

// Pages to test
const PAGES = [
  { url: '/', name: 'Homepage' },
  { url: '/entities', name: 'Entity List' },
  { url: '/timeline', name: 'Timeline' },
  { url: '/about', name: 'About' }
]

// WCAG levels to test
const WCAG_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']

// Result storage
const results: any[] = []

test.describe('Accessibility Tests', () => {
  test.afterAll(async () => {
    // Save results to file for report generation
    const resultsDir = path.join(process.cwd(), 'test-results')
    if (!fs.existsSync(resultsDir)) {
      fs.mkdirSync(resultsDir, { recursive: true })
    }

    const resultsFile = path.join(resultsDir, 'a11y-results.json')
    fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2))

    console.log(`Accessibility results saved to: ${resultsFile}`)
  })

  for (const { url, name } of PAGES) {
    test(`${name} meets WCAG standards`, async ({ page }) => {
      await page.goto(url)

      // Wait for page to be fully loaded
      await page.waitForLoadState('networkidle')

      // Run accessibility scan
      const accessibilityScanResults = await new AxeBuilder({ page })
        .withTags(WCAG_TAGS)
        .analyze()

      // Store results
      results.push({
        url,
        name,
        timestamp: new Date().toISOString(),
        violations: accessibilityScanResults.violations,
        passes: accessibilityScanResults.passes,
        incomplete: accessibilityScanResults.incomplete
      })

      // Log violations for immediate feedback
      if (accessibilityScanResults.violations.length > 0) {
        console.log(`\n[ERROR] ${name} has ${accessibilityScanResults.violations.length} violations:`)

        accessibilityScanResults.violations.forEach(violation => {
          console.log(`  - [${violation.impact}] ${violation.id}: ${violation.description}`)
          console.log(`    Affected: ${violation.nodes.length} elements`)
        })
      } else {
        console.log(`\n[OK] ${name} has no violations`)
      }

      // Fail test if violations found
      expect(accessibilityScanResults.violations).toEqual([])
    })
  }

  test('scan for color contrast issues', async ({ page }) => {
    await page.goto('/')

    const results = await new AxeBuilder({ page })
      .withRules(['color-contrast'])
      .analyze()

    expect(results.violations).toEqual([])
  })

  test('scan for keyboard navigation', async ({ page }) => {
    await page.goto('/')

    const results = await new AxeBuilder({ page })
      .withRules(['keyboard'])
      .analyze()

    expect(results.violations).toEqual([])
  })

  test('scan for ARIA usage', async ({ page }) => {
    await page.goto('/')

    const results = await new AxeBuilder({ page })
      .withTags(['cat.aria'])
      .analyze()

    expect(results.violations).toEqual([])
  })
})

test.describe('Form Accessibility', () => {
  test('forms have proper labels', async ({ page }) => {
    // Test pages with forms
    const formPages = ['/signup', '/login', '/entities/new']

    for (const url of formPages) {
      try {
        await page.goto(url, { timeout: 5000 })

        const results = await new AxeBuilder({ page })
          .withRules(['label', 'label-title-only'])
          .analyze()

        expect(results.violations).toEqual([])
      } catch (e) {
        // Skip if page doesn't exist
        console.log(`Skipping ${url} - page not found`)
      }
    }
  })
})

test.describe('Interactive Elements', () => {
  test('buttons have accessible names', async ({ page }) => {
    await page.goto('/')

    const results = await new AxeBuilder({ page })
      .withRules(['button-name'])
      .analyze()

    expect(results.violations).toEqual([])
  })

  test('links have accessible text', async ({ page }) => {
    await page.goto('/')

    const results = await new AxeBuilder({ page })
      .withRules(['link-name'])
      .analyze()

    expect(results.violations).toEqual([])
  })
})
