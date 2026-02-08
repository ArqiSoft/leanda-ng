# UI Engineer Implementation Plan

**Date**: 2025-01-22  
**Author**: UI/UX Lead  
**Status**: Ready for Implementation  
**Reference**: See `FRONTEND_GAP_ANALYSIS.md` for detailed gap analysis

## Overview

This document provides a detailed implementation plan for the UI Engineer agent to close the gaps between the legacy frontend and the new Angular 21 implementation. The plan is organized into phases with specific tasks, acceptance criteria, and dependencies.

## Implementation Phases

### Phase 1: Design System Foundation (Weeks 1-2)

#### 1.1 Design Tokens & SCSS Architecture

**Tasks**:
1. Create SCSS architecture structure:
   ```
   frontend/src/styles/
   ├── _tokens.scss          # Design tokens (colors, spacing, typography)
   ├── _mixins.scss          # Reusable mixins
   ├── _helpers.scss          # Utility classes
   ├── _variables.scss        # SCSS variables
   └── _master.scss          # Master stylesheet
   ```

2. Extract design tokens from legacy:
   - Colors: accent (cyan), sidebar, text, background
   - Spacing: base unit, component spacing
   - Typography: font families, sizes, weights
   - Layout: sidebar width, nav height, breakpoints
   - Shadows: Material Design box shadows

3. Create design token system:
   ```scss
   // _tokens.scss
   $color-accent: #00bcd4; // cyan
   $color-accent-darken: darken($color-accent, 20%);
   $color-sidebar-icon: rgba(0, 0, 0, 0.5);
   $text-color: #333;
   $bg-color: #fff;
   
   $spacing-base: 0.25rem;
   $spacing-sm: $spacing-base * 2;  // 0.5rem
   $spacing-md: $spacing-base * 4;  // 1rem
   $spacing-lg: $spacing-base * 8;  // 2rem
   
   $sidebar-width: 20rem;
   $nav-height: 3.3rem;
   ```

4. Update `styles.scss` to import new architecture

**Acceptance Criteria**:
- [ ] SCSS architecture created
- [ ] Design tokens extracted and documented
- [ ] All tokens follow consistent naming convention
- [ ] Tokens are used in at least 3 components
- [ ] Documentation created in `docs/frontend/design-system.md`

**Files to Create/Modify**:
- `frontend/src/styles/_tokens.scss` (new)
- `frontend/src/styles/_mixins.scss` (new)
- `frontend/src/styles/_helpers.scss` (new)
- `frontend/src/styles/_variables.scss` (new)
- `frontend/src/styles/_master.scss` (new)
- `frontend/src/styles.scss` (modify)
- `docs/frontend/design-system.md` (new)

---

#### 1.2 Icon System

**Tasks**:
1. Create icon service:
   ```typescript
   // frontend/src/app/shared/services/icon.service.ts
   @Injectable({ providedIn: 'root' })
   export class IconService {
     getIconPath(iconName: string): string {
       return `/assets/icons/${iconName}.svg`;
     }
   }
   ```

2. Create icon component:
   ```typescript
   // frontend/src/app/shared/components/icon/icon.component.ts
   @Component({
     selector: 'app-icon',
     template: `<img [src]="iconPath" [alt]="name" />`
   })
   export class IconComponent {
     @Input() name!: string;
     iconPath = computed(() => this.iconService.getIconPath(this.name));
   }
   ```

3. Migrate icons from legacy:
   - Copy SVG icons from `legacy/leanda-ui/src/img/svg/` to `frontend/src/assets/icons/`
   - Organize by category (material, actions, export, etc.)
   - Create icon registry/mapping

4. Replace emoji usage with icons

**Acceptance Criteria**:
- [ ] Icon service created
- [ ] Icon component created
- [ ] Icons migrated from legacy
- [ ] Icon registry documented
- [ ] All emoji usage replaced with icons
- [ ] Icon component used in at least 5 components

**Files to Create/Modify**:
- `frontend/src/app/shared/services/icon.service.ts` (new)
- `frontend/src/app/shared/components/icon/icon.component.ts` (new)
- `frontend/src/assets/icons/` (new directory, migrate icons)
- `docs/frontend/icon-system.md` (new)

---

#### 1.3 Component Styling Patterns

**Tasks**:
1. Create component styling guidelines:
   - External SCSS files for components (not inline)
   - Use design tokens
   - Follow BEM naming convention
   - Component-specific styles in `*.component.scss`

