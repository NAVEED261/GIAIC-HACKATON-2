"""
CI/CD Agent - POWERFUL Continuous Integration & Deployment Expert
Git, GitHub Actions, Docker builds, deployments, pipelines

@author: Phase-4 Multi-Agent System
"""

import asyncio
import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class CICDAgent(BaseAgent):
    """
    POWERFUL CI/CD Expert Agent
    - Git operations
    - GitHub Actions
    - Docker builds
    - Deployment pipelines
    - Version management
    """

    KEYWORDS = [
        'cicd', 'ci/cd', 'pipeline', 'git', 'github', 'deploy', 'deployment',
        'build', 'release', 'version', 'tag', 'branch', 'commit', 'push',
        'pull', 'merge', 'action', 'workflow', 'rollback'
    ]

    def __init__(self, repo_path: str = "."):
        super().__init__("CICD", "CI/CD expert - Git, GitHub Actions, builds, deployments")
        self.repo_path = repo_path
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all MCP tools for CI/CD operations"""

        # Tool: Git Status
        self.register_tool(MCPTool(
            name="git_status",
            description="Get git status - modified, staged, untracked files",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository path"}
                }
            },
            handler=self._git_status
        ))

        # Tool: Git Log
        self.register_tool(MCPTool(
            name="git_log",
            description="Get commit history with details",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "count": {"type": "integer", "description": "Number of commits"},
                    "branch": {"type": "string", "description": "Branch name"}
                }
            },
            handler=self._git_log
        ))

        # Tool: Git Branch
        self.register_tool(MCPTool(
            name="git_branch",
            description="List, create, or switch branches",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "description": "list, create, switch, delete"},
                    "name": {"type": "string", "description": "Branch name"},
                    "path": {"type": "string"}
                }
            },
            handler=self._git_branch
        ))

        # Tool: Git Commit
        self.register_tool(MCPTool(
            name="git_commit",
            description="Stage and commit changes",
            parameters={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Commit message"},
                    "files": {"type": "array", "description": "Files to stage (empty = all)"},
                    "path": {"type": "string"}
                },
                "required": ["message"]
            },
            handler=self._git_commit
        ))

        # Tool: Git Push
        self.register_tool(MCPTool(
            name="git_push",
            description="Push commits to remote",
            parameters={
                "type": "object",
                "properties": {
                    "remote": {"type": "string", "description": "Remote name (default: origin)"},
                    "branch": {"type": "string", "description": "Branch name"},
                    "force": {"type": "boolean", "description": "Force push"},
                    "path": {"type": "string"}
                }
            },
            handler=self._git_push
        ))

        # Tool: Git Pull
        self.register_tool(MCPTool(
            name="git_pull",
            description="Pull changes from remote",
            parameters={
                "type": "object",
                "properties": {
                    "remote": {"type": "string"},
                    "branch": {"type": "string"},
                    "path": {"type": "string"}
                }
            },
            handler=self._git_pull
        ))

        # Tool: Git Tag
        self.register_tool(MCPTool(
            name="git_tag",
            description="Create or list tags for releases",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "description": "list, create, delete"},
                    "name": {"type": "string", "description": "Tag name (e.g., v1.0.0)"},
                    "message": {"type": "string", "description": "Tag message"},
                    "path": {"type": "string"}
                }
            },
            handler=self._git_tag
        ))

        # Tool: Docker Build
        self.register_tool(MCPTool(
            name="docker_build",
            description="Build Docker image with tag",
            parameters={
                "type": "object",
                "properties": {
                    "dockerfile": {"type": "string", "description": "Dockerfile path"},
                    "tag": {"type": "string", "description": "Image tag"},
                    "context": {"type": "string", "description": "Build context path"},
                    "build_args": {"type": "object", "description": "Build arguments"}
                },
                "required": ["tag"]
            },
            handler=self._docker_build
        ))

        # Tool: Docker Push
        self.register_tool(MCPTool(
            name="docker_push",
            description="Push Docker image to registry",
            parameters={
                "type": "object",
                "properties": {
                    "image": {"type": "string", "description": "Image name:tag"},
                    "registry": {"type": "string", "description": "Registry URL"}
                },
                "required": ["image"]
            },
            handler=self._docker_push
        ))

        # Tool: Run Pipeline
        self.register_tool(MCPTool(
            name="run_pipeline",
            description="Execute a CI/CD pipeline - build, test, deploy",
            parameters={
                "type": "object",
                "properties": {
                    "steps": {"type": "array", "description": "Pipeline steps"},
                    "environment": {"type": "string", "description": "dev, staging, prod"}
                }
            },
            handler=self._run_pipeline
        ))

        # Tool: Check Workflow Status
        self.register_tool(MCPTool(
            name="check_workflow",
            description="Check GitHub Actions workflow status",
            parameters={
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "owner/repo"},
                    "workflow": {"type": "string", "description": "Workflow name or ID"},
                    "run_id": {"type": "string", "description": "Specific run ID"}
                }
            },
            handler=self._check_workflow
        ))

        # Tool: Trigger Workflow
        self.register_tool(MCPTool(
            name="trigger_workflow",
            description="Trigger a GitHub Actions workflow",
            parameters={
                "type": "object",
                "properties": {
                    "repo": {"type": "string"},
                    "workflow": {"type": "string"},
                    "ref": {"type": "string", "description": "Branch or tag"},
                    "inputs": {"type": "object", "description": "Workflow inputs"}
                },
                "required": ["repo", "workflow"]
            },
            handler=self._trigger_workflow
        ))

        # Tool: Rollback Deployment
        self.register_tool(MCPTool(
            name="rollback",
            description="Rollback to previous deployment",
            parameters={
                "type": "object",
                "properties": {
                    "deployment": {"type": "string", "description": "Deployment name"},
                    "revision": {"type": "string", "description": "Target revision"},
                    "namespace": {"type": "string"}
                },
                "required": ["deployment"]
            },
            handler=self._rollback
        ))

    # ==================== TOOL IMPLEMENTATIONS ====================

    async def _run_cmd(self, cmd: str, cwd: str = None) -> str:
        """Execute shell command"""
        self.log(f"$ {cmd}", "working")

        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0 and stderr:
            raise Exception(stderr.decode())

        return stdout.decode()

    async def _git_status(self, path: str = None, **kwargs) -> Dict:
        repo = path or self.repo_path
        result = await self._run_cmd("git status --porcelain", cwd=repo)

        modified = []
        staged = []
        untracked = []

        for line in result.strip().split('\n'):
            if not line:
                continue
            status = line[:2]
            file = line[3:]

            if status[0] == 'M':
                staged.append(file)
            elif status[1] == 'M':
                modified.append(file)
            elif status == '??':
                untracked.append(file)

        branch = (await self._run_cmd("git branch --show-current", cwd=repo)).strip()

        return {
            "branch": branch,
            "modified": modified,
            "staged": staged,
            "untracked": untracked,
            "clean": len(modified) == 0 and len(staged) == 0 and len(untracked) == 0
        }

    async def _git_log(self, path: str = None, count: int = 10, branch: str = None, **kwargs) -> List[Dict]:
        repo = path or self.repo_path
        branch_arg = branch or ""
        result = await self._run_cmd(
            f'git log {branch_arg} -n {count} --format="%H|%an|%ae|%ai|%s"',
            cwd=repo
        )

        commits = []
        for line in result.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= 5:
                commits.append({
                    "hash": parts[0][:8],
                    "author": parts[1],
                    "email": parts[2],
                    "date": parts[3],
                    "message": parts[4]
                })

        return commits

    async def _git_branch(self, action: str = "list", name: str = None, path: str = None, **kwargs) -> Dict:
        repo = path or self.repo_path

        if action == "list":
            result = await self._run_cmd("git branch -a", cwd=repo)
            branches = [b.strip().replace('* ', '') for b in result.strip().split('\n') if b.strip()]
            current = await self._run_cmd("git branch --show-current", cwd=repo)
            return {"branches": branches, "current": current.strip()}

        elif action == "create" and name:
            await self._run_cmd(f"git checkout -b {name}", cwd=repo)
            return {"created": name}

        elif action == "switch" and name:
            await self._run_cmd(f"git checkout {name}", cwd=repo)
            return {"switched": name}

        elif action == "delete" and name:
            await self._run_cmd(f"git branch -d {name}", cwd=repo)
            return {"deleted": name}

        return {"error": "Invalid action or missing name"}

    async def _git_commit(self, message: str, files: List = None, path: str = None, **kwargs) -> Dict:
        repo = path or self.repo_path

        if files:
            for f in files:
                await self._run_cmd(f'git add "{f}"', cwd=repo)
        else:
            await self._run_cmd("git add -A", cwd=repo)

        await self._run_cmd(f'git commit -m "{message}"', cwd=repo)

        # Get commit hash
        hash = (await self._run_cmd("git rev-parse --short HEAD", cwd=repo)).strip()

        return {"committed": True, "hash": hash, "message": message}

    async def _git_push(self, remote: str = "origin", branch: str = None, force: bool = False, path: str = None, **kwargs) -> Dict:
        repo = path or self.repo_path

        if not branch:
            branch = (await self._run_cmd("git branch --show-current", cwd=repo)).strip()

        force_flag = "-f" if force else ""
        await self._run_cmd(f"git push {force_flag} {remote} {branch}", cwd=repo)

        return {"pushed": True, "remote": remote, "branch": branch}

    async def _git_pull(self, remote: str = "origin", branch: str = None, path: str = None, **kwargs) -> Dict:
        repo = path or self.repo_path

        if not branch:
            branch = (await self._run_cmd("git branch --show-current", cwd=repo)).strip()

        await self._run_cmd(f"git pull {remote} {branch}", cwd=repo)

        return {"pulled": True, "remote": remote, "branch": branch}

    async def _git_tag(self, action: str = "list", name: str = None, message: str = None, path: str = None, **kwargs) -> Dict:
        repo = path or self.repo_path

        if action == "list":
            result = await self._run_cmd("git tag -l", cwd=repo)
            tags = [t.strip() for t in result.strip().split('\n') if t.strip()]
            return {"tags": tags}

        elif action == "create" and name:
            msg_flag = f'-m "{message}"' if message else ""
            await self._run_cmd(f"git tag -a {name} {msg_flag}", cwd=repo)
            return {"created": name}

        elif action == "delete" and name:
            await self._run_cmd(f"git tag -d {name}", cwd=repo)
            return {"deleted": name}

        return {"error": "Invalid action"}

    async def _docker_build(self, tag: str, dockerfile: str = "Dockerfile", context: str = ".", build_args: Dict = None, **kwargs) -> Dict:
        args = ""
        if build_args:
            args = " ".join([f"--build-arg {k}={v}" for k, v in build_args.items()])

        await self._run_cmd(f"docker build -t {tag} -f {dockerfile} {args} {context}")

        return {"built": True, "tag": tag}

    async def _docker_push(self, image: str, registry: str = None, **kwargs) -> Dict:
        full_image = f"{registry}/{image}" if registry else image

        if registry:
            await self._run_cmd(f"docker tag {image} {full_image}")

        await self._run_cmd(f"docker push {full_image}")

        return {"pushed": True, "image": full_image}

    async def _run_pipeline(self, steps: List = None, environment: str = "dev", **kwargs) -> Dict:
        if not steps:
            steps = ["test", "build", "deploy"]

        results = []
        for step in steps:
            self.log(f"Running pipeline step: {step}", "step")

            if step == "test":
                try:
                    await self._run_cmd("pytest tests/ -v")
                    results.append({"step": "test", "status": "passed"})
                except:
                    results.append({"step": "test", "status": "failed"})
                    break

            elif step == "build":
                try:
                    await self._run_cmd("docker build -t app:latest .")
                    results.append({"step": "build", "status": "success"})
                except Exception as e:
                    results.append({"step": "build", "status": "failed", "error": str(e)})

            elif step == "deploy":
                results.append({"step": "deploy", "status": "pending", "environment": environment})

        return {"pipeline": results, "environment": environment}

    async def _check_workflow(self, repo: str = None, workflow: str = None, run_id: str = None, **kwargs) -> Dict:
        if run_id:
            result = await self._run_cmd(f"gh run view {run_id} --json status,conclusion,name")
        elif workflow:
            result = await self._run_cmd(f"gh run list --workflow={workflow} --limit=5 --json status,conclusion,name")
        else:
            result = await self._run_cmd("gh run list --limit=10 --json status,conclusion,name")

        return json.loads(result)

    async def _trigger_workflow(self, repo: str, workflow: str, ref: str = "main", inputs: Dict = None, **kwargs) -> Dict:
        inputs_json = json.dumps(inputs) if inputs else "{}"
        await self._run_cmd(f'gh workflow run {workflow} -R {repo} --ref {ref} -f \'{inputs_json}\'')

        return {"triggered": True, "workflow": workflow, "repo": repo, "ref": ref}

    async def _rollback(self, deployment: str, revision: str = None, namespace: str = "default", **kwargs) -> Dict:
        if revision:
            await self._run_cmd(f"kubectl rollout undo deployment/{deployment} --to-revision={revision} -n {namespace}")
        else:
            await self._run_cmd(f"kubectl rollout undo deployment/{deployment} -n {namespace}")

        return {"rolled_back": True, "deployment": deployment, "namespace": namespace}

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
        if "status" in query and "git" in query:
            return await self._git_status()
        elif "log" in query and ("git" in query or "commit" in query):
            return await self._git_log()
        elif "branch" in query:
            return await self._git_branch(action="list")
        elif "tag" in query:
            return await self._git_tag(action="list")
        elif "push" in query:
            return {"status": "need_params", "message": "Provide: remote, branch"}
        elif "pull" in query:
            return {"status": "need_params", "message": "Provide: remote, branch"}
        elif "commit" in query:
            return {"status": "need_params", "message": "Provide: message"}
        elif "workflow" in query or "action" in query:
            return await self._check_workflow()
        elif "pipeline" in query:
            return await self._run_pipeline()

        return {"status": "no action taken", "query": query}
