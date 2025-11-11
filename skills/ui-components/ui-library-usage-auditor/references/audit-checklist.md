# UI Component Audit Checklist

## Accessibility Checklist

### Semantic HTML
- [ ] Use semantic elements (header, nav, main, article, aside, footer)
- [ ] Proper heading hierarchy (h1 → h2 → h3, no skips)
- [ ] Use button for actions, anchor for navigation
- [ ] Use lists (ul, ol) for list content
- [ ] Use appropriate input types (email, tel, url, number, etc.)

### ARIA Attributes
- [ ] All interactive elements have accessible names
- [ ] Form inputs have associated labels (explicit or aria-label)
- [ ] Images have alt text (or alt="" for decorative)
- [ ] Buttons have descriptive text or aria-label
- [ ] Links have descriptive text or aria-label
- [ ] aria-describedby used for additional context
- [ ] aria-required on required form fields
- [ ] aria-invalid on fields with errors
- [ ] aria-live regions for dynamic content
- [ ] Proper role attributes when needed

### Keyboard Navigation
- [ ] All interactive elements reachable via Tab
- [ ] Logical tab order
- [ ] Visible focus indicators
- [ ] Escape closes modals/dropdowns
- [ ] Enter/Space activates buttons
- [ ] Arrow keys navigate menus/lists
- [ ] No keyboard traps
- [ ] Skip links for navigation

### Forms
- [ ] All inputs have labels
- [ ] Required fields indicated visually and programmatically
- [ ] Error messages associated with fields
- [ ] Success messages announced to screen readers
- [ ] Fieldsets and legends for grouped fields
- [ ] Autocomplete attributes for common fields
- [ ] Clear error recovery instructions

### Visual Design
- [ ] Sufficient color contrast (4.5:1 for text, 3:1 for UI)
- [ ] Information not conveyed by color alone
- [ ] Text resizable to 200% without loss of functionality
- [ ] No content flashing more than 3 times per second
- [ ] Sufficient spacing for touch targets (44x44px min)

## shadcn/ui Best Practices

### Component Imports
- [ ] All UI components imported from @/components/ui
- [ ] No custom implementations of existing shadcn components
- [ ] Correct component variants used

### Form Components
- [ ] Using Form component wrapper
- [ ] FormField for each field with proper render prop
- [ ] FormLabel for all inputs
- [ ] FormControl wrapping input elements
- [ ] FormDescription for helpful context
- [ ] FormMessage for error display
- [ ] Proper form validation with zodResolver

### Button Usage
- [ ] Correct Button component used (not divs/spans)
- [ ] Appropriate variants (default, destructive, outline, ghost, link)
- [ ] Appropriate sizes (default, sm, lg, icon)
- [ ] Loading states with disabled prop
- [ ] Icons with proper sizing

### Dialog/Modal
- [ ] DialogTrigger wraps trigger element
- [ ] DialogContent contains modal content
- [ ] DialogHeader with DialogTitle
- [ ] DialogDescription for context
- [ ] DialogFooter for actions
- [ ] Proper close button with DialogClose

### Card Components
- [ ] Card wrapper for card layout
- [ ] CardHeader for card top section
- [ ] CardTitle for card heading
- [ ] CardDescription for card subtitle
- [ ] CardContent for main content
- [ ] CardFooter for actions/metadata

### Table Components
- [ ] Table wrapper for tables
- [ ] TableHeader with TableRow and TableHead
- [ ] TableBody with TableRow and TableCell
- [ ] TableCaption for table description
- [ ] Proper column alignment

### Select/Dropdown
- [ ] Select component for dropdowns
- [ ] SelectTrigger with SelectValue
- [ ] SelectContent with SelectItems
- [ ] SelectGroup and SelectLabel for grouping
- [ ] Proper placeholder text

## Consistency Checks

### Spacing
- [ ] Consistent spacing scale (gap-2, gap-4, gap-6, gap-8)
- [ ] Avoid odd spacing values (gap-3, gap-5)
- [ ] Consistent padding on containers
- [ ] Consistent margins between sections
- [ ] No hardcoded pixel values in spacing

### Typography
- [ ] Consistent font sizes using Tailwind scale
- [ ] Consistent font weights
- [ ] Consistent line heights
- [ ] Proper heading hierarchy and sizes
- [ ] Consistent text colors (foreground, muted-foreground, etc.)

### Colors
- [ ] Using theme colors from CSS variables
- [ ] Consistent color usage (primary, secondary, destructive, etc.)
- [ ] No hardcoded color values
- [ ] Proper use of foreground/background pairs

### Layout
- [ ] Consistent container max-widths
- [ ] Consistent grid/flex patterns
- [ ] Proper responsive breakpoints
- [ ] Mobile-first responsive design
- [ ] Consistent section spacing

### Icons
- [ ] Single icon library used consistently
- [ ] Consistent icon sizes (h-4 w-4, h-5 w-5, etc.)
- [ ] Icons have proper aria-hidden or aria-label
- [ ] Consistent icon placement (left/right of text)

## Component Patterns

### Loading States
- [ ] Loading indicators for async operations
- [ ] Skeleton loaders for content loading
- [ ] Disabled state during operations
- [ ] Loading text/icon feedback
- [ ] Proper loading state cleanup

### Error Handling
- [ ] Error messages displayed consistently
- [ ] Error states visually distinct
- [ ] Error recovery instructions provided
- [ ] Errors announced to screen readers
- [ ] Form field errors associated with inputs

### Empty States
- [ ] Meaningful empty state messages
- [ ] Call-to-action for empty states
- [ ] Icons/illustrations for visual interest
- [ ] Consistent empty state styling

