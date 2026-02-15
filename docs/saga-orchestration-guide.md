# Saga Orchestration Guide

This guide describes how saga orchestration works in Leanda NG (Phase 4, greenfield distro), how to add new workflows, compensation patterns, and correlation ID usage. See [ADR 0008](adr/0008-saga-orchestration-strategy.md).

## Overview

- **Phase 1 (event-driven)**: core-api runs `FileProcessingOrchestrator` and related components. State is stored in DynamoDB (`workflow-state` table). Kafka commands are sent to parser/office services; events are consumed to advance state. Used for Generic, Chemical, Office file processing.
- **Phase 2 (Step Functions)**: Optional CDK stack (`SagaOrchestrationStack`) defines state machines for file processing and ML training. Lambda handlers invoke parsers or publish to Kafka. EventBridge rules can start workflows when saga events are put on the event bus. Deploy with `DEPLOY_SAGA_ORCHESTRATION=true`.
- **Phase 3 (Kafka Streams)**: Optional high-volume processor in core-api (`FileProcessingStreamProcessor`) uses KTable for saga state. Enable by configuring `quarkus.kafka-streams.bootstrap-servers` and related options.

## Correlation ID Strategy

- Every saga instance has a **correlation ID** (UUID). It is set when the workflow starts and must be propagated in all commands and events.
- **Payload**: Commands and events include `CorrelationId` (or `correlationId` for camelCase contracts) in the JSON body.
- **Usage**: core-api generates the correlation ID in `FileProcessingOrchestrator.startFileProcessing()` and passes it to parser/office commands. Parser and office services echo it back in their events. The orchestrator uses it to look up `WorkflowState` and update state.
- **Contracts**: See `shared/contracts/events/file-processing-saga.yaml`, `record-processing-saga.yaml`, `ml-training-saga.yaml`.

## Adding a New File Workflow Type

1. **Contract**: Add the workflow type to the `WorkflowType` enum in `shared/contracts/events/file-processing-saga.yaml` if new.
2. **Orchestrator**: In `FileProcessingOrchestrator.startFileProcessing()`, add a `switch` case for the new type: create state, publish the first command to the appropriate Kafka topic (e.g. new parser command topic), and return the correlation ID.
3. **Event handlers**: Add `@Incoming("new-parser-events")` (and failed topic) in `FileProcessingOrchestrator` to update state (e.g. set parseCompleted) and call `checkAndAdvanceFileProcessing()` when the composite set is complete.
4. **Configuration**: Add Kafka channel config in core-api `application.properties` for the new command topic (outgoing) and event topics (incoming).

## Compensation

- **When**: On parser/office failure (e.g. `chemical-file-parse-failed`, or office conversion failed), the orchestrator calls `CompensationHandler.compensateFileProcessing(correlationId, message)`.
- **What**: Compensation publishes `FileProcessingFailed` and `FileProcessingCompensated` to Kafka, then deletes the workflow state for that correlation ID. Downstream consumers can mark the file as failed or trigger cleanup.
- **Extending**: To add rollback actions (e.g. delete blob, update file status in DB), implement them in `CompensationHandler` or call a dedicated service from there.

## Composite Events

- **Concept**: Some workflows advance only when multiple steps have completed (e.g. thumbnail + parse + record processing; patterns analogous to EndProcessing, FileParseDone, AllPersisted).
- **Implementation**: `FileProcessingState` has flags such as `thumbnailCompleted`, `parseCompleted`, `recordProcessingCompleted`, `metadataCompleted`, `indexingCompleted`. Event handlers set these when the corresponding events arrive. `checkAndAdvanceFileProcessing()` advances to Processed only when the required set for that workflow type is true.

## Step Functions (Phase 2)

- **Deploy**: Set `DEPLOY_SAGA_ORCHESTRATION=true` and run `cdk deploy` for the saga orchestration stack. IAM and CDK changes require explicit review per project rules.
- **EventBridge**: The stack adds a rule on the project event bus for `source: leanda.saga`, `detailType: FileProcessingStarted`. Put such events on the bus (e.g. from a Kafka connector or Lambda) to start the file processing state machine.
- **Lambdas**: Handlers under `infrastructure/lib/lambdas/saga-handlers/` are placeholders; implement Kafka publish or ECS/HTTP invocation as needed.

## Kafka Streams (Phase 3)

- **Config**: `quarkus.kafka-streams.bootstrap-servers`, `quarkus.kafka-streams.application-id=core-api-saga-streams`. Optional: `quarkus.kafka-streams.topics=file-processing-started` and timeout.
- **Topology**: `FileProcessingStreamProcessor` builds a minimal topology (KStream from `file-processing-started`, KTable state by correlationId). Extend for joins, aggregations, or output topics as needed.
