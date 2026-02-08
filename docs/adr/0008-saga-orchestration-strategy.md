# 0008. Saga Orchestration Strategy

## Status
Accepted

## Context

Leanda.io legacy system uses MassTransit/Automatonymous sagas with RabbitMQ and MongoDB for file processing, record processing, and ML training workflows. Sixteen saga types exist (eight file processing, five record processing, three ML); five are actively registered (Generic, Chemical, Substance, InvalidSubstance, Office). The platform is migrating to Kafka (MSK Serverless), DocumentDB, and AWS-native orchestration. A clear strategy is needed for saga modernization that preserves business logic, composite events, correlation IDs, and compensation while moving off deprecated stack.

## Decision

Adopt a phased saga modernization strategy with three orchestration options, applied by workflow complexity:

### Scope Split

1. **Phase 1 — Event-driven choreography (Quarkus + Kafka)**  
   - **Use for**: Simple file and record processing workflows (Generic, Chemical, Office, Substance, InvalidSubstance).  
   - **Implementation**: `FileProcessingOrchestrator` and related components in core-api; state in DocumentDB; SmallRye Reactive Messaging for Kafka commands/events; correlation ID propagation and compensation in application code.  
   - **Rationale**: Low operational overhead, aligns with existing Quarkus/Kafka stack, sufficient for linear or modest branching flows.

2. **Phase 2 — AWS Step Functions**  
   - **Use for**: Complex, long-running, or highly branching workflows (e.g. multi-step file processing with retries, ML training orchestration).  
   - **Implementation**: CDK stack (`saga-orchestration-stack.ts`), state machines for file processing and ML training, Lambda/ECS step handlers, EventBridge for Kafka ↔ Step Functions integration.  
   - **Rationale**: Managed orchestration, built-in retries and error handling, visual workflow definition, and auditability.

3. **Phase 3 — Kafka Streams (optional)**  
   - **Use for**: High-volume, stateful processing where exactly-once semantics and stream processing are required.  
   - **Implementation**: Quarkus Kafka Streams extension; `FileProcessingStreamProcessor` with KTable/KStream; state in Kafka state stores.  
   - **Rationale**: Optional enhancement for scale; implement only if Phase 1/2 cannot meet throughput or consistency requirements.

### Correlation ID Strategy

- All saga-related commands and events carry a `correlationId` (UUID) in payload and (where applicable) in message headers.  
- core-api propagates `correlationId` when publishing commands and when persisting workflow state.  
- Step Functions execution name or input can carry `correlationId` for traceability; Lambda handlers pass it through to Kafka events.  
- Document in AsyncAPI saga contracts and in `docs/saga-orchestration-guide.md`.

### Composite Events

- Legacy composite events (e.g. EndProcessing: wait for thumbnail, parse, record processing) are implemented in Phase 1 by: (1) storing completion flags per step in workflow state, and (2) advancing state only when all required steps are complete.  
- In Step Functions, equivalent behavior is achieved with parallel branches and Join state.  
- Contracts and guide document which events form a composite set and the required completion criteria.

### Compensation

- Phase 1: `CompensationHandler` in core-api invokes rollback actions per step (e.g. mark file failed, publish compensation events); triggered on failure or timeout.  
- Phase 2: Step Functions supports Catch and fallback states; compensation steps are explicit states that call Lambda/ECS to perform rollback.  
- Document rollback procedures per workflow in `docs/saga-orchestration-guide.md`.

## Consequences

**Positive**

- Clear separation: simple workflows stay in Quarkus, complex ones use Step Functions, optional scale path with Kafka Streams.  
- No big-bang rewrite; legacy and modern orchestration can run in parallel with gradual cutover.  
- Alignment with AWS Well-Architected and existing MSK/DocumentDB/CDK usage.

**Negative**

- Two (or three) orchestration styles to maintain and document.  
- EventBridge and Lambda add moving parts for Step Functions integration.  
- IAM and CDK changes for Step Functions require explicit review per project rules.

## Alternatives Considered

- **Step Functions only**: Rejected for simple flows due to higher latency and cost vs in-process orchestration.  
- **Kafka Streams only**: Rejected as default due to operational and cognitive overhead for straightforward workflows.  
- **Keep MassTransit on RabbitMQ**: Rejected; RabbitMQ is deprecated and migration to Kafka is already decided (ADR-0002).
