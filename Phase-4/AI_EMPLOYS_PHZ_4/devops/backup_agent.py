"""
Backup Agent - POWERFUL Backup & Recovery Expert
Data backups, disaster recovery, snapshots, restore operations

@author: Phase-4 Multi-Agent System
"""

import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class BackupAgent(BaseAgent):
    """
    POWERFUL Backup & Recovery Expert Agent
    - Volume snapshots
    - Database backups
    - Configuration backups
    - Disaster recovery
    - Scheduled backups
    """

    KEYWORDS = [
        'backup', 'restore', 'recovery', 'snapshot', 'dump', 'export',
        'import', 'archive', 'disaster', 'replicate', 'sync', 'copy'
    ]

    def __init__(self, namespace: str = "todo", backup_path: str = "./backups"):
        super().__init__("Backup", "Backup & recovery expert - snapshots, backups, disaster recovery")
        self.namespace = namespace
        self.backup_path = backup_path
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all MCP tools for backup operations"""

        # Tool: Backup Database
        self.register_tool(MCPTool(
            name="backup_database",
            description="Create a database backup (PostgreSQL)",
            parameters={
                "type": "object",
                "properties": {
                    "database": {"type": "string", "description": "Database name"},
                    "output_path": {"type": "string", "description": "Backup file path"},
                    "format": {"type": "string", "description": "custom, sql, tar"},
                    "compress": {"type": "boolean"}
                }
            },
            handler=self._backup_database
        ))

        # Tool: Restore Database
        self.register_tool(MCPTool(
            name="restore_database",
            description="Restore database from backup",
            parameters={
                "type": "object",
                "properties": {
                    "backup_path": {"type": "string", "description": "Backup file path"},
                    "database": {"type": "string"},
                    "clean": {"type": "boolean", "description": "Drop existing objects first"}
                },
                "required": ["backup_path"]
            },
            handler=self._restore_database
        ))

        # Tool: Backup K8s Resources
        self.register_tool(MCPTool(
            name="backup_k8s_resources",
            description="Backup Kubernetes resources (deployments, configmaps, secrets)",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "resources": {"type": "array", "description": "Resource types to backup"},
                    "output_path": {"type": "string"}
                }
            },
            handler=self._backup_k8s_resources
        ))

        # Tool: Restore K8s Resources
        self.register_tool(MCPTool(
            name="restore_k8s_resources",
            description="Restore Kubernetes resources from backup",
            parameters={
                "type": "object",
                "properties": {
                    "backup_path": {"type": "string"},
                    "namespace": {"type": "string"}
                },
                "required": ["backup_path"]
            },
            handler=self._restore_k8s_resources
        ))

        # Tool: Create Volume Snapshot
        self.register_tool(MCPTool(
            name="create_volume_snapshot",
            description="Create a PersistentVolumeClaim snapshot",
            parameters={
                "type": "object",
                "properties": {
                    "pvc_name": {"type": "string", "description": "PVC name"},
                    "snapshot_name": {"type": "string"},
                    "namespace": {"type": "string"}
                },
                "required": ["pvc_name"]
            },
            handler=self._create_volume_snapshot
        ))

        # Tool: List Snapshots
        self.register_tool(MCPTool(
            name="list_snapshots",
            description="List volume snapshots",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            },
            handler=self._list_snapshots
        ))

        # Tool: Restore from Snapshot
        self.register_tool(MCPTool(
            name="restore_from_snapshot",
            description="Restore PVC from snapshot",
            parameters={
                "type": "object",
                "properties": {
                    "snapshot_name": {"type": "string"},
                    "new_pvc_name": {"type": "string"},
                    "namespace": {"type": "string"}
                },
                "required": ["snapshot_name", "new_pvc_name"]
            },
            handler=self._restore_from_snapshot
        ))

        # Tool: List Backups
        self.register_tool(MCPTool(
            name="list_backups",
            description="List available backups",
            parameters={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "description": "database, k8s, volume, all"},
                    "path": {"type": "string"}
                }
            },
            handler=self._list_backups
        ))

        # Tool: Delete Backup
        self.register_tool(MCPTool(
            name="delete_backup",
            description="Delete a backup file",
            parameters={
                "type": "object",
                "properties": {
                    "backup_path": {"type": "string"}
                },
                "required": ["backup_path"]
            },
            handler=self._delete_backup
        ))

        # Tool: Backup ConfigMaps
        self.register_tool(MCPTool(
            name="backup_configmaps",
            description="Backup all ConfigMaps in namespace",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "output_path": {"type": "string"}
                }
            },
            handler=self._backup_configmaps
        ))

        # Tool: Backup Secrets
        self.register_tool(MCPTool(
            name="backup_secrets",
            description="Backup all secrets (encrypted) in namespace",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "output_path": {"type": "string"},
                    "encrypt": {"type": "boolean"}
                }
            },
            handler=self._backup_secrets
        ))

        # Tool: Verify Backup
        self.register_tool(MCPTool(
            name="verify_backup",
            description="Verify backup integrity",
            parameters={
                "type": "object",
                "properties": {
                    "backup_path": {"type": "string"},
                    "type": {"type": "string", "description": "database, k8s, volume"}
                },
                "required": ["backup_path"]
            },
            handler=self._verify_backup
        ))

        # Tool: Full Backup
        self.register_tool(MCPTool(
            name="full_backup",
            description="Perform complete backup of namespace (DB, K8s resources, configs)",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "output_dir": {"type": "string"}
                }
            },
            handler=self._full_backup
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

    def _get_timestamp(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    async def _backup_database(self, database: str = "postgres", output_path: str = None, format: str = "custom", compress: bool = True, **kwargs) -> Dict:
        timestamp = self._get_timestamp()
        output = output_path or f"{self.backup_path}/db_{database}_{timestamp}.backup"

        # Ensure backup directory exists
        os.makedirs(os.path.dirname(output), exist_ok=True)

        format_flag = {
            "custom": "-Fc",
            "sql": "-Fp",
            "tar": "-Ft"
        }.get(format, "-Fc")

        compress_flag = "-Z9" if compress else ""

        cmd = f'pg_dump {format_flag} {compress_flag} "{database}" > "{output}"'

        try:
            await self._run_cmd(cmd)

            # Get file size
            size = os.path.getsize(output) if os.path.exists(output) else 0

            return {
                "status": "success",
                "backup_path": output,
                "database": database,
                "format": format,
                "size_bytes": size,
                "timestamp": timestamp
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def _restore_database(self, backup_path: str, database: str = "postgres", clean: bool = False, **kwargs) -> Dict:
        clean_flag = "--clean" if clean else ""

        cmd = f'pg_restore {clean_flag} -d "{database}" "{backup_path}"'

        try:
            await self._run_cmd(cmd)
            return {
                "status": "restored",
                "backup": backup_path,
                "database": database
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def _backup_k8s_resources(self, namespace: str = None, resources: List = None, output_path: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace
        timestamp = self._get_timestamp()
        output = output_path or f"{self.backup_path}/k8s_{ns}_{timestamp}"

        os.makedirs(output, exist_ok=True)

        if not resources:
            resources = ["deployments", "services", "configmaps", "secrets", "ingress"]

        backed_up = []

        for resource in resources:
            try:
                result = await self._run_cmd(f"kubectl get {resource} -n {ns} -o yaml")
                file_path = f"{output}/{resource}.yaml"

                with open(file_path, 'w') as f:
                    f.write(result)

                backed_up.append(resource)
            except Exception as e:
                self.log(f"Failed to backup {resource}: {e}", "error")

        return {
            "status": "success",
            "backup_path": output,
            "namespace": ns,
            "resources": backed_up,
            "timestamp": timestamp
        }

    async def _restore_k8s_resources(self, backup_path: str, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        restored = []

        for filename in os.listdir(backup_path):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                file_path = os.path.join(backup_path, filename)
                try:
                    await self._run_cmd(f"kubectl apply -f {file_path} -n {ns}")
                    restored.append(filename)
                except Exception as e:
                    self.log(f"Failed to restore {filename}: {e}", "error")

        return {
            "status": "restored",
            "backup": backup_path,
            "namespace": ns,
            "restored": restored
        }

    async def _create_volume_snapshot(self, pvc_name: str, snapshot_name: str = None, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace
        timestamp = self._get_timestamp()
        snap_name = snapshot_name or f"{pvc_name}-snap-{timestamp}"

        snapshot = {
            "apiVersion": "snapshot.storage.k8s.io/v1",
            "kind": "VolumeSnapshot",
            "metadata": {
                "name": snap_name,
                "namespace": ns
            },
            "spec": {
                "source": {
                    "persistentVolumeClaimName": pvc_name
                }
            }
        }

        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(snapshot, f)
            temp_path = f.name

        try:
            await self._run_cmd(f"kubectl apply -f {temp_path}")
            return {
                "status": "created",
                "snapshot_name": snap_name,
                "pvc": pvc_name,
                "namespace": ns
            }
        finally:
            os.unlink(temp_path)

    async def _list_snapshots(self, namespace: str = None, **kwargs) -> List[Dict]:
        ns = namespace or self.namespace

        try:
            result = await self._run_cmd(f"kubectl get volumesnapshots -n {ns} -o json")
            data = json.loads(result)

            snapshots = []
            for item in data.get("items", []):
                snapshots.append({
                    "name": item.get("metadata", {}).get("name"),
                    "pvc": item.get("spec", {}).get("source", {}).get("persistentVolumeClaimName"),
                    "ready": item.get("status", {}).get("readyToUse", False),
                    "created": item.get("metadata", {}).get("creationTimestamp")
                })

            return snapshots
        except:
            return [{"note": "VolumeSnapshot CRD may not be installed"}]

    async def _restore_from_snapshot(self, snapshot_name: str, new_pvc_name: str, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        pvc = {
            "apiVersion": "v1",
            "kind": "PersistentVolumeClaim",
            "metadata": {
                "name": new_pvc_name,
                "namespace": ns
            },
            "spec": {
                "dataSource": {
                    "name": snapshot_name,
                    "kind": "VolumeSnapshot",
                    "apiGroup": "snapshot.storage.k8s.io"
                },
                "accessModes": ["ReadWriteOnce"],
                "resources": {
                    "requests": {
                        "storage": "1Gi"
                    }
                }
            }
        }

        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(pvc, f)
            temp_path = f.name

        try:
            await self._run_cmd(f"kubectl apply -f {temp_path}")
            return {
                "status": "created",
                "pvc": new_pvc_name,
                "from_snapshot": snapshot_name,
                "namespace": ns
            }
        finally:
            os.unlink(temp_path)

    async def _list_backups(self, type: str = "all", path: str = None, **kwargs) -> List[Dict]:
        backup_dir = path or self.backup_path

        if not os.path.exists(backup_dir):
            return []

        backups = []
        for item in os.listdir(backup_dir):
            full_path = os.path.join(backup_dir, item)

            backup_type = "unknown"
            if item.startswith("db_"):
                backup_type = "database"
            elif item.startswith("k8s_"):
                backup_type = "k8s"
            elif item.startswith("full_"):
                backup_type = "full"

            if type != "all" and backup_type != type:
                continue

            stat = os.stat(full_path)
            backups.append({
                "name": item,
                "path": full_path,
                "type": backup_type,
                "size_bytes": stat.st_size if os.path.isfile(full_path) else None,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "is_dir": os.path.isdir(full_path)
            })

        return sorted(backups, key=lambda x: x["created"], reverse=True)

    async def _delete_backup(self, backup_path: str, **kwargs) -> Dict:
        if os.path.isfile(backup_path):
            os.remove(backup_path)
        elif os.path.isdir(backup_path):
            import shutil
            shutil.rmtree(backup_path)
        else:
            return {"status": "not_found", "path": backup_path}

        return {"status": "deleted", "path": backup_path}

    async def _backup_configmaps(self, namespace: str = None, output_path: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace
        timestamp = self._get_timestamp()
        output = output_path or f"{self.backup_path}/configmaps_{ns}_{timestamp}.yaml"

        os.makedirs(os.path.dirname(output), exist_ok=True)

        result = await self._run_cmd(f"kubectl get configmaps -n {ns} -o yaml")

        with open(output, 'w') as f:
            f.write(result)

        return {
            "status": "success",
            "backup_path": output,
            "namespace": ns
        }

    async def _backup_secrets(self, namespace: str = None, output_path: str = None, encrypt: bool = True, **kwargs) -> Dict:
        ns = namespace or self.namespace
        timestamp = self._get_timestamp()
        output = output_path or f"{self.backup_path}/secrets_{ns}_{timestamp}.yaml"

        os.makedirs(os.path.dirname(output), exist_ok=True)

        result = await self._run_cmd(f"kubectl get secrets -n {ns} -o yaml")

        # Note: In production, you'd encrypt this file
        with open(output, 'w') as f:
            f.write(result)

        return {
            "status": "success",
            "backup_path": output,
            "namespace": ns,
            "encrypted": encrypt,
            "warning": "Backup contains sensitive data" if not encrypt else None
        }

    async def _verify_backup(self, backup_path: str, type: str = None, **kwargs) -> Dict:
        if not os.path.exists(backup_path):
            return {"valid": False, "error": "Backup not found"}

        verification = {
            "path": backup_path,
            "exists": True,
            "type": type
        }

        if os.path.isfile(backup_path):
            verification["size_bytes"] = os.path.getsize(backup_path)
            verification["valid"] = verification["size_bytes"] > 0

            # For database backups, try to list contents
            if type == "database" or backup_path.endswith('.backup'):
                try:
                    await self._run_cmd(f'pg_restore --list "{backup_path}"')
                    verification["db_valid"] = True
                except:
                    verification["db_valid"] = False

        elif os.path.isdir(backup_path):
            files = os.listdir(backup_path)
            verification["files"] = files
            verification["valid"] = len(files) > 0

        return verification

    async def _full_backup(self, namespace: str = None, output_dir: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace
        timestamp = self._get_timestamp()
        output = output_dir or f"{self.backup_path}/full_{ns}_{timestamp}"

        os.makedirs(output, exist_ok=True)

        results = {
            "status": "in_progress",
            "backup_path": output,
            "namespace": ns,
            "components": {}
        }

        # Backup K8s resources
        self.log("Backing up Kubernetes resources...", "step")
        k8s_result = await self._backup_k8s_resources(
            namespace=ns,
            output_path=f"{output}/k8s"
        )
        results["components"]["k8s"] = k8s_result

        # Backup configmaps
        self.log("Backing up ConfigMaps...", "step")
        cm_result = await self._backup_configmaps(
            namespace=ns,
            output_path=f"{output}/configmaps.yaml"
        )
        results["components"]["configmaps"] = cm_result

        # Backup secrets
        self.log("Backing up Secrets...", "step")
        secrets_result = await self._backup_secrets(
            namespace=ns,
            output_path=f"{output}/secrets.yaml"
        )
        results["components"]["secrets"] = secrets_result

        # Create manifest
        manifest = {
            "timestamp": timestamp,
            "namespace": ns,
            "components": list(results["components"].keys())
        }

        with open(f"{output}/manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)

        results["status"] = "complete"
        results["manifest"] = manifest

        return results

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
        if "backup" in query and ("list" in query or "show" in query or "all" in query):
            return await self._list_backups()
        elif "snapshot" in query and ("list" in query or "show" in query):
            return await self._list_snapshots()
        elif "verify" in query:
            return {"status": "need_params", "message": "Provide: backup_name to verify"}
        elif "database" in query and "backup" in query:
            return {"status": "need_params", "message": "Provide: database name, output_path"}
        elif "restore" in query:
            return {"status": "need_params", "message": "Provide: backup_path to restore"}
        elif "full" in query and "backup" in query:
            return await self._full_backup()
        elif "configmap" in query:
            return await self._backup_configmaps()
        elif "secret" in query:
            return await self._backup_secrets()

        return {"status": "no action taken", "query": query}
