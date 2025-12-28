"""
Phase-5 Orchestrator
Smart routing to domain expert agents

@author: Phase-5 Multi-Agent System
"""

from typing import Dict, List, Any, Optional

# Use relative imports when imported as package, else absolute
try:
    from .base_agent import BaseAgent, AgentResult
except ImportError:
    from base_agent import BaseAgent, AgentResult


# Domain keywords for smart routing
DOMAIN_KEYWORDS = {
    # Kafka/Event Streaming
    'kafka': 'kafka',
    'redpanda': 'kafka',
    'topic': 'kafka',
    'publish': 'kafka',
    'subscribe': 'kafka',
    'event': 'kafka',
    'producer': 'kafka',
    'consumer': 'kafka',
    'broker': 'kafka',
    'message queue': 'kafka',
    'streaming': 'kafka',

    # Dapr
    'dapr': 'dapr',
    'sidecar': 'dapr',
    'pubsub': 'dapr',
    'state store': 'dapr',
    'statestore': 'dapr',
    'binding': 'dapr',
    'secretstore': 'dapr',
    'service invocation': 'dapr',
    'distributed': 'dapr',

    # Features
    'priority': 'feature',
    'tag': 'feature',
    'label': 'feature',
    'category': 'feature',
    'search': 'feature',
    'filter': 'feature',
    'sort': 'feature',
    'high priority': 'feature',
    'low priority': 'feature',
    'medium priority': 'feature',

    # Recurring
    'recurring': 'recurring',
    'repeat': 'recurring',
    'daily': 'recurring',
    'weekly': 'recurring',
    'monthly': 'recurring',
    'schedule': 'recurring',
    'cron': 'recurring',
    'recurrence': 'recurring',

    # Reminder
    'reminder': 'reminder',
    'remind': 'reminder',
    'notification': 'reminder',
    'notify': 'reminder',
    'due date': 'reminder',
    'deadline': 'reminder',
    'alert': 'reminder',
    'overdue': 'reminder',

    # Kubernetes Deployment
    'deploy': 'k8s',
    'deployment': 'k8s',
    'kubernetes': 'k8s',
    'k8s': 'k8s',
    'kubectl': 'k8s',
    'pod': 'k8s',
    'namespace': 'k8s',
    'configmap': 'k8s',
    'secret': 'k8s',
    'rollout': 'k8s',

    # Minikube
    'minikube': 'minikube',
    'local cluster': 'minikube',
    'tunnel': 'minikube',
    'addon': 'minikube',
    'dashboard': 'minikube',

    # Helm
    'helm': 'helm',
    'chart': 'helm',
    'release': 'helm',
    'values': 'helm',
    'upgrade release': 'helm',
    'rollback release': 'helm',
}


class AgentOrchestrator:
    """
    Smart Orchestrator for Phase-5

    Features:
    - Domain-based routing
    - Keyword matching
    - Multi-agent delegation
    - Result aggregation
    - Auto-registration of all agents
    """

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.default_agent: str = None
        self._auto_register_agents()

    def _auto_register_agents(self):
        """Auto-register all available agents"""
        try:
            # Import all agents
            from infrastructure.kafka_agent import KafkaAgent
            from infrastructure.dapr_agent import DaprAgent
            from application.feature_agent import FeatureAgent
            from application.recurring_agent import RecurringAgent
            from application.reminder_agent import ReminderAgent
            from devops.k8s_deploy_agent import K8sDeployAgent
            from devops.helm_agent import HelmAgent
            from devops.minikube_agent import MinikubeAgent

            # Register all agents
            self.register_agent(KafkaAgent())
            self.register_agent(DaprAgent())
            self.register_agent(FeatureAgent())
            self.register_agent(RecurringAgent())
            self.register_agent(ReminderAgent())
            self.register_agent(K8sDeployAgent())
            self.register_agent(HelmAgent())
            self.register_agent(MinikubeAgent())

            # Set default
            self.set_default_agent('feature')

        except ImportError as e:
            print(f"⚠️ Warning: Could not auto-register agents: {e}")
            print("   Agents can be registered manually using register_agent()")

    def register_agent(self, agent: BaseAgent):
        """Register an agent"""
        self.agents[agent.domain] = agent
        print(f"  {agent.emoji} Registered: {agent.name} ({agent.domain})")

    def set_default_agent(self, domain: str):
        """Set default agent for unmatched queries"""
        self.default_agent = domain

    def _detect_domain(self, query: str) -> str:
        """Detect domain from query using keywords"""
        query_lower = query.lower()

        # Check each keyword
        for keyword, domain in DOMAIN_KEYWORDS.items():
            if keyword in query_lower:
                return domain

        # Return default if set
        if self.default_agent:
            return self.default_agent

        # Return first available agent
        if self.agents:
            return list(self.agents.keys())[0]

        return None

    def get_agent(self, domain: str) -> Optional[BaseAgent]:
        """Get agent by domain"""
        return self.agents.get(domain)

    async def delegate(self, query: str) -> AgentResult:
        """
        Delegate query to appropriate agent

        1. Detect domain
        2. Get agent
        3. Process query
        4. Return result
        """
        # Step 1: Detect domain
        domain = self._detect_domain(query)

        if not domain:
            return AgentResult(
                success=False,
                error="No agent available for this query",
                agent="Orchestrator"
            )

        # Step 2: Get agent
        agent = self.get_agent(domain)

        if not agent:
            return AgentResult(
                success=False,
                error=f"Agent for domain '{domain}' not found",
                agent="Orchestrator"
            )

        print(f"\n🎯 Routing to: {agent.emoji} {agent.name}")

        # Step 3: Process
        result = await agent.process(query)

        return result

    async def delegate_to(self, domain: str, query: str) -> AgentResult:
        """Delegate to specific agent"""
        agent = self.get_agent(domain)

        if not agent:
            return AgentResult(
                success=False,
                error=f"Agent '{domain}' not found",
                agent="Orchestrator"
            )

        return await agent.process(query)

    async def broadcast(self, query: str) -> Dict[str, AgentResult]:
        """Broadcast query to all agents"""
        results = {}

        for domain, agent in self.agents.items():
            results[domain] = await agent.process(query)

        return results

    def list_agents(self) -> List[Dict]:
        """List all registered agents"""
        return [agent.get_status() for agent in self.agents.values()]

    def get_status(self) -> Dict:
        """Get orchestrator status"""
        return {
            "total_agents": len(self.agents),
            "agents": self.list_agents(),
            "domains": list(self.agents.keys()),
            "default_agent": self.default_agent
        }

    def __repr__(self):
        return f"🎯 Orchestrator ({len(self.agents)} agents)"
