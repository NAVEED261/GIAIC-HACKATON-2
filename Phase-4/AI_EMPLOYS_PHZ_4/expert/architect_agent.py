"""
Architect Agent - POWERFUL System Architecture Expert
Design patterns, code analysis, architecture recommendations

@author: Phase-4 Multi-Agent System
"""

import asyncio
import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class ArchitectAgent(BaseAgent):
    """
    POWERFUL System Architect Expert Agent
    - Architecture analysis
    - Design patterns
    - Code structure review
    - Best practices
    - System design recommendations
    """

    KEYWORDS = [
        'architect', 'architecture', 'design', 'pattern', 'structure',
        'microservice', 'monolith', 'api', 'diagram', 'component',
        'dependency', 'coupling', 'cohesion', 'scalability', 'modularity'
    ]

    def __init__(self, project_path: str = "."):
        super().__init__("Architect", "System architecture expert - design patterns, structure analysis, recommendations")
        self.project_path = project_path
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all MCP tools for architecture analysis"""

        # Tool: Analyze Project Structure
        self.register_tool(MCPTool(
            name="analyze_structure",
            description="Analyze project directory structure and organization",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Project path"},
                    "depth": {"type": "integer", "description": "Directory depth to analyze"}
                }
            },
            handler=self._analyze_structure
        ))

        # Tool: Analyze Dependencies
        self.register_tool(MCPTool(
            name="analyze_dependencies",
            description="Analyze project dependencies (package.json, requirements.txt, etc.)",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "type": {"type": "string", "description": "python, node, go, etc."}
                }
            },
            handler=self._analyze_dependencies
        ))

        # Tool: Find Design Patterns
        self.register_tool(MCPTool(
            name="find_patterns",
            description="Identify design patterns used in codebase",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "language": {"type": "string"}
                }
            },
            handler=self._find_patterns
        ))

        # Tool: Check Architecture
        self.register_tool(MCPTool(
            name="check_architecture",
            description="Check if architecture follows best practices",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "type": {"type": "string", "description": "microservices, monolith, serverless"}
                }
            },
            handler=self._check_architecture
        ))

        # Tool: Generate Diagram
        self.register_tool(MCPTool(
            name="generate_diagram",
            description="Generate architecture diagram description (mermaid/plantuml)",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "format": {"type": "string", "description": "mermaid or plantuml"},
                    "type": {"type": "string", "description": "component, sequence, class"}
                }
            },
            handler=self._generate_diagram
        ))

        # Tool: Analyze API Design
        self.register_tool(MCPTool(
            name="analyze_api",
            description="Analyze API design and endpoints",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "framework": {"type": "string", "description": "fastapi, express, etc."}
                }
            },
            handler=self._analyze_api
        ))

        # Tool: Check Coupling
        self.register_tool(MCPTool(
            name="check_coupling",
            description="Analyze module coupling and dependencies",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                }
            },
            handler=self._check_coupling
        ))

        # Tool: Suggest Improvements
        self.register_tool(MCPTool(
            name="suggest_improvements",
            description="Suggest architectural improvements",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "focus": {"type": "string", "description": "scalability, maintainability, performance"}
                }
            },
            handler=self._suggest_improvements
        ))

        # Tool: Review Microservices
        self.register_tool(MCPTool(
            name="review_microservices",
            description="Review microservices architecture",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "K8s namespace"},
                    "path": {"type": "string"}
                }
            },
            handler=self._review_microservices
        ))

        # Tool: Generate ADR
        self.register_tool(MCPTool(
            name="generate_adr",
            description="Generate Architecture Decision Record",
            parameters={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Decision title"},
                    "context": {"type": "string"},
                    "decision": {"type": "string"},
                    "consequences": {"type": "string"}
                },
                "required": ["title", "decision"]
            },
            handler=self._generate_adr
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

        return stdout.decode()

    async def _analyze_structure(self, path: str = None, depth: int = 3, **kwargs) -> Dict:
        project_path = path or self.project_path

        # Get directory structure
        result = await self._run_cmd(f'tree -L {depth} -d "{project_path}"')

        # Analyze components
        components = []
        for item in os.listdir(project_path):
            item_path = os.path.join(project_path, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                components.append({
                    "name": item,
                    "type": self._identify_component_type(item)
                })

        return {
            "structure": result,
            "components": components,
            "root": project_path
        }

    def _identify_component_type(self, name: str) -> str:
        patterns = {
            "frontend": ["frontend", "client", "web", "ui", "app"],
            "backend": ["backend", "server", "api", "service"],
            "database": ["db", "database", "data", "migrations"],
            "infrastructure": ["k8s", "kubernetes", "docker", "helm", "infra"],
            "tests": ["test", "tests", "spec", "specs"],
            "docs": ["docs", "documentation", "doc"],
            "config": ["config", "settings", "env"]
        }

        name_lower = name.lower()
        for comp_type, keywords in patterns.items():
            if any(kw in name_lower for kw in keywords):
                return comp_type

        return "other"

    async def _analyze_dependencies(self, path: str = None, type: str = None, **kwargs) -> Dict:
        project_path = path or self.project_path

        dependencies = {}

        # Python
        req_file = os.path.join(project_path, "requirements.txt")
        if os.path.exists(req_file):
            with open(req_file) as f:
                dependencies["python"] = [
                    line.strip() for line in f.readlines()
                    if line.strip() and not line.startswith('#')
                ]

        # Node.js
        pkg_file = os.path.join(project_path, "package.json")
        if os.path.exists(pkg_file):
            with open(pkg_file) as f:
                pkg = json.load(f)
                dependencies["node"] = {
                    "dependencies": pkg.get("dependencies", {}),
                    "devDependencies": pkg.get("devDependencies", {})
                }

        # Go
        go_mod = os.path.join(project_path, "go.mod")
        if os.path.exists(go_mod):
            result = await self._run_cmd(f'cat "{go_mod}"')
            dependencies["go"] = result

        return {
            "dependencies": dependencies,
            "count": sum(len(v) if isinstance(v, list) else len(v.get("dependencies", {})) for v in dependencies.values())
        }

    async def _find_patterns(self, path: str = None, language: str = None, **kwargs) -> Dict:
        project_path = path or self.project_path

        patterns_found = []

        # Search for common patterns
        pattern_indicators = {
            "singleton": ["getInstance", "_instance", "Singleton"],
            "factory": ["Factory", "create_", "createInstance"],
            "observer": ["subscribe", "notify", "addEventListener", "on_"],
            "decorator": ["@", "decorator", "wrapper"],
            "repository": ["Repository", "repo", "DAO"],
            "service": ["Service", "service"],
            "controller": ["Controller", "router", "handler"],
            "model": ["Model", "Entity", "Schema"]
        }

        for pattern, indicators in pattern_indicators.items():
            for indicator in indicators:
                try:
                    result = await self._run_cmd(
                        f'grep -rl "{indicator}" "{project_path}" --include="*.py" --include="*.js" --include="*.ts" 2>/dev/null | head -5'
                    )
                    if result.strip():
                        patterns_found.append({
                            "pattern": pattern,
                            "indicator": indicator,
                            "files": result.strip().split('\n')[:3]
                        })
                        break
                except:
                    pass

        return {"patterns": patterns_found}

    async def _check_architecture(self, path: str = None, type: str = None, **kwargs) -> Dict:
        project_path = path or self.project_path

        analysis = {
            "path": project_path,
            "type": type or "unknown",
            "checks": [],
            "score": 100
        }

        # Check 1: Separation of concerns
        has_frontend = os.path.exists(os.path.join(project_path, "frontend"))
        has_backend = os.path.exists(os.path.join(project_path, "backend"))

        if has_frontend and has_backend:
            analysis["checks"].append({
                "name": "separation_of_concerns",
                "status": "pass",
                "message": "Frontend and backend are properly separated"
            })
        else:
            analysis["checks"].append({
                "name": "separation_of_concerns",
                "status": "info",
                "message": "Consider separating frontend and backend"
            })
            analysis["score"] -= 10

        # Check 2: Configuration files
        config_files = [".env", ".env.example", "config/", "settings/"]
        has_config = any(os.path.exists(os.path.join(project_path, f)) for f in config_files)

        if has_config:
            analysis["checks"].append({
                "name": "configuration",
                "status": "pass",
                "message": "Configuration files present"
            })
        else:
            analysis["checks"].append({
                "name": "configuration",
                "status": "warning",
                "message": "No configuration files found"
            })
            analysis["score"] -= 15

        # Check 3: Tests
        test_dirs = ["tests", "test", "__tests__", "spec"]
        has_tests = any(os.path.exists(os.path.join(project_path, d)) for d in test_dirs)

        if has_tests:
            analysis["checks"].append({
                "name": "tests",
                "status": "pass",
                "message": "Test directory found"
            })
        else:
            analysis["checks"].append({
                "name": "tests",
                "status": "warning",
                "message": "No test directory found"
            })
            analysis["score"] -= 20

        # Check 4: Documentation
        doc_files = ["README.md", "docs/", "CLAUDE.md"]
        has_docs = any(os.path.exists(os.path.join(project_path, f)) for f in doc_files)

        if has_docs:
            analysis["checks"].append({
                "name": "documentation",
                "status": "pass",
                "message": "Documentation found"
            })
        else:
            analysis["checks"].append({
                "name": "documentation",
                "status": "warning",
                "message": "No documentation found"
            })
            analysis["score"] -= 10

        return analysis

    async def _generate_diagram(self, path: str = None, format: str = "mermaid", type: str = "component", **kwargs) -> Dict:
        project_path = path or self.project_path

        # Analyze structure
        structure = await self._analyze_structure(path=project_path)

        if format == "mermaid":
            if type == "component":
                diagram = "graph TB\n"
                for comp in structure["components"]:
                    diagram += f'    {comp["name"]}["{comp["name"]}\\n({comp["type"]})"]\n'

                # Add connections based on type
                frontend = [c["name"] for c in structure["components"] if c["type"] == "frontend"]
                backend = [c["name"] for c in structure["components"] if c["type"] == "backend"]
                database = [c["name"] for c in structure["components"] if c["type"] == "database"]

                for f in frontend:
                    for b in backend:
                        diagram += f"    {f} --> {b}\n"
                for b in backend:
                    for d in database:
                        diagram += f"    {b} --> {d}\n"

            else:
                diagram = "classDiagram\n"
                for comp in structure["components"]:
                    diagram += f'    class {comp["name"]} {{\n        +{comp["type"]}\n    }}\n'

        else:  # plantuml
            diagram = "@startuml\n"
            for comp in structure["components"]:
                diagram += f'component "{comp["name"]}" as {comp["name"]}\n'
            diagram += "@enduml\n"

        return {
            "format": format,
            "type": type,
            "diagram": diagram
        }

    async def _analyze_api(self, path: str = None, framework: str = None, **kwargs) -> Dict:
        project_path = path or self.project_path

        endpoints = []

        # FastAPI
        try:
            result = await self._run_cmd(
                f'grep -rn "@app\\." "{project_path}" --include="*.py" 2>/dev/null | head -20'
            )
            for line in result.strip().split('\n'):
                if line and any(m in line for m in ['get', 'post', 'put', 'delete', 'patch']):
                    endpoints.append({"framework": "fastapi", "definition": line.strip()})
        except:
            pass

        # Express
        try:
            result = await self._run_cmd(
                f'grep -rn "router\\." "{project_path}" --include="*.js" --include="*.ts" 2>/dev/null | head -20'
            )
            for line in result.strip().split('\n'):
                if line:
                    endpoints.append({"framework": "express", "definition": line.strip()})
        except:
            pass

        return {
            "endpoints": endpoints,
            "count": len(endpoints)
        }

    async def _check_coupling(self, path: str = None, **kwargs) -> Dict:
        project_path = path or self.project_path

        coupling_analysis = {
            "imports": {},
            "coupling_level": "unknown"
        }

        # Analyze Python imports
        try:
            result = await self._run_cmd(
                f'grep -rh "^import\\|^from" "{project_path}" --include="*.py" 2>/dev/null | sort | uniq -c | sort -rn | head -20'
            )
            coupling_analysis["python_imports"] = result.strip()
        except:
            pass

        # Analyze JS/TS imports
        try:
            result = await self._run_cmd(
                f'grep -rh "^import\\|require(" "{project_path}" --include="*.js" --include="*.ts" 2>/dev/null | sort | uniq -c | sort -rn | head -20'
            )
            coupling_analysis["js_imports"] = result.strip()
        except:
            pass

        return coupling_analysis

    async def _suggest_improvements(self, path: str = None, focus: str = "maintainability", **kwargs) -> Dict:
        project_path = path or self.project_path

        # Run architecture check first
        arch_check = await self._check_architecture(path=project_path)

        suggestions = []

        for check in arch_check.get("checks", []):
            if check["status"] != "pass":
                suggestions.append({
                    "area": check["name"],
                    "suggestion": f"Improve: {check['message']}"
                })

        # Focus-specific suggestions
        if focus == "scalability":
            suggestions.extend([
                {"area": "caching", "suggestion": "Consider adding Redis/Memcached for caching"},
                {"area": "load_balancing", "suggestion": "Implement horizontal scaling with load balancer"},
                {"area": "async", "suggestion": "Use async operations for I/O bound tasks"}
            ])
        elif focus == "maintainability":
            suggestions.extend([
                {"area": "testing", "suggestion": "Increase test coverage to 80%+"},
                {"area": "documentation", "suggestion": "Add inline documentation and API docs"},
                {"area": "modularization", "suggestion": "Break large modules into smaller components"}
            ])
        elif focus == "performance":
            suggestions.extend([
                {"area": "database", "suggestion": "Add indexes for frequently queried columns"},
                {"area": "caching", "suggestion": "Implement query caching"},
                {"area": "optimization", "suggestion": "Profile and optimize hot paths"}
            ])

        return {"suggestions": suggestions, "focus": focus}

    async def _review_microservices(self, namespace: str = "todo", path: str = None, **kwargs) -> Dict:
        review = {
            "namespace": namespace,
            "services": [],
            "recommendations": []
        }

        # Get K8s services
        try:
            result = await self._run_cmd(f"kubectl get deployments -n {namespace} -o json")
            data = json.loads(result)

            for item in data.get("items", []):
                name = item.get("metadata", {}).get("name")
                replicas = item.get("spec", {}).get("replicas", 1)

                review["services"].append({
                    "name": name,
                    "replicas": replicas,
                    "containers": len(item.get("spec", {}).get("template", {}).get("spec", {}).get("containers", []))
                })

            # Generate recommendations
            if len(review["services"]) == 1:
                review["recommendations"].append("Consider splitting into multiple services for better scalability")

            for svc in review["services"]:
                if svc["replicas"] == 1:
                    review["recommendations"].append(f"{svc['name']}: Consider increasing replicas for high availability")

        except Exception as e:
            review["error"] = str(e)

        return review

    async def _generate_adr(self, title: str, decision: str, context: str = None, consequences: str = None, **kwargs) -> Dict:
        from datetime import datetime

        adr = f"""# ADR: {title}

## Status
Proposed

## Date
{datetime.now().strftime("%Y-%m-%d")}

## Context
{context or "Context not specified"}

## Decision
{decision}

## Consequences
{consequences or "To be determined"}

---
Generated by Architect Agent
"""

        return {
            "title": title,
            "content": adr,
            "status": "generated"
        }

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
        if "structure" in query or "architecture" in query or "analyze" in query:
            return await self._analyze_structure()
        elif "dependency" in query or "dependencies" in query:
            return await self._analyze_dependencies()
        elif "pattern" in query:
            return await self._find_patterns()
        elif "api" in query:
            return await self._analyze_api()
        elif "coupling" in query:
            return await self._check_coupling()
        elif "improve" in query or "suggest" in query:
            return await self._suggest_improvements()
        elif "microservice" in query:
            return await self._review_microservices()
        elif "diagram" in query:
            return await self._generate_diagram()

        return {"status": "analysis complete", "query": query}
