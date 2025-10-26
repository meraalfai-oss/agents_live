#!/bin/bash
# YMERA Platform Rollback Script
# Version: 2.0.0

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "============================================="
echo "YMERA Platform Rollback"
echo "============================================="
echo ""

# Check if backups exist
if [ ! -d "backups" ]; then
    echo -e "${RED}Error: No backups directory found${NC}"
    exit 1
fi

# List available backups
echo "Available backups:"
ls -1 backups/ | nl
echo ""

# Get latest backup
LATEST_BACKUP=$(ls -1t backups/ | head -1)
if [ -z "$LATEST_BACKUP" ]; then
    echo -e "${RED}Error: No backups found${NC}"
    exit 1
fi

echo "Latest backup: $LATEST_BACKUP"
read -p "Use this backup for rollback? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter backup directory name: " BACKUP_DIR
    LATEST_BACKUP=$BACKUP_DIR
fi

BACKUP_PATH="backups/$LATEST_BACKUP"

if [ ! -d "$BACKUP_PATH" ]; then
    echo -e "${RED}Error: Backup directory not found: $BACKUP_PATH${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Warning: This will stop the current deployment and restore from backup${NC}"
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Rollback cancelled"
    exit 0
fi

# Stop current services
echo ""
echo "Stopping current services..."
docker-compose down

# Restore database
if [ -f "$BACKUP_PATH/database.sql" ]; then
    echo ""
    echo "Restoring database..."
    docker-compose up -d db
    sleep 10
    docker-compose exec -T db psql -U ${DB_USER:-ymera} ${DB_NAME:-ymera} < "$BACKUP_PATH/database.sql"
    echo -e "${GREEN}✓${NC} Database restored"
else
    echo -e "${YELLOW}Warning: No database backup found in $BACKUP_PATH${NC}"
fi

# Restore data volumes
if [ -f "$BACKUP_PATH/data.tar.gz" ]; then
    echo ""
    echo "Restoring application data..."
    docker-compose up -d app
    sleep 5
    docker-compose exec -T app tar xzf - -C / < "$BACKUP_PATH/data.tar.gz"
    echo -e "${GREEN}✓${NC} Application data restored"
else
    echo -e "${YELLOW}Warning: No data backup found in $BACKUP_PATH${NC}"
fi

# Restart all services
echo ""
echo "Restarting services..."
docker-compose down
docker-compose up -d

# Wait and health check
echo ""
echo "Waiting for services..."
sleep 10

if curl -f -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Rollback successful"
    echo ""
    echo "Services restored from: $LATEST_BACKUP"
else
    echo -e "${RED}Error: Health check failed after rollback${NC}"
    echo "Check logs: docker-compose logs"
    exit 1
fi

echo ""
echo "============================================="
echo -e "${GREEN}Rollback Complete${NC}"
echo "============================================="