### Success Feedback
- [ ] Success messages/toasts for user actions
- [ ] Visual confirmation of changes
- [ ] Undo option when appropriate
- [ ] Success states don't obstruct content

## Component Extraction Opportunities

### Repeated Patterns (3+ instances)
- [ ] Card layouts with similar structure
- [ ] Form field groups
- [ ] List item layouts
- [ ] Modal/dialog content
- [ ] Table row formats
- [ ] Navigation items
- [ ] Status badges

### Complex Inline JSX (10+ lines)
- [ ] Complex conditional rendering
- [ ] Nested component structures
- [ ] Repeated layout patterns
- [ ] Form sections

### Shared Business Logic
- [ ] Similar data transformations
- [ ] Common validation logic
- [ ] Shared state management
- [ ] Repeated API calls

## Layout and Responsiveness

### Responsive Design
- [ ] Mobile-first approach
- [ ] Proper breakpoint usage (sm, md, lg, xl, 2xl)
- [ ] Content readable on mobile (320px+)
- [ ] Touch targets adequate size (44x44px)
- [ ] No horizontal scroll on mobile
- [ ] Appropriate font sizes on mobile

### Flexbox/Grid
- [ ] Proper flex/grid usage
- [ ] Appropriate flex properties
- [ ] Grid column/row definitions
- [ ] Gap instead of margin for spacing
- [ ] Proper alignment properties

### Overflow Handling
- [ ] Long text truncated or wrapped appropriately
- [ ] Scroll containers have proper styling
- [ ] Tables responsive (scroll or stack)
- [ ] Modal content scrollable when needed

### Z-index Management
- [ ] Logical z-index layering
- [ ] No arbitrary z-index values
- [ ] Proper stacking context
- [ ] Modals/dropdowns above other content

## Performance Considerations

### Component Optimization
- [ ] Appropriate use of React.memo
- [ ] Event handlers not recreated on every render
- [ ] Heavy computations memoized
- [ ] Proper key props on lists

### Image Optimization
- [ ] Next.js Image component used
- [ ] Appropriate image sizes
- [ ] Lazy loading for below-fold images
- [ ] Proper aspect ratios

### Bundle Size
- [ ] No unused component imports
- [ ] Dynamic imports for large components
- [ ] Proper tree-shaking

## Code Quality

### TypeScript
- [ ] Proper prop types defined
- [ ] No 'any' types
- [ ] Proper type inference
- [ ] Union types for variants

### Props Interface
- [ ] Clear prop names
- [ ] Appropriate default values
- [ ] Optional vs required props clearly defined
- [ ] Proper JSDoc comments

### Component Structure
- [ ] Single responsibility principle
- [ ] Appropriate component size (<200 lines)
- [ ] Clear component hierarchy
- [ ] Proper file organization

### State Management
- [ ] Appropriate state location
- [ ] No prop drilling (use context if needed)
- [ ] Proper state updates
- [ ] No unnecessary state

## Worldbuilding App Specific

### Entity Display
- [ ] Consistent card layout for entities
- [ ] Proper entity type indicators
- [ ] Consistent metadata display
- [ ] Relationship indicators

### Forms
- [ ] Consistent field ordering
- [ ] Appropriate input types for data
- [ ] Proper validation rules
- [ ] Consistent submit/cancel patterns

### Data Visualization
- [ ] Accessible color schemes
- [ ] Legend/key provided
- [ ] Keyboard navigation support
- [ ] Screen reader descriptions

### Navigation
- [ ] Consistent navigation patterns
- [ ] Breadcrumbs for deep navigation
- [ ] Clear current location indicator
- [ ] Consistent menu structure

## Testing Checklist

### Manual Testing
- [ ] Keyboard navigation tested
- [ ] Screen reader tested (NVDA/JAWS/VoiceOver)
- [ ] Mobile device tested
- [ ] Different browsers tested
- [ ] Different viewport sizes tested

### Automated Testing
- [ ] Unit tests for components
- [ ] Integration tests for forms
- [ ] Accessibility tests (axe, jest-axe)
- [ ] Visual regression tests

## Documentation

### Component Documentation
- [ ] Props documented
- [ ] Usage examples provided
- [ ] Variants documented
- [ ] Edge cases noted

### Style Guide
- [ ] Component patterns documented
- [ ] Color palette defined
- [ ] Typography scale defined
- [ ] Spacing scale defined
- [ ] Accessibility guidelines

## Common Issues to Flag

### Critical (Must Fix)
- Missing alt text on images
- Form inputs without labels
- Div/span with onClick (should be button)
- Missing keyboard navigation
- Insufficient color contrast
- Broken heading hierarchy

### High Priority (Should Fix Soon)
- Inline styles (use Tailwind classes)
- Inconsistent spacing values
- Missing loading states
- Missing error handling
- Inconsistent button variants
- Missing focus indicators

### Medium Priority (Should Address)
- Component duplication (3+ instances)
- Complex components (>200 lines)
- Inconsistent empty states
- Missing TypeScript types
- Inconsistent naming conventions

### Low Priority (Nice to Have)
- Component extraction opportunities (2 instances)
- Minor styling inconsistencies
- Missing JSDoc comments
- Optimization opportunities

## Audit Report Sections

Include in final report:
1. Executive Summary
2. Critical Issues (with file paths and line numbers)
3. Warnings (grouped by category)
4. Suggestions (component extractions, refactoring)
5. Metrics (files scanned, issues found, accessibility score)
6. Best Practices Adherence
7. Recommendations Priority
8. Next Steps
