"""
Helm Agent - Helm Charts Expert
Handles Helm chart operations for Phase-5

@author: Phase-5 AI Employs System
"""

import asyncio
import subprocess
from typing import Dict, List, Any, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class HelmAgent(BaseAgent):
    """
    Helm Charts Expert Agent

    Capabilities:
    - Install/upgrade Helm charts
    - Manage releases
    - Template generation
    - Values management
    - Repository management

    MCP Tools: 12
    """

    def __init__(self):
        super().__init__()
        self.name = "HelmAgent"
        self.domain = "helm"
        self.description = "Helm chart deployment expert"
        self.emoji = "⎈"
        self.namespace = "todo-phase5"

    def _setup_tools(self):
        """Setup Helm MCP tools"""

        # Tool 1: Install Chart
        self.register_tool(MCPTool(
            name="helm_install",
            description="Install a Helm chart",
            parameters={
                "release_name": "string (required)",
                "chart": "string (required)",
                "namespace": "string (optional)",
                "values_file": "string (optional)",
                "set_values": "dict (optional)"
            },
            handler=self._helm_install
        ))

        # Tool 2: Upgrade Release
        self.register_tool(MCPTool(
            name="helm_upgrade",
            description="Upgrade a Helm release",
            parameters={
                "release_name": "string (required)",
                "chart": "string (required)",
                "namespace": "string (optional)",
                "values_file": "string (optional)"
            },
            handler=self._helm_upgrade
        ))

        # Tool 3: Uninstall Release
        self.register_tool(MCPTool(
            name="helm_uninstall",
            description="Uninstall a Helm release",
            parameters={
                "release_name": "string (required)",
                "namespace": "string (optional)"
            },
            handler=self._helm_uninstall
        ))

        # Tool 4: List Releases
        self.register_tool(MCPTool(
            name="helm_list",
            description="List Helm releases",
            parameters={"namespace": "string (optional)"},
            handler=self._helm_list
        ))

        # Tool 5: Get Release Status
        self.register_tool(MCPTool(
            name="helm_status",
            description="Get status of a release",
            parameters={
                "release_name": "string (required)",
                "namespace": "string (optional)"
            },
            handler=self._helm_status
        ))

        # Tool 6: Template Chart
        self.register_tool(MCPTool(
            name="helm_template",
            description="Render chart templates locally",
            parameters={
                "release_name": "string (required)",
                "chart": "string (required)",
                "values_file": "string (optional)"
            },
            handler=self._helm_template
        ))

        # Tool 7: Add Repository
        self.register_tool(MCPTool(
            name="helm_repo_add",
            description="Add a Helm chart repository",
            parameters={
                "repo_name": "string (required)",
                "repo_url": "string (required)"
            },
            handler=self._helm_repo_add
        ))

        # Tool 8: Update Repositories
        self.register_tool(MCPTool(
            name="helm_repo_update",
            description="Update Helm chart repositories",
            parameters={},
            handler=self._helm_repo_update
        ))

        # Tool 9: Search Charts
        self.register_tool(MCPTool(
            name="helm_search",
            description="Search for Helm charts",
            parameters={"keyword": "string (required)"},
            handler=self._helm_search
        ))

        # Tool 10: Get Values
        self.register_tool(MCPTool(
            name="helm_get_values",
            description="Get values of a release",
            parameters={
                "release_name": "string (required)",
                "namespace": "string (optional)"
            },
            handler=self._helm_get_values
        ))

        # Tool 11: Rollback Release
        self.register_tool(MCPTool(
            name="helm_rollback",
            description="Rollback a release to previous version",
            parameters={
                "release_name": "string (required)",
                "revision": "int (optional)",
                "namespace": "string (optional)"
            },
            handler=self._helm_rollback
        ))

        # Tool 12: Get Release History
        self.register_tool(MCPTool(
            name="helm_history",
            description="Get release history",
            parameters={
                "release_name": "string (required)",
                "namespace": "string (optional)"
            },
            handler=self._helm_history
        ))

    def _match_tool(self, query: str) -> Optional[str]:
        """Match query to best Helm tool"""
        query = query.lower()

        if any(w in query for w in ['install', 'helm install']):
            return 'helm_install'
        elif any(w in query for w in ['upgrade']):
            return 'helm_upgrade'
        elif any(w in query for w in ['uninstall', 'delete release']):
            return 'helm_uninstall'
        elif any(w in query for w in ['list', 'releases']):
            return 'helm_list'
        elif any(w in query for w in ['status']):
            return 'helm_status'
        elif any(w in query for w in ['template', 'render']):
            return 'helm_template'
        elif any(w in query for w in ['add repo', 'repo add']):
            return 'helm_repo_add'
        elif any(w in query for w in ['update repo', 'repo update']):
            return 'helm_repo_update'
        elif any(w in query for w in ['search']):
            return 'helm_search'
        elif any(w in query for w in ['values', 'get values']):
            return 'helm_get_values'
        elif any(w in query for w in ['rollback']):
            return 'helm_rollback'
        elif any(w in query for w in ['history']):
            return 'helm_history'

        return 'helm_list'

    async def execute_direct(self, step: Dict) -> Any:
        """Smart direct execution"""
        query = step.get("query", "").lower()
        tool_name = step.get("tool") or self._match_tool(query)

        if tool_name == 'helm_install':
            return await self._helm_install(
                release_name="todo-backend",
                chart="./helm-charts/todo-backend"
            )

        elif tool_name == 'helm_upgrade':
            return await self._helm_upgrade(
                release_name="todo-backend",
                chart="./helm-charts/todo-backend"
            )

        elif tool_name == 'helm_list':
            return await self._helm_list()

        elif tool_name == 'helm_status':
            return await self._helm_status(release_name="todo-backend")

        else:
            return await self._helm_list()

    def _run_helm(self, args: List[str], timeout: int = 60) -> Dict:
        """Run helm command"""
        try:
            result = subprocess.run(
                ['helm'] + args,
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
                "error": "helm not found",
                "command": f"helm {' '.join(args)}"
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ==================== Tool Handlers ====================

    async def _helm_install(self, release_name: str, chart: str,
                           namespace: str = None, values_file: str = None,
                           set_values: Dict = None) -> Dict:
        """Install Helm chart"""
        ns = namespace or self.namespace
        args = ['install', release_name, chart, '-n', ns, '--create-namespace']

        if values_file:
            args.extend(['-f', values_file])

        if set_values:
            for k, v in set_values.items():
                args.extend(['--set', f"{k}={v}"])

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "release": release_name,
            "chart": chart,
            "namespace": ns,
            "output": result.get("output"),
            "command": f"helm install {release_name} {chart} -n {ns}"
        }

    async def _helm_upgrade(self, release_name: str, chart: str,
                           namespace: str = None,
                           values_file: str = None) -> Dict:
        """Upgrade Helm release"""
        ns = namespace or self.namespace
        args = ['upgrade', release_name, chart, '-n', ns, '--install']

        if values_file:
            args.extend(['-f', values_file])

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "release": release_name,
            "chart": chart,
            "namespace": ns,
            "output": result.get("output"),
            "command": f"helm upgrade {release_name} {chart} -n {ns} --install"
        }

    async def _helm_uninstall(self, release_name: str,
                             namespace: str = None) -> Dict:
        """Uninstall Helm release"""
        ns = namespace or self.namespace
        args = ['uninstall', release_name, '-n', ns]

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "release": release_name,
            "namespace": ns,
            "action": "uninstalled",
            "command": f"helm uninstall {release_name} -n {ns}"
        }

    async def _helm_list(self, namespace: str = None) -> Dict:
        """List Helm releases"""
        ns = namespace or self.namespace
        args = ['list', '-n', ns]

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "namespace": ns,
            "output": result.get("output"),
            "command": f"helm list -n {ns}"
        }

    async def _helm_status(self, release_name: str,
                          namespace: str = None) -> Dict:
        """Get release status"""
        ns = namespace or self.namespace
        args = ['status', release_name, '-n', ns]

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "release": release_name,
            "namespace": ns,
            "output": result.get("output"),
            "command": f"helm status {release_name} -n {ns}"
        }

    async def _helm_template(self, release_name: str, chart: str,
                            values_file: str = None) -> Dict:
        """Template chart"""
        args = ['template', release_name, chart]

        if values_file:
            args.extend(['-f', values_file])

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "release": release_name,
            "chart": chart,
            "output": result.get("output"),
            "command": f"helm template {release_name} {chart}"
        }

    async def _helm_repo_add(self, repo_name: str, repo_url: str) -> Dict:
        """Add Helm repository"""
        args = ['repo', 'add', repo_name, repo_url]

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "repository": repo_name,
            "url": repo_url,
            "output": result.get("output"),
            "command": f"helm repo add {repo_name} {repo_url}"
        }

    async def _helm_repo_update(self) -> Dict:
        """Update repositories"""
        args = ['repo', 'update']

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "action": "repositories_updated",
            "output": result.get("output"),
            "command": "helm repo update"
        }

    async def _helm_search(self, keyword: str) -> Dict:
        """Search for charts"""
        args = ['search', 'hub', keyword]

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "keyword": keyword,
            "output": result.get("output"),
            "command": f"helm search hub {keyword}"
        }

    async def _helm_get_values(self, release_name: str,
                              namespace: str = None) -> Dict:
        """Get release values"""
        ns = namespace or self.namespace
        args = ['get', 'values', release_name, '-n', ns]

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "release": release_name,
            "namespace": ns,
            "output": result.get("output"),
            "command": f"helm get values {release_name} -n {ns}"
        }

    async def _helm_rollback(self, release_name: str, revision: int = None,
                            namespace: str = None) -> Dict:
        """Rollback release"""
        ns = namespace or self.namespace
        args = ['rollback', release_name]

        if revision:
            args.append(str(revision))

        args.extend(['-n', ns])

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "release": release_name,
            "revision": revision or "previous",
            "namespace": ns,
            "command": f"helm rollback {release_name} {revision or ''} -n {ns}"
        }

    async def _helm_history(self, release_name: str,
                           namespace: str = None) -> Dict:
        """Get release history"""
        ns = namespace or self.namespace
        args = ['history', release_name, '-n', ns]

        result = self._run_helm(args)
        return {
            "status": "success" if result.get("success") else "info",
            "release": release_name,
            "namespace": ns,
            "output": result.get("output"),
            "command": f"helm history {release_name} -n {ns}"
        }
