"""
Metrics Collection Module
Implements comprehensive metrics collection in Prometheus format
"""

from prometheus_client import (
    Counter, Histogram, Gauge, Info,
    CollectorRegistry, generate_latest,
    CONTENT_TYPE_LATEST
)
from fastapi import APIRouter, Response
from typing import Dict
import time
import psutil

from core.integration_config import integration_settings


# Create custom registry
metrics_registry = CollectorRegistry()

# ============================================================================
# REQUEST METRICS
# ============================================================================

# Request counter by endpoint and method
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code'],
    registry=metrics_registry
)

# Request duration histogram
request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0),
    registry=metrics_registry
)

# Error rate counter
error_count = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['method', 'endpoint', 'error_type'],
    registry=metrics_registry
)

# ============================================================================
# CONNECTION METRICS
# ============================================================================

# Active connections gauge
active_connections = Gauge(
    'http_active_connections',
    'Number of active HTTP connections',
    registry=metrics_registry
)

# Database connection pool metrics
db_connections_active = Gauge(
    'db_connections_active',
    'Number of active database connections',
    registry=metrics_registry
)

db_connections_idle = Gauge(
    'db_connections_idle',
    'Number of idle database connections',
    registry=metrics_registry
)

# ============================================================================
# DATABASE METRICS
# ============================================================================

# Database query counter
db_query_count = Counter(
    'db_queries_total',
    'Total database queries',
    ['operation', 'table'],
    registry=metrics_registry
)

# Database query duration
db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table'],
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0),
    registry=metrics_registry
)

# ============================================================================
# AGENT METRICS
# ============================================================================

# Agent processing counter
agent_processing_count = Counter(
    'agent_processing_total',
    'Total agent processing requests',
    ['agent_id', 'task_type'],
    registry=metrics_registry
)

# Agent processing duration
agent_processing_duration = Histogram(
    'agent_processing_duration_seconds',
    'Agent processing duration in seconds',
    ['agent_id', 'task_type'],
    buckets=(1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0),
    registry=metrics_registry
)

# Agent errors
agent_errors = Counter(
    'agent_errors_total',
    'Total agent errors',
    ['agent_id', 'error_type'],
    registry=metrics_registry
)

# Active agents gauge
active_agents = Gauge(
    'agents_active',
    'Number of active agents',
    registry=metrics_registry
)

# ============================================================================
# QUEUE METRICS
# ============================================================================

# Queue depth gauge
queue_depth = Gauge(
    'queue_depth',
    'Number of items in queue',
    ['queue_name'],
    registry=metrics_registry
)

# Queue processing time
queue_processing_time = Histogram(
    'queue_processing_duration_seconds',
    'Queue item processing duration',
    ['queue_name'],
    buckets=(0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0),
    registry=metrics_registry
)

# ============================================================================
# CACHE METRICS
# ============================================================================

# Cache hit counter
cache_hits = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_name'],
    registry=metrics_registry
)

# Cache miss counter
cache_misses = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_name'],
    registry=metrics_registry
)

# Cache operations
cache_operations = Counter(
    'cache_operations_total',
    'Total cache operations',
    ['cache_name', 'operation'],
    registry=metrics_registry
)

# ============================================================================
# SYSTEM METRICS
# ============================================================================

# System info
system_info = Info(
    'system',
    'System information',
    registry=metrics_registry
)

# CPU usage gauge
cpu_usage = Gauge(
    'system_cpu_usage_percent',
    'CPU usage percentage',
    registry=metrics_registry
)

# Memory usage gauge
memory_usage = Gauge(
    'system_memory_usage_bytes',
    'Memory usage in bytes',
    registry=metrics_registry
)

memory_usage_percent = Gauge(
    'system_memory_usage_percent',
    'Memory usage percentage',
    registry=metrics_registry
)

# Disk usage gauge
disk_usage = Gauge(
    'system_disk_usage_bytes',
    'Disk usage in bytes',
    registry=metrics_registry
)

disk_usage_percent = Gauge(
    'system_disk_usage_percent',
    'Disk usage percentage',
    registry=metrics_registry
)

