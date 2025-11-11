# Testing Best Practices (2025)

Modern testing patterns using Vitest, React Testing Library, Playwright, and accessibility testing.

## Testing Stack

### Current Tools (2025)
- **Unit/Integration**: Vitest (not Jest)
- **Component Testing**: React Testing Library
- **E2E Testing**: Playwright
- **Accessibility**: axe-core + @axe-core/playwright
- **Coverage**: Vitest with v8 provider

### Deprecated Tools to Flag
- [ERROR] Jest (replaced by Vitest)
- [ERROR] Enzyme (replaced by React Testing Library)
- [ERROR] Karma, Jasmine (outdated)

## Vitest Configuration

### [OK] Modern: vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'test/',
        '**/*.config.{ts,js}',
        '**/*.d.ts',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### [ERROR] Deprecated: jest.config.js

```javascript
// OLD PATTERN - Don't use Jest
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
}
```

## Unit Testing Patterns

### [OK] Modern: Vitest Imports

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'

describe('validateEntity', () => {
  it('validates entity with required fields', () => {
    const result = validateEntity({
      name: 'Character',
      type: 'character'
    })

    expect(result.valid).toBe(true)
  })

  it('rejects entity with missing name', () => {
    const result = validateEntity({
      type: 'character'
    })

    expect(result.valid).toBe(false)
    expect(result.errors).toContain('Name is required')
  })
})
```

### Test Organization

```typescript
// Good structure: Arrange, Act, Assert (AAA)
describe('CharacterService', () => {
  describe('createCharacter', () => {
    it('creates character with valid data', async () => {
      // Arrange
      const characterData = {
        name: 'Aria',
        class: 'Rogue',
      }

      // Act
      const result = await createCharacter(characterData)

      // Assert
      expect(result.success).toBe(true)
      expect(result.character).toMatchObject(characterData)
    })
  })
})
```

## Component Testing with RTL

### [OK] Modern: React Testing Library

```typescript
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import { CharacterForm } from './CharacterForm'

describe('CharacterForm', () => {
  it('renders form fields', () => {
    render(<CharacterForm />)

    expect(screen.getByLabelText(/name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/class/i)).toBeInTheDocument()
  })

  it('submits form with valid data', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()

    render(<CharacterForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText(/name/i), 'Aria')
    await user.selectOptions(screen.getByLabelText(/class/i), 'rogue')
    await user.click(screen.getByRole('button', { name: /submit/i }))

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        name: 'Aria',
        class: 'rogue',
      })
    })
  })

  it('shows validation errors', async () => {
    const user = userEvent.setup()
    render(<CharacterForm />)

    await user.click(screen.getByRole('button', { name: /submit/i }))

    expect(await screen.findByText(/name is required/i)).toBeInTheDocument()
  })
})
```

### [ERROR] Deprecated: Enzyme

```typescript
// OLD PATTERN - Don't use Enzyme
import { shallow } from 'enzyme'

const wrapper = shallow(<CharacterForm />)
wrapper.find('input').simulate('change')
```

## Custom Render Function

### [OK] Create Test Utils

```typescript
// test/utils/render.tsx
import { render, RenderOptions } from '@testing-library/react'
import { ReactElement } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
})

function AllProviders({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllProviders, ...options })
}

export * from '@testing-library/react'
export { renderWithProviders as render }
```

## Mocking Patterns

### [OK] Vitest Mocks

```typescript
import { vi } from 'vitest'

// Mock module
vi.mock('@/lib/db', () => ({
  db: {
    character: {
      findMany: vi.fn(),
      create: vi.fn(),
    },
  },
}))

// Mock function
const mockFetch = vi.fn()
global.fetch = mockFetch

// Mock implementation
mockFetch.mockResolvedValue({
  ok: true,
  json: async () => ({ name: 'Test' }),
})

// Spy on method
const spy = vi.spyOn(console, 'error').mockImplementation(() => {})

// Cleanup
afterEach(() => {
  vi.clearAllMocks()
})
```

### [ERROR] Deprecated: Jest Mocks

```typescript
// OLD PATTERN
jest.mock('./module')
jest.fn()
jest.spyOn()
```

## Playwright E2E Testing

### [OK] Modern: Playwright Config

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './test/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

### [OK] E2E Test Patterns

```typescript
import { test, expect } from '@playwright/test'

test.describe('Character Creation', () => {
  test('creates new character', async ({ page }) => {
    await page.goto('/characters')

    // Navigate to create form
    await page.getByRole('button', { name: /create character/i }).click()

    // Fill form
    await page.getByLabel(/name/i).fill('Aria Shadowblade')
    await page.getByLabel(/class/i).selectOption('rogue')
    await page.getByLabel(/level/i).fill('5')

    // Submit
    await page.getByRole('button', { name: /save/i }).click()

    // Verify success
    await expect(page.getByText('Aria Shadowblade')).toBeVisible()
    await expect(page).toHaveURL(/\/characters\/\d+/)
  })

  test('shows validation errors', async ({ page }) => {
    await page.goto('/characters/create')

    await page.getByRole('button', { name: /save/i }).click()

    await expect(page.getByText(/name is required/i)).toBeVisible()
  })
})
```

## Accessibility Testing

### [OK] Component-Level A11y

```typescript
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { CharacterCard } from './CharacterCard'

expect.extend(toHaveNoViolations)

describe('CharacterCard Accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(
      <CharacterCard
        character={{
          name: 'Test',
          class: 'Warrior',
          level: 5,
        }}
      />
    )

    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