2. Migrate inline styles to external SCSS:
   - Start with 3 key components (OrganizeBrowser, FileView, Toolbar)
   - Extract styles to `*.component.scss` files
   - Use design tokens

3. Create styling utilities:
   - Hover states mixin
   - Transition mixin
   - Shadow mixin
   - Responsive breakpoint mixins

**Acceptance Criteria**:
- [ ] Styling guidelines documented
- [ ] At least 3 components migrated to external SCSS
- [ ] Design tokens used in migrated components
- [ ] Styling utilities created and documented

**Files to Create/Modify**:
- `frontend/src/app/shared/components/organize-browser/organize-browser.component.scss` (new)
- `frontend/src/app/features/file-view/file-view.component.scss` (new)
- `frontend/src/app/shared/components/organize-toolbar/organize-toolbar.component.scss` (new)
- `docs/frontend/styling-guidelines.md` (new)

---

### Phase 2: Core Layout & Navigation (Weeks 3-4)

#### 2.1 Sidebar Layout System

**Tasks**:
1. Implement `SidebarContentComponent`:
   ```typescript
   // Enhanced sidebar with collapsible functionality
   @Component({
     selector: 'app-sidebar-content',
     template: `
       <div class="sidebar-content">
         <aside [class.collapsed]="collapsed()">
           <ng-content select="[sidebar]"></ng-content>
         </aside>
         <main>
           <ng-content select="[content]"></ng-content>
         </main>
       </div>
     `
   })
   ```

2. Add sidebar state management:
   - Collapsed/expanded state (signal)
   - Toggle functionality
   - Persist state in localStorage
   - Responsive behavior (auto-collapse on mobile)

3. Update OrganizeComponent to use sidebar:
   - Add sidebar with categories/filters tabs
   - Add content area with browser
   - Implement sidebar toggle

4. Update FileViewComponent to use sidebar:
   - Add sidebar with file info and actions
   - Add content area with tabs
   - Implement sidebar toggle

**Acceptance Criteria**:
- [ ] SidebarContentComponent fully implemented
- [ ] Collapsible functionality working
- [ ] State persisted in localStorage
- [ ] Responsive behavior implemented
- [ ] Used in OrganizeComponent and FileViewComponent
- [ ] Matches legacy sidebar behavior

**Files to Create/Modify**:
- `frontend/src/app/shared/components/sidebar-content/sidebar-content.component.ts` (modify)
- `frontend/src/app/shared/components/sidebar-content/sidebar-content.component.scss` (new)
- `frontend/src/app/features/organize/organize.component.ts` (modify)
- `frontend/src/app/features/file-view/file-view.component.ts` (modify)

---

#### 2.2 Tab Navigation System

**Tasks**:
1. Create tab component:
   ```typescript
   @Component({
     selector: 'app-tabs',
     template: `
       <div class="tabs">
         <nav class="tab-nav">
           @for (tab of tabs(); track tab.id) {
             <button 
               [class.active]="activeTab() === tab.id"
               (click)="selectTab(tab.id)">
               {{ tab.label }}
             </button>
           }
         </nav>
         <div class="tab-content">
           <ng-content></ng-content>
         </div>
       </div>
     `
   })
   ```

2. Implement tab state management:
   - Active tab signal
   - Tab switching
   - Tab content projection

3. Integrate tabs into FileViewComponent:
   - Records tab
   - Preview tab
   - Properties tab

**Acceptance Criteria**:
- [ ] Tab component created
- [ ] Tab state management working
- [ ] Tabs integrated into FileViewComponent
- [ ] Matches legacy tab behavior
- [ ] Accessible (keyboard navigation, ARIA)

**Files to Create/Modify**:
- `frontend/src/app/shared/components/tabs/tabs.component.ts` (new)
- `frontend/src/app/shared/components/tabs/tabs.component.scss` (new)
- `frontend/src/app/features/file-view/file-view.component.ts` (modify)

---

#### 2.3 Context Menu System

**Tasks**:
1. Create context menu service:
   ```typescript
   @Injectable({ providedIn: 'root' })
   export class ContextMenuService {
     showMenu(event: MouseEvent, items: ContextMenuItem[]): void {
       // Show context menu at event position
     }
   }
   ```

