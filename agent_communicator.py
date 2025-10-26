"""
Agent Communicator compatibility layer
"""

class AgentCommunicator:
    """Stub AgentCommunicator for compatibility"""
    
    def __init__(self, *args, **kwargs):
        self.agents = {}
    
    async def send_message(self, agent_id: str, message: dict):
        """Stub send message method"""
        pass
    
    async def broadcast(self, message: dict):
        """Stub broadcast method"""
        pass
    
    async def register_agent(self, agent_id: str, agent):
        """Stub register agent method"""
        self.agents[agent_id] = agent
    
    async def unregister_agent(self, agent_id: str):
        """Stub unregister agent method"""
        self.agents.pop(agent_id, None)

__all__ = ['AgentCommunicator']
