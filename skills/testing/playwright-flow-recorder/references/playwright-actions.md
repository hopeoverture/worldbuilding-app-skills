# Playwright Actions Reference

Comprehensive mapping of natural language actions to Playwright code.

## Navigation Actions

### Navigate to Page

**Natural Language:**
- "navigate to X"
- "go to X"
- "visit X"
- "open X"

**Playwright Code:**
```typescript
await page.goto('/x')
```

### Navigate Back

**Natural Language:**
- "go back"
- "navigate back"

**Playwright Code:**
```typescript
await page.goBack()
```

### Navigate Forward

**Natural Language:**
- "go forward"
- "navigate forward"

**Playwright Code:**
```typescript
await page.goForward()
```

### Reload Page

**Natural Language:**
- "reload"
- "refresh page"

**Playwright Code:**
```typescript
await page.reload()
```

## Click Actions

### Click Button

**Natural Language:**
- "click X button"
- "click on X"
- "press X"

**Playwright Code:**
```typescript
await page.getByRole('button', { name: /x/i }).click()
```

### Click Link

**Natural Language:**
- "click X link"
- "follow X link"

**Playwright Code:**
```typescript
await page.getByRole('link', { name: /x/i }).click()
```

### Double Click

**Natural Language:**
- "double click X"

**Playwright Code:**
```typescript
await page.getByRole('button', { name: /x/i }).dblclick()
```

### Right Click

**Natural Language:**
- "right click X"
- "context menu on X"

**Playwright Code:**
```typescript
await page.getByRole('button', { name: /x/i }).click({ button: 'right' })
```

## Form Input Actions

### Fill Text Input

**Natural Language:**
- "fill X with Y"
- "enter Y in X"
- "type Y in X field"

**Playwright Code:**
```typescript
await page.getByLabel(/x/i).fill('y')
```

### Clear Input

**Natural Language:**
- "clear X"
- "empty X field"

**Playwright Code:**
```typescript
await page.getByLabel(/x/i).clear()
```

### Type with Delay

**Natural Language:**
- "slowly type X"
- "type X with delay"

**Playwright Code:**
```typescript
await page.getByLabel(/field/i).type('x', { delay: 100 })
```

### Select Dropdown Option

**Natural Language:**
- "select X from Y"
- "choose X in Y dropdown"

**Playwright Code:**
```typescript
await page.getByLabel(/y/i).selectOption('x')
```

### Check Checkbox

**Natural Language:**
- "check X"
- "enable X checkbox"

**Playwright Code:**
```typescript
await page.getByLabel(/x/i).check()
```

### Uncheck Checkbox

**Natural Language:**
- "uncheck X"
- "disable X checkbox"

**Playwright Code:**
```typescript
await page.getByLabel(/x/i).uncheck()
```

### Upload File

**Natural Language:**
- "upload X file"
- "attach X"

**Playwright Code:**
```typescript
await page.getByLabel(/upload/i).setInputFiles('path/to/file.txt')
```

## Keyboard Actions

### Press Key

**Natural Language:**
- "press Enter"
- "hit Escape key"

**Playwright Code:**
```typescript
await page.keyboard.press('Enter')
await page.keyboard.press('Escape')
```

### Type Text

**Natural Language:**
- "type X"

**Playwright Code:**
```typescript
await page.keyboard.type('x')
```

### Key Combination

**Natural Language:**
- "press Ctrl+S"
- "use keyboard shortcut Cmd+K"

**Playwright Code:**
```typescript
await page.keyboard.press('Control+S')
await page.keyboard.press('Meta+K')
```

## Mouse Actions

### Hover

**Natural Language:**
- "hover over X"
- "mouse over X"

**Playwright Code:**
```typescript
await page.getByRole('button', { name: /x/i }).hover()
```

### Drag and Drop

**Natural Language:**
- "drag X to Y"
- "move X to Y"

