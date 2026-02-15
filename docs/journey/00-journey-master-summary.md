# Leanda NG Journey — Master Summary

Single place that summarizes the journey from Week 1 through Week 5 for the repo and for future Substack/audience use. For full detail, read the individual journey docs linked below.

---

## Overview

What started as a weekend hobby project (“what if I just modernize this entire platform?”) produced an initial “92% complete” claim from multi-agent work. The public post explicitly warned not to trust that number. Weeks 2–5 showed the reality: many services didn’t compile, test progress had been overstated, and tools (Cursor, Claude Code) had real limits. By Week 5 we had an honest picture—front-end ~22% complete by gap analysis, DynamoDB/S3 migration done (metadata on DynamoDB, blobs on S3/MinIO), and a clear lesson that AI model behavior can change without notice, so guardrails and model choice matter. The new codebase is now **124K lines** (124,652 total: Java ~40K, TypeScript ~28K, JSON ~20K, then YAML, shell, Markdown, etc.—see [10-journey-week-5-loc.png](10-journey-week-5-loc.png)), a lot of it from the extra testing added once we stopped trusting “92% done.”

---

## Journey at a Glance

- **Week 1** — Discovery weekend: what Leanda.io is, legacy stack, “92% complete” claim, multi-agent setup, tech stack summary. See [01-journey-week-1.md](01-journey-week-1.md) and [02-journey-week-1-report.md](02-journey-week-1-report.md).
- **Week 2** — Reality check: unit tests failing, services not compiling; “92% was bogus”; Claude Code token limit; Cursor reported success while code didn’t compile; “pre-existing” excuses; Cursor removed functionality to make Docker build succeed. See [03-journey-week-2.md](03-journey-week-2.md) and [04-journey-week-2-testing-gaps.md](04-journey-week-2-testing-gaps.md).
- **Week 3** — Front-end finally up; old vs new home page; E2E tests are mocks that call APIs, not full UI flows; Codex/Claude helped where Cursor Auto failed. Gap analysis: front-end ~22% complete. See [05-jorney-week-3.md](05-jorney-week-3.md), [06-jorney-week-3-front-end-gaps.md](06-jorney-week-3-front-end-gaps.md), and screenshots 07–08.
- **Week 4** — Docker on Mac issues; adding E2E tests; Cursor “incredibly stubborn” ignoring rules; mock auth for testing. See [09-journey-week-4.md](09-journey-week-4.md) and 10 (LOC image).
- **Week 5** — Cursor “got dumber” (Composer); context loss; Opus 4.5 worked; lesson: AI providers can change behavior anytime—guardrails needed; DynamoDB/S3 migration done. See [11-journey-week-5.md](11-journey-week-5.md) and 12 (image).

**Narrative arc:** Week 1 = optimism and “92% done”; Week 2 = compile/test reality and tool limits; Week 3 = front-end visible but gaps and E2E are mocks; Week 4 = Docker + E2E + Cursor ignoring rules; Week 5 = model behavior change and DynamoDB/S3 migration done.

---

## Wins (What Actually Worked)

- **Scaffold and design** — 11 services migrated to Quarkus, CDK stacks designed, contracts (OpenAPI/AsyncAPI) and multi-agent coordination structure in place (01, 02).
- **Front-end running** — New Angular 21 app up; old vs new home page captured (05, 07–08).
- **Codex/Claude for UI** — More useful than Cursor Auto for migrating visuals (05).
- **Opus 4.5** — Switching model restored useful behavior when default Composer regressed (11).
- **Testing infrastructure** — Integration test base, workflow tests (BlobStorage, ChemicalParsing, OfficeProcessor, Indexing), root-cause doc [EC2_MINIMAL_ROOT_CAUSES.md](../../.archive/2025-02-15/EC2_MINIMAL_ROOT_CAUSES.md) (archived), E2E phases and Playwright config.
- **DynamoDB/S3 migration** — Done. Metadata on DynamoDB, blobs on S3/MinIO, using existing contracts and tests (11).
- **Gap clarity** — Front-end gap analysis (22% complete) and UI engineer plan give a realistic roadmap (06, [docs/frontend/](../frontend/)).
- **Auth for tests** — Mock auth and backend auth configuration for testing (docs/testing).
- **Scale** — 124K total lines of code since Week 1 (124,652 total; Java ~40K, TypeScript ~28K, JSON ~20K—full breakdown in [10-journey-week-5-loc.png](10-journey-week-5-loc.png)), more than the original repo, much of it from added testing once we stopped trusting “92% done.”

