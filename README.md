# Enhanced Platform Deployment

This directory contains the deployment configuration for the Enhanced Platform.

## Structure

```
enhanced_workspace/deployment/
├── docker-compose.yml      # Docker Compose configuration for production
├── .env.production        # Production environment variables
├── deploy.sh             # Main deployment script
├── validate_deployment.py # Pre-deployment validation
├── health_check.py       # Post-deployment health checks
├── init_database.py      # Database initialization
└── integration/          # API Gateway build context
    └── Dockerfile        # API Gateway Docker image
```

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11 or higher

### Deployment Steps

1. **Change to the deployment directory**:
   ```bash
   cd enhanced_workspace/deployment
   ```bash
   ./deploy.sh
   ```

### Manual Steps

You can also run each step individually:

```bash
# 1. Validate deployment readiness
python validate_deployment.py

# 2. Build and start services
docker-compose up -d --build

# 3. Check service health
python health_check.py

# 4. Initialize database
python init_database.py
```

## Services

The deployment includes the following services:

- **api-gateway**: Main API Gateway (port 8000)
- **redis**: Redis cache (port 6379)
- **postgres**: PostgreSQL database (port 5432)

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://admin:secure_password@postgres:5432/enhanced_platform` |
| `REDIS_URL` | Redis connection string | `redis://redis:6379/0` |
| `API_PORT` | API Gateway port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ENVIRONMENT` | Deployment environment | `production` |
| `ENABLE_ALL_AGENTS` | Enable all agents | `true` |
| `ENABLE_ALL_ENGINES` | Enable all engines | `true` |
| `ENABLE_MONITORING` | Enable monitoring | `true` |
| `ENABLE_LOGGING` | Enable logging | `true` |

### Docker Compose

The `docker-compose.yml` file defines:
- Service dependencies
- Port mappings
- Environment variables
- Volume mounts for data persistence

## Validation

The `validate_deployment.py` script checks:
- Required environment variables
- Docker installation and daemon status
- Docker Compose availability
- Required deployment files
- Integration directory structure

## Health Checks

The `health_check.py` script verifies:
- Redis connectivity and health
- PostgreSQL connectivity and health
- API Gateway availability

## Database Initialization

The `init_database.py` script:
- Waits for PostgreSQL to be ready
- Creates required database tables
- Seeds initial data

## Troubleshooting

### Services not starting

1. Check Docker daemon status:
   ```bash
   docker ps
   ```

2. View service logs:
   ```bash
   docker-compose logs -f
   ```

### Database connection issues

1. Verify PostgreSQL is running:
   ```bash
   docker-compose ps postgres
   ```

2. Check database logs:
   ```bash
   docker-compose logs postgres
   ```

### Port conflicts

If ports are already in use, modify the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change host port
```

## Maintenance

### Stop services
```bash
docker-compose down
```

### Remove volumes (data will be lost)
```bash
docker-compose down -v
```

### Update services
```bash
docker-compose pull
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f [service-name]
```

## Security Notes

⚠️ **Important**: The default credentials in `.env.production` are for development only. 
For production deployments:
- Change all passwords and secrets
- Use secure credential management (e.g., Docker secrets, environment variable injection)
- Enable SSL/TLS for database connections
- Configure firewall rules
- Enable authentication on Redis
