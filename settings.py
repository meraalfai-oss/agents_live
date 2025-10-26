"""
Settings compatibility layer - redirects to core.config
"""
try:
    from core.config import Settings
except ImportError:
    from config import Settings

__all__ = ['Settings']