# ============================================================================
# APPLICATION METRICS
# ============================================================================

# Application info
application_info = Info(
    'application',
    'Application information',
    registry=metrics_registry
)

# Uptime gauge
uptime_seconds = Gauge(
    'application_uptime_seconds',
    'Application uptime in seconds',
    registry=metrics_registry
)

# Start time
_start_time = time.time()


def update_system_metrics():
    """Update system resource metrics"""
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_usage.set(cpu_percent)
        
        # Memory
        memory = psutil.virtual_memory()
        memory_usage.set(memory.used)
        memory_usage_percent.set(memory.percent)
        
        # Disk
        disk = psutil.disk_usage('/')
        disk_usage.set(disk.used)
        disk_usage_percent.set(disk.percent)
        
        # Uptime
        uptime = time.time() - _start_time
        uptime_seconds.set(uptime)
        
    except Exception as e:
        # Log but don't fail
        import logging
        logging.error(f"Failed to update system metrics: {e}")


def initialize_metrics():
    """Initialize metrics with application info"""
    application_info.info({
        'service_name': integration_settings.service_name,
        'version': integration_settings.service_version,
        'service_id': integration_settings.service_id,
    })
    
    system_info.info({
        'python_version': '3.11',
        'platform': 'linux',
    })


# Create metrics router
metrics_router = APIRouter()


@metrics_router.get(
    integration_settings.metrics_endpoint,
    tags=["Monitoring"]
)
async def metrics_endpoint():
    """
    Prometheus metrics endpoint
    Exposes all collected metrics in Prometheus format
    """
    # Update system metrics before returning
    update_system_metrics()
    
    # Generate metrics in Prometheus format
    metrics_output = generate_latest(metrics_registry)
    
    return Response(
        content=metrics_output,
        media_type=CONTENT_TYPE_LATEST
    )


class MetricsCollector:
    """
    Metrics collector helper class
    Provides convenient methods for collecting metrics
    """
    
    @staticmethod
    def record_request(method: str, endpoint: str, status_code: int, duration: float):
        """Record HTTP request metrics"""
        request_count.labels(
            method=method,
            endpoint=endpoint,
            status_code=status_code
        ).inc()
        
        request_duration.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
    
    @staticmethod
    def record_error(method: str, endpoint: str, error_type: str):
        """Record HTTP error"""
        error_count.labels(
            method=method,
            endpoint=endpoint,
            error_type=error_type
        ).inc()
    
    @staticmethod
    def record_db_query(operation: str, table: str, duration: float):
        """Record database query metrics"""
        db_query_count.labels(
            operation=operation,
            table=table
        ).inc()
        
        db_query_duration.labels(
            operation=operation,
            table=table
        ).observe(duration)
    
    @staticmethod
    def record_agent_processing(agent_id: str, task_type: str, duration: float):
        """Record agent processing metrics"""
        agent_processing_count.labels(
            agent_id=agent_id,
            task_type=task_type
        ).inc()
        
        agent_processing_duration.labels(
            agent_id=agent_id,
            task_type=task_type
        ).observe(duration)
    
    @staticmethod
    def record_agent_error(agent_id: str, error_type: str):
        """Record agent error"""
        agent_errors.labels(
            agent_id=agent_id,
            error_type=error_type
        ).inc()
    
    @staticmethod
    def record_cache_hit(cache_name: str):
        """Record cache hit"""
        cache_hits.labels(cache_name=cache_name).inc()
    
    @staticmethod
    def record_cache_miss(cache_name: str):
        """Record cache miss"""
        cache_misses.labels(cache_name=cache_name).inc()
    
    @staticmethod
    def set_queue_depth(queue_name: str, depth: int):
        """Set queue depth"""
        queue_depth.labels(queue_name=queue_name).set(depth)
    
    @staticmethod
    def set_active_agents(count: int):
        """Set number of active agents"""
        active_agents.set(count)
    
    @staticmethod
    def set_active_connections(count: int):
        """Set number of active connections"""
        active_connections.set(count)
