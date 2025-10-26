"""
Database models compatibility layer
"""
try:
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
except ImportError:
    try:
        from sqlalchemy.orm import declarative_base
        Base = declarative_base()
    except ImportError:
        # Fallback: create a stub
        class Base:
            """Stub Base for compatibility"""
            def __init__(self, *args, **kwargs):
                pass

try:
    # Import models if available
    from models import User, Product, Agent, Task
except ImportError:
    pass

try:
    # Import from sqlalchemy_models if available
    from sqlalchemy_models import User, Product
except ImportError:
    pass

__all__ = ['Base']