2. Create context menu component:
   ```typescript
   @Component({
     selector: 'app-context-menu',
     template: `
       <div class="context-menu" [style.left.px]="x()" [style.top.px]="y()">
         @for (item of items(); track item.id) {
           <button (click)="item.action()">{{ item.label }}</button>
         }
       </div>
     `
   })
   ```

3. Integrate into OrganizeBrowserComponent:
   - Right-click handler
   - Context menu items (Create, Delete, Rename, Move, Export, Share)
   - Menu positioning

**Acceptance Criteria**:
- [ ] Context menu service created
- [ ] Context menu component created
- [ ] Integrated into OrganizeBrowserComponent
- [ ] All context menu actions working
- [ ] Keyboard accessible (ESC to close)
- [ ] Matches legacy context menu behavior

**Files to Create/Modify**:
- `frontend/src/app/shared/services/context-menu.service.ts` (new)
- `frontend/src/app/shared/components/context-menu/context-menu.component.ts` (new)
- `frontend/src/app/shared/components/organize-browser/organize-browser.component.ts` (modify)

---

### Phase 3: Core Features (Weeks 5-7)

#### 3.1 Notifications System

**Tasks**:
1. Create notification models:
   ```typescript
   export interface Notification {
     id: string;
     type: 'upload' | 'export' | 'process' | 'common';
     title: string;
     message: string;
     timestamp: Date;
     read: boolean;
   }
   ```

2. Create notification service:
   - SignalR integration for real-time notifications
   - Notification storage (localStorage or API)
   - Notification state management (signals)

3. Create notification components:
   - `NotificationsSideBarComponent` - Sidebar notification panel
   - `SplashNotificationsComponent` - Toast notifications
   - `NotificationItemFactory` - Dynamic notification item rendering
   - Notification item components (Upload, Export, Process, Common)

4. Integrate SignalR for real-time updates:
   - Connect to SignalR hub
   - Listen for notification events
   - Update UI in real-time

**Acceptance Criteria**:
- [ ] Notification models created
- [ ] Notification service created with SignalR integration
- [ ] All notification components created
- [ ] Real-time notifications working
- [ ] Notification persistence working
- [ ] Matches legacy notification behavior

**Files to Create/Modify**:
- `frontend/src/app/shared/models/notification.model.ts` (new)
- `frontend/src/app/shared/services/notification.service.ts` (new)
- `frontend/src/app/shared/components/notifications/` (new directory)
- `frontend/src/app/core/services/signalr/signalr.service.ts` (modify)

---

#### 3.2 Category Management

**Tasks**:
1. Create category models:
   ```typescript
   export interface CategoryNode {
     id: string;
     title: string;
     children?: CategoryNode[];
   }
   ```

2. Create category service:
   - Load category tree
   - Assign categories to entities
   - Remove categories
   - Category filtering

3. Create category components:
   - `CategoryTaggingComponent` - Autocomplete with chips
   - `CategoryTreeComponent` - Full category tree display
   - `CategoryAssignDialogComponent` - Category assignment dialog

4. Integrate into OrganizeView and FileView:
   - Category sidebar in OrganizeView
   - Category assignment in FileView
   - Category filtering

**Acceptance Criteria**:
- [ ] Category models created
- [ ] Category service created
- [ ] All category components created
- [ ] Integrated into OrganizeView and FileView
- [ ] Category assignment working
- [ ] Category filtering working
- [ ] Matches legacy category behavior

**Files to Create/Modify**:
- `frontend/src/app/shared/models/category.model.ts` (new)
- `frontend/src/app/shared/services/category.service.ts` (new)
- `frontend/src/app/shared/components/category-tagging/` (new)
- `frontend/src/app/shared/components/category-tree/` (new)
- `frontend/src/app/features/organize/organize.component.ts` (modify)
- `frontend/src/app/features/file-view/file-view.component.ts` (modify)

---

#### 3.3 Drag-and-Drop Upload

**Tasks**:
1. Create drag-and-drop directive:
   ```typescript
   @Directive({
     selector: '[appFileDragDrop]'
   })
   export class FileDragDropDirective {
     @Output() fileDrop = new EventEmitter<File[]>();
     // Handle drag events
   }
   ```

2. Create upload service:
   - File upload to blob-storage API
   - Upload progress tracking
   - Upload queue management

3. Create upload components:
   - `UploadInfoBoxComponent` - Upload progress and status
   - Upload queue display

4. Integrate into OrganizeView:
   - Drag-and-drop zone
   - File input
   - Upload progress display

