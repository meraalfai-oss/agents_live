# PLUGIN ARCHITECTURE FOR EXPANSION

from collections import defaultdict


class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.hooks = defaultdict(list)
    
    def register_plugin(self, plugin_name, plugin_class):
        self.plugins[plugin_name] = plugin_class
        print(f"✅ Plugin registered: {plugin_name}")
    
    def add_hook(self, hook_name, callback):
        self.hooks[hook_name].append(callback)
    
    def execute_hook(self, hook_name, *args, **kwargs):
        for callback in self.hooks.get(hook_name, []):
            callback(*args, **kwargs)


# Base plugin class
class BasePlugin:
    def __init__(self, name, version):
        self.name = name
        self.version = version
    
    async def initialize(self):
        pass
    
    async def execute(self, context):
        pass
