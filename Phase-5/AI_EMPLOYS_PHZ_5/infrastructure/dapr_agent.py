"""
Dapr Agent - Distributed Runtime Expert
Handles Dapr operations for Phase-5

@author: Phase-5 AI Employs System
"""

import asyncio
import subprocess
import json
from typing import Dict, List, Any, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class DaprAgent(BaseAgent):
    """
    Dapr Expert Agent

    Capabilities:
    - Component management (pub/sub, state, bindings, secrets)
    - Service invocation
    - State management
    - Pub/Sub messaging
    - Health checks

    MCP Tools: 15
    """

    def __init__(self):
        super().__init__()
        self.name = "DaprAgent"
        self.domain = "dapr"
        self.description = "Dapr distributed runtime expert"
        self.emoji = "🔗"
        self.dapr_http_port = 3500
        self.namespace = "todo-phase5"

    def _setup_tools(self):
        """Setup Dapr MCP tools"""

        # Tool 1: Check Dapr Status
        self.register_tool(MCPTool(
            name="check_dapr_status",
            description="Check Dapr installation status on Kubernetes",
            parameters={},
            handler=self._check_dapr_status
        ))

        # Tool 2: Initialize Dapr
        self.register_tool(MCPTool(
            name="init_dapr",
            description="Initialize Dapr on Kubernetes",
            parameters={"wait": "bool (default: True)"},
            handler=self._init_dapr
        ))

        # Tool 3: List Components
        self.register_tool(MCPTool(
            name="list_components",
            description="List all Dapr components",
            parameters={"namespace": "string (optional)"},
            handler=self._list_components
        ))

        # Tool 4: Create PubSub Component
        self.register_tool(MCPTool(
            name="create_pubsub_component",
            description="Create a Dapr pub/sub component for Kafka",
            parameters={
                "name": "string (required)",
                "broker": "string (required)"
            },
            handler=self._create_pubsub_component
        ))

        # Tool 5: Create State Store
        self.register_tool(MCPTool(
            name="create_statestore",
            description="Create a Dapr state store component",
            parameters={
                "name": "string (required)",
                "connection_string": "string (required)"
            },
            handler=self._create_statestore
        ))

        # Tool 6: Create Cron Binding
        self.register_tool(MCPTool(
            name="create_cron_binding",
            description="Create a Dapr cron binding for scheduled tasks",
            parameters={
                "name": "string (required)",
                "schedule": "string (cron expression)"
            },
            handler=self._create_cron_binding
        ))

        # Tool 7: Create Secret Store
        self.register_tool(MCPTool(
            name="create_secretstore",
            description="Create a Dapr secret store component",
            parameters={"name": "string (required)"},
            handler=self._create_secretstore
        ))

        # Tool 8: Publish Message
        self.register_tool(MCPTool(
            name="publish_message",
            description="Publish a message via Dapr pub/sub",
            parameters={
                "pubsub_name": "string (required)",
                "topic": "string (required)",
                "data": "dict (required)"
            },
            handler=self._publish_message
        ))

        # Tool 9: Save State
        self.register_tool(MCPTool(
            name="save_state",
            description="Save state via Dapr state store",
            parameters={
                "store_name": "string (required)",
                "key": "string (required)",
                "value": "any (required)"
            },
            handler=self._save_state
        ))

        # Tool 10: Get State
        self.register_tool(MCPTool(
            name="get_state",
            description="Get state from Dapr state store",
            parameters={
                "store_name": "string (required)",
                "key": "string (required)"
            },
            handler=self._get_state
        ))

        # Tool 11: Invoke Service
        self.register_tool(MCPTool(
            name="invoke_service",
            description="Invoke a service via Dapr",
            parameters={
                "app_id": "string (required)",
                "method": "string (required)",
                "data": "dict (optional)"
            },
            handler=self._invoke_service
        ))

        # Tool 12: Get Secret
        self.register_tool(MCPTool(
            name="get_secret",
            description="Get secret from Dapr secret store",
            parameters={
                "store_name": "string (required)",
                "secret_name": "string (required)"
            },
            handler=self._get_secret
        ))

        # Tool 13: List Apps
        self.register_tool(MCPTool(
            name="list_dapr_apps",
            description="List all Dapr-enabled applications",
            parameters={},
            handler=self._list_apps
        ))

        # Tool 14: Get Dapr Logs
        self.register_tool(MCPTool(
            name="get_dapr_logs",
            description="Get logs from Dapr sidecar",
            parameters={"app_id": "string (required)"},
            handler=self._get_dapr_logs
        ))

        # Tool 15: Generate Annotations
        self.register_tool(MCPTool(
            name="generate_annotations",
            description="Generate Dapr annotations for Kubernetes deployment",
            parameters={
                "app_id": "string (required)",
                "app_port": "int (required)"
            },
            handler=self._generate_annotations
        ))

    def _match_tool(self, query: str) -> Optional[str]:
        """Match query to best Dapr tool"""
        query = query.lower()

        if any(w in query for w in ['status', 'check', 'health']):
            return 'check_dapr_status'
        elif any(w in query for w in ['init', 'install', 'setup']):
            return 'init_dapr'
        elif any(w in query for w in ['list component', 'show component']):
            return 'list_components'
        elif any(w in query for w in ['pubsub', 'pub/sub', 'kafka component']):
            return 'create_pubsub_component'
        elif any(w in query for w in ['state store', 'statestore']):
            return 'create_statestore'
        elif any(w in query for w in ['cron', 'schedule', 'binding']):
            return 'create_cron_binding'
        elif any(w in query for w in ['secret store', 'secretstore']):
            return 'create_secretstore'
        elif any(w in query for w in ['publish', 'send message']):
            return 'publish_message'
        elif any(w in query for w in ['save state', 'store state']):
            return 'save_state'
        elif any(w in query for w in ['get state', 'read state']):
            return 'get_state'
        elif any(w in query for w in ['invoke', 'call service']):
            return 'invoke_service'
        elif any(w in query for w in ['secret', 'get secret']):
            return 'get_secret'
        elif any(w in query for w in ['list app', 'show app', 'dapr app']):
            return 'list_dapr_apps'
        elif any(w in query for w in ['log', 'sidecar log']):
            return 'get_dapr_logs'
        elif any(w in query for w in ['annotation', 'deployment']):
            return 'generate_annotations'

        return 'check_dapr_status'

    async def execute_direct(self, step: Dict) -> Any:
        """Smart direct execution"""
        query = step.get("query", "").lower()
        tool_name = step.get("tool") or self._match_tool(query)

        if tool_name == 'check_dapr_status':
            return await self._check_dapr_status()
        elif tool_name == 'init_dapr':
            return await self._init_dapr()
        elif tool_name == 'list_components':
            return await self._list_components()
        elif tool_name == 'create_pubsub_component':
            return await self._create_pubsub_component(
                name="kafka-pubsub",
                broker="redpanda:9092"
            )
        elif tool_name == 'create_statestore':
            return await self._create_statestore(
                name="statestore",
                connection_string="postgresql://..."
            )
        elif tool_name == 'create_cron_binding':
            return await self._create_cron_binding(
                name="reminder-cron",
                schedule="*/5 * * * *"
            )
        elif tool_name == 'list_dapr_apps':
            return await self._list_apps()
        elif tool_name == 'generate_annotations':
            return await self._generate_annotations(
                app_id="todo-backend",
                app_port=8000
            )
        else:
            return await self._check_dapr_status()

    # ==================== Tool Handlers ====================

    async def _check_dapr_status(self) -> Dict:
        """Check Dapr status on Kubernetes"""
        try:
            result = subprocess.run(
                ['dapr', 'status', '-k'],
                capture_output=True, text=True, timeout=15
            )

            if result.returncode == 0:
                return {
                    "status": "installed",
                    "output": result.stdout,
                    "namespace": "dapr-system"
                }
            else:
                return {
                    "status": "not_installed",
                    "message": "Dapr not found on Kubernetes",
                    "install_command": "dapr init -k --wait"
                }
        except FileNotFoundError:
            return {
                "status": "cli_not_found",
                "message": "Dapr CLI not installed",
                "install_command": "powershell -Command \"iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex\""
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _init_dapr(self, wait: bool = True) -> Dict:
        """Initialize Dapr on Kubernetes"""
        try:
            cmd = ['dapr', 'init', '-k']
            if wait:
                cmd.append('--wait')

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout or result.stderr,
                "command": " ".join(cmd)
            }
        except Exception as e:
            return {
                "status": "info",
                "command": "dapr init -k --wait",
                "note": str(e)
            }

    async def _list_components(self, namespace: str = None) -> Dict:
        """List Dapr components"""
        namespace = namespace or self.namespace
        try:
            result = subprocess.run(
                ['kubectl', 'get', 'components', '-n', namespace, '-o', 'json'],
                capture_output=True, text=True, timeout=15
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                components = [
                    {
                        "name": item["metadata"]["name"],
                        "type": item["spec"]["type"]
                    }
                    for item in data.get("items", [])
                ]
                return {
                    "status": "success",
                    "namespace": namespace,
                    "components": components,
                    "count": len(components)
                }
            else:
                return {
                    "status": "info",
                    "command": f"kubectl get components -n {namespace}",
                    "note": result.stderr
                }
        except Exception as e:
            return {
                "status": "info",
                "command": f"kubectl get components -n {namespace}",
                "note": str(e)
            }

    async def _create_pubsub_component(self, name: str, broker: str) -> Dict:
        """Create pub/sub component YAML"""
        yaml_content = f"""apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: {name}
  namespace: {self.namespace}
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "{broker}"
  - name: consumerGroup
    value: "todo-service"
  - name: authType
    value: "none"
"""
        return {
            "status": "generated",
            "component_name": name,
            "type": "pubsub.kafka",
            "yaml": yaml_content,
            "apply_command": f"kubectl apply -f pubsub.yaml -n {self.namespace}"
        }

    async def _create_statestore(self, name: str, connection_string: str) -> Dict:
        """Create state store component YAML"""
        yaml_content = f"""apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: {name}
  namespace: {self.namespace}
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: db-secrets
      key: connection-string
"""
        return {
            "status": "generated",
            "component_name": name,
            "type": "state.postgresql",
            "yaml": yaml_content,
            "apply_command": f"kubectl apply -f statestore.yaml -n {self.namespace}"
        }

    async def _create_cron_binding(self, name: str, schedule: str) -> Dict:
        """Create cron binding component YAML"""
        yaml_content = f"""apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: {name}
  namespace: {self.namespace}
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "{schedule}"
"""
        return {
            "status": "generated",
            "component_name": name,
            "type": "bindings.cron",
            "schedule": schedule,
            "yaml": yaml_content,
            "apply_command": f"kubectl apply -f cron-binding.yaml -n {self.namespace}",
            "note": "Your app needs a POST endpoint matching the binding name"
        }

    async def _create_secretstore(self, name: str) -> Dict:
        """Create secret store component YAML"""
        yaml_content = f"""apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: {name}
  namespace: {self.namespace}
spec:
  type: secretstores.kubernetes
  version: v1
"""
        return {
            "status": "generated",
            "component_name": name,
            "type": "secretstores.kubernetes",
            "yaml": yaml_content,
            "apply_command": f"kubectl apply -f secretstore.yaml -n {self.namespace}"
        }

    async def _publish_message(self, pubsub_name: str, topic: str, data: Dict) -> Dict:
        """Generate publish message code"""
        return {
            "status": "code_generated",
            "endpoint": f"http://localhost:{self.dapr_http_port}/v1.0/publish/{pubsub_name}/{topic}",
            "method": "POST",
            "body": data,
            "python_code": f"""
import httpx

async def publish_event():
    await httpx.post(
        "http://localhost:{self.dapr_http_port}/v1.0/publish/{pubsub_name}/{topic}",
        json={json.dumps(data)}
    )
""",
            "curl_command": f"curl -X POST http://localhost:{self.dapr_http_port}/v1.0/publish/{pubsub_name}/{topic} -H 'Content-Type: application/json' -d '{json.dumps(data)}'"
        }

    async def _save_state(self, store_name: str, key: str, value: Any) -> Dict:
        """Generate save state code"""
        return {
            "status": "code_generated",
            "endpoint": f"http://localhost:{self.dapr_http_port}/v1.0/state/{store_name}",
            "method": "POST",
            "body": [{"key": key, "value": value}],
            "python_code": f"""
import httpx

async def save_state():
    await httpx.post(
        "http://localhost:{self.dapr_http_port}/v1.0/state/{store_name}",
        json=[{{"key": "{key}", "value": {json.dumps(value)}}}]
    )
"""
        }

    async def _get_state(self, store_name: str, key: str) -> Dict:
        """Generate get state code"""
        return {
            "status": "code_generated",
            "endpoint": f"http://localhost:{self.dapr_http_port}/v1.0/state/{store_name}/{key}",
            "method": "GET",
            "python_code": f"""
import httpx

async def get_state():
    response = await httpx.get(
        "http://localhost:{self.dapr_http_port}/v1.0/state/{store_name}/{key}"
    )
    return response.json()
"""
        }

    async def _invoke_service(self, app_id: str, method: str, data: Dict = None) -> Dict:
        """Generate service invocation code"""
        return {
            "status": "code_generated",
            "endpoint": f"http://localhost:{self.dapr_http_port}/v1.0/invoke/{app_id}/method/{method}",
            "python_code": f"""
import httpx

async def invoke_service():
    response = await httpx.post(
        "http://localhost:{self.dapr_http_port}/v1.0/invoke/{app_id}/method/{method}",
        json={json.dumps(data) if data else "{}"}
    )
    return response.json()
"""
        }

    async def _get_secret(self, store_name: str, secret_name: str) -> Dict:
        """Generate get secret code"""
        return {
            "status": "code_generated",
            "endpoint": f"http://localhost:{self.dapr_http_port}/v1.0/secrets/{store_name}/{secret_name}",
            "python_code": f"""
import httpx

async def get_secret():
    response = await httpx.get(
        "http://localhost:{self.dapr_http_port}/v1.0/secrets/{store_name}/{secret_name}"
    )
    return response.json()
"""
        }

    async def _list_apps(self) -> Dict:
        """List Dapr-enabled apps"""
        try:
            result = subprocess.run(
                ['dapr', 'list', '-k'],
                capture_output=True, text=True, timeout=15
            )

            return {
                "status": "success" if result.returncode == 0 else "info",
                "output": result.stdout,
                "command": "dapr list -k"
            }
        except Exception as e:
            return {
                "status": "info",
                "command": "dapr list -k",
                "note": str(e)
            }

    async def _get_dapr_logs(self, app_id: str) -> Dict:
        """Get Dapr sidecar logs"""
        return {
            "status": "info",
            "command": f"kubectl logs -l app={app_id} -c daprd -n {self.namespace}",
            "note": "Run this command to see Dapr sidecar logs"
        }

    async def _generate_annotations(self, app_id: str, app_port: int) -> Dict:
        """Generate Dapr annotations for deployment"""
        annotations = {
            "dapr.io/enabled": "true",
            "dapr.io/app-id": app_id,
            "dapr.io/app-port": str(app_port),
            "dapr.io/enable-api-logging": "true"
        }

        yaml_snippet = f"""metadata:
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "{app_id}"
    dapr.io/app-port: "{app_port}"
    dapr.io/enable-api-logging: "true"
"""

        return {
            "status": "generated",
            "annotations": annotations,
            "yaml_snippet": yaml_snippet,
            "note": "Add these annotations to your Kubernetes deployment spec.template.metadata"
        }
