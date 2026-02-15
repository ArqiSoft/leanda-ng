# Legacy Saga Implementations Inventory

## Overview

This document catalogs all legacy saga implementations using MassTransit/Automatonymous state machines in the .NET codebase. These sagas orchestrate long-running distributed transactions for file processing, record processing, and ML training workflows.

**Total Unique Sagas**: 16 unique saga types (duplicated between `leanda-core` and `leanda-services`)

**Technology Stack**:
- **Framework**: MassTransit with Automatonymous
- **State Storage**: MongoDB (`SagaStateMachineInstance`)
- **Messaging**: RabbitMQ (deprecated, migrating to Kafka)
- **Pattern**: Orchestration-based sagas with centralized state machines

## Saga Categories

### 1. File Processing Sagas (8 types)

Orchestrate the complete workflow from file upload to processed state, including parsing, thumbnail generation, metadata extraction, and indexing.

#### 1.1 ChemicalFileProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Chemicals/Sagas/ChemicalFileProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Chemicals/Sagas/ChemicalFileProcessingStateMachine.cs`
- **State Class**: `ChemicalFileProcessingState`
- **Purpose**: Orchestrates chemical file (MOL, SDF, CDX) processing workflow
- **States**: `Processing` → `PostProcessing` → `Processed`
- **Key Events**: 
  - `ProcessFile` (initial)
  - `FileParsed` / `FileParseFailed`
  - `SubstanceProcessed` / `InvalidRecordProcessed`
  - `ThumbnailGenerated`
  - `AggregatedPropertiesAdded`
  - `MetadataGenerated`
- **Composite Events**: 
  - `EndProcessing` (waits for thumbnail generation, file parsing, record processing)
  - `FileParseDone` (waits for total records update, fields addition)
  - `AllPersisted` (waits for status persistence)

#### 1.2 CrystalFileProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Crystals/Sagas/CrystalFileProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Crystals/Sagas/CrystalFileProcessingStateMachine.cs`
- **State Class**: `CrystalFileProcessingState`
- **Purpose**: Orchestrates crystal file (CIF) processing workflow
- **Similar pattern to ChemicalFileProcessingStateMachine**

#### 1.3 ReactionFileProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Reactions/Sagas/ReactionFileProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Reactions/Sagas/ReactionFileProcessingStateMachine.cs`
- **State Class**: `ReactionFileProcessingState`
- **Purpose**: Orchestrates reaction file (RXN, RDF) processing workflow

#### 1.4 SpectrumFileProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Spectra/Sagas/SpectrumFileProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Spectra/Sagas/SpectrumFileProcessingStateMachine.cs`
- **State Class**: `SpectrumFileProcessingState`
- **Purpose**: Orchestrates spectra file (JCAMP-DX) processing workflow
- **States**: `Processing` → `PostProcessing` → `Processed`
- **Key Events**:
  - `ProcessFile` (initial)
  - `FileParsed` / `FileParseFailed`
  - `SpectrumProcessed` / `SpectrumProcessingFailed`
  - `MetadataGenerated`

#### 1.5 GenericFileProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Generic/Sagas/GenericFileProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Generic/Sagas/GenericFileProcessingStateMachine.cs`
- **State Class**: `GenericFileProcessingState`
- **Purpose**: Orchestrates generic file processing workflow (fallback for unknown file types)
- **Key Events**:
  - `ProcessGenericFile` (initial)
  - `ImageGenerated` / `ImageGenerationFailed`
  - `ImageAdded`
  - `FileProcessed`

#### 1.6 OfficeFileProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Office/Sagas/OfficeFileProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Office/Sagas/OfficeFileProcessingStateMachine.cs`
- **State Class**: `OfficeFileProcessingState`
- **Purpose**: Orchestrates office document processing workflow (Word, Excel, PowerPoint, etc.)

#### 1.7 WebPageProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.WebPage/Sagas/WebPageProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.WebPage/Sagas/WebPageProcessingStateMachine.cs`
- **State Class**: `WebPageProcessingState`
- **Purpose**: Orchestrates web page processing workflow

#### 1.8 MicroscopyFileProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Leanda.Microscopy/Sagas/MicroscopyFileProcessingStateMachine.cs`
- **State Class**: `MicroscopyFileProcessingState`
- **Purpose**: Orchestrates microscopy file processing workflow
- **Note**: Only exists in `leanda-core`, not in `leanda-services`

