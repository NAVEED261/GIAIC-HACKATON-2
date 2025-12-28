"""
Docker Agent - POWERFUL Container Management Expert with MCP Tools
Self-reasoning, multi-step execution, comprehensive Docker operations

@author: Phase-4 Multi-Agent System
"""

import asyncio
import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class DockerAgent(BaseAgent):
    """
    POWERFUL Docker Expert Agent
    - Self-reasoning for complex queries
    - MCP Tools for all Docker operations
    - Multi-step execution
    - Error recovery
    """

    KEYWORDS = [
        'docker', 'build', 'image', 'container', 'dockerfile',
        'compose', 'push', 'pull', 'run', 'stop', 'logs',
        'registry', 'tag', 'volume', 'network', 'prune'
    ]

    def __init__(self):
        super().__init__("Docker", "Container management expert - builds, images, containers, compose")
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all MCP tools for Docker operations"""

        # Tool: List Containers
        self.register_tool(MCPTool(
            name="list_containers",
            description="List all Docker containers with status",
            parameters={
                "type": "object",
                "properties": {
                    "all": {"type": "boolean", "description": "Include stopped containers"},
                    "filter": {"type": "string", "description": "Filter by name or status"}
                }
            },
            handler=self._list_containers
        ))

        # Tool: List Images
        self.register_tool(MCPTool(
            name="list_images",
            description="List Docker images with size and tags",
            parameters={
                "type": "object",
                "properties": {
                    "filter": {"type": "string", "description": "Filter by repository name"}
                }
            },
            handler=self._list_images
        ))

        # Tool: Build Image
        self.register_tool(MCPTool(
            name="build_image",
            description="Build a Docker image from Dockerfile",
            parameters={
                "type": "object",
                "properties": {
                    "tag": {"type": "string", "description": "Image tag (name:version)"},
                    "dockerfile": {"type": "string", "description": "Dockerfile path"},
                    "context": {"type": "string", "description": "Build context path"},
                    "build_args": {"type": "object", "description": "Build arguments"},
                    "no_cache": {"type": "boolean", "description": "Build without cache"}
                },
                "required": ["tag"]
            },
            handler=self._build_image
        ))

        # Tool: Run Container
        self.register_tool(MCPTool(
            name="run_container",
            description="Run a new container from an image",
            parameters={
                "type": "object",
                "properties": {
                    "image": {"type": "string", "description": "Image name:tag"},
                    "name": {"type": "string", "description": "Container name"},
                    "ports": {"type": "string", "description": "Port mapping (8080:80)"},
                    "volumes": {"type": "string", "description": "Volume mapping"},
                    "env": {"type": "object", "description": "Environment variables"},
                    "detach": {"type": "boolean", "description": "Run in background"}
                },
                "required": ["image"]
            },
            handler=self._run_container
        ))

        # Tool: Stop Container
        self.register_tool(MCPTool(
            name="stop_container",
            description="Stop a running container",
            parameters={
                "type": "object",
                "properties": {
                    "container": {"type": "string", "description": "Container name or ID"},
                    "timeout": {"type": "integer", "description": "Timeout before force kill"}
                },
                "required": ["container"]
            },
            handler=self._stop_container
        ))

        # Tool: Remove Container
        self.register_tool(MCPTool(
            name="remove_container",
            description="Remove a container",
            parameters={
                "type": "object",
                "properties": {
                    "container": {"type": "string", "description": "Container name or ID"},
                    "force": {"type": "boolean", "description": "Force remove running container"}
                },
                "required": ["container"]
            },
            handler=self._remove_container
        ))

        # Tool: Get Logs
        self.register_tool(MCPTool(
            name="get_container_logs",
            description="Get container logs",
            parameters={
                "type": "object",
                "properties": {
                    "container": {"type": "string", "description": "Container name or ID"},
                    "tail": {"type": "integer", "description": "Number of lines"},
                    "follow": {"type": "boolean", "description": "Follow log output"},
                    "since": {"type": "string", "description": "Show logs since (e.g., 10m)"}
                },
                "required": ["container"]
            },
            handler=self._get_logs
        ))

        # Tool: Inspect Container
        self.register_tool(MCPTool(
            name="inspect_container",
            description="Get detailed container information",
            parameters={
                "type": "object",
                "properties": {
                    "container": {"type": "string", "description": "Container name or ID"}
                },
                "required": ["container"]
            },
            handler=self._inspect_container
        ))

        # Tool: Push Image
        self.register_tool(MCPTool(
            name="push_image",
            description="Push an image to registry",
            parameters={
                "type": "object",
                "properties": {
                    "image": {"type": "string", "description": "Image name:tag"},
                    "registry": {"type": "string", "description": "Registry URL"}
                },
                "required": ["image"]
            },
            handler=self._push_image
        ))

        # Tool: Pull Image
        self.register_tool(MCPTool(
            name="pull_image",
            description="Pull an image from registry",
            parameters={
                "type": "object",
                "properties": {
                    "image": {"type": "string", "description": "Image name:tag"}
                },
                "required": ["image"]
            },
            handler=self._pull_image
        ))

        # Tool: Tag Image
        self.register_tool(MCPTool(
            name="tag_image",
            description="Create a tag for an image",
            parameters={
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "Source image"},
                    "target": {"type": "string", "description": "Target tag"}
                },
                "required": ["source", "target"]
            },
            handler=self._tag_image
        ))

        # Tool: Remove Image
        self.register_tool(MCPTool(
            name="remove_image",
            description="Remove a Docker image",
            parameters={
                "type": "object",
                "properties": {
                    "image": {"type": "string", "description": "Image name or ID"},
                    "force": {"type": "boolean", "description": "Force remove"}
                },
                "required": ["image"]
            },
            handler=self._remove_image
        ))

        # Tool: Docker Compose
        self.register_tool(MCPTool(
            name="compose",
            description="Run docker-compose commands",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "description": "up, down, ps, logs, restart"},
                    "file": {"type": "string", "description": "Compose file path"},
                    "service": {"type": "string", "description": "Specific service"},
                    "detach": {"type": "boolean"}
                },
                "required": ["action"]
            },
            handler=self._compose
        ))

        # Tool: List Volumes
        self.register_tool(MCPTool(
            name="list_volumes",
            description="List Docker volumes",
            parameters={
                "type": "object",
                "properties": {}
            },
            handler=self._list_volumes
        ))

        # Tool: List Networks
        self.register_tool(MCPTool(
            name="list_networks",
            description="List Docker networks",
            parameters={
                "type": "object",
                "properties": {}
            },
            handler=self._list_networks
        ))

        # Tool: Prune System
        self.register_tool(MCPTool(
            name="prune_system",
            description="Clean up unused Docker resources",
            parameters={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "description": "containers, images, volumes, all"}
                }
            },
            handler=self._prune_system
        ))

        # Tool: System Info
        self.register_tool(MCPTool(
            name="system_info",
            description="Get Docker system information",
            parameters={
                "type": "object",
                "properties": {}
            },
            handler=self._system_info
        ))

        # Tool: Execute in Container
        self.register_tool(MCPTool(
            name="exec_container",
            description="Execute command in running container",
            parameters={
                "type": "object",
                "properties": {
                    "container": {"type": "string", "description": "Container name or ID"},
                    "command": {"type": "string", "description": "Command to execute"},
                    "interactive": {"type": "boolean"}
                },
                "required": ["container", "command"]
            },
            handler=self._exec_container
        ))

    # ==================== TOOL IMPLEMENTATIONS ====================

    async def _run_docker(self, cmd: str) -> str:
        """Execute docker command"""
        if not cmd.startswith("docker"):
            cmd = f"docker {cmd}"

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

    async def _list_containers(self, all: bool = True, filter: str = None, **kwargs) -> List[Dict]:
        all_flag = "-a" if all else ""
        # Use Windows-compatible format (no single quotes, use double braces for escaping)
        fmt = "{{.ID}}|{{.Names}}|{{.Image}}|{{.Status}}|{{.Ports}}"
        cmd = f'docker ps {all_flag} --format "{fmt}"'

        result = await self._run_docker(cmd)

        containers = []
        for line in result.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) >= 4:
                    container = {
                        "id": parts[0],
                        "name": parts[1],
                        "image": parts[2],
                        "status": parts[3],
                        "ports": parts[4] if len(parts) > 4 else ""
                    }

                    if filter and filter.lower() not in str(container).lower():
                        continue

                    containers.append(container)

        return containers

    async def _list_images(self, filter: str = None, **kwargs) -> List[Dict]:
        # Use Windows-compatible format
        fmt = "{{.Repository}}|{{.Tag}}|{{.ID}}|{{.Size}}|{{.CreatedAt}}"
        cmd = f'docker images --format "{fmt}"'

        result = await self._run_docker(cmd)

        images = []
        for line in result.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) >= 4:
                    image = {
                        "repository": parts[0],
                        "tag": parts[1],
                        "id": parts[2],
                        "size": parts[3],
                        "created": parts[4] if len(parts) > 4 else ""
                    }

                    if filter and filter.lower() not in image["repository"].lower():
                        continue

                    images.append(image)

        return images

    async def _build_image(self, tag: str, dockerfile: str = "Dockerfile", context: str = ".", build_args: Dict = None, no_cache: bool = False, **kwargs) -> Dict:
        cmd = f"docker build -t {tag} -f {dockerfile}"

        if no_cache:
            cmd += " --no-cache"

        if build_args:
            for key, value in build_args.items():
                cmd += f" --build-arg {key}={value}"

        cmd += f" {context}"

        result = await self._run_docker(cmd)

        return {"status": "built", "tag": tag, "output": result[-500:]}

    async def _run_container(self, image: str, name: str = None, ports: str = None, volumes: str = None, env: Dict = None, detach: bool = True, **kwargs) -> Dict:
        cmd = "docker run"

        if detach:
            cmd += " -d"

        if name:
            cmd += f" --name {name}"

        if ports:
            cmd += f" -p {ports}"

        if volumes:
            cmd += f" -v {volumes}"

        if env:
            for key, value in env.items():
                cmd += f" -e {key}={value}"

        cmd += f" {image}"

        result = await self._run_docker(cmd)

        return {
            "status": "running",
            "container_id": result.strip()[:12],
            "image": image,
            "name": name
        }

    async def _stop_container(self, container: str, timeout: int = 10, **kwargs) -> Dict:
        await self._run_docker(f"docker stop -t {timeout} {container}")
        return {"status": "stopped", "container": container}

    async def _remove_container(self, container: str, force: bool = False, **kwargs) -> Dict:
        force_flag = "-f" if force else ""
        await self._run_docker(f"docker rm {force_flag} {container}")
        return {"status": "removed", "container": container}

    async def _get_logs(self, container: str, tail: int = 100, follow: bool = False, since: str = None, **kwargs) -> str:
        cmd = f"docker logs --tail {tail}"

        if since:
            cmd += f" --since {since}"

        cmd += f" {container}"

        return await self._run_docker(cmd)

    async def _inspect_container(self, container: str, **kwargs) -> Dict:
        result = await self._run_docker(f"docker inspect {container}")
        data = json.loads(result)
        return data[0] if data else {}

    async def _push_image(self, image: str, registry: str = None, **kwargs) -> Dict:
        if registry:
            full_image = f"{registry}/{image}"
            await self._run_docker(f"docker tag {image} {full_image}")
        else:
            full_image = image

        await self._run_docker(f"docker push {full_image}")
        return {"status": "pushed", "image": full_image}

    async def _pull_image(self, image: str, **kwargs) -> Dict:
        await self._run_docker(f"docker pull {image}")
        return {"status": "pulled", "image": image}

    async def _tag_image(self, source: str, target: str, **kwargs) -> Dict:
        await self._run_docker(f"docker tag {source} {target}")
        return {"status": "tagged", "source": source, "target": target}

    async def _remove_image(self, image: str, force: bool = False, **kwargs) -> Dict:
        force_flag = "-f" if force else ""
        await self._run_docker(f"docker rmi {force_flag} {image}")
        return {"status": "removed", "image": image}

    async def _compose(self, action: str, file: str = "docker-compose.yml", service: str = None, detach: bool = True, **kwargs) -> Dict:
        cmd = f"docker-compose -f {file} {action}"

        if action == "up" and detach:
            cmd += " -d"

        if service:
            cmd += f" {service}"

        result = await self._run_docker(cmd)
        return {"action": action, "output": result}

    async def _list_volumes(self, **kwargs) -> List[Dict]:
        # Use Windows-compatible format
        fmt = "{{.Name}}|{{.Driver}}"
        result = await self._run_docker(f'docker volume ls --format "{fmt}"')

        volumes = []
        for line in result.strip().split('\n'):
            if line:
                parts = line.split('|')
                volumes.append({
                    "name": parts[0],
                    "driver": parts[1] if len(parts) > 1 else "local"
                })

        return volumes

    async def _list_networks(self, **kwargs) -> List[Dict]:
        # Use Windows-compatible format
        fmt = "{{.ID}}|{{.Name}}|{{.Driver}}"
        result = await self._run_docker(f'docker network ls --format "{fmt}"')

        networks = []
        for line in result.strip().split('\n'):
            if line:
                parts = line.split('|')
                networks.append({
                    "id": parts[0],
                    "name": parts[1],
                    "driver": parts[2] if len(parts) > 2 else ""
                })

        return networks

    async def _prune_system(self, type: str = "all", **kwargs) -> Dict:
        if type == "containers":
            result = await self._run_docker("docker container prune -f")
        elif type == "images":
            result = await self._run_docker("docker image prune -a -f")
        elif type == "volumes":
            result = await self._run_docker("docker volume prune -f")
        else:
            result = await self._run_docker("docker system prune -a -f")

        return {"status": "pruned", "type": type, "output": result}

    async def _system_info(self, **kwargs) -> Dict:
        # Use Windows-compatible format
        result = await self._run_docker('docker info --format "{{json .}}"')

        try:
            info = json.loads(result)
            return {
                "containers": info.get("Containers"),
                "containers_running": info.get("ContainersRunning"),
                "containers_paused": info.get("ContainersPaused"),
                "containers_stopped": info.get("ContainersStopped"),
                "images": info.get("Images"),
                "server_version": info.get("ServerVersion"),
                "storage_driver": info.get("Driver"),
                "os": info.get("OperatingSystem"),
                "architecture": info.get("Architecture")
            }
        except:
            return {"raw": result}

    async def _exec_container(self, container: str, command: str, interactive: bool = False, **kwargs) -> str:
        it_flag = "-it" if interactive else ""
        return await self._run_docker(f"docker exec {it_flag} {container} {command}")

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
        """Direct execution for steps without specific tools - Smart matching"""
        query = step.get("query", step.get("action", "")).lower()

        # Smart matching to MCP tools based on query content
        if "container" in query and ("list" in query or "show" in query or "all" in query):
            return await self._list_containers()
        elif "image" in query and ("list" in query or "show" in query or "all" in query):
            return await self._list_images()
        elif "volume" in query:
            return await self._list_volumes()
        elif "network" in query:
            return await self._list_networks()
        elif "info" in query or "status" in query:
            return await self._system_info()
        elif "build" in query:
            return {"status": "need_params", "message": "Provide: tag, dockerfile, context"}
        elif "run" in query:
            return {"status": "need_params", "message": "Provide: image, name, ports"}

        return {"status": "no action taken", "query": query}