**Acceptance Criteria**:
- [ ] Drag-and-drop directive created
- [ ] Upload service created
- [ ] Upload components created
- [ ] Integrated into OrganizeView
- [ ] Upload progress tracking working
- [ ] Matches legacy upload behavior

**Files to Create/Modify**:
- `frontend/src/app/shared/directives/file-drag-drop.directive.ts` (new)
- `frontend/src/app/shared/services/upload.service.ts` (new)
- `frontend/src/app/shared/components/upload-info-box/` (new)
- `frontend/src/app/features/organize/organize.component.ts` (modify)

---

#### 3.4 View Toggle (Tile/Table)

**Tasks**:
1. Enhance OrganizeBrowserComponent:
   - Add view mode signal (tile | table)
   - Implement tile view layout
   - Implement table view layout
   - Add view toggle buttons

2. Create view components:
   - `TileViewComponent` - Tile/grid view
   - `TableViewComponent` - Table view with sortable columns

3. Add view state persistence:
   - Save view preference in localStorage
   - Restore on component load

**Acceptance Criteria**:
- [ ] View toggle functionality working
- [ ] Tile view implemented
- [ ] Table view implemented
- [ ] View preference persisted
- [ ] Matches legacy view toggle behavior

**Files to Create/Modify**:
- `frontend/src/app/shared/components/organize-browser/organize-browser.component.ts` (modify)
- `frontend/src/app/shared/components/tile-view/` (new)
- `frontend/src/app/shared/components/table-view/` (new)

---

### Phase 4: Enhanced Features (Weeks 8-10)

#### 4.1 Search Integration

**Tasks**:
1. Enhance OrganizeToolbarComponent:
   - Add search input
   - Search state management
   - Search API integration

2. Create search service:
   - Full-text search API calls
   - Search result management
   - Search history

3. Create search components:
   - `FullTextSearchViewComponent` - Dedicated search interface
   - Search results display

**Acceptance Criteria**:
- [ ] Search integrated into toolbar
- [ ] Search service created
- [ ] Search components created
- [ ] Full-text search working
- [ ] Search results displayed correctly

**Files to Create/Modify**:
- `frontend/src/app/shared/components/organize-toolbar/organize-toolbar.component.ts` (modify)
- `frontend/src/app/shared/services/search.service.ts` (new)
- `frontend/src/app/shared/components/full-text-search-view/` (new)

---

#### 4.2 Info Boxes System

**Tasks**:
1. Create info box models:
   ```typescript
   export interface InfoBox {
     id: string;
     type: 'common' | 'cvsp' | 'properties';
     title: string;
     data: any;
   }
   ```

2. Create info box factory:
   - Dynamic info box generation
   - Info box component selection

3. Create info box components:
   - `CommonInfoBoxComponent`
   - `CvspInfoBoxComponent`
   - `PropertiesInfoBoxComponent`

4. Integrate into FileView:
   - Dynamic info box generation
   - Info box display in Properties tab

**Acceptance Criteria**:
- [ ] Info box models created
- [ ] Info box factory created
- [ ] Info box components created
- [ ] Integrated into FileView
- [ ] Dynamic generation working

**Files to Create/Modify**:
- `frontend/src/app/shared/models/info-box.model.ts` (new)
- `frontend/src/app/shared/services/info-box-factory.service.ts` (new)
- `frontend/src/app/shared/components/info-box/` (new)
- `frontend/src/app/features/file-view/file-view.component.ts` (modify)

---

#### 4.3 Properties Editor

**Tasks**:
1. Enhance PropertiesEditorComponent:
   - Full property editing
   - Property validation
   - Property types (text, number, date, etc.)
   - Save/cancel functionality

2. Integrate into FileView:
   - Properties tab
   - Edit mode toggle
   - Property editing UI

**Acceptance Criteria**:
- [ ] Properties editor fully functional
- [ ] Property validation working
- [ ] Integrated into FileView
- [ ] Save/cancel working
- [ ] Matches legacy properties editor

**Files to Create/Modify**:
- `frontend/src/app/shared/components/properties-editor/properties-editor.component.ts` (modify)
- `frontend/src/app/features/file-view/file-view.component.ts` (modify)

---

### Phase 5: Advanced Features (Weeks 11-12)

#### 5.1 Chemical Editor

**Tasks**:
1. Integrate Ketcher:
   - Install Ketcher package
   - Create Ketcher wrapper component
   - SMILES/MOL file editing

