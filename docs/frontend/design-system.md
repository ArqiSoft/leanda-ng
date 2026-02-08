# Design System Documentation

**Date**: 2025-01-22  
**Status**: Phase 1 Implementation  
**Version**: 1.0

## Overview

The Leanda NG design system provides a consistent visual language across the application. It includes design tokens, reusable components, and styling patterns extracted from the legacy implementation and modernized for Angular 21.

## Design Tokens

Design tokens are defined in `frontend/src/styles/_tokens.scss` and provide the foundation for all styling.

### Colors

#### Accent Colors
- `$color-accent`: #00bcd4 (cyan) - Primary accent color
- `$color-accent-darken`: Darkened version (20% darker)
- `$color-accent-muted`: Muted/transparent version

#### Text Colors
- `$text-color`: #333 - Primary text color
- `$text-color-light`: #666 - Light text
- `$text-color-muted`: #999 - Muted text
- `$text-color-inverse`: #fff - Inverse text (for dark backgrounds)

#### Background Colors
- `$bg-color`: #fff - Primary background
- `$bg-color-secondary`: #f8f9fa - Secondary background
- `$bg-color-tertiary`: #e9ecef - Tertiary background

#### Sidebar Colors
- `$color-sidebar-icon`: rgba(0, 0, 0, 0.5) - Sidebar icon color
- `$color-sidebar-bg`: #f5f5f5 - Sidebar background
- `$color-sidebar-border`: #dee2e6 - Sidebar border

#### State Colors
- `$color-success`: #28a745
- `$color-warning`: #ffc107
- `$color-danger`: #dc3545
- `$color-info`: #17a2b8

### Spacing

Spacing uses a base unit of 0.25rem (4px):

- `$spacing-xs`: 2px
- `$spacing-sm`: 8px
- `$spacing-md`: 16px
- `$spacing-lg`: 32px
- `$spacing-xl`: 48px
- `$spacing-xxl`: 64px

### Typography

#### Font Families
- `$font-family-primary`: "Open Sans", system fonts
- `$font-family-monospace`: "Courier New", monospace

#### Font Sizes
- `$font-size-xs`: 12px
- `$font-size-sm`: 14px
- `$font-size-base`: 16px
- `$font-size-lg`: 18px
- `$font-size-xl`: 20px
- `$font-size-xxl`: 24px
- `$font-size-xxxl`: 32px

#### Font Weights
- `$font-weight-light`: 300
- `$font-weight-normal`: 400
- `$font-weight-medium`: 500
- `$font-weight-semibold`: 600
- `$font-weight-bold`: 700

### Layout

- `$sidebar-width`: 20rem (320px)
- `$sidebar-width-collapsed`: 4rem (64px)
- `$nav-height`: 3.3rem (52.8px)

### Breakpoints

- `$breakpoint-xs`: 0
- `$breakpoint-sm`: 576px
- `$breakpoint-md`: 768px
- `$breakpoint-lg`: 992px
- `$breakpoint-xl`: 1200px
- `$breakpoint-xxl`: 1400px

### Borders & Radius

- `$border-radius`: 4px
- `$border-radius-sm`: 2px
- `$border-radius-lg`: 8px
- `$border-radius-xl`: 16px
- `$border-radius-full`: 9999px

### Shadows

- `$shadow-sm`: Small shadow
- `$shadow-md`: Medium shadow
- `$shadow-lg`: Large shadow
- `$shadow-xl`: Extra large shadow
- `$shadow-mat`: Material Design shadow (legacy)

### Transitions

- `$transition-fast`: 0.15s
- `$transition-normal`: 0.2s
- `$transition-slow`: 0.3s

## Mixins

Reusable mixins are defined in `frontend/src/styles/_mixins.scss`:

### Placeholder Styling
```scss
@include placeholder($color);
```

### Shadows
```scss
@include mat-box-shadow;
@include card-shadow($drop-times);
@include shadow-sm;
@include shadow-md;
@include shadow-lg;
@include shadow-xl;
```

### Transitions
```scss
@include transition($property, $duration, $timing);
@include transition-fast($property);
@include transition-normal($property);
@include transition-slow($property);
```

### Hover States
```scss
@include hover-lift;
@include hover-scale($scale);
@include hover-opacity($opacity);
```

### Responsive Breakpoints
```scss
@include respond-to(md) {
  // Styles for medium screens and up
}

@include respond-below(md) {
  // Styles for screens below medium
}
```

