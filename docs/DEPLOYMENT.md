# Deployment Guide

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Local Development

### Prerequisites
- Python 3.10 or higher
- pip and virtualenv
- Google Cloud service account with Vertex AI access

### Setup Steps

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Add service account**:
- Place your `service-account.json` in the project root
- Ensure it has Vertex AI User permissions

5. **Run the application**:
```bash
python -m app.main
```

6. **Verify**:
- Web UI: http://localhost:8000
- Parlant Playground: http://localhost:8800
- API Docs: http://localhost:8000/docs

## Docker Deployment

### Quick Start

1. **Build and run with Docker Compose**:
```bash
docker-compose up -d
```

2. **View logs**:
```bash
docker-compose logs -f
```

3. **Stop services**:
```bash
docker-compose down
```

### Custom Docker Build

1. **Build image**:
```bash
docker build -t parlant-lifestyle-agent:latest .
```

2. **Run container**:
```bash
docker run -d \
  --name parlant-agent \
  -p 8000:8000 \
  -p 8800:8800 \
  -v $(pwd)/service-account.json:/app/service-account.json:ro \
  -e VERTEX_AI_PROJECT_ID=your-project-id \
  parlant-lifestyle-agent:latest
```

3. **Check status**:
```bash
docker ps
docker logs parlant-agent
```

### Docker Configuration

**Dockerfile highlights**:
- Based on Python 3.11 slim
- Installs all dependencies
- Exposes ports 8000 and 8800
- Non-root user for security

**docker-compose.yml features**:
- Auto-restart policy
- Volume mounting for service account
- Environment variable support
- Network configuration

## Production Deployment

### System Requirements

**Minimum**:
- 2 CPU cores
- 4 GB RAM
- 10 GB disk space

**Recommended**:
- 4 CPU cores
- 8 GB RAM
- 20 GB disk space
- SSD storage

### Security Considerations

1. **Service Account**:
```bash
# Use secret management
export GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account.json
```

2. **Environment Variables**:
```bash
# Use .env file with restricted permissions
chmod 600 .env
```

3. **API Security**:
- Implement API key authentication
- Add rate limiting
- Use HTTPS/TLS
- Enable CORS properly

4. **Firewall Rules**:
```bash
# Allow only necessary ports
ufw allow 8000/tcp
ufw allow 8800/tcp
ufw enable
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /parlant/ {
        proxy_pass http://localhost:8800/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Process Management with Systemd

Create `/etc/systemd/system/parlant-agent.service`:

```ini
[Unit]
Description=Parlant Lifestyle Agent
After=network.target

[Service]
Type=simple
User=parlant
WorkingDirectory=/opt/parlant-agent
Environment="PATH=/opt/parlant-agent/venv/bin"
ExecStart=/opt/parlant-agent/venv/bin/python -m app.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable parlant-agent
sudo systemctl start parlant-agent
sudo systemctl status parlant-agent
```

## Cloud Deployment

### Google Cloud Run

1. **Build and push image**:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/parlant-agent

# Or using Artifact Registry
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT_ID/REPO/parlant-agent
```

2. **Deploy to Cloud Run**:
```bash
gcloud run deploy parlant-agent \
  --image gcr.io/PROJECT_ID/parlant-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --set-env-vars VERTEX_AI_PROJECT_ID=PROJECT_ID
```

3. **Add service account**:
```bash
gcloud run services update parlant-agent \
  --service-account=your-service-account@PROJECT_ID.iam.gserviceaccount.com
```

### AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04, t3.medium or larger)

2. **Connect and setup**:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Clone repository
git clone https://github.com/yourusername/parlant-agent.git
cd parlant-agent
```

3. **Configure and run**:
```bash
# Add service account
vim service-account.json

# Configure environment
cp .env.example .env
vim .env

# Deploy
docker-compose up -d
```

### Azure Container Instances

```bash
# Create resource group
az group create --name parlant-rg --location eastus

# Create container
az container create \
  --resource-group parlant-rg \
  --name parlant-agent \
  --image yourdockerhub/parlant-agent:latest \
  --dns-name-label parlant-agent \
  --ports 8000 8800 \
  --environment-variables \
    VERTEX_AI_PROJECT_ID=your-project-id
```

### Kubernetes

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: parlant-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: parlant-agent
  template:
    metadata:
      labels:
        app: parlant-agent
    spec:
      containers:
      - name: parlant-agent
        image: yourdockerhub/parlant-agent:latest
        ports:
        - containerPort: 8000
        - containerPort: 8800
        env:
        - name: VERTEX_AI_PROJECT_ID
          valueFrom:
            secretKeyRef:
              name: parlant-secrets
              key: project-id
        volumeMounts:
        - name: service-account
          mountPath: /app/service-account.json
          subPath: service-account.json
      volumes:
      - name: service-account
        secret:
          secretName: gcp-service-account
---
apiVersion: v1
kind: Service
metadata:
  name: parlant-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
    name: api
  - port: 8800
    targetPort: 8800
    name: parlant
  selector:
    app: parlant-agent
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
```

## Monitoring

### Health Checks

```bash
# API health
curl http://localhost:8000/api/health

# Docker health
docker inspect --format='{{.State.Health.Status}}' parlant-agent
```

### Logging

**Docker logs**:
```bash
docker logs -f parlant-agent
docker logs --tail 100 parlant-agent
```

**Application logs**:
```python
# Add to app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Monitoring Tools

**Prometheus + Grafana**:
```bash
# Add to docker-compose.yml
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
```

## Troubleshooting

### Common Issues

1. **Service account not found**:
```bash
# Check file exists
ls -la service-account.json

# Verify JSON format
python -m json.tool service-account.json
```

2. **Port already in use**:
```bash
# Find process using port
lsof -i :8000
# or
netstat -tulpn | grep 8000

# Kill process
kill -9 <PID>
```

3. **Vertex AI authentication error**:
```bash
# Test authentication
gcloud auth application-default login
gcloud auth list

# Verify service account permissions
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:YOUR_SA_EMAIL"
```

4. **Container fails to start**:
```bash
# Check logs
docker-compose logs

# Inspect container
docker inspect parlant-agent

# Rebuild without cache
docker-compose build --no-cache
```

### Debug Mode

Enable debug logging:
```python
# In app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Tuning

1. **Increase workers**:
```python
# In app/main.py
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    workers=4  # Adjust based on CPU cores
)
```

2. **Connection pooling**:
```python
# Use connection pools for HTTP requests
aiohttp.ClientSession(
    connector=aiohttp.TCPConnector(limit=100)
)
```

3. **Caching**:
```python
# Add Redis for caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
```

## Backup and Recovery

### Backup Strategy

```bash
# Backup configuration
tar -czf backup-$(date +%Y%m%d).tar.gz \
  .env service-account.json docker-compose.yml

# Backup logs
docker logs parlant-agent > logs-$(date +%Y%m%d).log
```

### Disaster Recovery

1. Store backups in cloud storage (S3, GCS, Azure Blob)
2. Document recovery procedures
3. Test recovery process regularly
4. Keep multiple versions of service accounts

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  parlant-agent:
    deploy:
      replicas: 3
```

### Load Balancing

Use Nginx or HAProxy for load balancing multiple instances.

---

For additional help, consult:
- [Parlant Documentation](https://parlant.io/docs)
- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
