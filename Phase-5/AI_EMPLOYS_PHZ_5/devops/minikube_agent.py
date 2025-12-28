"""
Minikube Agent - Local Kubernetes Expert
Handles Minikube operations for Phase-5 local development

@author: Phase-5 AI Employs System
"""

import asyncio
import subprocess
from typing import Dict, List, Any, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class MinikubeAgent(BaseAgent):
    """
    Minikube Local Kubernetes Expert Agent

    Capabilities:
    - Start/stop Minikube cluster
    - Enable addons
    - Tunnel for LoadBalancer
    - Docker environment
    - Dashboard access

    MCP Tools: 12
    """

    def __init__(self):
        super().__init__()
        self.name = "MinikubeAgent"
        self.domain = "minikube"
        self.description = "Minikube local Kubernetes expert"
        self.emoji = "🏠"

    def _setup_tools(self):
        """Setup Minikube MCP tools"""

        # Tool 1: Start Cluster
        self.register_tool(MCPTool(
            name="minikube_start",
            description="Start Minikube cluster",
            parameters={
                "driver": "string (docker/hyperv/virtualbox)",
                "cpus": "int (default: 4)",
                "memory": "string (default: 8g)"
            },
            handler=self._minikube_start
        ))

        # Tool 2: Stop Cluster
        self.register_tool(MCPTool(
            name="minikube_stop",
            description="Stop Minikube cluster",
            parameters={},
            handler=self._minikube_stop
        ))

        # Tool 3: Delete Cluster
        self.register_tool(MCPTool(
            name="minikube_delete",
            description="Delete Minikube cluster",
            parameters={},
            handler=self._minikube_delete
        ))

        # Tool 4: Get Status
        self.register_tool(MCPTool(
            name="minikube_status",
            description="Get Minikube cluster status",
            parameters={},
            handler=self._minikube_status
        ))

        # Tool 5: Enable Addon
        self.register_tool(MCPTool(
            name="enable_addon",
            description="Enable a Minikube addon",
            parameters={"addon": "string (required)"},
            handler=self._enable_addon
        ))

        # Tool 6: List Addons
        self.register_tool(MCPTool(
            name="list_addons",
            description="List available Minikube addons",
            parameters={},
            handler=self._list_addons
        ))

        # Tool 7: Start Tunnel
        self.register_tool(MCPTool(
            name="minikube_tunnel",
            description="Start Minikube tunnel for LoadBalancer services",
            parameters={},
            handler=self._minikube_tunnel
        ))

        # Tool 8: Docker Env
        self.register_tool(MCPTool(
            name="docker_env",
            description="Get Docker environment for Minikube",
            parameters={},
            handler=self._docker_env
        ))

        # Tool 9: Get IP
        self.register_tool(MCPTool(
            name="minikube_ip",
            description="Get Minikube IP address",
            parameters={},
            handler=self._minikube_ip
        ))

        # Tool 10: Dashboard
        self.register_tool(MCPTool(
            name="minikube_dashboard",
            description="Open Kubernetes dashboard",
            parameters={},
            handler=self._minikube_dashboard
        ))

        # Tool 11: Service URL
        self.register_tool(MCPTool(
            name="minikube_service",
            description="Get URL for a service",
            parameters={
                "service_name": "string (required)",
                "namespace": "string (optional)"
            },
            handler=self._minikube_service
        ))

        # Tool 12: SSH
        self.register_tool(MCPTool(
            name="minikube_ssh",
            description="SSH into Minikube node",
            parameters={"command": "string (optional)"},
            handler=self._minikube_ssh
        ))

    def _match_tool(self, query: str) -> Optional[str]:
        """Match query to best Minikube tool"""
        query = query.lower()

        if any(w in query for w in ['start minikube', 'minikube start', 'start cluster']):
            return 'minikube_start'
        elif any(w in query for w in ['stop minikube', 'minikube stop', 'stop cluster']):
            return 'minikube_stop'
        elif any(w in query for w in ['delete minikube', 'minikube delete']):
            return 'minikube_delete'
        elif any(w in query for w in ['status', 'minikube status']):
            return 'minikube_status'
        elif any(w in query for w in ['enable addon', 'addon enable']):
            return 'enable_addon'
        elif any(w in query for w in ['list addon', 'addons']):
            return 'list_addons'
        elif any(w in query for w in ['tunnel']):
            return 'minikube_tunnel'
        elif any(w in query for w in ['docker env', 'docker-env']):
            return 'docker_env'
        elif any(w in query for w in ['ip', 'minikube ip']):
            return 'minikube_ip'
        elif any(w in query for w in ['dashboard']):
            return 'minikube_dashboard'
        elif any(w in query for w in ['service url', 'service']):
            return 'minikube_service'
        elif any(w in query for w in ['ssh']):
            return 'minikube_ssh'

        return 'minikube_status'

    async def execute_direct(self, step: Dict) -> Any:
        """Smart direct execution"""
        query = step.get("query", "").lower()
        tool_name = step.get("tool") or self._match_tool(query)

        if tool_name == 'minikube_start':
            return await self._minikube_start()

        elif tool_name == 'minikube_stop':
            return await self._minikube_stop()

        elif tool_name == 'minikube_status':
            return await self._minikube_status()

        elif tool_name == 'enable_addon':
            addon = self._extract_addon(query)
            return await self._enable_addon(addon=addon)

        elif tool_name == 'list_addons':
            return await self._list_addons()

        else:
            return await self._minikube_status()

    def _extract_addon(self, query: str) -> str:
        """Extract addon name from query"""
        addons = ['ingress', 'dashboard', 'metrics-server', 'registry']
        for addon in addons:
            if addon in query:
                return addon
        return 'ingress'

    def _run_minikube(self, args: List[str], timeout: int = 120) -> Dict:
        """Run minikube command"""
        try:
            result = subprocess.run(
                ['minikube'] + args,
                capture_output=True, text=True, timeout=timeout
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "minikube not found",
                "command": f"minikube {' '.join(args)}",
                "install_guide": "https://minikube.sigs.k8s.io/docs/start/"
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ==================== Tool Handlers ====================

    async def _minikube_start(self, driver: str = "docker",
                             cpus: int = 4, memory: str = "8g") -> Dict:
        """Start Minikube cluster"""
        args = ['start', '--driver', driver, '--cpus', str(cpus),
                '--memory', memory]

        result = self._run_minikube(args, timeout=300)
        return {
            "status": "started" if result.get("success") else "info",
            "driver": driver,
            "cpus": cpus,
            "memory": memory,
            "output": result.get("output"),
            "command": f"minikube start --driver={driver} --cpus={cpus} --memory={memory}",
            "next_steps": [
                "minikube status",
                "kubectl get nodes",
                "Enable addons: minikube addons enable ingress"
            ]
        }

    async def _minikube_stop(self) -> Dict:
        """Stop Minikube cluster"""
        result = self._run_minikube(['stop'])
        return {
            "status": "stopped" if result.get("success") else "info",
            "output": result.get("output"),
            "command": "minikube stop"
        }

    async def _minikube_delete(self) -> Dict:
        """Delete Minikube cluster"""
        result = self._run_minikube(['delete'])
        return {
            "status": "deleted" if result.get("success") else "info",
            "output": result.get("output"),
            "command": "minikube delete",
            "warning": "All cluster data will be lost"
        }

    async def _minikube_status(self) -> Dict:
        """Get cluster status"""
        result = self._run_minikube(['status'])
        return {
            "status": "success" if result.get("success") else "info",
            "output": result.get("output"),
            "command": "minikube status"
        }

    async def _enable_addon(self, addon: str) -> Dict:
        """Enable addon"""
        result = self._run_minikube(['addons', 'enable', addon])
        return {
            "status": "enabled" if result.get("success") else "info",
            "addon": addon,
            "output": result.get("output"),
            "command": f"minikube addons enable {addon}",
            "recommended_addons": [
                "ingress - NGINX Ingress Controller",
                "dashboard - Kubernetes Dashboard",
                "metrics-server - Resource metrics",
                "registry - Local Docker registry"
            ]
        }

    async def _list_addons(self) -> Dict:
        """List addons"""
        result = self._run_minikube(['addons', 'list'])
        return {
            "status": "success" if result.get("success") else "info",
            "output": result.get("output"),
            "command": "minikube addons list",
            "phase5_required": [
                "ingress - for external access",
                "metrics-server - for HPA"
            ]
        }

    async def _minikube_tunnel(self) -> Dict:
        """Start tunnel for LoadBalancer"""
        return {
            "status": "info",
            "command": "minikube tunnel",
            "note": "Run this in a separate terminal (it blocks)",
            "purpose": "Exposes LoadBalancer services on localhost",
            "example": """
# Terminal 1: Start tunnel (requires admin/sudo)
minikube tunnel

# Terminal 2: Check services
kubectl get svc -A
# LoadBalancer services will now have EXTERNAL-IP
"""
        }

    async def _docker_env(self) -> Dict:
        """Get Docker environment"""
        result = self._run_minikube(['docker-env'])

        return {
            "status": "success" if result.get("success") else "info",
            "output": result.get("output"),
            "command": "minikube docker-env",
            "usage": """
# Use Minikube's Docker daemon:
# PowerShell:
& minikube docker-env --shell powershell | Invoke-Expression

# Bash:
eval $(minikube docker-env)

# Then build images directly to Minikube
docker build -t my-app:latest .
""",
            "purpose": "Build images directly in Minikube's Docker"
        }

    async def _minikube_ip(self) -> Dict:
        """Get Minikube IP"""
        result = self._run_minikube(['ip'])
        return {
            "status": "success" if result.get("success") else "info",
            "ip": result.get("output", "").strip(),
            "command": "minikube ip",
            "usage": "Use this IP to access NodePort services"
        }

    async def _minikube_dashboard(self) -> Dict:
        """Open dashboard"""
        return {
            "status": "info",
            "command": "minikube dashboard",
            "note": "Opens Kubernetes Dashboard in browser",
            "alternative": "minikube dashboard --url (just get URL)"
        }

    async def _minikube_service(self, service_name: str,
                               namespace: str = "default") -> Dict:
        """Get service URL"""
        args = ['service', service_name, '-n', namespace, '--url']
        result = self._run_minikube(args)

        return {
            "status": "success" if result.get("success") else "info",
            "service": service_name,
            "namespace": namespace,
            "url": result.get("output", "").strip(),
            "command": f"minikube service {service_name} -n {namespace} --url"
        }

    async def _minikube_ssh(self, command: str = None) -> Dict:
        """SSH into node"""
        if command:
            return {
                "status": "info",
                "command": f"minikube ssh '{command}'",
                "note": "Runs command inside Minikube VM"
            }
        return {
            "status": "info",
            "command": "minikube ssh",
            "note": "Opens SSH shell to Minikube node"
        }
