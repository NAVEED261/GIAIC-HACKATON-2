"""
Kubernetes Agent - POWERFUL K8s Expert with MCP Tools
Self-reasoning, multi-step execution, complex query handling

@author: Phase-4 Multi-Agent System
"""

import asyncio
import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class KubernetesAgent(BaseAgent):
    """
    POWERFUL Kubernetes Expert Agent
    - Self-reasoning for complex queries
    - MCP Tools for all K8s operations
    - Multi-step execution
    - Error recovery
    """

    KEYWORDS = [
        'kubernetes', 'k8s', 'pod', 'pods', 'deployment', 'deploy',
        'service', 'svc', 'namespace', 'ns', 'kubectl', 'replica',
        'rollout', 'scale', 'node', 'cluster', 'minikube', 'container',
        'restart', 'logs', 'describe', 'delete', 'create', 'apply'
    ]

    def __init__(self):
        super().__init__("Kubernetes", "K8s cluster management expert - handles complex multi-step operations")
        self.namespace = "todo"
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all MCP tools for K8s operations"""

        # Tool: Get Pods
        self.register_tool(MCPTool(
            name="get_pods",
            description="Get all pods in a namespace with status, ready state, restarts, and age",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "Kubernetes namespace"},
                    "label_selector": {"type": "string", "description": "Label selector to filter pods"}
                }
            },
            handler=self._get_pods
        ))

        # Tool: Get Pod Logs
        self.register_tool(MCPTool(
            name="get_pod_logs",
            description="Get logs from a pod or deployment",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Pod or deployment name"},
                    "namespace": {"type": "string"},
                    "tail": {"type": "integer", "description": "Number of lines to show"},
                    "container": {"type": "string", "description": "Container name if multi-container pod"}
                },
                "required": ["name"]
            },
            handler=self._get_logs
        ))

        # Tool: Restart Deployment
        self.register_tool(MCPTool(
            name="restart_deployment",
            description="Restart a deployment by triggering a rolling update",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Deployment name"},
                    "namespace": {"type": "string"}
                },
                "required": ["name"]
            },
            handler=self._restart_deployment
        ))

        # Tool: Scale Deployment
        self.register_tool(MCPTool(
            name="scale_deployment",
            description="Scale a deployment to specified replicas",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Deployment name"},
                    "replicas": {"type": "integer", "description": "Number of replicas"},
                    "namespace": {"type": "string"}
                },
                "required": ["name", "replicas"]
            },
            handler=self._scale_deployment
        ))

        # Tool: Get Deployments
        self.register_tool(MCPTool(
            name="get_deployments",
            description="Get all deployments in a namespace",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            },
            handler=self._get_deployments
        ))

        # Tool: Get Services
        self.register_tool(MCPTool(
            name="get_services",
            description="Get all services with their types, ports, and endpoints",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            },
            handler=self._get_services
        ))

        # Tool: Describe Resource
        self.register_tool(MCPTool(
            name="describe_resource",
            description="Get detailed description of any K8s resource",
            parameters={
                "type": "object",
                "properties": {
                    "kind": {"type": "string", "description": "Resource kind (pod, deployment, service, etc.)"},
                    "name": {"type": "string", "description": "Resource name"},
                    "namespace": {"type": "string"}
                },
                "required": ["kind", "name"]
            },
            handler=self._describe_resource
        ))

        # Tool: Get Events
        self.register_tool(MCPTool(
            name="get_events",
            description="Get recent events in namespace for debugging",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "resource_name": {"type": "string", "description": "Filter events for specific resource"}
                }
            },
            handler=self._get_events
        ))

        # Tool: Execute kubectl
        self.register_tool(MCPTool(
            name="kubectl_exec",
            description="Execute any kubectl command directly",
            parameters={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "kubectl command to execute"}
                },
                "required": ["command"]
            },
            handler=self._kubectl_exec
        ))

        # Tool: Check Health
        self.register_tool(MCPTool(
            name="check_cluster_health",
            description="Comprehensive cluster health check - pods, deployments, services",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            },
            handler=self._check_health
        ))

        # Tool: Port Forward
        self.register_tool(MCPTool(
            name="get_service_url",
            description="Get external URL for a service via minikube",
            parameters={
                "type": "object",
                "properties": {
                    "service": {"type": "string", "description": "Service name"},
                    "namespace": {"type": "string"}
                },
                "required": ["service"]
            },
            handler=self._get_service_url
        ))

        # Tool: Apply YAML
        self.register_tool(MCPTool(
            name="apply_yaml",
            description="Apply a YAML manifest file",
            parameters={
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "Path to YAML file"},
                    "namespace": {"type": "string"}
                },
                "required": ["file"]
            },
            handler=self._apply_yaml
        ))

        # Tool: Delete Resource
        self.register_tool(MCPTool(
            name="delete_resource",
            description="Delete a Kubernetes resource",
            parameters={
                "type": "object",
                "properties": {
                    "kind": {"type": "string", "description": "Resource kind"},
                    "name": {"type": "string", "description": "Resource name"},
                    "namespace": {"type": "string"}
                },
                "required": ["kind", "name"]
            },
            handler=self._delete_resource
        ))

    # ==================== TOOL IMPLEMENTATIONS ====================

    async def _run_kubectl(self, cmd: str) -> str:
        """Execute kubectl command"""
        if not cmd.startswith("kubectl"):
            cmd = f"kubectl {cmd}"

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

    async def _get_pods(self, namespace: str = None, label_selector: str = None, **kwargs) -> List[Dict]:
        ns = namespace or self.namespace
        cmd = f"kubectl get pods -n {ns} -o json"
        if label_selector:
            cmd += f" -l {label_selector}"

        result = await self._run_kubectl(cmd)
        data = json.loads(result)

        pods = []
        for item in data.get("items", []):
            status = item.get("status", {})
            containers = status.get("containerStatuses", [{}])

            pods.append({
                "name": item.get("metadata", {}).get("name"),
                "namespace": item.get("metadata", {}).get("namespace"),
                "status": status.get("phase"),
                "ready": f"{sum(1 for c in containers if c.get('ready'))}/{len(containers)}",
                "restarts": sum(c.get("restartCount", 0) for c in containers),
                "age": item.get("metadata", {}).get("creationTimestamp"),
                "node": item.get("spec", {}).get("nodeName"),
                "ip": status.get("podIP")
            })

        return pods

    async def _get_logs(self, name: str, namespace: str = None, tail: int = 50, container: str = None, **kwargs) -> str:
        ns = namespace or self.namespace
        cmd = f"kubectl logs -n {ns} --tail={tail}"

        if "deployment" in name.lower() or not "/" in name:
            cmd += f" deployment/{name.replace('deployment/', '')}"
        else:
            cmd += f" {name}"

        if container:
            cmd += f" -c {container}"

        return await self._run_kubectl(cmd)

    async def _restart_deployment(self, name: str, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace
        result = await self._run_kubectl(f"kubectl rollout restart deployment/{name} -n {ns}")

        # Wait for rollout
        await self._run_kubectl(f"kubectl rollout status deployment/{name} -n {ns} --timeout=120s")

        return {"status": "restarted", "deployment": name, "output": result}

    async def _scale_deployment(self, name: str, replicas: int, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace
        result = await self._run_kubectl(f"kubectl scale deployment/{name} --replicas={replicas} -n {ns}")
        return {"status": "scaled", "deployment": name, "replicas": replicas, "output": result}

    async def _get_deployments(self, namespace: str = None, **kwargs) -> List[Dict]:
        ns = namespace or self.namespace
        result = await self._run_kubectl(f"kubectl get deployments -n {ns} -o json")
        data = json.loads(result)

        deployments = []
        for item in data.get("items", []):
            status = item.get("status", {})
            deployments.append({
                "name": item.get("metadata", {}).get("name"),
                "ready": f"{status.get('readyReplicas', 0)}/{status.get('replicas', 0)}",
                "available": status.get("availableReplicas", 0),
                "age": item.get("metadata", {}).get("creationTimestamp")
            })

        return deployments

    async def _get_services(self, namespace: str = None, **kwargs) -> List[Dict]:
        ns = namespace or self.namespace
        result = await self._run_kubectl(f"kubectl get svc -n {ns} -o json")
        data = json.loads(result)

        services = []
        for item in data.get("items", []):
            spec = item.get("spec", {})
            ports = spec.get("ports", [])

            services.append({
                "name": item.get("metadata", {}).get("name"),
                "type": spec.get("type"),
                "clusterIP": spec.get("clusterIP"),
                "ports": [f"{p.get('port')}:{p.get('nodePort', 'N/A')}/{p.get('protocol')}" for p in ports],
                "selector": spec.get("selector", {})
            })

        return services

    async def _describe_resource(self, kind: str, name: str, namespace: str = None, **kwargs) -> str:
        ns = namespace or self.namespace
        return await self._run_kubectl(f"kubectl describe {kind} {name} -n {ns}")

    async def _get_events(self, namespace: str = None, resource_name: str = None, **kwargs) -> List[Dict]:
        ns = namespace or self.namespace
        cmd = f"kubectl get events -n {ns} -o json --sort-by='.lastTimestamp'"

        result = await self._run_kubectl(cmd)
        data = json.loads(result)

        events = []
        for item in data.get("items", [])[-20:]:  # Last 20 events
            if resource_name and resource_name not in item.get("involvedObject", {}).get("name", ""):
                continue

            events.append({
                "type": item.get("type"),
                "reason": item.get("reason"),
                "message": item.get("message"),
                "object": f"{item.get('involvedObject', {}).get('kind')}/{item.get('involvedObject', {}).get('name')}",
                "time": item.get("lastTimestamp")
            })

        return events

    async def _kubectl_exec(self, command: str, **kwargs) -> str:
        return await self._run_kubectl(command)

    async def _check_health(self, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        pods = await self._get_pods(namespace=ns)
        deployments = await self._get_deployments(namespace=ns)
        services = await self._get_services(namespace=ns)

        # Analyze health
        running_pods = [p for p in pods if p.get("status") == "Running"]
        unhealthy_pods = [p for p in pods if p.get("status") != "Running"]
        high_restart_pods = [p for p in pods if p.get("restarts", 0) > 5]

        health_status = "Healthy"
        issues = []

        if unhealthy_pods:
            health_status = "Degraded"
            issues.append(f"{len(unhealthy_pods)} pods not running")

        if high_restart_pods:
            health_status = "Warning"
            issues.append(f"{len(high_restart_pods)} pods with high restarts")

        return {
            "status": health_status,
            "namespace": ns,
            "summary": {
                "pods": {"total": len(pods), "running": len(running_pods)},
                "deployments": len(deployments),
                "services": len(services)
            },
            "issues": issues,
            "pods": pods,
            "deployments": deployments,
            "services": services
        }

    async def _get_service_url(self, service: str, namespace: str = None, **kwargs) -> str:
        ns = namespace or self.namespace
        result = await self._run_kubectl(f"minikube service {service} -n {ns} --url")
        return result.strip()

    async def _apply_yaml(self, file: str, namespace: str = None, **kwargs) -> str:
        ns = namespace or self.namespace
        return await self._run_kubectl(f"kubectl apply -f {file} -n {ns}")

    async def _delete_resource(self, kind: str, name: str, namespace: str = None, **kwargs) -> str:
        ns = namespace or self.namespace
        return await self._run_kubectl(f"kubectl delete {kind} {name} -n {ns}")

    # ==================== AGENT INTERFACE ====================

    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in self.KEYWORDS)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute using self-reasoning and MCP tools"""
        query = task.get("task", "")
        params = task.get("params", {})

        # Use powerful process method with reasoning
        return await self.process(query, params)

    async def execute_direct(self, step: Dict) -> Any:
        """Direct execution for steps without specific tools"""
        query = step.get("query", step.get("action", "")).lower()

        # Smart matching to MCP tools based on query content
        if "pod" in query:
            return await self._get_pods()
        elif "deployment" in query:
            return await self._get_deployments()
        elif "service" in query or "svc" in query:
            return await self._get_services()
        elif "health" in query or "status" in query:
            return await self._check_health()
        elif "log" in query:
            # Try to extract deployment name
            return await self._get_logs(name="todo-backend")
        elif "event" in query:
            return await self._get_events()

        return {"status": "no action taken"}
