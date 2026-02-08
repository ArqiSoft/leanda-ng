# Week 1: My Weekend Hobby Project - The Leanda.io Adventure 🚀

*"What if I just... modernize this entire platform in my spare time?"*

## What Are We Modernizing? 🎯

So, what exactly is [Leanda.io](https://github.com/ArqiSoft/leanda.io)? It's an **extensible open science data repository** that helps researchers consume, process, visualize, and analyze different scientific data types, formats, and volumes. Think of it as a GitHub for scientific data, but way cooler because it handles:

- **Chemical structures** (SDF, MOL files)
- **Crystallographic data** (CIF files)
- **Spectra** (JDX files)
- **Chemical reactions** (RXN files)
- **Microscopy images**
- **Machine learning models**
- **Office documents, PDFs, tabular data** - basically everything a scientist might need!

The platform does real-time data curation, ontology-based property assignment, complex semantic searches, and even has an embedded ML framework for building training datasets. It's genuinely impressive stuff!

**But here's the thing:** The entire platform is built on technology from 2018-2020, and most of it has reached end-of-life. We're talking about:

- **112+ .NET Core 3.1 projects** (EOL since December 2022)
- **10+ Java 8 services** with Spring Boot 2.0.0.RC1 (yes, a *release candidate* from 2018!)
- **Angular 9 frontend** (EOL since May 2021)
- **MongoDB 3.6, EventStore 4.0.2, Redis 4** (all ancient)
- **28 separate GitHub repos** with almost no activity since 2020-2021

The goal? Modernize the entire platform to an **AWS-native, serverless-first architecture** using modern technologies (Java 21/Quarkus, Angular 21, Python 3.12+, Apache Iceberg, AWS Bedrock AI) while keeping all the cool scientific data processing capabilities. It's ambitious, but hey, that's what makes it fun! 🚀

## Saturday Morning: The Discovery 🕵️

So, I was browsing through some old open-source projects this weekend (you know, normal Saturday morning activities 😅) and stumbled across Leanda.io. It's this really cool open science platform that helps researchers manage and process scientific data. I thought, "Hey, let me just take a quick look at the codebase..."

*Spoiler alert: it was NOT a quick look.*

I opened up the repo and discovered that Leanda.io had been living in a time capsule since 2020. It was like finding a vintage computer in your attic - fascinating, but also slightly concerning! Here's what I found:

- **.NET Core 3.1** (which went EOL in December 2022 - RIP 🪦)
- **Angular 9** (the framework equivalent of a flip phone)
- **Java 8** (still functional, but feeling its age)
- **Spring Boot 2.0.0.RC1** (yes, a *release candidate* from 2018 - still running!)
- **MongoDB 3.6** (ancient by database standards)
- **28 separate GitHub repos** with the activity level of a ghost town

My initial reaction? 😱 → 🤔 → 😤 → "You know what? This could be a fun weekend project!" 💪

## Saturday Afternoon: The Deep Dive 📚

After lunch (and maybe a second coffee), I started really digging into what Leanda.io actually does. It's genuinely impressive:

- Researchers can upload and process scientific data (chemicals, crystals, spectra, all that good stuff!)
- Real-time curation with AI-powered metadata extraction
- Build ML training datasets on the fly
- Share data with granular privacy controls

But the architecture? Oh boy, it's a beautiful polyglot mess:

- C# for the core services
- Java for file parsers
- Python for ML services
- TypeScript/Angular for the frontend

It's like a United Nations of programming languages, but without the translators! 🌍

I thought to myself: "This would be SO much cooler if it was modernized..." And that's how my weekend hobby project was born.

## Saturday Evening: The Planning Session 🗺️

After dinner, I sat down with a notebook (yes, an actual paper notebook - I'm old school like that) and started sketching out options. I had three paths:

1. **Incremental Modernization** (the safe, boring path)
   - Upgrade everything piece by piece
   - Keep the polyglot stack
   - 12 months of careful, methodical work
   - Result: Modern but still fragmented
   - *Verdict: Too boring for a hobby project*

2. **Full Rewrite** (the "burn it all down" path)
   - Greenfield AWS-native architecture
   - Unify to Java/Python
   - 10-15 months of exciting chaos
   - Result: Clean slate, but risky
   - *Verdict: Too risky, might never finish*

3. **Lakehouse Architecture** (the "let's be cutting-edge" path)
   - Apache Iceberg + SageMaker Lakehouse
   - Serverless-first, AI-native
   - Open table formats for future-proofing
   - Result: The future of data platforms
   - *Verdict: Perfect! Ambitious but achievable, and I'll learn a ton!*

I'm going with option 3, because why not aim for the stars? ⭐ Plus, I've been wanting to play with AWS Bedrock and Iceberg tables anyway...

## Sunday Morning: The Architecture Sketch 🏗️

Sunday morning, fresh coffee in hand, I started sketching out what a modern Leanda.io would look like. I drew it on my whiteboard (yes, I have a whiteboard in my home office - don't judge):

```text
Scientific Community → API Gateway → Ingestion → S3 Landing Zone
                                              ↓
Real-time Curation Pipeline (Glue + Bedrock AI) → Iceberg Tables
                                              ↓
OpenSearch (Vector Search) → Athena (SQL Analytics) → SageMaker (ML)
```

It's like a data science theme park! 🎢 Every layer does something cool:

- **Bedrock AI** for automated curation (Claude, you're hired!)
- **Iceberg tables** for ACID transactions on S3 (because we're fancy)
- **OpenSearch** for semantic search (find that molecule by describing it!)
- **SageMaker** for ML pipelines (train models on your curated data)

My partner walked in, saw the whiteboard, and just shook their head. "Another weekend project?" they asked. "Yep!" I said, grinning. "This one's going to be epic."

## Sunday Afternoon: The "Leanda NG" Vision 🎯

Sunday afternoon was naming time! I decided to call the new version **"Leanda NG"** (Next Generation, obviously - I'm not creative with names). Here's my plan:

### The Stack (2025 Edition)

- **Backend**: Java 21 + Quarkus 3.x (fast, cloud-native, beautiful - and I've been wanting to try Quarkus!)
- **ML Services**: Python 3.12+ + FastAPI (because ML needs Python, and FastAPI is just delightful)
- **Frontend**: Angular 21 (zoneless, Signal Forms, AI tooling - the works!)
- **Infrastructure**: AWS CDK (TypeScript, because I'm already comfortable with it)
- **Messaging**: Amazon MSK (Kafka) + EventBridge (bye bye RabbitMQ - never liked you anyway!)
- **Database**: DocumentDB + DynamoDB Streams (managed, scalable, and I don't have to babysit it)

### The Timeline (Realistic Weekend Hobby Edition)

- **Weeks 1-4**: Foundation setup (IAM, CDK, project structure) - *Evenings and weekends*
- **Weeks 5-12**: Core services rewrite (.NET → Quarkus) - *This is where it gets fun*
- **Weeks 13-18**: Domain parsers migration (Java 8 → 21) - *Should be straightforward*
- **Weeks 19-22**: ML services modernization - *Python time!*
- **Weeks 23-28**: Frontend rewrite (Angular 21) - *The pretty part*
- **Weeks 29-32**: Testing & deployment - *Make it actually work*

That's 8 months of weekend/evening work. Totally doable for a hobby project! 💪

## Sunday Evening: Weekend Reflections 🤔

As I'm wrapping up this first week of planning, here's what I learned:

1. **Technical debt is real** (and it accumulates interest faster than credit cards)
2. **Modernization is actually fun** (when it's not your day job!)
3. **Architecture matters** (a good foundation makes everything easier)
4. **AWS has amazing tools** (lakehouse architecture? Yes please! And I can learn it on AWS Free Tier first)
5. **Hobby projects are the best** (no deadlines, no pressure, just pure learning and fun)

## Technical Summary: The Legacy Stack 📊

Okay, so I spent some time cataloging what we're actually dealing with here. It's... a lot. But knowledge is power, right? Here's the complete technical inventory:

### Technology Stack Summary

Here's the complete rundown of what we're modernizing:

**Backend Frameworks:**

- **.NET Core** - Currently 3.1 / Standard 2.0 (EOL since Dec 2022) → **Target: Java 21 + Quarkus 3.x**
- **Java** - Currently Java 8 (EOL) → **Target: Java 21 LTS**
- **Spring Boot** - Currently 2.0.0.RC1 (a pre-release from 2018!) → **Target: Quarkus 3.x**

**Frontend:**

- **Angular** - Currently Angular 9 (EOL since May 2021) → **Target: Angular 21**
- **TypeScript** - Currently 3.7.5 (EOL) → **Target: TypeScript 5.x**

**Databases & Storage:**

- **MongoDB** - Currently 3.6 (EOL) → **Target: DocumentDB / MongoDB 7+**
- **EventStore** - Currently 4.0.2 (EOL) → **Target: DynamoDB Streams**
- **Redis** - Currently Redis 4 (EOL) → **Target: Redis 7+ / ElastiCache**

**Messaging & Infrastructure:**

- **RabbitMQ** - Currently legacy version (deprecated) → **Target: Amazon MSK / EventBridge**

**ML & Data Science:**

- **Python ML** - Currently legacy stack with RDKit 2017 (very outdated) → **Target: Python 3.12+ / FastAPI**

**Testing & CI/CD:**

- **Testing** - Currently Protractor (deprecated) → **Target: Playwright**
- **CI/CD** - Currently Travis CI (shut down in 2023) → **Target: GitHub Actions** (CI/CD postponed until full migration is complete)

### Repository Structure

The project is split across **28 separate GitHub repositories** in the [ArqiSoft organization](https://github.com/ArqiSoft):

- Most repos last updated 2019-2021
- Low community engagement (0 stars, 0 forks, no active issues/PRs in most repos)
- Fragmented structure makes maintenance and coordination difficult
- Each microservice is its own repo, leading to duplicated CI/CD setups and inconsistent versioning

### The Challenge

We're not just upgrading versions - we're:

1. **Unifying the stack** - From C#/Java/Python/TypeScript to Java/Python/TypeScript
2. **Modernizing infrastructure** - From self-managed (RabbitMQ, MongoDB, EventStore) to AWS managed services
3. **Adopting modern patterns** - Serverless-first, event-driven, AI-native
4. **Improving developer experience** - Better tooling, testing, CI/CD, documentation
5. **Reducing operational overhead** - Managed services, auto-scaling, less babysitting

It's a complete platform modernization, but done as a weekend hobby project because... why not? 😄

## Key Decisions Made This Weekend ✅

- ✅ Adopt AWS-native architecture (serverless-first, managed services - less ops for me!)
- ✅ Unify backend to Java 21/Quarkus (bye bye C# fragmentation - one less language to context-switch)
- ✅ Use Apache Iceberg for data lake (open standards, future-proof, and I've been curious about it)
- ✅ Integrate Bedrock AI for curation (let AI do the heavy lifting - I'm lazy like that)
- ✅ Create "Leanda NG" as greenfield rewrite (parallel to existing system - no pressure!)

## What's Next Weekend? 🔮

*Update: Well, we've come a long way since that first weekend! Here's what's actually next:*

Since we're at ~92% complete, the remaining work is mostly polish and final touches:

- **Expand monitoring & alerting** - Add more CloudWatch alarms and X-Ray integration for better observability
- **Final integration testing** - Run end-to-end tests to verify everything works together in the CDK-deployed environment
- **Fix minor issues** - Address a few topic name mismatches and API version alignment issues
- **Production deployment prep** - Final checklist and deployment runbooks

Honestly, we're so close to done that it's kind of surreal. What started as a weekend curiosity has become a nearly complete, production-ready platform. The multi-agent system did most of the heavy lifting, and I'm just here to add the finishing touches! 🎨

Stay tuned for the final deployment! 🚀

---

*P.S. - If you're reading this in the future and Leanda NG is already deployed, know that I started with curiosity, a whiteboard, way too much coffee, and the naive optimism that comes with weekend hobby projects. Also, my AWS bill better not be too high... ☕*

*P.P.S. - If this project is still incomplete in 6 months, no judgment. Hobby projects are allowed to evolve at their own pace! 😊*

*P.P.P.S. - The multi-agent coordination framework might be overkill for a solo hobby project, but hey, I like to plan things properly. Plus, if I ever get help (or clone myself), we'll be ready! 🤖*

*P.P.P.P.S. - UPDATE: I've actually set up the AI agent execution framework! Created with COORDINATION.md, agent prompts, and helper scripts. Now I can run AI agents (like Cursor's agent system) in parallel to work on different parts. Each agent reads COORDINATION.md to check dependencies, does their work, and updates the coordination file. It's like having 5 AI assistants working together! The prompts are ready in `AGENT_PROMPTS.md` - just copy and paste into Cursor to start each agent session. This is going to be fun! 🚀*

---

## Where We Are Now: The Journey So Far 🎉

*Update: This weekend hobby project has evolved into something much bigger!*

### Current Status: ~92% Complete! 🎊

What started as a "quick weekend look" has turned into a comprehensive modernization effort. Here's the quick summary:

**What's Done:**
- ✅ **11 services** migrated to Java 21/Quarkus (100% complete!)
- ✅ **Frontend** migrated to Angular 21
- ✅ **Infrastructure** fully designed with AWS CDK (9 stacks)
- ✅ **CI/CD** automated with GitHub Actions (postponed until full migration)
- ✅ **Multi-agent system** - 24 AI agents coordinated the work in parallel
- ✅ **Autonomous testing** - Self-healing test suite that fixes issues automatically!

**What's Left:**
Just a few finishing touches - monitoring expansion, final integration tests, and some minor fixes.

From a weekend hobby project to a ~92% complete, production-ready modernization. The multi-agent coordination system worked better than expected - it was like having a whole team of developers working simultaneously! 🚀

*Last Updated: 2025-12-28*