2. Create ChemEditorComponent:
   - Ketcher integration
   - Structure editing
   - File export (SMILES, MOL)

**Acceptance Criteria**:
- [ ] Ketcher integrated
- [ ] ChemEditorComponent created
- [ ] Structure editing working
- [ ] File export working

**Files to Create/Modify**:
- `frontend/package.json` (add Ketcher dependency)
- `frontend/src/app/shared/components/chem-editor/` (new)

---

#### 5.2 Dataset Stepper

**Tasks**:
1. Create DatasetStepperComponent:
   - Multi-step wizard
   - Step navigation
   - Form validation
   - Progress indicator

**Acceptance Criteria**:
- [ ] DatasetStepperComponent created
- [ ] Multi-step wizard working
- [ ] Form validation working
- [ ] Progress indicator working

**Files to Create/Modify**:
- `frontend/src/app/shared/components/dataset-stepper/` (new)

---

#### 5.3 Visual Polish

**Tasks**:
1. Add hover states to all interactive elements
2. Add transitions and animations
3. Add loading indicators (skeleton screens)
4. Add error states and messages
5. Improve responsive design

**Acceptance Criteria**:
- [ ] Hover states on all interactive elements
- [ ] Smooth transitions and animations
- [ ] Loading indicators implemented
- [ ] Error states implemented
- [ ] Responsive design improved

**Files to Modify**:
- All component SCSS files
- Global styles

---

## Testing Requirements

### Unit Tests
- Each new component must have unit tests (>80% coverage)
- Test component inputs, outputs, and state
- Test service methods

### Integration Tests
- Test component interactions
- Test service integrations
- Test API integrations

### E2E Tests
- Test critical user workflows:
  - File upload
  - Category assignment
  - File viewing
  - Search
  - Notifications

---

## Documentation Requirements

1. **Component Documentation**:
   - JSDoc comments for all public APIs
   - Usage examples
   - Input/output documentation

2. **Design System Documentation**:
   - Design tokens reference
   - Component library documentation
   - Styling guidelines

3. **Implementation Notes**:
   - Document any deviations from legacy
   - Document new patterns used
   - Document migration decisions

---

## Success Criteria

### Phase 1 Complete
- [ ] Design system foundation implemented
- [ ] Icon system implemented
- [ ] Component styling patterns established

### Phase 2 Complete
- [ ] Sidebar layout system working
- [ ] Tab navigation working
- [ ] Context menu working

### Phase 3 Complete
- [ ] Notifications system working
- [ ] Category management working
- [ ] Drag-and-drop upload working
- [ ] View toggle working

### Phase 4 Complete
- [ ] Search integration working
- [ ] Info boxes working
- [ ] Properties editor working

### Phase 5 Complete
- [ ] Chemical editor working
- [ ] Dataset stepper working
- [ ] Visual polish complete

### Overall Success
- [ ] 80%+ feature parity with legacy
- [ ] All critical user workflows working
- [ ] Visual design matches or exceeds legacy
- [ ] Performance improved over legacy
- [ ] Accessibility compliance (WCAG 2.1 AA)

---

## Dependencies

### External Dependencies
- Ketcher (for chemical editor)
- SignalR client (already integrated)
- Bootstrap 5 (already mentioned in README)

### Internal Dependencies
- Backend APIs must be available:
  - Nodes API
  - Entities API
  - Search API
  - Categories API
  - Notifications API (SignalR)

---

## Risk Mitigation

1. **Legacy Code Complexity**:
   - Review legacy code thoroughly before implementing
   - Document legacy behavior
   - Test against legacy for comparison

2. **API Availability**:
   - Verify APIs are available before implementing
   - Create mock services for development
   - Coordinate with backend team

3. **Performance**:
   - Monitor bundle size
   - Use lazy loading
   - Optimize change detection

4. **Accessibility**:
   - Test with screen readers
   - Verify keyboard navigation
   - Check color contrast

---

## Timeline Summary

- **Phase 1**: Weeks 1-2 (Design System Foundation)
- **Phase 2**: Weeks 3-4 (Core Layout & Navigation)
- **Phase 3**: Weeks 5-7 (Core Features)
- **Phase 4**: Weeks 8-10 (Enhanced Features)
- **Phase 5**: Weeks 11-12 (Advanced Features & Polish)

**Total Estimated Time**: 12 weeks

---

**Last Updated**: 2025-01-22  
**Next Review**: After Phase 1 completion
