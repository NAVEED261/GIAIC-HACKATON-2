"""
Helm Agent - Kubernetes Package Management Expert
Handles Helm charts, releases, upgrades

@author: Phase-4 Multi-Agent System
"""

import asyncio
from typing import Dict, Any, List
import sys
sys.path.append('..')
from base_agent import BaseAgent


class HelmAgent(BaseAgent):
    """
    Helm Expert Agent
    Handles: charts, releases, upgrades, rollbacks
    """

    KEYWORDS = [
        'helm', 'chart', 'release', 'upgrade', 'install',
        'uninstall', 'rollback', 'values', 'template'
    ]

    def __init__(self):
        super().__init__("Helm", "Kubernetes package management expert")
        self.namespace = "todo"

    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in self.KEYWORDS)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_str = task.get("task", "")
        params = task.get("params", {})

        self.start_work(task_str)

        try:
            if "list" in task_str.lower() or "releases" in task_str.lower():
                result = await self.list_releases(params)
            elif "install" in task_str.lower():
                result = await self.install_chart(params)
            elif "upgrade" in task_str.lower():
                result = await self.upgrade_release(params)
            elif "uninstall" in task_str.lower() or "delete" in task_str.lower():
                result = await self.uninstall_release(params)
            elif "rollback" in task_str.lower():
                result = await self.rollback_release(params)
            elif "status" in task_str.lower():
                result = await self.release_status(params)
            elif "values" in task_str.lower():
                result = await self.get_values(params)
            else:
                result = await self.run_helm(task_str)

            self.end_work("Task completed")
            return {"success": True, "data": result}

        except Exception as e:
            self.report_error(str(e))
            return {"success": False, "error": str(e)}

    async def run_helm(self, cmd: str) -> str:
        if not cmd.startswith("helm"):
            cmd = f"helm {cmd}"

        self.log(f"Executing: {cmd}", "working")
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(stderr.decode())

        return stdout.decode()

    async def list_releases(self, params: Dict) -> List[Dict]:
        ns = params.get("namespace", self.namespace)
        self.log(f"Listing releases in {ns}", "working")

        result = await self.run_helm(f"helm list -n {ns} --output json")
        import json
        return json.loads(result) if result.strip() else []

    async def install_chart(self, params: Dict) -> str:
        name = params.get("name", "")
        chart = params.get("chart", "")
        ns = params.get("namespace", self.namespace)
        values = params.get("values", "")

        self.log(f"Installing {name} from {chart}", "working")

        cmd = f"helm install {name} {chart} -n {ns}"
        if values:
            cmd += f" -f {values}"

        return await self.run_helm(cmd)

    async def upgrade_release(self, params: Dict) -> str:
        name = params.get("name", "")
        chart = params.get("chart", "")
        ns = params.get("namespace", self.namespace)

        self.log(f"Upgrading {name}", "working")
        return await self.run_helm(f"helm upgrade {name} {chart} -n {ns}")

    async def uninstall_release(self, params: Dict) -> str:
        name = params.get("name", "")
        ns = params.get("namespace", self.namespace)

        self.log(f"Uninstalling {name}", "working")
        return await self.run_helm(f"helm uninstall {name} -n {ns}")

    async def rollback_release(self, params: Dict) -> str:
        name = params.get("name", "")
        revision = params.get("revision", 1)
        ns = params.get("namespace", self.namespace)

        self.log(f"Rolling back {name} to revision {revision}", "working")
        return await self.run_helm(f"helm rollback {name} {revision} -n {ns}")

    async def release_status(self, params: Dict) -> str:
        name = params.get("name", "")
        ns = params.get("namespace", self.namespace)

        self.log(f"Getting status: {name}", "working")
        return await self.run_helm(f"helm status {name} -n {ns}")

    async def get_values(self, params: Dict) -> str:
        name = params.get("name", "")
        ns = params.get("namespace", self.namespace)

        self.log(f"Getting values: {name}", "working")
        return await self.run_helm(f"helm get values {name} -n {ns}")
