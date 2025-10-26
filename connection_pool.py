"""
Database connection pool compatibility layer
"""
try:
    from core.database import DatabaseManager
except ImportError:
    try:
        from database import DatabaseManager
    except ImportError:
        # Fallback: create a stub
        class DatabaseManager:
            """Stub DatabaseManager for compatibility"""
            def __init__(self, *args, **kwargs):
                raise NotImplementedError("Stub DatabaseManager cannot be instantiated. The real DatabaseManager is not available.")

            def __getattr__(self, name):
                raise NotImplementedError(f"Stub DatabaseManager: method '{name}' is not implemented. The real DatabaseManager is not available.")
__all__ = ['DatabaseManager']
