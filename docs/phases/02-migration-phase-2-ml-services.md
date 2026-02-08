# Phase 2: ML Services Migration

## Overview

Modernize the ML Services from legacy Python to Python 3.12+ / FastAPI, maintaining ML functionality while improving architecture and deployment.

## Current State Analysis

### Legacy Services
- **Location**: `ml-services/Source/`
- **Stack**: Python (legacy versions), TensorFlow/Keras, scikit-learn
- **Services**:
  1. **Feature Vector Calculator** (`osdr_feature_vectors_calculator/`)
  2. **ML Modeler** (`osdr_ml_modeler/`) - Training, optimization, report generation
  3. **ML Predictor** (`osdr_ml_predictor/`) - Property prediction

### Service 1: Feature Vector Calculator

**Purpose**: Calculate molecular feature vectors from SDF files

**Message Contracts**:
- **Command**: `CalculateFeatureVectors` (from `calculate_feature_vectors.json`)
- **Event**: `FeatureVectorsCalculated` / `FeatureVectorsCalculationFailed`

**Processing**:
1. Receive command with SDF file blob ID
2. Download SDF file
3. Calculate fingerprints/features using RDKit
4. Store feature vectors
5. Publish success/failure event

### Service 2: ML Modeler

**Purpose**: Train ML models, optimize hyperparameters, generate reports

**Components**:
- **Model Trainer** (`model_trainer.py`) - Train models
- **Optimizer** (`optimizer.py`) - Hyperparameter optimization
- **Report Generator** (`report_generator.py`) - Generate training reports

**Message Contracts**:
- **Command**: `TrainModel` (from `train_model.json`)
- **Command**: `OptimizeTraining` (from `optimize_training.json`)
- **Event**: `ModelTrained`, `TrainingFailed`, `TrainingOptimized`, etc.

**Supported Algorithms**:
- Classic ML: Random Forest, SVM, Neural Networks
- Deep Learning: LSTM, DNN
- Feature types: Fingerprints, descriptors

### Service 3: ML Predictor

**Purpose**: Predict properties using trained models

**Components**:
- **Properties Predictor** (`properties_predictor.py`) - Batch prediction
- **Single Structure Predictor** (`single_structure_predictor.py`) - Single molecule prediction

**Message Contracts**:
- **Command**: `PredictProperties` (from `predictor_command.json`)
- **Command**: `SingleStructurePredict` (from `single_structure_predict_property.json`)
- **Event**: `PropertiesPredicted`, `PredictionFailed`

### Dependencies

- **RDKit**: Molecular processing
- **scikit-learn**: Classic ML algorithms
- **TensorFlow/Keras**: Deep learning
- **NumPy, Pandas**: Data processing
- **RabbitMQ**: Message consumption (via `mass_transit/`)

---

## Target Architecture

### FastAPI Service Structure

```
ml-services/
├── feature-vectors/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── services/
│   │   │   └── feature_calculator.py
│   │   └── models/
│   │       └── schemas.py
│   ├── tests/
│   └── requirements.txt
├── modeler/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── services/
│   │   │   ├── trainer.py
│   │   │   ├── optimizer.py
│   │   │   └── report_generator.py
│   │   └── models/
│   ├── tests/
│   └── requirements.txt
└── predictor/
    ├── app/
    │   ├── main.py
    │   ├── api/
    │   ├── services/
    │   │   ├── batch_predictor.py
    │   │   └── single_predictor.py
    │   └── models/
    ├── tests/
    └── requirements.txt
```

### Technology Stack

- **Framework**: FastAPI 0.115+
- **Python**: 3.12+
- **ML Libraries**:
  - RDKit 2024.x
  - scikit-learn 1.5+
  - PyTorch 2.5+ (replace TensorFlow)
- **Data**: Pandas 2.2+, NumPy 2.0+
- **Validation**: Pydantic v2
- **Messaging**: Kafka (via `aiokafka`)
- **Deployment**: AWS Lambda containers or ECS Fargate

---

## Migration Strategy

### Phase 1: Modernize Dependencies

1. **Update Python** to 3.12+
2. **Replace TensorFlow** with PyTorch (optional, can keep TF if needed)
3. **Update RDKit** to latest version
4. **Update scikit-learn** to 1.5+
5. **Replace RabbitMQ** with Kafka

### Phase 2: Refactor to FastAPI

