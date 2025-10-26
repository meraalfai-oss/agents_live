#!/bin/bash
# YMERA Platform Health Check Script
# Version: 2.0.0

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "============================================="
echo "YMERA Platform Health Check"
echo "============================================="
echo ""
echo "Checking: $BASE_URL"
echo ""

# Function to check endpoint
check_endpoint() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}
    
    printf "%-25s" "$name:"
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$response" -eq "$expected_code" ]; then
        echo -e "${GREEN}✓ OK${NC} (HTTP $response)"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $response)"
        return 1
    fi
}

# Check main endpoints
PASSED=0
FAILED=0

# Application health
if check_endpoint "Application Health" "$BASE_URL/health"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

# Database health
if check_endpoint "Database Health" "$BASE_URL/health/db"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

# Redis health
if check_endpoint "Cache Health" "$BASE_URL/health/redis"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

# Metrics endpoint
if check_endpoint "Metrics Endpoint" "$BASE_URL/metrics"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

# API Documentation
if check_endpoint "API Documentation" "$BASE_URL/docs"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

# Check Docker containers if docker-compose is available
echo ""
echo "Docker Container Status:"
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1; then
    docker-compose ps 2>/dev/null || docker compose ps 2>/dev/null || echo "No containers running"
else
    echo "Docker Compose not available"
fi

# Summary
echo ""
echo "============================================="
echo "Health Check Summary"
echo "============================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed${NC}"
    exit 0
else
    echo -e "${RED}✗ Some checks failed${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check if services are running: docker-compose ps"
    echo "  2. View logs: docker-compose logs -f"
    echo "  3. Restart services: docker-compose restart"
    exit 1
fi
