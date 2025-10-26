"""
Request Tracking Middleware
Generates request IDs and implements distributed tracing headers
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Callable
import uuid
import time
import logging

logger = logging.getLogger(__name__)


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to track requests with unique IDs
    Supports distributed tracing headers
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and add tracking information"""
        
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Extract distributed tracing headers
        trace_id = request.headers.get("X-Trace-ID") or request_id
        span_id = request.headers.get("X-Span-ID") or str(uuid.uuid4())
        parent_span_id = request.headers.get("X-Parent-Span-ID")
        
        # Store in request state
        request.state.request_id = request_id
        request.state.trace_id = trace_id
        request.state.span_id = span_id
        request.state.parent_span_id = parent_span_id
        
        # Start timer
        start_time = time.time()
        
        # Log request
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": span_id,
                "method": request.method,
                "path": request.url.path,
                "client_host": request.client.host if request.client else None,
            }
        )
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log error
            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "trace_id": trace_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                exc_info=True
            )
            raise
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Add tracking headers to response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Trace-ID"] = trace_id
        response.headers["X-Span-ID"] = span_id
        if parent_span_id:
            response.headers["X-Parent-Span-ID"] = parent_span_id
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        
        # Log response
        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": span_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration": duration,
            }
        )
        
        return response


def get_request_id(request: Request) -> str:
    """Get request ID from request state"""
    return getattr(request.state, "request_id", "unknown")


def get_trace_id(request: Request) -> str:
    """Get trace ID from request state"""
    return getattr(request.state, "trace_id", "unknown")


def get_span_id(request: Request) -> str:
    """Get span ID from request state"""
    return getattr(request.state, "span_id", "unknown")
