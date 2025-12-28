"""
Monitoring Agent - POWERFUL Observability Expert
Metrics, logs, alerts, health checks, performance monitoring

@author: Phase-4 Multi-Agent System
"""

import asyncio
import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class MonitoringAgent(BaseAgent):
    """
    POWERFUL Monitoring Expert Agent
    - Metrics collection
    - Log aggregation
    - Alert management
    - Health checks
    - Performance analysis
    """

    KEYWORDS = [
        'monitor', 'monitoring', 'metrics', 'logs', 'alert', 'health',
        'prometheus', 'grafana', 'performance', 'cpu', 'memory', 'disk',
        'latency', 'throughput', 'error rate', 'uptime', 'dashboard'
    ]

    def __init__(self, namespace: str = "todo"):
        super().__init__("Monitoring", "Observability expert - metrics, logs, alerts, performance")
        self.namespace = namespace
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all MCP tools for monitoring operations"""

        # Tool: Get Pod Metrics
        self.register_tool(MCPTool(
            name="get_pod_metrics",
            description="Get CPU/memory metrics for pods",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "pod": {"type": "string", "description": "Specific pod name"}
                }
            },
            handler=self._get_pod_metrics
        ))

        # Tool: Get Node Metrics
        self.register_tool(MCPTool(
            name="get_node_metrics",
            description="Get node-level resource metrics",
            parameters={
                "type": "object",
                "properties": {
                    "node": {"type": "string", "description": "Specific node name"}
                }
            },
            handler=self._get_node_metrics
        ))

        # Tool: Get Logs
        self.register_tool(MCPTool(
            name="get_logs",
            description="Get logs from pods with filtering",
            parameters={
                "type": "object",
                "properties": {
                    "pod": {"type": "string", "description": "Pod name or deployment"},
                    "namespace": {"type": "string"},
                    "tail": {"type": "integer", "description": "Number of lines"},
                    "since": {"type": "string", "description": "Time duration (e.g., 1h, 30m)"},
                    "grep": {"type": "string", "description": "Filter pattern"}
                },
                "required": ["pod"]
            },
            handler=self._get_logs
        ))

        # Tool: Health Check
        self.register_tool(MCPTool(
            name="health_check",
            description="Comprehensive health check of all services",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "service": {"type": "string", "description": "Specific service to check"}
                }
            },
            handler=self._health_check
        ))

        # Tool: Get Error Rate
        self.register_tool(MCPTool(
            name="get_error_rate",
            description="Calculate error rate from logs",
            parameters={
                "type": "object",
                "properties": {
                    "pod": {"type": "string"},
                    "namespace": {"type": "string"},
                    "duration": {"type": "string", "description": "Time window"}
                }
            },
            handler=self._get_error_rate
        ))

        # Tool: Get Resource Usage
        self.register_tool(MCPTool(
            name="get_resource_usage",
            description="Get resource usage summary",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "resource_type": {"type": "string", "description": "pods, nodes, or all"}
                }
            },
            handler=self._get_resource_usage
        ))

        # Tool: Check Endpoints
        self.register_tool(MCPTool(
            name="check_endpoints",
            description="Check if service endpoints are healthy",
            parameters={
                "type": "object",
                "properties": {
                    "service": {"type": "string", "description": "Service name"},
                    "namespace": {"type": "string"},
                    "port": {"type": "integer"}
                },
                "required": ["service"]
            },
            handler=self._check_endpoints
        ))

        # Tool: Get Events
        self.register_tool(MCPTool(
            name="get_events",
            description="Get Kubernetes events for debugging",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "type": {"type": "string", "description": "Normal or Warning"},
                    "resource": {"type": "string", "description": "Filter by resource name"}
                }
            },
            handler=self._get_events
        ))

        # Tool: Analyze Performance
        self.register_tool(MCPTool(
            name="analyze_performance",
            description="Analyze application performance from metrics",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "deployment": {"type": "string"}
                }
            },
            handler=self._analyze_performance
        ))

        # Tool: Create Alert
        self.register_tool(MCPTool(
            name="create_alert",
            description="Create monitoring alert rule",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Alert name"},
                    "condition": {"type": "string", "description": "Alert condition"},
                    "threshold": {"type": "number"},
                    "severity": {"type": "string", "description": "critical, warning, info"}
                },
                "required": ["name", "condition"]
            },
            handler=self._create_alert
        ))

        # Tool: Get Uptime
        self.register_tool(MCPTool(
            name="get_uptime",
            description="Get service uptime statistics",
            parameters={
                "type": "object",
                "properties": {
                    "deployment": {"type": "string"},
                    "namespace": {"type": "string"}
                }
            },
            handler=self._get_uptime
        ))

    # ==================== TOOL IMPLEMENTATIONS ====================

    async def _run_cmd(self, cmd: str) -> str:
        """Execute shell command"""
        self.log(f"$ {cmd}", "working")

        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0 and stderr:
            raise Exception(stderr.decode())

        return stdout.decode()

    async def _get_pod_metrics(self, namespace: str = None, pod: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        if pod:
            result = await self._run_cmd(f"kubectl top pod {pod} -n {ns}")
        else:
            result = await self._run_cmd(f"kubectl top pods -n {ns}")

        # Parse metrics
        lines = result.strip().split('\n')
        metrics = []

        for line in lines[1:]:  # Skip header
            parts = line.split()
            if len(parts) >= 3:
                metrics.append({
                    "pod": parts[0],
                    "cpu": parts[1],
                    "memory": parts[2]
                })

        return {"metrics": metrics, "namespace": ns}

    async def _get_node_metrics(self, node: str = None, **kwargs) -> Dict:
        if node:
            result = await self._run_cmd(f"kubectl top node {node}")
        else:
            result = await self._run_cmd("kubectl top nodes")

        lines = result.strip().split('\n')
        metrics = []

        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 5:
                metrics.append({
                    "node": parts[0],
                    "cpu": parts[1],
                    "cpu_percent": parts[2],
                    "memory": parts[3],
                    "memory_percent": parts[4]
                })

        return {"nodes": metrics}

    async def _get_logs(self, pod: str, namespace: str = None, tail: int = 100, since: str = None, grep: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        cmd = f"kubectl logs -n {ns} --tail={tail}"

        if "/" not in pod:
            cmd += f" deployment/{pod}"
        else:
            cmd += f" {pod}"

        if since:
            cmd += f" --since={since}"

        result = await self._run_cmd(cmd)

        logs = result.strip().split('\n')

        if grep:
            logs = [l for l in logs if grep.lower() in l.lower()]

        return {
            "logs": logs[-tail:],
            "count": len(logs),
            "pod": pod
        }

    async def _health_check(self, namespace: str = None, service: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        # Get pods
        pods_result = await self._run_cmd(f"kubectl get pods -n {ns} -o json")
        pods_data = json.loads(pods_result)

        health = {
            "status": "healthy",
            "namespace": ns,
            "pods": [],
            "issues": []
        }

        for pod in pods_data.get("items", []):
            name = pod.get("metadata", {}).get("name")
            status = pod.get("status", {})
            phase = status.get("phase")

            pod_health = {
                "name": name,
                "phase": phase,
                "ready": False
            }

            # Check containers
            containers = status.get("containerStatuses", [])
            ready_count = sum(1 for c in containers if c.get("ready"))
            pod_health["ready"] = ready_count == len(containers)
            pod_health["containers"] = f"{ready_count}/{len(containers)}"

            if phase != "Running":
                health["status"] = "degraded"
                health["issues"].append(f"Pod {name} is {phase}")

            if not pod_health["ready"]:
                health["status"] = "degraded"
                health["issues"].append(f"Pod {name} containers not ready")

            health["pods"].append(pod_health)

        return health

    async def _get_error_rate(self, pod: str = None, namespace: str = None, duration: str = "1h", **kwargs) -> Dict:
        ns = namespace or self.namespace

        if pod:
            cmd = f"kubectl logs -n {ns} deployment/{pod} --since={duration}"
        else:
            cmd = f"kubectl logs -n {ns} -l app --since={duration}"

        try:
            result = await self._run_cmd(cmd)
            logs = result.strip().split('\n')

            total = len(logs)
            errors = sum(1 for l in logs if 'error' in l.lower() or 'exception' in l.lower())
            warnings = sum(1 for l in logs if 'warning' in l.lower() or 'warn' in l.lower())

            error_rate = (errors / total * 100) if total > 0 else 0

            return {
                "total_logs": total,
                "errors": errors,
                "warnings": warnings,
                "error_rate": f"{error_rate:.2f}%",
                "duration": duration
            }
        except:
            return {"error": "Could not calculate error rate"}

    async def _get_resource_usage(self, namespace: str = None, resource_type: str = "all", **kwargs) -> Dict:
        ns = namespace or self.namespace
        usage = {}

        if resource_type in ["pods", "all"]:
            try:
                result = await self._run_cmd(f"kubectl top pods -n {ns}")
                usage["pods"] = result
            except:
                usage["pods"] = "metrics-server not available"

        if resource_type in ["nodes", "all"]:
            try:
                result = await self._run_cmd("kubectl top nodes")
                usage["nodes"] = result
            except:
                usage["nodes"] = "metrics-server not available"

        return usage

    async def _check_endpoints(self, service: str, namespace: str = None, port: int = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        # Get endpoints
        result = await self._run_cmd(f"kubectl get endpoints {service} -n {ns} -o json")
        data = json.loads(result)

        subsets = data.get("subsets", [])
        endpoints = []

        for subset in subsets:
            addresses = subset.get("addresses", [])
            ports = subset.get("ports", [])

            for addr in addresses:
                for p in ports:
                    endpoints.append({
                        "ip": addr.get("ip"),
                        "port": p.get("port"),
                        "protocol": p.get("protocol"),
                        "ready": True
                    })

        return {
            "service": service,
            "endpoints": endpoints,
            "healthy": len(endpoints) > 0
        }

    async def _get_events(self, namespace: str = None, type: str = None, resource: str = None, **kwargs) -> List[Dict]:
        ns = namespace or self.namespace

        cmd = f"kubectl get events -n {ns} --sort-by='.lastTimestamp' -o json"

        result = await self._run_cmd(cmd)
        data = json.loads(result)

        events = []
        for item in data.get("items", [])[-20:]:  # Last 20
            event = {
                "type": item.get("type"),
                "reason": item.get("reason"),
                "message": item.get("message"),
                "object": f"{item.get('involvedObject', {}).get('kind')}/{item.get('involvedObject', {}).get('name')}",
                "time": item.get("lastTimestamp")
            }

            if type and event["type"] != type:
                continue
            if resource and resource not in event["object"]:
                continue

            events.append(event)

        return events

    async def _analyze_performance(self, namespace: str = None, deployment: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        analysis = {
            "status": "analyzing",
            "metrics": {},
            "recommendations": []
        }

        # Get pod metrics
        try:
            metrics = await self._get_pod_metrics(namespace=ns)
            analysis["metrics"]["pods"] = metrics
        except:
            analysis["metrics"]["pods"] = "unavailable"

        # Get health
        health = await self._health_check(namespace=ns)
        analysis["health"] = health

        # Get error rate
        if deployment:
            errors = await self._get_error_rate(pod=deployment, namespace=ns)
            analysis["metrics"]["errors"] = errors

        # Generate recommendations
        if health["status"] != "healthy":
            analysis["recommendations"].append("Investigate unhealthy pods")

        analysis["status"] = "complete"
        return analysis

    async def _create_alert(self, name: str, condition: str, threshold: float = None, severity: str = "warning", **kwargs) -> Dict:
        # This would integrate with Prometheus AlertManager in real scenario
        alert = {
            "name": name,
            "condition": condition,
            "threshold": threshold,
            "severity": severity,
            "status": "created",
            "note": "Alert configuration saved (would integrate with AlertManager)"
        }

        self.log(f"Alert created: {name} - {condition}", "success")
        return alert

    async def _get_uptime(self, deployment: str = None, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        if deployment:
            result = await self._run_cmd(f"kubectl get deployment {deployment} -n {ns} -o json")
            data = json.loads(result)

            creation = data.get("metadata", {}).get("creationTimestamp")
            replicas = data.get("status", {}).get("replicas", 0)
            available = data.get("status", {}).get("availableReplicas", 0)

            return {
                "deployment": deployment,
                "created": creation,
                "replicas": replicas,
                "available": available,
                "availability": f"{(available/replicas*100) if replicas > 0 else 0:.1f}%"
            }

        # Get all deployments
        result = await self._run_cmd(f"kubectl get deployments -n {ns} -o json")
        data = json.loads(result)

        deployments = []
        for item in data.get("items", []):
            name = item.get("metadata", {}).get("name")
            replicas = item.get("status", {}).get("replicas", 0)
            available = item.get("status", {}).get("availableReplicas", 0)

            deployments.append({
                "name": name,
                "replicas": replicas,
                "available": available,
                "availability": f"{(available/replicas*100) if replicas > 0 else 0:.1f}%"
            })

        return {"deployments": deployments}

    # ==================== AGENT INTERFACE ====================

    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in self.KEYWORDS)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute using self-reasoning and MCP tools"""
        query = task.get("task", "")
        params = task.get("params", {})

        return await self.process(query, params)

    async def execute_direct(self, step: Dict) -> Any:
        """Direct execution for steps - Smart matching to MCP tools"""
        query = step.get("query", step.get("action", "")).lower()

        # Smart matching to MCP tools based on query content
        if "metric" in query or "cpu" in query or "memory" in query:
            return await self._get_pod_metrics()
        elif "log" in query:
            return await self._get_logs(pod="todo-backend")
        elif "health" in query or "check" in query:
            return await self._health_check()
        elif "error" in query:
            return await self._get_error_rate()
        elif "resource" in query or "usage" in query:
            return await self._get_resource_usage()
        elif "endpoint" in query:
            return await self._check_endpoints(service="todo-backend-service")
        elif "event" in query:
            return await self._get_events()
        elif "uptime" in query:
            return await self._get_uptime()

        return {"status": "no action taken", "query": query}