### 2. Record Processing Sagas (5 types)

Orchestrate individual record processing within files (e.g., processing each chemical substance, crystal, or spectrum record).

#### 2.1 SubstanceProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Chemicals/Sagas/SubstanceProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Chemicals/Sagas/SubstanceProcessingStateMachine.cs`
- **State Class**: `SubstanceProcessingState`
- **Purpose**: Orchestrates individual chemical substance record processing
- **Note**: Triggered by `ChemicalFileProcessingStateMachine` for each record

#### 2.2 InvalidSubstanceProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Chemicals/Sagas/InvalidSubstanceProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Chemicals/Sagas/InvalidSubstanceProcessingStateMachine.cs`
- **State Class**: `InvalidSubstanceProcessingState`
- **Purpose**: Handles invalid chemical substance records that fail validation

#### 2.3 CrystalProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Crystals/Sagas/CrystalProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Crystals/Sagas/CrystalProcessingStateMachine.cs`
- **State Class**: `CrystalProcessingState`
- **Purpose**: Orchestrates individual crystal record processing

#### 2.4 ReactionProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Reactions/Sagas/ReactionProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Reactions/Sagas/ReactionProcessingStateMachine.cs`
- **State Class**: `ReactionProcessingState`
- **Purpose**: Orchestrates individual reaction record processing

#### 2.5 SpectrumProcessingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.Spectra/Sagas/SpectrumProcessingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.Spectra/Sagas/SpectrumProcessingStateMachine.cs`
- **State Class**: `SpectrumProcessingState`
- **Purpose**: Orchestrates individual spectrum record processing

### 3. Machine Learning Sagas (3 types)

Orchestrate ML model training, optimization, and prediction workflows.

#### 3.1 TrainingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.MachineLearning/Sagas/TrainingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.MachineLearning/Sagas/TrainingStateMachine.cs`
- **State Class**: `TrainingState`
- **Purpose**: Orchestrates ML model training workflow
- **States**: `Optimization` → `Training` → `Processed`
- **Key Events**:
  - `StartTraining` (initial)
  - `TrainingOptimized` / `TrainingOptimizationFailed`
  - `ModelTrainingFinished` / `ModelTrainingFailed`
  - `ReportGenerated` / `ReportGenerationFailed`
  - `GenericFileProcessed`
  - `FolderDeleted` (cancellation)
- **Composite Events**:
  - `EndOptimization` (waits for optimization and metrics processing)
  - `EndTraining` (waits for report generation and all generic file processing)

#### 3.2 ModelTrainingStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.MachineLearning/Sagas/ModelTrainingStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.MachineLearning/Sagas/ModelTrainingStateMachine.cs`
- **State Class**: `ModelTrainingState`
- **Purpose**: Orchestrates individual ML model training (one model per training method)
- **Note**: Multiple instances created by `TrainingStateMachine` (one per training method)

#### 3.3 PropertiesPredictionStateMachine
- **Location**: 
  - `legacy/leanda-core/Sds.Osdr.MachineLearning/Sagas/PropertiesPredictionStateMachine.cs`
  - `legacy/leanda-services/Source/Services/OsdrService/Sds.Osdr.MachineLearning/Sagas/PropertiesPredictionStateMachine.cs`
- **State Class**: `PropertiesPredictionState`
- **Purpose**: Orchestrates property prediction workflow using trained models

## Active Sagas (Registered in SagaHost)

Based on `DomainSagaHostService.cs`, the following sagas are **actively registered**:

```csharp
// Active modules in SagaHost
Assembly.LoadFrom("Sds.Osdr.Generic.dll"),           // GenericFileProcessingStateMachine
Assembly.LoadFrom("Sds.Osdr.RecordsFile.dll"),       // (no saga, but used)
Assembly.LoadFrom("Sds.Osdr.Chemicals.dll"),         // ChemicalFileProcessingStateMachine, SubstanceProcessingStateMachine, InvalidSubstanceProcessingStateMachine
Assembly.LoadFrom("Sds.Osdr.Pdf.dll"),              // (no saga found)
Assembly.LoadFrom("Sds.Osdr.Images.dll"),            // (no saga found)
Assembly.LoadFrom("Sds.Osdr.Office.dll"),            // OfficeFileProcessingStateMachine
Assembly.LoadFrom("Sds.Osdr.Tabular.dll"),           // (no saga found)
```

