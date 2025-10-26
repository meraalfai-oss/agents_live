"""
Message Broker compatibility layer
"""
try:
    from message_broker import MessageBroker
except ImportError:
    try:
        from core.messaging import MessageBroker
    except ImportError:
        # Fallback: create a stub
        class MessageBroker:
            """Stub MessageBroker for compatibility"""
            def __init__(self, *args, **kwargs):
                self._subscribers = {}
            
            async def publish(self, channel: str, message: dict):
                """Stub publish method"""
                pass
            
            async def subscribe(self, channel: str, callback):
                """Stub subscribe method"""
                if channel not in self._subscribers:
                    self._subscribers[channel] = []
                self._subscribers[channel].append(callback)
            
            async def unsubscribe(self, channel: str, callback):
                """Stub unsubscribe method"""
                if channel in self._subscribers:
                    self._subscribers[channel].remove(callback)
            
            def __getattr__(self, name):
                """Return a stub method for any other calls"""
                def stub_method(*args, **kwargs):
                    raise NotImplementedError(f"MessageBroker stub: '{name}' is not available. Install the full messaging package for complete functionality.")
                return stub_method

__all__ = ['MessageBroker']
