# Claude Code Agent Coordination

This document provides Claude Code-specific guidance for working with the Leanda.io multi-agent coordination system.

**Last Updated**: 2025-01-10
**AI Tool**: Claude Code (CLI)

---

## Quick Start for Claude Code

### 1. Initial Setup

When starting a Claude Code session for this project:

```bash
# Navigate to project root
cd /path/to/mono-repo

# Start Claude Code
claude

# First command: Read the coordination status
# Claude will automatically read CLAUDE.md, then you can ask it to:
# "Read docs/agents/COORDINATION.md and summarize the current project status"
```

### 2. Understanding Your Role

Claude Code can operate as any of the defined agents. Before starting work:

1. **Read CLAUDE.md** - Claude Code reads this automatically
2. **Read COORDINATION.md** - Check current status and blockers
3. **Identify your task** - What agent role are you fulfilling?
4. **Check dependencies** - Are prerequisite agents complete?

---

## Claude Code Agent Types

### Available Subagent Types

Claude Code has specialized agents you can invoke via the `Task` tool:

| Subagent Type | Purpose | When to Use |
|--------------|---------|-------------|
| `Explore` | Codebase exploration | Finding files, understanding structure |
| `Plan` | Implementation planning | Designing solutions, creating plans |
| `Bash` | Command execution | Git, npm, docker operations |
| `general-purpose` | Multi-step tasks | Complex research, code changes |

### Mapping to Leanda Agents

| Leanda Agent | Claude Code Approach |
|-------------|---------------------|
| Team Lead | Use `general-purpose` agent for technology monitoring |
| Cloud QA | Use `Explore` + `general-purpose` for test analysis |
| PROD-1 (CDK) | Use `Plan` for design, then implement directly |
| PROD-2 (CI/CD) | Edit workflow files directly after exploration (CI/CD postponed until full migration) |
| PROD-3 (Monitoring) | Use `Explore` to understand, then implement |
| UI-UX | Use `Explore` for frontend analysis |

---

## Workflow Patterns

### Pattern 1: Exploration Task

For understanding the codebase or researching a topic:

```
User: "Find all event handlers in the codebase"

Claude Code should:
1. Use Task tool with subagent_type="Explore"
2. Search for event handler patterns
3. Summarize findings
```

### Pattern 2: Implementation Task

For implementing features or fixing bugs:

```
User: "Add a new health endpoint to the blob-storage service"

Claude Code should:
1. Read docs/agents/COORDINATION.md (check status)
2. Read existing service code (understand patterns)
3. Use TodoWrite to plan steps
4. Implement changes using Edit tool
5. Run tests via Bash
6. Update documentation
```

### Pattern 3: Multi-Agent Coordination

For complex tasks requiring multiple agent perspectives:

```
User: "Review and improve the integration tests"

Claude Code should:
1. Read COORDINATION.md (understand Agent QA-Cloud's work)
2. Launch Explore agent to analyze test coverage
3. Use Plan agent for improvement strategy
4. Implement changes iteratively
5. Update COORDINATION.md with progress
```

---

## Claude Code-Specific Commands

### Checking Project Status

```
# Ask Claude to summarize current status
"What's the current project status? Read COORDINATION.md"

# Ask Claude to check a specific agent
"What's Agent PROD-6's status and what needs to be done?"
```

### Running Services Locally

```
# Ask Claude to start services
"Start the local development environment using docker-compose"

# Claude will run:
# cd docker && docker-compose up -d
```

### Running Tests

```
# Ask Claude to run tests for a service
"Run tests for the chemical-parser service"

# Claude will run:
# cd services/chemical-parser && mvn test
```

### Checking Health

```
# Ask Claude to check service health
"Check if all services are healthy"

# Claude will use the health-check.sh script or curl commands
```

---

## Coordination Protocol for Claude Code

### Before Starting Work

1. **Read CLAUDE.md** (automatic)
2. **Read COORDINATION.md**:
   ```
   "Read docs/agents/COORDINATION.md and tell me:
    - What phase are we in?
    - What agents are active?
    - Are there any blockers?"
   ```
3. **Identify your agent role**:
   ```
   "I want to work as Agent PROD-6 (Saga Modernization).
    What are the prerequisites and current status?"
   ```

### During Work

