#!/bin/bash

echo "=== YMERA Platform API Testing ==="
echo ""

echo "1. Testing Health Endpoint..."
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo ""

echo "2. Testing OpenAPI Schema..."
curl -s http://localhost:8000/openapi.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'API Title: {data[\"info\"][\"title\"]}\nVersion: {data[\"info\"][\"version\"]}\nEndpoints: {len(data[\"paths\"])}')"
echo ""
echo ""

echo "3. Testing Metrics Endpoint..."
curl -s http://localhost:8000/metrics | head -20
echo ""

echo "=== All tests completed! ==="