1. **Create FastAPI applications** for each service
2. **Port message handlers** to FastAPI routes + Kafka consumers
3. **Update Pydantic models** (v2)
4. **Add OpenAPI documentation**

### Phase 3: Testing & Deployment

1. **Unit tests** - ML logic, feature calculation
2. **Integration tests** - End-to-end workflows
3. **Deployment** - Lambda containers or ECS

---

## Implementation Details

### Feature Vector Calculator (FastAPI)

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio

app = FastAPI(title="Feature Vector Calculator")

class CalculateFeatureVectorsCommand(BaseModel):
    id: str
    blob_id: str
    bucket: str
    user_id: str
    correlation_id: str

@app.post("/api/v1/calculate-feature-vectors")
async def calculate_feature_vectors(
    command: CalculateFeatureVectorsCommand,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(process_feature_calculation, command)
    return {"status": "accepted", "id": command.id}

async def process_feature_calculation(command: CalculateFeatureVectorsCommand):
    # Download SDF file
    sdf_data = await blob_storage.download_blob(command.blob_id, command.bucket)
    
    # Calculate features
    feature_vectors = await feature_calculator.calculate(sdf_data)
    
    # Store feature vectors
    await feature_storage.store(command.id, feature_vectors)
    
    # Publish event
    await event_publisher.publish_feature_vectors_calculated(
        command.id, feature_vectors, command.correlation_id
    )
```

### ML Modeler (FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ML Modeler")

class TrainModelCommand(BaseModel):
    id: str
    dataset_id: str
    algorithm: str
    hyperparameters: dict
    user_id: str
    correlation_id: str

@app.post("/api/v1/train-model")
async def train_model(command: TrainModelCommand):
    # Load dataset
    dataset = await dataset_storage.load(command.dataset_id)
    
    # Train model
    model = await trainer.train(
        dataset=dataset,
        algorithm=command.algorithm,
        hyperparameters=command.hyperparameters
    )
    
    # Save model
    model_id = await model_storage.save(model)
    
    # Publish event
    await event_publisher.publish_model_trained(
        command.id, model_id, command.correlation_id
    )
    
    return {"status": "completed", "model_id": model_id}
```

### ML Predictor (FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ML Predictor")

class PredictPropertiesCommand(BaseModel):
    id: str
    model_id: str
    dataset_id: str
    user_id: str
    correlation_id: str

@app.post("/api/v1/predict-properties")
async def predict_properties(command: PredictPropertiesCommand):
    # Load model
    model = await model_storage.load(command.model_id)
    
    # Load dataset
    dataset = await dataset_storage.load(command.dataset_id)
    
    # Predict
    predictions = await predictor.predict(model, dataset)
    
    # Publish event
    await event_publisher.publish_properties_predicted(
        command.id, predictions, command.correlation_id
    )
    
    return {"status": "completed", "predictions": predictions}
```

---

## Breaking Changes & Compatibility

### Python Version
- **Changed**: Legacy Python → Python 3.12+
- **Impact**: Update all dependencies

### ML Framework
- **Optional**: TensorFlow → PyTorch (can keep TF if needed)
- **Maintained**: scikit-learn algorithms

### Messaging
- **Changed**: RabbitMQ → Kafka
- **Changed**: Custom message format → Avro/JSON Schema

### API
- **New**: REST API endpoints (FastAPI)
- **Maintained**: Message-based processing (Kafka)

---

## Testing Requirements

### Unit Tests (>80% coverage)
- Feature calculation logic
- Model training logic
- Prediction logic
- Error handling

### Integration Tests
- Kafka message consumption
- End-to-end workflows
- Model training and prediction

### ML Tests
- Model accuracy validation
- Feature vector correctness
- Prediction accuracy

---

## Dependencies

### Needs From
- Agent 3: Blob Storage service
- Agent 8: Kafka infrastructure
- Agent 1: Chemical Parser (for parsed molecules)

### Provides To
- Core API: ML predictions
- Frontend: Model training UI, prediction results

---

## Success Criteria

- [ ] All services ported to FastAPI
- [ ] Python 3.12+ compatibility
- [ ] Dependencies updated
- [ ] Kafka integration working
- [ ] Unit test coverage >80%
- [ ] Integration tests passing
- [ ] ML functionality verified

---

## Timeline

- **Week 1**: Dependency updates, FastAPI setup
- **Week 2**: Service refactoring
- **Week 3**: Testing, deployment

**Total: 3 weeks**

