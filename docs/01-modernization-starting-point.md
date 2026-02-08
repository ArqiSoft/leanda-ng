# Leanda Platform Modernization Plan

## Executive Summary

The Leanda platform is a complex microservices-based scientific data management system with significant technical debt. This plan addresses critical modernization needs across all technology stacks to improve security, performance, maintainability, and developer experience.

## Current State Analysis

### Architecture Overview

- **Pattern**: Microservices with event-driven architecture (CQRS/ES)

- **Communication**: RabbitMQ with MassTransit (C#) and custom messaging (Java)

- **Data Stores**: MongoDB 3.6, EventStore 4.0.2, Redis 4

- **Frontend**: Angular 9 with TypeScript 3.7.5

- **Backend Services**:

- .NET Core 3.1 services (leanda-core)

- Java 8 / Spring Boot 2.0.0.RC1 services (file parsers)

- Python services (ML services)

- **Authentication**: Keycloak with OIDC/JWT

- **Testing**: Protractor (deprecated), Cucumber

- **CI/CD**: Travis CI (deprecated); CI/CD is postponed until full migration is complete

### Critical Issues Identified

1. **Security Vulnerabilities**

- Outdated dependencies with known CVEs

- Spring Boot 2.0.0.RC1 (pre-release version)

- Angular 9 (EOL, no security patches)

- MongoDB 3.6 (EOL)

- Java 8 (approaching EOL)

2. **Technology Stack Obsolescence**

- .NET Core 3.1 (EOL since Dec 2022)

- Angular 9 (EOL since May 2021)

- TypeScript 3.7.5 (current is 5.x)

- Spring Boot 2.0.0.RC1 (should be 2.7+ or 3.x)

- Protractor (deprecated, replaced by Playwright/Cypress)

3. **Infrastructure**

- Travis CI (shut down in 2023)
- Old Docker base images

- No modern observability (OpenTelemetry, structured logging)

4. **Code Quality**

- Mixed dependency versions across services

- Inconsistent patterns

- Limited test coverage

## Modernization Strategy

### Phase 1: Foundation & Security (Months 1-3)

**Priority: Critical - Security patches and dependency updates**

#### 1.1 .NET Core Modernization

- **Target**: Upgrade from .NET Core 3.1 to .NET 8 LTS

- **Files**: All `.csproj` files in `leanda-core/`
- **Key Changes**:

- Update `TargetFramework` from `netcoreapp3.1` to `net8.0`

- Update NuGet packages to latest compatible versions

- Migrate from `Microsoft.AspNetCore.SignalR.Protocols.NewtonsoftJson` to System.Text.Json

- Update MassTransit to latest version (8.x)

- Update Serilog and logging packages

- Replace deprecated `IHostApplicationLifetime` usage

**Affected Services**:

- `Sds.Osdr.WebApi` - Main API gateway

- `Sds.Osdr.Domain.BackEnd` - Domain backend service

- `Sds.Osdr.Domain.FrontEnd` - Domain frontend service

- `Sds.Osdr.Persistence` - Persistence service

- All domain modules (Chemicals, Crystals, Spectra, etc.)

#### 1.2 Java Services Modernization

- **Target**: Upgrade from Java 8 to Java 17 LTS (or Java 21 LTS)

- **Spring Boot**: Upgrade from 2.0.0.RC1 to 3.1.x (requires Java 17+)

- **Files**: All `pom.xml` files in Java services

- **Key Changes**:

- Update Java version in `pom.xml` properties

- Upgrade Spring Boot parent to 3.1.x

- Migrate from `javax.*` to `jakarta.*` packages

- Update MongoDB driver to latest version

- Update custom dependencies (`jtransit-light`, `storage`, etc.)

**Affected Services**:

- `chemical-file-parser-service`

- `chemical-properties-service`
- `chemical-export-service`
- `crystal-file-parser-service`

- `spectra-file-parser-service`

- `reaction-file-parser-service`

- `imaging-service`

- `microscopy-metadata-service`

- `office-file-processor-service`
- `web-importer-service`

#### 1.3 Frontend Modernization

- **Target**: Upgrade from Angular 9 to Angular 17 LTS

- **Files**: `leanda-ui/package.json`, `angular.json`, `tsconfig.json`
- **Key Changes**:

- Angular 9 → 17 migration (requires incremental steps: 9→10→11→12→13→14→15→16→17)

- TypeScript 3.7.5 → 5.3.x

- Replace `@aspnet/signalr` with `@microsoft/signalr`
- Update Angular Material to v17

- Migrate from TSLint to ESLint

- Update RxJS to latest version

- Replace deprecated `HttpClient` patterns

**Breaking Changes to Address**:

- Module system changes (standalone components)

- Strict mode enforcement

- New Angular CLI structure

- Updated routing syntax

#### 1.4 Infrastructure Updates

- **MongoDB**: Upgrade from 3.6 to 7.0 (or at least 6.0)

- **EventStore**: Upgrade from 4.0.2 to 23.10+

- **Redis**: Upgrade from 4 to 7.x

- **Docker**: Update base images to latest LTS versions

- **Files**: All `docker-compose.yml` files and `Dockerfile` files

### Phase 2: Testing & CI/CD Modernization (Months 4-5) — CI/CD postponed until full migration is complete

**Priority: High - Improve development workflow**

#### 2.1 Testing Framework Migration

- **Replace Protractor** with Playwright or Cypress

- **Files**: `leanda-test/package.json`, test configuration files
- **Key Changes**:

- Migrate from Protractor to Playwright (recommended) or Cypress

- Update Cucumber integration

- Modernize test structure

- Add component testing for Angular

#### 2.2 CI/CD Migration (postponed until full migration is complete)

- **Replace Travis CI** with GitHub Actions

- **Files**: Create `.github/workflows/` directory structure
- **Key Changes**:

- Create GitHub Actions workflows for:

    - Build and test for each service type (.NET, Java, Angular, Python)

    - Docker image building

    - Integration tests
    - Deployment pipelines

- Remove `.travis.yml` files

- Add proper secrets management

- Implement matrix builds for multiple environments

**Workflow Structure**:

```javascript
.github/workflows/
  ├── dotnet-build-test.yml
  ├── java-build-test.yml
  ├── angular-build-test.yml
  ├── python-build-test.yml
  ├── docker-build-push.yml
  └── integration-tests.yml
```



### Phase 3: Architecture & Patterns (Months 6-8)

**Priority: Medium - Improve maintainability**

#### 3.1 Observability Enhancement

- **Add OpenTelemetry** instrumentation

- **Structured Logging**: Enhance Serilog configuration

- **Metrics**: Add Prometheus metrics endpoints

- **Distributed Tracing**: Implement across all services

- **Files**: Update startup configurations in all services

#### 3.2 API Modernization

- **OpenAPI 3.0**: Update Swagger/OpenAPI specifications

- **API Versioning**: Implement proper versioning strategy

- **GraphQL Consideration**: Evaluate for complex queries

- **Files**: `Sds.Osdr.WebApi/Startup.cs`, Swagger configurations

#### 3.3 Dependency Management

- **Centralize Dependencies**: Use Directory.Build.props for .NET

- **Dependency Updates**: Implement Dependabot or Renovate

- **Security Scanning**: Add Snyk or GitHub Security Advisories

#### 3.4 Code Quality

- **.NET**: Add .editorconfig, enable nullable reference types

- **Java**: Add Checkstyle, SpotBugs, PMD

- **TypeScript**: Strict mode, better type safety

- **Linting**: Standardize across all projects

### Phase 4: Performance & Scalability (Months 9-10)

**Priority: Medium - Optimize for scale**

#### 4.1 Performance Optimization

- **Caching Strategy**: Enhance Redis usage patterns

- **Database Optimization**: MongoDB indexing review

- **API Response Times**: Implement response caching
- **Frontend**: Lazy loading, code splitting optimization

#### 4.2 Scalability Improvements

- **Horizontal Scaling**: Ensure stateless services

- **Message Queue**: Optimize RabbitMQ configuration

- **Load Testing**: Implement with k6 or JMeter

### Phase 5: Developer Experience (Months 11-12)

**Priority: Low - Quality of life improvements**

#### 5.1 Development Environment

- **Docker Compose**: Improve local development setup

- **Documentation**: Update README files, add architecture diagrams

- **Scripts**: Standardize build and run scripts

- **Hot Reload**: Improve development feedback loops

#### 5.2 Documentation

- **API Documentation**: Enhance Swagger/OpenAPI docs

- **Architecture Decision Records (ADRs)**: Document key decisions

- **Runbooks**: Operational documentation

## Implementation Approach

### Migration Strategy

1. **Incremental Migration**: Service-by-service approach

2. **Feature Flags**: Use feature flags for gradual rollout
3. **Parallel Running**: Run old and new versions during transition

4. **Comprehensive Testing**: Integration tests at each phase

### Risk Mitigation

- **Backup Strategy**: Full backups before major upgrades

- **Rollback Plans**: Documented rollback procedures

- **Staging Environment**: Test all changes in staging first

- **Monitoring**: Enhanced monitoring during migrations

### Success Metrics

- **Security**: Zero critical vulnerabilities

- **Performance**: <5% performance regression

- **Uptime**: 99.9% availability during migration

- **Developer Satisfaction**: Improved build times, better DX

## Dependencies and Prerequisites

### External Dependencies

- Custom libraries (`jtransit-light`, `storage`, `messaging`) need compatibility verification

- Third-party services (Keycloak) compatibility checks

- Database migration scripts for MongoDB and EventStore

### Team Requirements

- Training on new framework versions

- Updated development environment setup

- CI/CD pipeline access and configuration

## Estimated Timeline

- **Phase 1**: 3 months (Critical security updates)

- **Phase 2**: 2 months (Testing and CI/CD; CI/CD postponed until full migration)

- **Phase 3**: 3 months (Architecture improvements)

- **Phase 4**: 2 months (Performance optimization)
- **Phase 5**: 2 months (Developer experience)

**Total**: ~12 months for complete modernization

## Quick Wins (Can Start Immediately)

1. **Update .NET packages** to latest 3.1-compatible versions (before .NET 8 migration)

2. **Add Dependabot** for automated dependency updates

3. **Create GitHub Actions** for basic CI (parallel to Travis)

4. **Security audit** with `npm audit`, `dotnet list package --vulnerable`, `mvn dependency-check`
5. **Update Docker base images** to latest LTS versions

## Notes

- This is a large-scale modernization requiring careful planning

- Consider pausing new feature development during Phase 1

- Allocate dedicated resources for migration work

- Regular stakeholder communication on progress