# Week 2–5: What Actually Happened After “92% Complete”

In the first post I said not to trust that number. Here's what happened when I started running the code.

## The Reality Check

So in [the first post](https://rickzakharov.substack.com/p/leandaio-nextgen-can-we-build-an) I shared the caveat: *do you trust them that just after a few hours of work it was 92% complete? I absolutely do not. And neither should you.* I meant it. What I didn’t know yet was how quickly the next few weeks would prove the point.

I went back to the repo, ran the tests, and tried to build everything. Turns out a lot of the services didn’t even compile. The AI had been reporting success while tests were failing and calling the rest “pre-existing” problems. In one case it had even removed functionality so the Docker build would succeed. So we had a green build and less working code. Not exactly progress.

First order of business: make everything compile. Then figure out what was actually missing or broken. Only then did “completion percentage” start to mean anything.

## What I Learned (Weeks 2–5)

**Nothing is “done” until it builds and tests run.** Completion percentages from the AI were meaningless until we had green builds and real test results. Obvious in hindsight. Painful in practice.

**AI assistants overclaim.** Cursor kept saying things were done while tests were failing. It loved the phrase “pre-existing” for anything it didn’t fix. The lesson: treat every “done” from an agent as a hypothesis. Run the build and the test suite yourself.

**Model behavior isn’t stable.** By Week 5 the default Composer felt a lot dumber—it lost context after two or three responses and started telling *me* to do the work instead of doing it. Switching to Opus 4.5 fixed that. So the same product can change behavior overnight. You can’t rely on “how it worked last week” without guardrails: run compile, run tests, review agent edits. And if you’re paying per use, know which model actually works for your task.

**“Front-end migrated” is not “feature-complete.”** We had a new Angular 21 app and a nice before/after of the home page. Then we did a real gap analysis. Result: the front-end was about 22% complete—missing design system, full layout, notifications, categories, drag-and-drop, and more. So “migrated” meant “scaffold and some screens,” not “ready to replace the old UI.” We now have a phased plan and a number we can believe.

**E2E tests can be misleading.** Our E2E tests emulate UI flows but call APIs directly. Useful for contract and integration coverage, but they don’t prove the real UI works end-to-end. We had to get clear on what “E2E” actually covered.

## What Actually Works Now

- **Services** — Eleven services migrated to Quarkus. After Week 2 we got them compiling and improved test coverage. We have integration workflow tests (BlobStorage, ChemicalParsing, OfficeProcessor, Indexing) and root-cause docs so we don’t repeat the same failures.
- **Front-end** — The new Angular 21 app is up. We have a clear gap analysis and a UI implementation plan instead of a fake completion number.
- **DynamoDB/S3** — We have enough contract, unit, integration, and E2E coverage to justify moving metadata to DynamoDB and blobs to S3/MinIO. That’s the next concrete step.
- **Guardrails** — Run `mvn compile` and the integration suite before trusting agent output. Switch to a better model (e.g. Opus 4.5) when the default degrades. Document root causes when something breaks.

## What’s Next

- **DynamoDB/S3 migration** — Proceed with metadata to DynamoDB and blobs to S3/MinIO, using the existing contracts and tests as the definition of “done.”
- **Front-end P0 gaps** — Work through the 5-phase UI plan (design system, layout, core features) and track progress with the gap analysis, not a single percentage.
- **Stabilize integration tests** — Keep fixing and documenting issues (e.g. EC2/minimal distribution) and make the test suite the gate for “ready to deploy.”
- **Measure progress with criteria** — No more “92%” without a definition. Use: “all services compile,” “integration suite green,” “front-end phase N complete,” “DynamoDB migration done.”

## Takeaways for Building with AI

1. **Verify compile and tests every time.** If the agent says it’s done, run the build and the relevant tests. Treat “pre-existing” with suspicion until you’ve confirmed what’s actually broken.
2. **Don’t trust completion % without criteria.** Define “done” (e.g. compile, tests, contract coverage, gap analysis). Report against that, not a number the model made up.
3. **Switch model when quality drops.** If the default gets worse (context loss, instructing you instead of doing), try another model and document what worked when.
4. **Document root causes.** When something fails—wrong base image, missing Kafka topic, wrong event payload—write it down. It prevents repeat failures and gives the next agent (or you) something to search.
5. **Use gap analysis for UI.** “Migrated” UI can be a shell. Do a real gap analysis and a phased plan so you know what’s left and in what order.

The weekend hobby project is still going. It’s just running on honest numbers and real guardrails now.

You can watch the repo for progress: [https://github.com/ArqiSoft/leanda-ng](https://github.com/ArqiSoft/leanda-ng)

---

*P.S. — If you’re building with Cursor or any AI coding tool, assume every “done” is a draft. Your build and your tests are the final say.*

*P.P.S. — When the default model suddenly feels useless, try another model (e.g. Opus 4.5) before you assume the task is impossible. Sometimes it’s the model, not you.*


References:

https://x.com/kareldoostrlnck/status/2019477361557926281?s=12&utm_source=tldrai

https://substack.com/inbox/post/186649722?utm_source=unread-posts-digest-email&inbox=true&utm_medium=email&triedRedirect=true
