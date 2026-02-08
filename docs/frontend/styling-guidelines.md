# Styling Guidelines

**Date**: 2025-01-22  
**Status**: Phase 1 Implementation

## Overview

This document provides guidelines for styling components in the Leanda NG frontend application. These guidelines ensure consistency, maintainability, and adherence to the design system.

## File Structure

Each component should have its own SCSS file:

```
component-name/
├── component-name.component.ts
├── component-name.component.html
└── component-name.component.scss
```

## Importing Design Tokens and Mixins

Always import design tokens and mixins at the top of your SCSS file:

```scss
@import '../../../styles/tokens';
@import '../../../styles/mixins';
```

**Note**: Adjust the relative path based on your component's location:
- Components in `app/shared/components/` → `@import '../../../styles/tokens';`
- Components in `app/features/` → `@import '../../styles/tokens';`

## Naming Convention

Use BEM (Block Element Modifier) naming convention:

```scss
// Block
.component-name { }

// Element
.component-name__element { }

// Modifier
.component-name--modifier { }
.component-name__element--modifier { }
```

### Examples

```scss
.button { }                    // Block
.button__icon { }             // Element
.button--primary { }           // Modifier
.button--disabled { }          // Modifier
.button__icon--large { }      // Element with modifier
```

## Using Design Tokens

**Always use design tokens** instead of hardcoded values:

### Colors

```scss
// Good
.component {
  color: $text-color;
  background-color: $bg-color-secondary;
  border-color: $border-color;
}

// Bad
.component {
  color: #333;
  background-color: #f8f9fa;
  border-color: #dee2e6;
}
```

### Spacing

```scss
// Good
.component {
  padding: $spacing-md;
  margin: $spacing-sm;
  gap: $spacing-lg;
}

// Bad
.component {
  padding: 16px;
  margin: 8px;
  gap: 32px;
}
```

### Typography

```scss
// Good
.component {
  font-size: $font-size-sm;
  font-weight: $font-weight-semibold;
  line-height: $line-height-normal;
}

// Bad
.component {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.5;
}
```

## Using Mixins

Use mixins for common patterns to avoid code duplication:

### Transitions

```scss
.component {
  @include transition(all, $transition-fast);
  @include transition-fast(transform);
  @include transition-normal(opacity);
}
```

### Hover States

```scss
.button {
  @include hover-lift;
  @include hover-scale(1.05);
  @include hover-opacity(0.8);
}
```

### Shadows

```scss
.card {
  @include shadow-md;
  @include mat-box-shadow;
  @include card-shadow(2);
}
```

### Responsive Design

```scss
.component {
  width: 100%;
  
  @include respond-to(md) {
    width: 50%;
  }
  
  @include respond-below(lg) {
    padding: $spacing-sm;
  }
}
```

### Text Truncation

```scss
.title {
  @include truncate; // Single line
}

.description {
  @include truncate-lines(3); // Three lines
}
```

### Flexbox Utilities

```scss
.toolbar {
  @include flex-between;
}

.center-content {
  @include flex-center;
}
```

## Component Styling Patterns

### Basic Component Structure

```scss
@import '../../../styles/tokens';
@import '../../../styles/mixins';

.component-name {
  // Base styles using design tokens
  padding: $spacing-md;
  color: $text-color;
  background-color: $bg-color;
  border: $border-width solid $border-color;
  border-radius: $border-radius;
  
  // Transitions
  @include transition(all, $transition-normal);
  
  // Hover states
  &:hover {
    background-color: $bg-color-secondary;
  }
  
  // Modifiers
  &--variant {
    background-color: $color-accent;
    color: $text-color-inverse;
  }
  
  // Elements
  &__element {
    margin-top: $spacing-sm;
  }
  
  // Responsive
  @include respond-below(md) {
    padding: $spacing-sm;
  }
}
```

### Button Component Example

```scss
@import '../../../styles/tokens';
@import '../../../styles/mixins';

.button {
  display: inline-flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm $spacing-md;
  color: $text-color-inverse;
  background-color: $color-accent;
  border: none;
  border-radius: $border-radius;
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;
  cursor: pointer;
  
  @include transition(all, $transition-fast);
  @include hover-lift;
  @include shadow-md;
  
  &:hover {
    background-color: $color-accent-darken;
  }
  
  &:focus {
    @include focus-ring($color-accent);
  }
  
  &:active {
    transform: translateY(0);
  }
  
  &--secondary {
    background-color: $bg-color-secondary;
    color: $text-color;
    
    &:hover {
      background-color: $bg-color-tertiary;
    }
  }
  
  &--disabled {
    opacity: 0.5;
    cursor: not-allowed;
    
    &:hover {
      transform: none;
    }
  }
  
  &__icon {
    width: $icon-size-sm;
    height: $icon-size-sm;
  }
}
```

## Best Practices

### 1. External SCSS Files

**Always use external SCSS files** instead of inline styles:

```typescript
// Good
@Component({
  styleUrls: ['./component.component.scss']
})

// Bad
@Component({
  styles: [`...`]
})
```

### 2. Design Tokens First

**Always use design tokens** before creating custom values:

```scss
// Good - uses design token
.component {
  padding: $spacing-md;
}

// Bad - hardcoded value
.component {
  padding: 16px;
}
```

### 3. Use Mixins for Common Patterns

**Use mixins** to avoid code duplication:

```scss
// Good - uses mixin
.button {
  @include hover-lift;
}

// Bad - duplicates code
.button {
  transition: transform 0.15s;
  &:hover {
    transform: translateY(-2px);
  }
}
```

### 4. Mobile-First Approach

**Design for mobile first**, then enhance for larger screens:

```scss
.component {
  width: 100%;
  padding: $spacing-sm;
  
  @include respond-to(md) {
    width: 50%;
    padding: $spacing-md;
  }
}
```

### 5. Consistent Naming

**Follow BEM naming convention** consistently:

```scss
// Good
.card { }
.card__header { }
.card__body { }
.card--highlighted { }

// Bad
.card { }
.cardHeader { }
.cardBody { }
.cardHighlighted { }
```

### 6. Accessibility

**Ensure proper contrast and focus states**:

```scss
.button {
  // Ensure sufficient color contrast
  color: $text-color-inverse;
  background-color: $color-accent;
  
  // Focus state for keyboard navigation
  &:focus {
    @include focus-ring($color-accent);
  }
}
```

## Migration Checklist

When migrating components from inline styles to external SCSS:

- [ ] Create `component.component.scss` file
- [ ] Import design tokens and mixins
- [ ] Extract inline styles to SCSS file
- [ ] Replace hardcoded values with design tokens
- [ ] Use mixins for common patterns
- [ ] Apply BEM naming convention
- [ ] Update component to use `styleUrls`
- [ ] Test component rendering
- [ ] Verify responsive behavior
- [ ] Check accessibility (focus states, contrast)

## Examples

### Migrated Components

The following components have been migrated to external SCSS:

1. **OrganizeBrowserComponent** - `organize-browser.component.scss`
2. **OrganizeToolbarComponent** - `organize-toolbar.component.scss`
3. **FileViewComponent** - `file-view.component.scss`

These components serve as reference examples for proper styling patterns.

## Resources

- **Design System**: `docs/frontend/design-system.md`
- **Design Tokens**: `frontend/src/styles/_tokens.scss`
- **Mixins**: `frontend/src/styles/_mixins.scss`
- **Helpers**: `frontend/src/styles/_helpers.scss`