### Text Truncation
```scss
@include truncate; // Single line
@include truncate-lines(2); // Multi-line (2 lines)
```

### Flexbox Utilities
```scss
@include flex-center;
@include flex-between;
@include flex-start;
@include flex-end;
```

### Focus States
```scss
@include focus-outline($color, $width);
@include focus-ring($color);
```

### Scrollbar Styling
```scss
@include custom-scrollbar($thumb-color, $track-color);
```

## Utility Classes

Utility classes are defined in `frontend/src/styles/_helpers.scss`:

### Text Utilities
- `.truncate` - Single line truncation
- `.truncate-2` - Two line truncation
- `.truncate-3` - Three line truncation

### Icon Utilities
- `.svg-icon` - Standard icon size (24px)
- `.svg-icon-sm` - Small icon (20px)
- `.svg-icon-lg` - Large icon (32px)

### Spacing Utilities
- `.m-{0-4}` - Margin utilities
- `.mt-{0-4}`, `.mr-{0-4}`, `.mb-{0-4}`, `.ml-{0-4}` - Directional margins
- `.p-{0-4}` - Padding utilities
- `.pt-{0-4}`, `.pr-{0-4}`, `.pb-{0-4}`, `.pl-{0-4}` - Directional padding

### Display Utilities
- `.d-none`, `.d-block`, `.d-inline`, `.d-inline-block`, `.d-flex`, `.d-grid`

### Flexbox Utilities
- `.flex-center`, `.flex-between`, `.flex-start`, `.flex-end`
- `.flex-column`, `.flex-wrap`

### Other Utilities
- `.sticky` - Sticky positioning
- `.c-pointer` - Pointer cursor
- `.text-left`, `.text-center`, `.text-right` - Text alignment

## Component Styling Guidelines

### File Structure

Each component should have its own SCSS file:
```
component-name/
├── component-name.component.ts
├── component-name.component.html
└── component-name.component.scss
```

### Naming Convention

Use BEM (Block Element Modifier) naming convention:
```scss
.component-name { } // Block
.component-name__element { } // Element
.component-name--modifier { } // Modifier
```

### Using Design Tokens

Always use design tokens instead of hardcoded values:
```scss
// Good
.component {
  color: $text-color;
  padding: $spacing-md;
  border-radius: $border-radius;
}

// Bad
.component {
  color: #333;
  padding: 16px;
  border-radius: 4px;
}
```

### Using Mixins

Use mixins for common patterns:
```scss
.button {
  @include transition(transform, $transition-fast);
  @include hover-lift;
  @include shadow-md;
}
```

### Responsive Design

Use breakpoint mixins for responsive styles:
```scss
.component {
  width: 100%;
  
  @include respond-to(md) {
    width: 50%;
  }
}
```

## Migration from Legacy

The design system is based on the legacy implementation but modernized:

1. **Design Tokens**: Extracted from `legacy/leanda-ui/src/assets/sass/_vars.scss`
2. **Mixins**: Extracted from `legacy/leanda-ui/src/assets/sass/_mixins.scss`
3. **Helpers**: Extracted from `legacy/leanda-ui/src/assets/sass/_helpers.scss`

### Key Differences

- **Modernized**: Updated to use modern CSS features
- **Organized**: Better structure and organization
- **Documented**: Comprehensive documentation
- **Consistent**: Consistent naming and patterns

## Best Practices

1. **Always use design tokens** - Never hardcode colors, spacing, or typography
2. **Use mixins for common patterns** - Don't repeat code
3. **Follow BEM naming** - Consistent component naming
4. **External SCSS files** - Don't use inline styles
5. **Mobile-first** - Design for mobile, enhance for desktop
6. **Accessibility** - Ensure proper contrast and focus states

## Examples

### Component Styling Example

```scss
@import '../../styles/tokens';
@import '../../styles/mixins';

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
  
  &--secondary {
    background-color: $bg-color-secondary;
    color: $text-color;
  }
  
  &--disabled {
    opacity: 0.5;
    cursor: not-allowed;
    
    &:hover {
      transform: none;
    }
  }
}
```

## Resources

- **Design Tokens**: `frontend/src/styles/_tokens.scss`
- **Mixins**: `frontend/src/styles/_mixins.scss`
- **Helpers**: `frontend/src/styles/_helpers.scss`
- **Icon System**: See `docs/frontend/icon-system.md`
