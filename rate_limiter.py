from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.types import ASGIApp
import redis.asyncio as redis
import time

from core.config import Settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, settings: Settings):
        super().__init__(app)
        self.settings = settings
        self.redis = redis.Redis.from_url(settings.redis_url)
    
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/auth") or request.url.path.startswith("/api/admin"):
            client_ip = request.client.host
            key = f"rate_limit:{client_ip}"
            
            current_time = time.time()
            window_start = current_time - self.settings.rate_limit_window
            
            # Remove expired requests efficiently using ZREMRANGEBYSCORE
            await self.redis.zremrangebyscore(key, '-inf', f'({window_start}')
            
            # Count requests in the current window
            req_count = await self.redis.zcount(key, window_start, current_time)
            
            if req_count >= self.settings.rate_limit_requests:
                return JSONResponse(
                    {"detail": "Rate limit exceeded"},
                    status_code=429
                )
            
            # Add current request timestamp to the sorted set
            await self.redis.zadd(key, {str(current_time): current_time})
            await self.redis.expire(key, self.settings.rate_limit_window)
        
        response = await call_next(request)
        return response

