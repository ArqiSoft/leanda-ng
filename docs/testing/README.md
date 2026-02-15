# Integration Testing Documentation

This directory contains documentation for the Leanda integration testing infrastructure.

## Status

- **Test Infrastructure**: Fully functional
- **Minimal Distribution Tests**: Partially passing (2/5) due to known limitation
- **Docker Infrastructure**: All services operational

## Which script?

| Goal | Script |
|------|--------|
| **E2E locally vs EC2 APIs** (frontend + Playwright, backend on EC2) | `./scripts/run-e2e-local-ec2.sh` — resolves EC2 IP, tunnel + local frontend + Phase 1 tests. Use `--deploy` to deploy minimal on EC2 first. |
| Backend integration, EC2 infra + local JVM apps (Java tests only) | `./scripts/run-e2e-minimal-ec2-tunnel.sh` |
| Backend integration, all on EC2 (build + run on EC2) | `./scripts/run-system-integration-tests-ec2-tunnel.sh --minimal` |
| Local-only (Docker infra + local JVM, frontend E2E) | `./scripts/start-minimal-distro-local.sh` then `./scripts/run-frontend-e2e-minimal-local.sh` |

## Key Documents

- **[TESTING.md](TESTING.md)** — Strategy, eight test tiers, run commands per tier, CI mapping, artifact paths, unit vs integration (Java).
- **[E2E.md](E2E.md)** — Canonical vs mocked E2E, how to run E2E (local JVM, EC2, Docker), Playwright projects/tags, test catalog, selectors/fixtures reference.
- **[EC2-TESTING.md](EC2-TESTING.md)** — Test-runner EC2 instance, get IP, run integration and Phase 1 E2E on EC2, troubleshooting (root causes archived).
- **[AUTHENTICATION.md](AUTHENTICATION.md)** — Auth status (frontend/backend), config for tests (OIDC disabled), where auth tests live and how to run them.
- **[SERVICE_ISOLATION_PATTERN.md](SERVICE_ISOLATION_PATTERN.md)** — Tier 2/4/5 classification and service isolation pattern.

### Archived

- Troubleshooting, root-cause, phase-completion, and audit docs: **`.archive/2025-02-15/`** (e.g. EC2_MINIMAL_ROOT_CAUSES.md, PHASE_*_COMPLETE.md, INTEGRATION_TEST_TIER_AUDIT.md).
- Detailed E2E reference (selectors, page objects, fixtures, Playwright config): **`.archive/2025-02-15/testing-reference/`**.

## Quick reference

- **Rapid E2E** (infra in Docker, apps in JVM): `./scripts/start-minimal-distro-local.sh` then `./scripts/run-frontend-e2e-minimal-local.sh` or `./scripts/run-integration-tests-minimal-local.sh`. See [E2E.md](E2E.md).
- **All tiers and commands**: See [TESTING.md](TESTING.md).

## Known limitations

1. **Jandex REST client**: Services using `BlobStorageApi` from `shared-models.jar` fail in local JAR mode (imaging, office-processor, indexing). Use Docker for full functionality.
2. **Local JVM**: REST clients from external JARs not supported; use Docker or `./mvnw quarkus:dev`.

Production deployments (Docker Compose, Kubernetes, native image) are not affected.

## Contributing

When adding new tests: document dependencies, update test status, note limitations, verify in Docker mode.
