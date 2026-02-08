# Phase 2: Frontend Migration

## Overview

Migrate the frontend from Angular 9 to Angular 21, creating a modern, zoneless application with Signal Forms and improved performance.

## Current State Analysis

### Legacy Frontend
- **Location**: `leanda-ui/`
- **Stack**: Angular 9, TypeScript, RxJS
- **Build**: Angular CLI
- **State Management**: Services + RxJS
- **HTTP Client**: Angular HttpClient
- **Real-time**: SignalR (`@aspnet/signalr`)

### Key Components

1. **Core Modules**:
   - `core/services/` - API services, auth, SignalR
   - `core/navbar/` - Navigation component

2. **Views**:
   - `views/home-page/` - Dashboard
   - `views/organize-view/` - File browser
   - `views/file-view/` - File preview
   - `views/record-view/` - Record details
   - `views/prediction/` - ML predictions

3. **Shared Components**:
   - `shared/components/` - Reusable components
   - `shared/directives/` - Custom directives
   - `shared/pipes/` - Custom pipes

4. **Services**:
   - API services (REST calls)
   - Auth service (OIDC)
   - SignalR service (real-time updates)
   - Search service
   - Export service

### Dependencies

- **Angular**: 9.x
- **RxJS**: 6.x
- **SignalR**: `@aspnet/signalr` (deprecated)
- **Bootstrap**: 4.0.0-alpha.6
- **JSmol**: For molecular visualization
- **Ketcher**: For chemical structure editor

---

## Target Architecture

### Angular 21 Application Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── services/
│   │   │   │   ├── api/
│   │   │   │   ├── auth/
│   │   │   │   └── signalr/
│   │   │   └── components/
│   │   │       └── navbar/
│   │   ├── features/
│   │   │   ├── home/
│   │   │   ├── organize/
│   │   │   ├── file-view/
│   │   │   ├── record-view/
│   │   │   └── prediction/
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   ├── directives/
│   │   │   └── pipes/
│   │   └── app.config.ts
│   ├── assets/
│   └── styles/
├── angular.json
└── package.json
```

### Technology Stack

- **Framework**: Angular 21
- **TypeScript**: 5.7+
- **RxJS**: 7.8+
- **State Management**: Signals (built-in)
- **Forms**: Signal Forms
- **HTTP**: Angular HttpClient
- **Real-time**: `@microsoft/signalr` (latest)
- **Testing**: Playwright (replaces Protractor)
- **Build**: Angular CLI 21
- **Deployment**: S3 + CloudFront (via CDK)

---

## Migration Strategy

### Phase 1: Project Setup

1. **Create new Angular 21 project**
   ```bash
   ng new leanda-ng-frontend --routing --style=scss
   ```

2. **Install dependencies**:
   - `@microsoft/signalr` (replace `@aspnet/signalr`)
   - Bootstrap 5.x (replace 4.0.0-alpha.6)
   - Update JSmol, Ketcher to latest versions

3. **Configure Angular**:
   - Enable zoneless mode
   - Configure Signal Forms
   - Set up routing

### Phase 2: Component Migration

1. **Migrate core services**:
   - API services (update to new endpoints)
   - Auth service (OIDC)
   - SignalR service (new package)

2. **Migrate components**:
   - Convert to standalone components
   - Use Signals instead of RxJS where possible
   - Update to Signal Forms

3. **Migrate views**:
   - Home page
   - Organize view
   - File view
   - Record view
   - Prediction view

### Phase 3: Testing & Deployment

1. **E2E tests** - Playwright
2. **Unit tests** - Jest or Angular Testing Library
3. **Deployment** - S3 + CloudFront

---

## Implementation Details

### App Configuration (Zoneless)

```typescript
// app.config.ts
import { ApplicationConfig, provideExperimentalZonelessChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideExperimentalZonelessChangeDetection(),
    provideRouter(routes),
    provideHttpClient(),
    // ... other providers
  ]
};
```

### SignalR Service (Updated)

```typescript
import { Injectable, signal } from '@angular/core';
import * as signalR from '@microsoft/signalr';

@Injectable({ providedIn: 'root' })
export class SignalRService {
  private connection: signalR.HubConnection | null = null;
  public connected = signal(false);
  
  async connect(hubUrl: string): Promise<void> {
    this.connection = new signalR.HubConnectionBuilder()
      .withUrl(hubUrl)
      .withAutomaticReconnect()
      .build();
    
    await this.connection.start();
    this.connected.set(true);
  }
  
  on<T>(methodName: string, callback: (data: T) => void): void {
    this.connection?.on(methodName, callback);
  }
}
```

### API Service (Signals)

```typescript
import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { toSignal } from '@angular/core/rxjs-interop';

@Injectable({ providedIn: 'root' })
export class FileService {
  private files = signal<File[]>([]);
  
  constructor(private http: HttpClient) {}
  
  loadFiles(): void {
    this.http.get<File[]>('/api/v1/files')
      .subscribe(files => this.files.set(files));
  }
  
  getFiles() {
    return this.files.asReadonly();
  }
}
```

### Signal Forms

```typescript
import { Component, signal } from '@angular/core';
import { signalForm, signalFormGroup } from '@angular/forms';

@Component({
  selector: 'app-file-upload',
  template: `
    <form [formGroup]="form()">
      <input formControlName="fileName" />
      <input type="file" formControlName="file" />
      <button (click)="upload()">Upload</button>
    </form>
  `
})
export class FileUploadComponent {
  form = signalFormGroup({
    fileName: signalForm.control(''),
    file: signalForm.control<File | null>(null)
  });
  
  upload(): void {
    const value = this.form().value();
    // Upload file
  }
}
```

---

## Breaking Changes & Compatibility

### Angular Version
- **Changed**: Angular 9 → Angular 21
- **Impact**: Major breaking changes, rewrite required

### SignalR
- **Changed**: `@aspnet/signalr` → `@microsoft/signalr`
- **Impact**: API changes, update connection code

### Testing
- **Changed**: Protractor → Playwright
- **Impact**: Rewrite E2E tests

### Forms
- **New**: Signal Forms (optional, can use reactive forms)
- **Impact**: Update form implementations

---

## Testing Requirements

### Unit Tests (>80% coverage)
- Component logic
- Service methods
- Utility functions

### E2E Tests (Playwright)
- Critical user journeys:
  - File upload
  - File browsing
  - Record viewing
  - ML prediction
  - Search

### Performance Tests
- Initial load time
- Route navigation
- Large file list rendering

---

## Dependencies

### Needs From
- Agent 1: Core API endpoints
- Agent 3: Blob Storage URLs
- Agent 5: ML Services APIs
- Agent 8: Infrastructure (S3, CloudFront)

### Provides To
- End users: Web interface

---

## Success Criteria

- [ ] Angular 21 application created
- [ ] All views migrated
- [ ] SignalR updated to `@microsoft/signalr`
- [ ] Signal Forms implemented (where applicable)
- [ ] Playwright E2E tests passing
- [ ] Unit test coverage >80%
- [ ] Deployed to S3 + CloudFront
- [ ] Performance meets or exceeds Angular 9 version

---

## Timeline

- **Week 1**: Project setup, core services migration
- **Week 2**: Component migration
- **Week 3**: Views migration
- **Week 4**: Testing, deployment

**Total: 4 weeks**

