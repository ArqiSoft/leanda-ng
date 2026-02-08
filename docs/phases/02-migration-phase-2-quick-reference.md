# Phase 2: Quick Reference Guide

## Overview

Quick reference for commands, troubleshooting, and common tasks during Phase 2 migration.

## Common Commands

### Docker Operations

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f <service-name>

# Restart a service
docker-compose restart <service-name>

# Stop all services
docker-compose down

# Rebuild a service
docker-compose build <service-name>
```

### Quarkus Development

```bash
# Create new Quarkus project
mvn io.quarkus.platform:quarkus-maven-plugin:3.17.0:create \
  -DprojectGroupId=io.leanda.ng \
  -DprojectArtifactId=<service-name> \
  -Dextensions="kafka,reactive-messaging,mongodb-client"

# Run in dev mode
./mvnw quarkus:dev

# Run tests
./mvnw test

# Build native image
./mvnw package -Pnative
```

### FastAPI Development

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run in dev mode
uvicorn app.main:app --reload --port 8000

# Run tests
pytest

# Format code
black .
isort .
```

### Angular Development

```bash
# Create new Angular project
ng new <project-name> --routing --style=scss

# Run in dev mode
ng serve

# Run tests
ng test

# Build for production
ng build --configuration production

# Run E2E tests
npx playwright test
```

## Service-Specific Commands

### Blob Storage

```bash
# Test blob upload
curl -X POST http://localhost:8080/api/blobs/test-bucket \
  -F "file=@test.txt" \
  -H "Authorization: Bearer <token>"

# Test blob download
curl http://localhost:8080/api/blobs/test-bucket/<blob-id> \
  -H "Authorization: Bearer <token>"
```

### Chemical Parser

```bash
# Send parse command via Kafka
kafka-console-producer --topic chemical-parse-commands \
  --bootstrap-server localhost:9092 \
  --property parse.key=true \
  --property key.separator=: \
  < parse-command.json
```

### Indexing Service

```bash
# Check OpenSearch index
curl -X GET "http://localhost:9200/files/_search?q=*" \
  -H "Authorization: Bearer <token>"

# Reindex all files
curl -X POST "http://localhost:8080/api/v1/indexing/reindex" \
  -H "Authorization: Bearer <token>"
```

## Troubleshooting

### Service Won't Start

1. **Check logs**: `docker-compose logs <service-name>`
2. **Check dependencies**: Verify all required services are running
3. **Check ports**: Ensure ports aren't already in use
4. **Check environment variables**: Verify `.env` file is correct

### Kafka Connection Issues

1. **Check Kafka is running**: `docker-compose ps kafka`
2. **Check topic exists**: `kafka-topics --list --bootstrap-server localhost:9092`
3. **Check consumer groups**: `kafka-consumer-groups --bootstrap-server localhost:9092 --list`

### MongoDB Connection Issues

1. **Check MongoDB is running**: `docker-compose ps mongo`
2. **Test connection**: `mongosh mongodb://localhost:27017`
3. **Check credentials**: Verify MongoDB username/password

### OpenSearch Issues

1. **Check OpenSearch is running**: `docker-compose ps opensearch`
2. **Test connection**: `curl http://localhost:9200`
3. **Check indices**: `curl http://localhost:9200/_cat/indices`

### Test Failures

1. **Run tests individually**: `./mvnw test -Dtest=SpecificTest`
2. **Check testcontainers**: Ensure Docker is running
3. **Check test data**: Verify test fixtures are correct
4. **Check dependencies**: Ensure all test dependencies are installed

## File Locations

### Service Code
- **Java Services**: `services/<service-name>/`
- **Python Services**: `ml-services/<service-name>/`
- **Frontend**: `frontend/`

### Configuration
- **Docker Compose**: `docker-compose.yml`
- **Environment Variables**: `.env`
- **Service Configs**: `services/<service-name>/src/main/resources/application.properties`

### Documentation
- **Migration Specs**: `docs/phases/02-migration-phase-2-*.md`
- **Coordination**: `leanda-ng-phase2/COORDINATION.md`
- **Agent Prompts**: `leanda-ng-phase2/AGENT_PROMPTS.md`

### Shared Artifacts
- **API Contracts**: `leanda-ng-phase2/shared/contracts/`
- **Domain Models**: `leanda-ng-phase2/shared/models/`

## Testing

### Run All Tests
```bash
# Java services
./mvnw test

# Python services
pytest

# Frontend
ng test
npx playwright test
```

### Run Integration Tests
```bash
# Start test infrastructure
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
./mvnw verify -Pintegration-tests
```

### Check Test Coverage
```bash
# Java
./mvnw test jacoco:report
open target/site/jacoco/index.html

# Python
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## Git Workflow

### Before Starting Work
```bash
# Pull latest changes
git pull origin main

# Check current branch
git branch --show-current

# Create feature branch
git checkout -b agent-X/<service-name>
```

### During Work
```bash
# Stage changes
git add <files>

# Commit with clear message
git commit -m "feat(service-name): implement feature X"

# Push to remote
git push origin agent-X/<service-name>
```

### Updating COORDINATION.md
```bash
# Always pull latest before updating
git pull origin main

# Update COORDINATION.md
# ... make changes ...

# Commit coordination update
git add leanda-ng-phase2/COORDINATION.md
git commit -m "docs: update coordination status for Agent X"
git push origin agent-X/<service-name>
```

## Useful Scripts

### Check Service Status
```bash
# Check if service is running
./scripts/check-status.sh <service-name>

# Check all services
./scripts/check-status.sh
```

### Check Dependencies
```bash
# Check if dependencies are met
./scripts/check-dependencies.sh <service-name>
```

### Validate Contracts
```bash
# Validate OpenAPI/AsyncAPI contracts
./scripts/validate-contracts.sh
```

## Common Issues & Solutions

### Issue: Port Already in Use
**Solution**: 
```bash
# Find process using port
lsof -i :8080

# Kill process
kill -9 <PID>
```

### Issue: Docker Container Won't Start
**Solution**:
```bash
# Remove container
docker-compose rm -f <service-name>

# Rebuild and start
docker-compose up -d --build <service-name>
```

### Issue: Kafka Consumer Lag
**Solution**:
```bash
# Check consumer lag
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group <consumer-group>

# Reset consumer group (if needed)
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --reset-offsets --to-earliest --group <consumer-group> \
  --topic <topic> --execute
```

### Issue: MongoDB Connection Refused
**Solution**:
```bash
# Check MongoDB logs
docker-compose logs mongo

# Restart MongoDB
docker-compose restart mongo

# Verify connection
mongosh mongodb://localhost:27017/leanda_dev
```

## Performance Tips

### Java Services
- Use Quarkus dev mode for hot reload
- Enable native compilation for production
- Use GraalVM for smaller images

### Python Services
- Use async/await for I/O operations
- Use connection pooling for databases
- Enable gunicorn workers for production

### Frontend
- Use lazy loading for routes
- Enable production build optimizations
- Use CDN for static assets

## Next Steps

1. **Read your agent's work package**: `docs/phases/02-migration-phase-2-agent-work-packages.md`
2. **Check COORDINATION.md**: `leanda-ng-phase2/COORDINATION.md`
3. **Start implementation**: Follow your service's migration spec
4. **Update status daily**: Keep COORDINATION.md updated

