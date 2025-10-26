#!/bin/bash
set -euo pipefail

# Ensure we are in the script's directory
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$script_dir"

echo "🚀 Deploying Enhanced Platform..."

# 1. Validate deployment readiness
python3 ./validate_deployment.py

# 2. Build and start services
docker compose up -d --build

# 3. Run health checks
python3 ./health_check.py

# 4. Initialize database
python3 ./init_database.py

echo "✅ Deployment completed successfully!"