**Commented Out (Not Active)**:
- `Sds.Osdr.Crystals.dll` - CrystalFileProcessingStateMachine, CrystalProcessingStateMachine
- `Sds.Osdr.Reactions.dll` - ReactionFileProcessingStateMachine, ReactionProcessingStateMachine
- `Sds.Osdr.Spectra.dll` - SpectrumFileProcessingStateMachine, SpectrumProcessingStateMachine
- `Sds.Osdr.MachineLearning.dll` - TrainingStateMachine, ModelTrainingStateMachine, PropertiesPredictionStateMachine
- `Sds.Osdr.WebPage.dll` - WebPageProcessingStateMachine
- `Leanda.Microscopy.dll` - MicroscopyFileProcessingStateMachine

## Saga Infrastructure

### State Storage
- **Repository**: MongoDB (`MongoDbSagaRepositoryFactory`)
- **Collection**: `sagas` (default)
- **State Interface**: `SagaStateMachineInstance` (from MassTransit)
- **Versioning**: `IVersionedSaga` interface for optimistic concurrency

### Registration Pattern
Sagas are registered via module extensions:
```csharp
// In each module's Module.cs
configurator.RegisterStateMachine<ChemicalFileProcessingStateMachine, ChemicalFileProcessingState>(provider);
```

### Common State Properties
All saga states include:
- `Guid CorrelationId` - For event correlation
- `string CurrentState` - Current state machine state
- `Guid _id` - MongoDB document ID
- `int Version` - For optimistic concurrency
- `DateTimeOffset Created` - Creation timestamp
- `DateTimeOffset Updated` - Last update timestamp

## Migration Notes

### Key Patterns to Preserve
1. **Composite Events**: Waiting for multiple events before proceeding (e.g., `EndProcessing`)
2. **State Transitions**: Clear state progression (Processing → PostProcessing → Processed)
3. **Compensation**: Implicit through state machine transitions
4. **Correlation IDs**: Used throughout for event correlation
5. **Concurrency Control**: Version-based optimistic locking

### Modernization Targets
- Replace MassTransit/Automatonymous with AWS Step Functions or Kafka Streams
- Replace RabbitMQ with MSK Serverless (Kafka)
- Replace MongoDB saga storage with DynamoDB (for Step Functions) or KTable (for Kafka Streams)
- Maintain correlation ID propagation
- Preserve composite event patterns

### Correlation ID Strategy (Modern)
- All saga-related commands and events carry a `correlationId` (UUID) in payload and (where applicable) in Kafka headers.
- core-api propagates `correlationId` when publishing commands and when persisting workflow state (see `shared/models/.../workflow/`).
- Format: UUID; same value for the entire saga instance. Documented in `shared/contracts/events/file-processing-saga.yaml`, `record-processing-saga.yaml`, `ml-training-saga.yaml`, and [ADR 0008](docs/adr/0008-saga-orchestration-strategy.md).

### Composite Event Equivalents (Modern)
- **EndProcessing** (file): Orchestrator stores completion flags per step (`thumbnailCompleted`, `parseCompleted`, `recordProcessingCompleted`, etc.) in `FileProcessingState`; advances to PostProcessing only when all required steps are complete (see `FileProcessingState` in shared/models).
- **EndOptimization** (ML): Orchestrator waits for optimization and metrics processing flags before advancing.
- **EndTraining** (ML): Orchestrator waits for report generation and generic file processing before marking Processed.

## File Count Summary

- **Total StateMachine files**: 31 (duplicated between core and services)
- **Unique saga types**: 16
- **Active sagas**: ~6 (based on SagaHost registration)
- **Infrastructure files**: 6 (saga observers, repository factories)

## References

- [Modern Saga Pattern Implementation Plan](../.cursor/plans/modernize_saga_pattern_implementation_c2e80b0d.plan.md)
- [Core Services Implementation Plan](../shared/specs/implementation/core-services-plan.md)
- Legacy saga implementations in `legacy/leanda-core/` and `legacy/leanda-services/`