1. **Track progress with TodoWrite**:
   ```
   Claude Code should use TodoWrite to:
   - Create task list at start
   - Mark tasks in_progress/completed
   - Track blockers
   ```

2. **Update COORDINATION.md** (every 30-60 minutes for long tasks):
   ```
   "Update my status in COORDINATION.md to show:
    - Current task being worked on
    - Progress made
    - Any blockers encountered"
   ```

### When Completing

1. **Run all tests**:
   ```
   "Run the full test suite and verify everything passes"
   ```

2. **Update documentation**:
   ```
   "Update the service README to reflect the changes made"
   ```

3. **Mark complete in COORDINATION.md**:
   ```
   "Mark Agent [X] as complete in COORDINATION.md and
    document what was accomplished"
   ```

---

## Parallel Agent Execution

Claude Code can run multiple agents in parallel for independent tasks:

### Example: Parallel Exploration

```
User: "Explore both the frontend and backend test patterns"

Claude Code should launch parallel Task agents:
1. Task agent 1: Explore frontend/src/**/*.spec.ts
2. Task agent 2: Explore services/**/src/test/**
```

### Example: Parallel Health Checks

```
User: "Check health of all services"

Claude Code should:
- Launch multiple parallel Bash commands for health checks
- Aggregate results
```

---

## Best Practices for Claude Code

### Do

- **Read before writing**: Always read existing code before making changes
- **Use Explore agent**: For codebase understanding, use specialized Explore agent
- **Track with TodoWrite**: Break complex tasks into tracked items
- **Run tests**: Always run tests after making changes
- **Check COORDINATION.md**: Verify status before major work

### Don't

- **Don't guess file locations**: Use Glob/Grep to find files
- **Don't skip tests**: Always verify changes work
- **Don't ignore blockers**: Report blockers in COORDINATION.md
- **Don't work on blocked tasks**: Check dependencies first
- **Don't forget documentation**: Update READMEs and contracts

---

## Common Claude Code Commands for This Project

### Project Navigation

```
"Show me the project structure"
"Find all Java services in the project"
"What contracts exist in shared/contracts?"
```

### Code Understanding

```
"Explain how the chemical-parser service processes files"
"What events does core-api publish?"
"Show me the integration test patterns used"
```

### Implementation

```
"Add a new endpoint to [service] that does [X]"
"Create an integration test for [scenario]"
"Update the CDK stack to add [resource]"
```

### Testing

```
"Run tests for all services"
"Run integration tests only"
"Check test coverage for [service]"
```

### Documentation

```
"Update the README for [service]"
"Create an ADR for [decision]"
"Document the new [feature]"
```

---

## Troubleshooting

### Claude Code Can't Find Files

```
# Use Explore agent for broad searches
"Use Explore agent to find files related to [topic]"

# Use Glob for pattern-based searches
"Find all files matching *.yaml in shared/"
```

### Tests Are Failing

```
# Get detailed test output
"Run tests with verbose output and show failures"

# Check test dependencies
"Are all test infrastructure services running?"
```

### Services Not Starting

```
# Check docker status
"Run docker ps and show service status"

# Check logs
"Show logs for [service] from docker-compose"
```

---

## Integration with Cursor Agents

This project also supports Cursor AI agents. The coordination files are shared:

- **COORDINATION.md** - Used by both Cursor and Claude Code
- **AGENT_PROMPTS.md** - Cursor-optimized prompts
- **CLAUDE_AGENT_PROMPTS.md** - Claude Code-optimized prompts

Both tools can work on the project simultaneously if they coordinate through COORDINATION.md.

---

## Quick Reference Card

| Task | Command/Action |
|------|---------------|
| Check status | Read `docs/agents/COORDINATION.md` |
| Start services | `cd docker && docker-compose up -d` |
| Run tests | `cd services/[name] && mvn test` |
| Check health | `./docs/agents/scripts/health-check.sh` |
| Update status | Edit `docs/agents/COORDINATION.md` |
| Find files | Use Glob or Explore agent |
| Understand code | Use Explore agent |
| Plan changes | Use Plan agent |
| Track tasks | Use TodoWrite tool |

---

**See Also**:
- `CLAUDE.md` - Main Claude Code configuration
- `COORDINATION.md` - Full agent status and dependencies
- `CLAUDE_AGENT_PROMPTS.md` - Claude Code agent prompts
- `README.md` - Agent system overview
