#!/usr/bin/env python3
"""
Health Check Script
Validates that all services are running and healthy after deployment
"""

import os
import sys
import time
import socket


def check_port(host: str, port: int, timeout: int = 5) -> bool:
    """Check if a port is open and accepting connections"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"   Error checking {host}:{port} - {e}")
        return False


def check_redis(host: str = 'localhost', port: int = 6379, max_retries: int = 30) -> bool:
    """Check if Redis is healthy"""
    print("🔴 Checking Redis...")
    
    for attempt in range(max_retries):
        if check_port(host, port):
            try:
                import redis
                client = redis.Redis(host=host, port=port, socket_connect_timeout=5)
                client.ping()
                print(f"✅ Redis is healthy at {host}:{port}")
                return True
            except ImportError:
                # If redis package not available, just check port
                print(f"✅ Redis port is open at {host}:{port}")
                return True
            except Exception as e:
                print(f"   Attempt {attempt + 1}/{max_retries}: Redis not ready - {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2)
    
    print(f"❌ Redis is not healthy at {host}:{port}")
    return False


def check_postgres(host: str = 'localhost', port: int = 5432, max_retries: int = 30) -> bool:
    """Check if PostgreSQL is healthy"""
    print("🐘 Checking PostgreSQL...")
    
    for attempt in range(max_retries):
        if check_port(host, port):
            try:
                import psycopg2
                db_url = os.getenv('DATABASE_URL', 
                                  f'postgresql://admin:secure_password@{host}:{port}/enhanced_platform')
                
                # Parse connection string
                conn = psycopg2.connect(db_url)
                cursor = conn.cursor()
                cursor.execute('SELECT 1')
                cursor.close()
                conn.close()
                
                print(f"✅ PostgreSQL is healthy at {host}:{port}")
                return True
            except ImportError:
                # If psycopg2 not available, just check port
                print(f"✅ PostgreSQL port is open at {host}:{port}")
                return True
            except Exception as e:
                print(f"   Attempt {attempt + 1}/{max_retries}: PostgreSQL not ready - {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2)
    
    print(f"❌ PostgreSQL is not healthy at {host}:{port}")
    return False


def check_api_gateway(host: str = 'localhost', port: int = 8000, max_retries: int = 30) -> bool:
    """Check if API Gateway is healthy"""
    print("🌐 Checking API Gateway...")
    
    for attempt in range(max_retries):
        if check_port(host, port):
            try:
                import requests
                response = requests.get(f'http://{host}:{port}/health', timeout=5)
                if response.status_code == 200:
                    print(f"✅ API Gateway is healthy at {host}:{port}")
                    return True
                else:
                    print(f"   Attempt {attempt + 1}/{max_retries}: API Gateway returned status {response.status_code}")
            except ImportError:
                # If requests not available, just check port
                print(f"✅ API Gateway port is open at {host}:{port}")
                return True
            except Exception as e:
                print(f"   Attempt {attempt + 1}/{max_retries}: API Gateway not ready - {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2)
    
    print(f"❌ API Gateway is not healthy at {host}:{port}")
    return False


def main():
    """Main health check function"""
    print("=" * 60)
    print("🏥 HEALTH CHECK")
    print("=" * 60)
    
    # Get host configuration
    host = os.getenv('DOCKER_HOST', 'localhost')
    
    checks = [
        ("Redis", lambda: check_redis(host, 6379)),
        ("PostgreSQL", lambda: check_postgres(host, 5432)),
        ("API Gateway", lambda: check_api_gateway(host, 8000)),
    ]
    
    all_healthy = True
    for name, check_func in checks:
        try:
            if not check_func():
                all_healthy = False
        except Exception as e:
            print(f"❌ {name} health check failed with error: {e}")
            all_healthy = False
        print()
    
    print("=" * 60)
    if all_healthy:
        print("✅ All services are healthy!")
        print("=" * 60)
        return 0
    else:
        print("❌ Some services are not healthy. Check logs above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
