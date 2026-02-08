# Agent Coordination System

This directory contains the agent coordination system for parallel development of the Leanda NG modernization project using multiple AI agents.

## Overview

The agent coordination system enables multiple AI agents to work in parallel on different parts of the project while maintaining coordination and avoiding conflicts.

**Supported AI Tools**:
- **Cursor** - IDE-based AI assistant
- **Claude Code** - Anthropic's CLI for Claude

---

## Quick Start by Tool

### Cursor Quick Start

1. Open project in Cursor
2. Read `AGENT_PROMPTS.md` and copy your agent prompt
3. Paste into Cursor chat
4. Follow agent workflow

### Claude Code Quick Start

1. Navigate to project root: `cd /path/to/mono-repo`
2. Start Claude Code: `claude`
3. Claude reads `CLAUDE.md` automatically
4. Ask Claude to read `docs/agents/CLAUDE_AGENT_PROMPTS.md`
5. Copy desired agent prompt and paste

```bash
# Or use helper scripts
./docs/agents/scripts/claude-agent-init.sh   # Initialize session
./docs/agents/scripts/claude-status.sh       # Check status
./docs/agents/scripts/claude-commands.sh     # Common commands
```

---

## Key Files

### Shared Files (Both Tools)
- **`COORDINATION.md`** - Single source of truth for all agent status, dependencies, and project state

### Cursor Files
- **`AGENT_PROMPTS.md`** - Ready-to-use prompts for Cursor agents
- **`scripts/agent-init.sh`** - Cursor agent initialization
- **`scripts/agent-status.sh`** - Cursor agent status check
- **`scripts/health-check.sh`** - Service health check

### Claude Code Files
- **`CLAUDE.md`** (repo root) - Main Claude Code configuration
- **`CLAUDE_COORDINATION.md`** - Claude Code-specific coordination guide
- **`CLAUDE_AGENT_PROMPTS.md`** - Ready-to-use prompts for Claude Code
- **`scripts/claude-agent-init.sh`** - Claude Code agent initialization
- **`scripts/claude-status.sh`** - Claude Code status check
- **`scripts/claude-commands.sh`** - Common Claude Code commands

## Quick Start

### 1. Choose Your Agent

Open `AGENT_PROMPTS.md` and find your agent's prompt:
- **Phase 3 ML Services**: Agent ML-1, ML-2, ML-3
- **Phase 4 Production**: Agent PROD-1, PROD-2, PROD-3
- **General Purpose**: Feature Agent, Bug Fix Agent, Refactor Agent, Documentation Agent

### 2. Initialize Agent Session

```bash
# Run initialization script
./docs/agents/scripts/agent-init.sh

# Or manually read coordination file
cat docs/agents/COORDINATION.md
```

### 3. Start Agent Work

1. Copy your agent's prompt from `AGENT_PROMPTS.md`
2. Paste into Cursor chat
3. Agent will:
   - Read `COORDINATION.md`
   - Check dependencies
   - Update status
   - Begin work

### 4. Check Status

```bash
# Check all agent status
./docs/agents/scripts/agent-status.sh

# Check service health
./docs/agents/scripts/health-check.sh
```

## How It Works

### Coordination Protocol

1. **Before Starting**: Agent reads `COORDINATION.md` to check:
   - Dependencies (are required agents/services complete?)
   - Current status (is someone else working on this?)
   - Blockers (any issues preventing work?)

2. **During Work**: Agent updates `COORDINATION.md`:
   - Mark status as "🟢 In Progress"
   - Update progress every 30-60 minutes
   - Propose changes to shared artifacts if needed

3. **When Complete**: Agent updates `COORDINATION.md`:
   - Mark status as "✅ Complete"
   - Document what was completed
   - Note any blockers or issues

### Status Indicators

- ⏳ **Not Started** - Agent hasn't begun work
- 🟢 **In Progress** - Agent is actively working
- 🟡 **Blocked** - Agent is waiting on dependencies or blockers
- ✅ **Complete** - Agent has finished their work
- 📋 **Planned** - Work is planned but not yet started

### Path Structure

All agents use the **consolidated project structure**:

```
mono-repo/
├── services/              # All microservices
├── ml-services/          # Python ML services
├── shared/               # Shared models and contracts
├── frontend/             # Angular 21 application
├── infrastructure/       # AWS CDK stacks
├── docker/               # docker-compose.yml
├── tests/                # Integration and E2E tests
└── docs/                 # Documentation
```

**Important**: All paths in agent prompts use this structure. Do not use old paths like `leanda-ng-phase2/` or `leanda-ng-core-distro/`.

## Agent Workflow

### Standard Workflow

1. **Read COORDINATION.md** - Check dependencies and status
2. **Read your agent prompt** - Understand your responsibilities
3. **Update status** - Mark yourself as "🟢 In Progress"
4. **Do the work** - Implement according to your prompt
5. **Update regularly** - Update COORDINATION.md every 30-60 minutes
6. **Test** - Ensure >80% code coverage
7. **Document** - Update service READMEs
8. **Mark complete** - Update status to "✅ Complete"

### Proposing Changes

If you need to change shared artifacts (models, contracts, etc.):

1. Add a proposal in `COORDINATION.md` under "Change Proposals"
2. Describe the change and rationale
3. Wait for coordination (check if other agents object)
4. Implement after coordination

## Helper Scripts

### agent-init.sh

Initializes an agent session by reading COORDINATION.md and showing current status.

```bash
./docs/agents/scripts/agent-init.sh
```

### agent-status.sh

Shows current status of all agents.

```bash
./docs/agents/scripts/agent-status.sh
```

### health-check.sh

Checks health of all services in docker-compose.

```bash
./docs/agents/scripts/health-check.sh
```

## Current Project Status

- ✅ **Phase 1**: Complete (Core API, Domain Services, Persistence, Testing, Docker)
- ✅ **Phase 2**: Complete (Parsers, Blob Storage, Office, Metadata, Indexing, Frontend, Integration)
- ⏳ **Phase 3**: Pending (ML Services - Feature Vectors, Modeler, Predictor)
- 📋 **Phase 4**: Planned (Production Deployment - AWS CDK, CI/CD postponed until full migration, Monitoring)

See `COORDINATION.md` for detailed status of each agent.

## Best Practices

1. **Always read COORDINATION.md first** - Don't start work without checking dependencies
2. **Update status regularly** - Keep others informed of your progress
3. **Coordinate changes** - Propose shared artifact changes before implementing
4. **Write tests** - Ensure >80% code coverage
5. **Document** - Update READMEs and documentation
6. **Report blockers** - Mark yourself as "🟡 Blocked" if stuck

## Troubleshooting

### Agent can't find COORDINATION.md

Make sure you're in the repo root:
```bash
cd /path/to/mono-repo
ls docs/agents/COORDINATION.md
```

### Dependencies not met

Check `COORDINATION.md` for dependency status. Wait for required agents to complete or mark yourself as "🟡 Blocked".

### Path errors

All paths use the consolidated structure. Use:
- `services/[service-name]/` (not `leanda-ng-phase2/services/`)
- `shared/` (not `leanda-ng-phase2/shared/`)
- `docker/docker-compose.yml` (not `leanda-ng-phase2/docker-compose.yml`)

## Additional Resources

- **Architecture Documentation**: `docs/architecture.md`
- **Migration Specs**: `docs/phases/`
- **Service READMEs**: `services/[service-name]/README.md`

---

**Last Updated**: 2025-01-10 - Added Claude Code support (CLAUDE.md, CLAUDE_COORDINATION.md, CLAUDE_AGENT_PROMPTS.md, helper scripts)