**Playwright Code:**
```typescript
await page.getByText('X').dragTo(page.getByText('Y'))
```

## Wait Actions

### Wait for Element

**Natural Language:**
- "wait for X"
- "wait until X appears"

**Playwright Code:**
```typescript
await page.getByText(/x/i).waitFor()
```

### Wait for Navigation

**Natural Language:**
- "wait for page load"
- "wait for navigation"

**Playwright Code:**
```typescript
await page.waitForLoadState('networkidle')
```

### Wait for Timeout

**Natural Language:**
- "wait 2 seconds"
- "pause for 1000ms"

**Playwright Code:**
```typescript
await page.waitForTimeout(2000)
```

## Assertion Actions

### Assert Visible

**Natural Language:**
- "see X"
- "verify X is visible"
- "X is displayed"

**Playwright Code:**
```typescript
await expect(page.getByText(/x/i)).toBeVisible()
```

### Assert Not Visible

**Natural Language:**
- "X is hidden"
- "don't see X"
- "X not visible"

**Playwright Code:**
```typescript
await expect(page.getByText(/x/i)).not.toBeVisible()
```

### Assert URL

**Natural Language:**
- "is redirected to X"
- "URL is X"
- "page is X"

**Playwright Code:**
```typescript
await expect(page).toHaveURL(/x/)
```

### Assert Text Content

**Natural Language:**
- "X contains Y"
- "X displays Y"

**Playwright Code:**
```typescript
await expect(page.getByRole('x')).toContainText(/y/i)
```

### Assert Enabled/Disabled

**Natural Language:**
- "X is enabled"
- "X is disabled"

**Playwright Code:**
```typescript
await expect(page.getByRole('button', { name: /x/i })).toBeEnabled()
await expect(page.getByRole('button', { name: /x/i })).toBeDisabled()
```

### Assert Checked

**Natural Language:**
- "X is checked"
- "X is unchecked"

**Playwright Code:**
```typescript
await expect(page.getByLabel(/x/i)).toBeChecked()
await expect(page.getByLabel(/x/i)).not.toBeChecked()
```

### Assert Count

**Natural Language:**
- "there are X items"
- "X items are displayed"

**Playwright Code:**
```typescript
await expect(page.getByRole('listitem')).toHaveCount(5)
```

## Selector Patterns

### By Role

**Use for semantic elements:**
```typescript
page.getByRole('button', { name: /submit/i })
page.getByRole('link', { name: /home/i })
page.getByRole('heading', { name: /title/i, level: 1 })
page.getByRole('textbox', { name: /search/i })
```

### By Label

**Use for form inputs:**
```typescript
page.getByLabel(/email/i)
page.getByLabel(/password/i)
```

### By Text

**Use for visible text:**
```typescript
page.getByText(/welcome/i)
page.getByText('Exact Text')
```

### By Test ID

**Use for custom test identifiers:**
```typescript
page.getByTestId('entity-card')
page.getByTestId('create-button')
```

### By Placeholder

**Use for input placeholders:**
```typescript
page.getByPlaceholder(/enter name/i)
```

## Common Patterns

### Fill Form

```typescript
await page.getByLabel(/name/i).fill('John Doe')
await page.getByLabel(/email/i).fill('john@example.com')
await page.getByLabel(/type/i).selectOption('character')
await page.getByRole('button', { name: /submit/i }).click()
```

### Navigate and Verify

```typescript
await page.goto('/entities')
await expect(page).toHaveURL(/entities/)
await expect(page.getByRole('heading', { name: /entities/i })).toBeVisible()
```

### Conditional Actions

```typescript
const deleteButton = page.getByRole('button', { name: /delete/i })
if (await deleteButton.isVisible()) {
  await deleteButton.click()
}
```

### Loop Through Items

```typescript
const items = page.getByRole('listitem')
const count = await items.count()

for (let i = 0; i < count; i++) {
  await expect(items.nth(i)).toBeVisible()
}
```
