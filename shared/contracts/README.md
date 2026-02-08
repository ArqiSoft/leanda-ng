# Leanda Contracts

This directory contains API and event contracts for the Leanda platform.

## Contents

- **blob-storage-api.yaml** – OpenAPI 3.1 for the Blob Storage service (upload, download, delete, info).
- **events.yaml** – Index of event specifications (see below). The canonical domain event spec is in `../specs/events/domain-events.yaml`.
- **events/** – Service-specific AsyncAPI contracts (blob, imaging, indexing, office-processor, parsers, sagas).

## Domain events (canonical)

**Source of truth:** [../specs/events/domain-events.yaml](../specs/events/domain-events.yaml)

That file defines all domain events and commands (users, folders, files, records, ML, exports, processing, notifications) in AsyncAPI 2.6 format. Use it for payload schemas and channel names when implementing or consuming domain events.

## Service-specific contracts

Each file under `events/` describes the Kafka topics, commands, and events for one service or saga:

| File | Description |
|------|-------------|
| blob-events.yaml | BlobLoaded when files are uploaded |
| imaging-events.yaml | GenerateImage command; ImageGenerated / ImageGenerationFailed |
| office-processor-events.yaml | ConvertToPdf, ExtractMeta commands and result events |
| indexing-events.yaml | File/folder/record persisted; EntityIndexed |
| metadata-events.yaml | Metadata generation command and events |
| chemical-parser-events.yaml | Chemical file parse commands and events |
| chemical-properties-events.yaml | Chemical properties calculation |
| reaction-parser-events.yaml | Reaction file parser |
| crystal-parser-events.yaml | Crystal parser |
| spectra-parser-events.yaml | Spectra parser |
| file-processing-saga.yaml | File processing saga |
| record-processing-saga.yaml | Record processing saga |
| ml-training-saga.yaml | ML training saga |

## API contracts

- **Core API:** [../specs/api/core-api.yaml](../specs/api/core-api.yaml) – OpenAPI 3.1 for the Core API (nodes, entities, users, exports, ML, categories, search, notifications, etc.).
