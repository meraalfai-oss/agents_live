"""
Cache Manager compatibility layer
"""
try:
    from cache_manager import CacheManager
except ImportError:
    try:
        from core.cache import CacheManager
    except ImportError:
        # Fallback: create a stub
        class CacheManager:
            """Stub CacheManager for compatibility"""
            def __init__(self, *args, **kwargs):
                self._cache = {}
            
            async def get(self, key: str):
                """Stub get method"""
                return self._cache.get(key)
            
            async def set(self, key: str, value, ttl: int = None):
                """Stub set method"""
                self._cache[key] = value
            
            async def delete(self, key: str):
                """Stub delete method"""
                self._cache.pop(key, None)
            
            async def clear(self):
                """Stub clear method"""
                self._cache.clear()
            
            def __getattr__(self, name):
                """Return a stub method for any other calls"""
                def stub_method(*args, **kwargs):
                    raise NotImplementedError(f"CacheManager stub: '{name}' is not available. Install the full cache package for complete functionality.")
                return stub_method

__all__ = ['CacheManager']
