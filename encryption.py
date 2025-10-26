"""
Encryption Manager compatibility layer
"""
try:
    from encryption import EncryptionManager
except ImportError:
    try:
        from core.security import EncryptionManager
    except ImportError:
        # Fallback: create a stub
        class EncryptionManager:
            """Stub EncryptionManager for compatibility"""
            def __init__(self, *args, **kwargs):
                if 'key' not in kwargs:
                    raise ValueError('Encryption key required - this is a stub for testing')
                self.key = kwargs['key']
            
            def encrypt(self, data: str) -> str:
                """Stub encrypt method"""
                return f"encrypted:{data}"
            
            def decrypt(self, data: str) -> str:
                """Stub decrypt method"""
                if data.startswith("encrypted:"):
                    return data[10:]
                return data
            
            def __getattr__(self, name):
                """Return a stub method for any other calls"""
                def stub_method(*args, **kwargs):
                    raise NotImplementedError(f"EncryptionManager stub: '{name}' is not available. Install the full security package for complete functionality.")
                return stub_method

__all__ = ['EncryptionManager']