```

### [OK] E2E A11y with Playwright

```typescript
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test.describe('Accessibility', () => {
  test('homepage meets WCAG 2.1 AA', async ({ page }) => {
    await page.goto('/')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    expect(accessibilityScanResults.violations).toEqual([])
  })

  test('character form is accessible', async ({ page }) => {
    await page.goto('/characters/create')

    const results = await new AxeBuilder({ page })
      .exclude('#third-party-widget')  // Exclude external widgets
      .analyze()

    expect(results.violations).toEqual([])
  })
})
```

## Test Coverage

### [OK] Coverage Configuration

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'test/',
        '**/*.config.{ts,js}',
        '**/*.d.ts',
        '**/types.ts',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
})
```

### Running Coverage

```bash
# Run with coverage
vitest run --coverage

# Watch mode with coverage
vitest --coverage --watch

# Coverage for specific files
vitest run --coverage --changed
```

## Testing Best Practices

### 1. Query Priority (React Testing Library)

Use queries in this priority order:

1. **Accessible to everyone**:
   - `getByRole`
   - `getByLabelText`
   - `getByPlaceholderText`
   - `getByText`

2. **Semantic queries**:
   - `getByAltText`
   - `getByTitle`

3. **Test IDs** (last resort):
   - `getByTestId`

```typescript
// [OK] Good
screen.getByRole('button', { name: /submit/i })
screen.getByLabelText(/email/i)

// [ERROR] Avoid
screen.getByTestId('submit-button')
```

### 2. Async Testing

```typescript
import { waitFor, screen } from '@testing-library/react'

// [OK] Use waitFor for async assertions
await waitFor(() => {
  expect(screen.getByText(/success/i)).toBeInTheDocument()
})

// [OK] Use findBy queries (combines getBy + waitFor)
const element = await screen.findByText(/success/i)

// [ERROR] Don't use arbitrary timeouts
await new Promise(resolve => setTimeout(resolve, 1000))
```

### 3. User Interactions

```typescript
import userEvent from '@testing-library/user-event'

// [OK] Use userEvent (more realistic)
const user = userEvent.setup()
await user.type(input, 'text')
await user.click(button)

// [ERROR] Avoid fireEvent
import { fireEvent } from '@testing-library/react'
fireEvent.click(button)
```

### 4. Test Independence

```typescript
// [OK] Each test is independent
describe('CharacterList', () => {
  beforeEach(() => {
    // Fresh data for each test
    mockCharacters = [...]
  })

  it('displays characters', () => {
    render(<CharacterList characters={mockCharacters} />)
    // Test logic
  })

  it('filters characters', () => {
    render(<CharacterList characters={mockCharacters} />)
    // Test logic
  })
})

// [ERROR] Tests depend on each other
let sharedState

it('creates character', () => {
  sharedState = createCharacter()
})

it('updates character', () => {
  updateCharacter(sharedState)  // Depends on previous test
})
```

### 5. What to Test

**[OK] Do Test:**
- User interactions and workflows
- Component rendering with different props
- Conditional logic and edge cases
- Form validation
- Error handling
- Accessibility

**[ERROR] Don't Test:**
- Implementation details
- Third-party library internals
- Exact CSS values
- Component internal state
- Trivial code

## Common Anti-Patterns

### [ERROR] Testing Implementation Details

```typescript
// BAD: Testing state directly
const { result } = renderHook(() => useCounter())
expect(result.current.count).toBe(0)

// GOOD: Testing behavior
render(<Counter />)
expect(screen.getByText(/count: 0/i)).toBeInTheDocument()
```

### [ERROR] Snapshot Testing Overuse

```typescript
// BAD: Large snapshots
expect(container).toMatchSnapshot()

// GOOD: Specific assertions
expect(screen.getByRole('heading')).toHaveTextContent('Characters')
```

### [ERROR] Not Cleaning Up

```typescript
// BAD: No cleanup
afterEach(() => {
  // Missing cleanup
})

// GOOD: Proper cleanup
afterEach(() => {
  vi.clearAllMocks()
  cleanup()
})
```

## Package Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage",
    "test:watch": "vitest --watch",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug",
    "test:a11y": "playwright test a11y.spec.ts"
  }
}
```

## Validation Checklist

When reviewing testing skills, check for:

- [ ] Uses Vitest (not Jest)
- [ ] Uses React Testing Library (not Enzyme)
- [ ] Uses Playwright for E2E
- [ ] Includes accessibility testing with axe-core
- [ ] Proper query priority (role, label, text)
- [ ] userEvent instead of fireEvent
- [ ] Async testing with waitFor/findBy
- [ ] Proper mocking with vi.*
- [ ] Coverage configuration
- [ ] Independent tests
- [ ] Tests behavior, not implementation
- [ ] Cleanup in afterEach
- [ ] Descriptive test names
- [ ] AAA pattern (Arrange, Act, Assert)

## Migration Guide

### Jest → Vitest

```typescript
// Jest
import { jest } from '@jest/globals'
jest.fn()
jest.spyOn()
jest.mock()

// Vitest
import { vi } from 'vitest'
vi.fn()
vi.spyOn()
vi.mock()
```

### Update Imports

```typescript
// Old
import { describe, it, expect } from '@jest/globals'

// New
import { describe, it, expect } from 'vitest'
```

### Update Config

```bash
# Remove
npm uninstall jest @types/jest

# Install
npm install -D vitest @vitejs/plugin-react jsdom
```

## Quick Reference

### Must Use (Modern)
- [OK] Vitest (not Jest)
- [OK] React Testing Library
- [OK] Playwright
- [OK] axe-core for a11y
- [OK] userEvent for interactions
- [OK] waitFor/findBy for async
- [OK] getByRole queries

### Must Avoid (Deprecated)
- [ERROR] Jest
- [ERROR] Enzyme
- [ERROR] fireEvent
- [ERROR] getByTestId (overuse)
- [ERROR] Snapshot tests (overuse)
- [ERROR] Testing implementation details
- [ERROR] Arbitrary timeouts