---

## Misses / Lessons

- **Compile** — Many services did not compile at start of Week 2; “make everything compile” was first order of business (03).
- **Test quality** — Previously reported test progress was “bogus”; integration tests lacking; many services missing unit tests (04).
- **Cursor behavior** — Reported success while tests failed; labeled remaining issues “pre-existing”; removed functionality to get Docker build to succeed (03); ignored rules (09); default Composer “got dumber” over time (11).
- **Claude Code** — Hit token limit after ~45 min on codebase analysis (03).
- **Front-end** — Only ~22% complete; E2E tests are API-driven mocks using the UI, not full UI flows (03, 06).
- **Home page “fail”** — Week 3: new app “up” but old vs new home page (05, 07–08) showed “migrated” meant a shell, not a replacement; gap analysis and “don’t declare front-end done until you compare to the old UI” lesson (14-substack).
- **Operational issues** — Docker on Mac (09); EC2/minimal distribution issues (RocksDB/Alpine, missing topics, JARs, .git, health timing, event payloads) documented in [EC2_MINIMAL_ROOT_CAUSES.md](../../.archive/2025-02-15/EC2_MINIMAL_ROOT_CAUSES.md) (archived).

---

## Substack and Public Narrative

The first public post is **[Leanda.io NextGen - can we build an enterprise platform using just Cursor AI?](https://rickzakharov.substack.com/p/leandaio-nextgen-can-we-build-an)**. It includes Week 1 content and this caveat:

> *"The most important part: do you trust them that just after a few hours of work it was 92% complete? I absolutely do not. And neither should you. All of these agents take after their human models and will happily report their huge achievements, while there was very little actual work done."*

Repo link for progress: [https://github.com/ArqiSoft/leanda-ng](https://github.com/ArqiSoft/leanda-ng).

The continuation document ([14-journey-continuation-after-week-5.md](14-journey-continuation-after-week-5.md)) picks up from that framing and summarizes what actually happened in Weeks 2–5. A **Substack-ready version** ([14-journey-continuation-after-week-5-substack.md](14-journey-continuation-after-week-5-substack.md)) adds mild humor, the Week 3 home-page “fail” with before/after screenshots (07–08) and lessons learned, and the **124K total lines of code** stat (more than the original repo, largely from added testing).

---

## References

**Journey docs (this folder):**  
01-journey-week-1.md, 02-journey-week-1-report.md, 03-journey-week-2.md, 04-journey-week-2-testing-gaps.md, 05-jorney-week-3.md, 06-jorney-week-3-front-end-gaps.md, 07-jorney-week-3-home-page-old.png, 08-jorney-week-3-home-page-new.png, 09-journey-week-4.md, 10-journey-week-4-loc.png, 11-journey-week-5.md, 12-journey-week-5.png, 14-journey-continuation-after-week-5.md, 14-journey-continuation-after-week-5-substack.md.

**Key testing / architecture docs:**

- [EC2_MINIMAL_ROOT_CAUSES.md](../../.archive/2025-02-15/EC2_MINIMAL_ROOT_CAUSES.md) (archived)  
- [docs/testing/TESTING.md](../testing/TESTING.md), [E2E.md](../testing/E2E.md), [EC2-TESTING.md](../testing/EC2-TESTING.md)  
- [docs/frontend/UI_ENGINEER_IMPLEMENTATION_PLAN.md](../frontend/UI_ENGINEER_IMPLEMENTATION_PLAN.md) (and frontend gap analysis)  
- [docs/agents/COORDINATION.md](../agents/COORDINATION.md)
