"""
Metrics Collector compatibility layer
"""
try:
    from metrics_collector import MetricsCollector
except ImportError:
    try:
        from metrics import MetricsCollector
    except ImportError:
        try:
            from core.metrics import MetricsCollector
        except ImportError:
            # Fallback: create a stub
            class MetricsCollector:
                """Stub MetricsCollector for compatibility"""
                def __init__(self, *args, **kwargs):
                    self._metrics = {}
                
                def record_metric(self, name: str, value: float, labels: dict = None):
                    """Stub record_metric method"""
                    self._metrics[name] = value
                
                def increment(self, name: str, labels: dict = None):
                    """Stub increment method"""
                    self._metrics[name] = self._metrics.get(name, 0) + 1
                
                def get_metrics(self):
                    """Stub get_metrics method"""
                    return self._metrics
                
                def __getattr__(self, name):
                    """Return a stub method for any other calls"""
                    def stub_method(*args, **kwargs):
                        raise NotImplementedError(f"MetricsCollector stub: '{name}' is not available. Install the full metrics package for complete functionality.")
                    return stub_method

__all__ = ['MetricsCollector']
