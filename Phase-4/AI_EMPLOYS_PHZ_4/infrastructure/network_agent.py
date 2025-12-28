"""
Network Agent - Networking & Connectivity Expert
Handles ingress, DNS, ports, connectivity

@author: Phase-4 Multi-Agent System
"""

import asyncio
from typing import Dict, Any, List
import sys
sys.path.append('..')
from base_agent import BaseAgent


class NetworkAgent(BaseAgent):
    """
    Network Expert Agent
    Handles: ingress, ports, DNS, connectivity
    """

    KEYWORDS = [
        'network', 'ingress', 'port', 'dns', 'url', 'endpoint',
        'connectivity', 'tunnel', 'proxy', 'cors', 'ssl', 'tls'
    ]

    def __init__(self):
        super().__init__("Network", "Networking & connectivity expert")

    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in self.KEYWORDS)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_str = task.get("task", "")
        params = task.get("params", {})

        self.start_work(task_str)

        try:
            if "url" in task_str.lower() or "endpoint" in task_str.lower():
                result = await self.get_service_urls(params)
            elif "ingress" in task_str.lower():
                result = await self.get_ingress(params)
            elif "port" in task_str.lower():
                result = await self.check_ports(params)
            elif "connectivity" in task_str.lower() or "health" in task_str.lower():
                result = await self.check_connectivity(params)
            elif "tunnel" in task_str.lower():
                result = await self.setup_tunnel(params)
            else:
                result = await self.network_status()

            self.end_work("Task completed")
            return {"success": True, "data": result}

        except Exception as e:
            self.report_error(str(e))
            return {"success": False, "error": str(e)}

    async def run_command(self, cmd: str) -> str:
        self.log(f"Executing: {cmd}", "working")
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode()

    async def get_service_urls(self, params: Dict) -> Dict[str, str]:
        ns = params.get("namespace", "todo")
        self.log(f"Getting service URLs in {ns}", "working")

        urls = {}
        result = await self.run_command(
            f"kubectl get svc -n {ns} -o jsonpath='{{range .items[*]}}{{.metadata.name}}:{{.spec.ports[0].nodePort}}{{\"\\n\"}}{{end}}'"
        )

        for line in result.strip().split('\n'):
            if ':' in line:
                name, port = line.split(':')
                if port and port != '<none>':
                    urls[name] = f"http://127.0.0.1:{port}"

        return urls

    async def get_ingress(self, params: Dict) -> List[Dict]:
        ns = params.get("namespace", "todo")
        self.log(f"Getting ingress in {ns}", "working")

        result = await self.run_command(f"kubectl get ingress -n {ns} -o json")
        import json
        try:
            data = json.loads(result)
            return data.get("items", [])
        except:
            return []

    async def check_ports(self, params: Dict) -> List[Dict]:
        ns = params.get("namespace", "todo")
        self.log("Checking service ports", "working")

        result = await self.run_command(
            f"kubectl get svc -n {ns} -o custom-columns='NAME:.metadata.name,TYPE:.spec.type,PORT:.spec.ports[0].port,NODEPORT:.spec.ports[0].nodePort'"
        )

        ports = []
        lines = result.strip().split('\n')[1:]  # Skip header
        for line in lines:
            parts = line.split()
            if len(parts) >= 4:
                ports.append({
                    "service": parts[0],
                    "type": parts[1],
                    "port": parts[2],
                    "nodePort": parts[3]
                })

        return ports

    async def check_connectivity(self, params: Dict) -> Dict:
        url = params.get("url", "http://127.0.0.1:65525/health")
        self.log(f"Checking connectivity to {url}", "working")

        try:
            result = await self.run_command(f"curl -s -o /dev/null -w '%{{http_code}}' {url}")
            status_code = result.strip()
            return {
                "url": url,
                "status": "healthy" if status_code == "200" else "unhealthy",
                "http_code": status_code
            }
        except:
            return {"url": url, "status": "unreachable"}

    async def setup_tunnel(self, params: Dict) -> str:
        service = params.get("service", "")
        ns = params.get("namespace", "todo")

        self.log(f"Setting up tunnel for {service}", "working")
        result = await self.run_command(f"minikube service {service} -n {ns} --url")
        return result.strip()

    async def network_status(self) -> Dict:
        self.log("Getting network status", "working")

        urls = await self.get_service_urls({})
        ports = await self.check_ports({})

        # Check health of each URL
        health = {}
        for name, url in urls.items():
            check = await self.check_connectivity({"url": f"{url}/health"})
            health[name] = check.get("status", "unknown")

        return {
            "services": urls,
            "ports": ports,
            "health": health
        }
