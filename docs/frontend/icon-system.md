# Icon System Documentation

**Date**: 2025-01-22  
**Status**: Phase 1 Implementation

## Overview

The icon system provides a consistent way to display SVG icons throughout the application. It includes an icon service for path resolution and an icon component for rendering.

## Architecture

### IconService

The `IconService` provides:
- Icon path resolution
- Icon registry for aliasing
- Icon management utilities

**Location**: `frontend/src/app/shared/services/icon.service.ts`

### IconComponent

The `IconComponent` provides:
- Consistent icon rendering
- Size presets (xs, sm, md, lg, xl)
- Custom size support
- Accessibility support (alt text)

**Location**: `frontend/src/app/shared/components/icon/icon.component.ts`

## Usage

### Basic Usage

```typescript
import { IconComponent } from '@app/shared/components/icon/icon.component';

@Component({
  template: `
    <app-icon name="close" />
    <app-icon name="download" sizePreset="lg" />
    <app-icon name="share" size="32" />
  `
})
```

### With Icon Service

```typescript
import { IconService } from '@app/shared/services/icon.service';

constructor(private iconService: IconService) {}

getIconPath() {
  return this.iconService.getIconPath('close');
}
```

## Icon Registry

Icons are registered in the `IconService` icon registry. Registered icons can be referenced by name:

- `close` → `material/ic_close_black_24px.svg`
- `download` → `material/ic_file_download_black_24px.svg`
- `share` → `material/ic_share_black_24px.svg`
- `delete` → `draft-menu/delete.svg`
- `rename` → `draft-menu/rename.svg`
- `export-csv` → `export-to-csv.svg`
- `export-sdf` → `export-to-sdf.svg`

## Icon Organization

Icons are organized in `frontend/src/assets/icons/`:

```
assets/icons/
├── material/          # Material Design icons
├── draft-menu/        # Action menu icons
├── imp/               # Import/action icons
└── *.svg              # Root level icons
```

## Size Presets

- `xs`: 16px (1rem)
- `sm`: 20px (1.25rem)
- `md`: 24px (1.5rem) - default
- `lg`: 32px (2rem)
- `xl`: 40px (2.5rem)

## Migration from Legacy

Icons from the legacy implementation should be migrated to the new structure:

1. Copy SVG files from `legacy/leanda-ui/src/img/svg/` to `frontend/src/assets/icons/`
2. Maintain directory structure (material/, draft-menu/, etc.)
3. Register icons in `IconService.iconRegistry`
4. Replace emoji usage with icon components

## Adding New Icons

1. Place SVG file in appropriate directory under `assets/icons/`
2. Register icon in `IconService.iconRegistry`:
   ```typescript
   this.iconService.registerIcon('new-icon', 'path/to/icon.svg');
   ```
3. Use in components:
   ```html
   <app-icon name="new-icon" />
   ```

## Accessibility

- Always provide meaningful `alt` text when using icons
- Icons should have descriptive names
- Use `alt` input for custom alt text:
  ```html
  <app-icon name="close" alt="Close dialog" />
  ```

## Best Practices

1. Use registered icon names when possible
2. Use size presets for consistency
3. Provide alt text for accessibility
4. Use icon component instead of direct `<img>` tags
5. Replace emoji usage with icon components

## Examples

### Replacing Emoji with Icons

**Before:**
```html
<button>🔗 Share</button>
```

**After:**
```html
<button>
  <app-icon name="link" sizePreset="sm" />
  Share
</button>
```

### Using in Toolbar

```html
<button class="toolbar-button">
  <app-icon name="download" />
  Download
</button>
```

### Custom Size

```html
<app-icon name="close" size="48" />
```
