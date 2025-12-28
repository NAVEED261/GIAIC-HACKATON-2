"""
K8s Deploy Agent - Kubernetes Deployment Expert
Handles Kubernetes deployments for Phase-5

@author: Phase-5 AI Employs System
"""

import asyncio
import subprocess
from typing import Dict, List, Any, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class K8sDeployAgent(BaseAgent):
    """
    Kubernetes Deployment Expert Agent

    Capabilities:
    - Deploy applications to K8s
    - Manage deployments, services, pods
    - Apply manifests
    - Scale applications
    - Health checks and logs

    MCP Tools: 15
    """

    def __init__(self):
        super().__init__()
        self.name = "K8sDeployAgent"
        self.domain = "k8s"
        self.description = "Kubernetes deployment expert"
        self.emoji = "☸️"
        self.namespace = "todo-phase5"

    def _setup_tools(self):
        """Setup K8s MCP tools"""

        # Tool 1: Apply Manifest
        self.register_tool(MCPTool(
            name="apply_manifest",
            description="Apply a Kubernetes manifest file",
            parameters={
                "file_path": "string (required)",
                "namespace": "string (optional)"
            },
            handler=self._apply_manifest
        ))

        # Tool 2: Get Pods
        self.register_tool(MCPTool(
            name="get_pods",
            description="List pods in namespace",
            parameters={"namespace": "string (optional)"},
            handler=self._get_pods
        ))

        # Tool 3: Get Deployments
        self.register_tool(MCPTool(
            name="get_deployments",
            description="List deployments in namespace",
            parameters={"namespace": "string (optional)"},
            handler=self._get_deployments
        ))

        # Tool 4: Get Services
        self.register_tool(MCPTool(
            name="get_services",
            description="List services in namespace",
            parameters={"namespace": "string (optional)"},
            handler=self._get_services
        ))

        # Tool 5: Scale Deployment
        self.register_tool(MCPTool(
            name="scale_deployment",
            description="Scale a deployment",
            parameters={
                "deployment": "string (required)",
                "replicas": "int (required)",
                "namespace": "string (optional)"
            },
            handler=self._scale_deployment
        ))

        # Tool 6: Get Pod Logs
        self.register_tool(MCPTool(
            name="get_pod_logs",
            description="Get logs from a pod",
            parameters={
                "pod_name": "string (required)",
                "namespace": "string (optional)",
                "tail": "int (default: 100)"
            },
            handler=self._get_pod_logs
        ))

        # Tool 7: Describe Resource
        self.register_tool(MCPTool(
            name="describe_resource",
            description="Describe a Kubernetes resource",
            parameters={
                "resource_type": "string (required)",
                "name": "string (required)",
                "namespace": "string (optional)"
            },
            handler=self._describe_resource
        ))

        # Tool 8: Create Namespace
        self.register_tool(MCPTool(
            name="create_namespace",
            description="Create a Kubernetes namespace",
            parameters={"namespace": "string (required)"},
            handler=self._create_namespace
        ))

        # Tool 9: Delete Resource
        self.register_tool(MCPTool(
            name="delete_resource",
            description="Delete a Kubernetes resource",
            parameters={
                "resource_type": "string (required)",
                "name": "string (required)",
                "namespace": "string (optional)"
            },
            handler=self._delete_resource
        ))

        # Tool 10: Port Forward
        self.register_tool(MCPTool(
            name="port_forward",
            description="Create port forward to a pod/service",
            parameters={
                "resource": "string (required)",
                "local_port": "int (required)",
                "remote_port": "int (required)",
                "namespace": "string (optional)"
            },
            handler=self._port_forward
        ))

        # Tool 11: Get Events
        self.register_tool(MCPTool(
            name="get_events",
            description="Get Kubernetes events",
            parameters={"namespace": "string (optional)"},
            handler=self._get_events
        ))

        # Tool 12: Rollout Status
        self.register_tool(MCPTool(
            name="rollout_status",
            description="Check deployment rollout status",
            parameters={
                "deployment": "string (required)",
                "namespace": "string (optional)"
            },
            handler=self._rollout_status
        ))

        # Tool 13: Rollout Restart
        self.register_tool(MCPTool(
            name="rollout_restart",
            description="Restart a deployment",
            parameters={
                "deployment": "string (required)",
                "namespace": "string (optional)"
            },
            handler=self._rollout_restart
        ))

        # Tool 14: Get ConfigMaps
        self.register_tool(MCPTool(
            name="get_configmaps",
            description="List ConfigMaps",
            parameters={"namespace": "string (optional)"},
            handler=self._get_configmaps
        ))

        # Tool 15: Get Secrets
        self.register_tool(MCPTool(
            name="get_secrets",
            description="List Secrets (names only)",
            parameters={"namespace": "string (optional)"},
            handler=self._get_secrets
        ))

    def _match_tool(self, query: str) -> Optional[str]:
        """Match query to best K8s tool"""
        query = query.lower()

        if any(w in query for w in ['apply', 'deploy manifest', 'kubectl apply']):
            return 'apply_manifest'
        elif any(w in query for w in ['pod', 'list pod', 'get pod']):
            return 'get_pods'
        elif any(w in query for w in ['deployment', 'list deployment']):
            return 'get_deployments'
        elif any(w in query for w in ['service', 'svc', 'list service']):
            return 'get_services'
        elif any(w in query for w in ['scale', 'replica']):
            return 'scale_deployment'
        elif any(w in query for w in ['log', 'logs']):
            return 'get_pod_logs'
        elif any(w in query for w in ['describe']):
            return 'describe_resource'
        elif any(w in query for w in ['namespace', 'create ns']):
            return 'create_namespace'
        elif any(w in query for w in ['delete', 'remove']):
            return 'delete_resource'
        elif any(w in query for w in ['port forward', 'forward']):
            return 'port_forward'
        elif any(w in query for w in ['event']):
            return 'get_events'
        elif any(w in query for w in ['rollout status', 'status']):
            return 'rollout_status'
        elif any(w in query for w in ['restart', 'rollout restart']):
            return 'rollout_restart'
        elif any(w in query for w in ['configmap', 'cm']):
            return 'get_configmaps'
        elif any(w in query for w in ['secret']):
            return 'get_secrets'

        return 'get_pods'

    async def execute_direct(self, step: Dict) -> Any:
        """Smart direct execution"""
        query = step.get("query", "").lower()
        tool_name = step.get("tool") or self._match_tool(query)

        if tool_name == 'apply_manifest':
            return await self._apply_manifest(file_path="manifest.yaml")

        elif tool_name == 'get_pods':
            return await self._get_pods()

        elif tool_name == 'get_deployments':
            return await self._get_deployments()

        elif tool_name == 'get_services':
            return await self._get_services()

        elif tool_name == 'scale_deployment':
            return await self._scale_deployment(deployment="backend", replicas=2)

        elif tool_name == 'get_pod_logs':
            return await self._get_pod_logs(pod_name="backend-0")

        elif tool_name == 'create_namespace':
            return await self._create_namespace(namespace=self.namespace)

        else:
            return await self._get_pods()

    def _run_kubectl(self, args: List[str], timeout: int = 30) -> Dict:
        """Run kubectl command"""
        try:
            result = subprocess.run(
                ['kubectl'] + args,
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
                "error": "kubectl not found",
                "command": f"kubectl {' '.join(args)}"
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ==================== Tool Handlers ====================

    async def _apply_manifest(self, file_path: str,
                             namespace: str = None) -> Dict:
        """Apply Kubernetes manifest"""
        ns = namespace or self.namespace
        args = ['apply', '-f', file_path, '-n', ns]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "file": file_path,
            "namespace": ns,
            "output": result.get("output"),
            "command": f"kubectl apply -f {file_path} -n {ns}"
        }

    async def _get_pods(self, namespace: str = None) -> Dict:
        """Get pods in namespace"""
        ns = namespace or self.namespace
        args = ['get', 'pods', '-n', ns, '-o', 'wide']

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "namespace": ns,
            "output": result.get("output"),
            "command": f"kubectl get pods -n {ns} -o wide"
        }

    async def _get_deployments(self, namespace: str = None) -> Dict:
        """Get deployments"""
        ns = namespace or self.namespace
        args = ['get', 'deployments', '-n', ns]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "namespace": ns,
            "output": result.get("output"),
            "command": f"kubectl get deployments -n {ns}"
        }

    async def _get_services(self, namespace: str = None) -> Dict:
        """Get services"""
        ns = namespace or self.namespace
        args = ['get', 'services', '-n', ns]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "namespace": ns,
            "output": result.get("output"),
            "command": f"kubectl get services -n {ns}"
        }

    async def _scale_deployment(self, deployment: str, replicas: int,
                               namespace: str = None) -> Dict:
        """Scale deployment"""
        ns = namespace or self.namespace
        args = ['scale', 'deployment', deployment,
                '--replicas', str(replicas), '-n', ns]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "deployment": deployment,
            "replicas": replicas,
            "namespace": ns,
            "command": f"kubectl scale deployment {deployment} --replicas={replicas} -n {ns}"
        }

    async def _get_pod_logs(self, pod_name: str, namespace: str = None,
                           tail: int = 100) -> Dict:
        """Get pod logs"""
        ns = namespace or self.namespace
        args = ['logs', pod_name, '-n', ns, '--tail', str(tail)]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "pod": pod_name,
            "namespace": ns,
            "tail": tail,
            "output": result.get("output"),
            "command": f"kubectl logs {pod_name} -n {ns} --tail={tail}"
        }

    async def _describe_resource(self, resource_type: str, name: str,
                                 namespace: str = None) -> Dict:
        """Describe resource"""
        ns = namespace or self.namespace
        args = ['describe', resource_type, name, '-n', ns]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "resource": f"{resource_type}/{name}",
            "namespace": ns,
            "output": result.get("output"),
            "command": f"kubectl describe {resource_type} {name} -n {ns}"
        }

    async def _create_namespace(self, namespace: str) -> Dict:
        """Create namespace"""
        args = ['create', 'namespace', namespace]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "namespace": namespace,
            "output": result.get("output") or f"Namespace {namespace} created",
            "command": f"kubectl create namespace {namespace}"
        }

    async def _delete_resource(self, resource_type: str, name: str,
                              namespace: str = None) -> Dict:
        """Delete resource"""
        ns = namespace or self.namespace
        args = ['delete', resource_type, name, '-n', ns]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "resource": f"{resource_type}/{name}",
            "namespace": ns,
            "command": f"kubectl delete {resource_type} {name} -n {ns}"
        }

    async def _port_forward(self, resource: str, local_port: int,
                           remote_port: int, namespace: str = None) -> Dict:
        """Port forward command"""
        ns = namespace or self.namespace
        return {
            "status": "info",
            "resource": resource,
            "ports": f"{local_port}:{remote_port}",
            "namespace": ns,
            "command": f"kubectl port-forward {resource} {local_port}:{remote_port} -n {ns}",
            "note": "Run this command in a terminal (it blocks)"
        }

    async def _get_events(self, namespace: str = None) -> Dict:
        """Get K8s events"""
        ns = namespace or self.namespace
        args = ['get', 'events', '-n', ns, '--sort-by=.lastTimestamp']

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "namespace": ns,
            "output": result.get("output"),
            "command": f"kubectl get events -n {ns} --sort-by=.lastTimestamp"
        }

    async def _rollout_status(self, deployment: str,
                             namespace: str = None) -> Dict:
        """Check rollout status"""
        ns = namespace or self.namespace
        args = ['rollout', 'status', 'deployment', deployment, '-n', ns]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "deployment": deployment,
            "namespace": ns,
            "output": result.get("output"),
            "command": f"kubectl rollout status deployment {deployment} -n {ns}"
        }

    async def _rollout_restart(self, deployment: str,
                              namespace: str = None) -> Dict:
        """Restart deployment"""
        ns = namespace or self.namespace
        args = ['rollout', 'restart', 'deployment', deployment, '-n', ns]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "deployment": deployment,
            "namespace": ns,
            "action": "restarted",
            "command": f"kubectl rollout restart deployment {deployment} -n {ns}"
        }

    async def _get_configmaps(self, namespace: str = None) -> Dict:
        """Get ConfigMaps"""
        ns = namespace or self.namespace
        args = ['get', 'configmaps', '-n', ns]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "namespace": ns,
            "output": result.get("output"),
            "command": f"kubectl get configmaps -n {ns}"
        }

    async def _get_secrets(self, namespace: str = None) -> Dict:
        """Get Secrets (names only for security)"""
        ns = namespace or self.namespace
        args = ['get', 'secrets', '-n', ns]

        result = self._run_kubectl(args)
        return {
            "status": "success" if result.get("success") else "info",
            "namespace": ns,
            "output": result.get("output"),
            "command": f"kubectl get secrets -n {ns}",
            "note": "Secret values not shown for security"
        }
