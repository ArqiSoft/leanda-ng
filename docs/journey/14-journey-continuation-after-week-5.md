# After Week 5: What Actually Happened (and What’s Next)

In the first post I said not to trust the 92% claim. Here’s what actually happened next.

---

## What We Learned (Weeks 2–5)

**Compile and test reality.** Nothing is “done” until it builds and tests run. At the start of Week 2, many services didn’t even compile. The first order of business was “make everything compile,” then figure out missing or incompatible functionality. Completion percentages from the AI were meaningless until we had green builds and real test results.

**AI assistants overclaim.** Cursor repeatedly reported success while tests were failing, and dismissed remaining problems as “pre-existing.” In at least one case it removed functionality so the Docker build would succeed. So we got a green build at the cost of working code. That’s the opposite of progress. The lesson: treat every “done” from an agent as a hypothesis until you’ve run the build and the test suite yourself.

**Model behavior isn’t stable.** By Week 5 the default Composer felt “a lot dumber”—it lost context after two or three responses and started instructing me to do the work instead of doing it. Switching to Opus 4.5 restored useful behavior. So the same product can change behavior overnight. You can’t rely on “how it worked last week” without guardrails: run compile, run tests, and review agent edits. And know which model actually works for your task when you’re paying per use.

**Front-end “migrated” is not “feature-complete.”** We had a new Angular 21 app and a nice before/after of the home page. A real gap analysis put the front-end at ~22% complete (visual ~20%, functionality ~25%)—missing design system, full layout, notifications, categories, drag-and-drop, and more. So “front-end migrated” meant “scaffold and some screens,” not “ready to replace the old UI.” We now have a phased plan and a realistic number.

**E2E tests that are API mocks are valuable but not the same as full UI E2E.** Our E2E tests emulate UI flows but call APIs directly. That’s useful for contract and integration coverage, but it doesn’t prove the real UI works end-to-end. We had to be clear about what “E2E” actually covers.

---

## What Actually Works Now

- **Services:** Eleven services migrated to Quarkus; after Week 2 we got them compiling and improved test coverage. Integration workflow tests (e.g. BlobStorage, ChemicalParsing, OfficeProcessor, Indexing) and root-cause docs (e.g. EC2 minimal distribution) exist and are maintained.
- **Front-end:** New Angular 21 app is up; we have a clear gap analysis and a UI engineer implementation plan instead of a fake completion number.
- **DynamoDB/S3 decision:** We have enough contract, unit, integration, and E2E coverage to justify migrating metadata to DynamoDB and blobs to S3/MinIO. That’s a concrete next step, not a headline.
- **Guardrails in practice:** Run `mvn compile` and the integration suite before trusting agent output; switch to a better model (e.g. Opus 4.5) when the default degrades; document root causes when something breaks so we don’t regress.

---

## What’s Next

- **DynamoDB/S3 migration** — Proceed with metadata to DynamoDB and blobs to S3/MinIO, using the existing contracts and tests as the definition of “done.”
- **Front-end P0 gaps** — Work through the 5-phase UI plan (design system, layout, core features) and track progress with the gap analysis, not a single percentage.
- **Stabilize integration tests** — Keep fixing and documenting EC2/minimal distribution issues (see EC2_MINIMAL_ROOT_CAUSES) and make the test suite the gate for “ready to deploy.”
- **Measure progress with criteria** — No more “92%” without a definition. Use: “all services compile,” “integration suite green,” “front-end phase N complete,” “DynamoDB migration done.”

---

## Takeaways for Building with AI

1. **Verify compile and tests every time.** If the agent says it’s done, run the build and the relevant tests. Treat “pre-existing” with suspicion until you’ve confirmed what’s actually broken.
2. **Don’t trust completion % without criteria.** Define “done” (e.g. compile, tests, contract coverage, gap analysis). Report against that, not a number the model made up.
3. **Switch model when quality drops.** If the default model gets worse (context loss, instructing you instead of doing), try another model (e.g. Opus 4.5) and document what worked when.
4. **Document root causes.** When something fails (Alpine vs RocksDB, missing Kafka topic, wrong event payload), write it down. It prevents repeat failures and gives the next agent (or you) something to search.
5. **Use gap analysis for UI.** “Migrated” UI can be a shell. Do a real gap analysis (design, layout, features) and a phased plan so you know what’s left and in what order.

The weekend hobby project is still going. It’s just running on honest numbers and real guardrails now.
