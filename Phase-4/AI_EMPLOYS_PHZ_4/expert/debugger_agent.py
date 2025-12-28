"""
Debugger Agent - POWERFUL Debugging & Troubleshooting Expert
Error analysis, log investigation, root cause analysis

@author: Phase-4 Multi-Agent System
"""

import asyncio
import json
import re
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class DebuggerAgent(BaseAgent):
    """
    POWERFUL Debugger Expert Agent
    - Error analysis
    - Log investigation
    - Root cause analysis
    - Stack trace parsing
    - Debugging strategies
    """

    KEYWORDS = [
        'debug', 'error', 'exception', 'bug', 'issue', 'problem',
        'crash', 'fail', 'trace', 'stacktrace', 'log', 'investigate',
        'troubleshoot', 'diagnose', 'fix', 'broken', 'not working'
    ]

    def __init__(self, namespace: str = "todo"):
        super().__init__("Debugger", "Debugging expert - error analysis, root cause, troubleshooting")
        self.namespace = namespace
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all MCP tools for debugging operations"""

        # Tool: Analyze Error
        self.register_tool(MCPTool(
            name="analyze_error",
            description="Analyze an error message or stack trace",
            parameters={
                "type": "object",
                "properties": {
                    "error": {"type": "string", "description": "Error message or stack trace"},
                    "language": {"type": "string", "description": "Programming language"}
                },
                "required": ["error"]
            },
            handler=self._analyze_error
        ))

        # Tool: Search Logs
        self.register_tool(MCPTool(
            name="search_logs",
            description="Search logs for errors and patterns",
            parameters={
                "type": "object",
                "properties": {
                    "pod": {"type": "string", "description": "Pod or deployment name"},
                    "namespace": {"type": "string"},
                    "pattern": {"type": "string", "description": "Search pattern"},
                    "level": {"type": "string", "description": "error, warning, info"},
                    "since": {"type": "string", "description": "Time duration (1h, 30m)"}
                }
            },
            handler=self._search_logs
        ))

        # Tool: Get Pod Events
        self.register_tool(MCPTool(
            name="get_pod_events",
            description="Get Kubernetes events for debugging",
            parameters={
                "type": "object",
                "properties": {
                    "pod": {"type": "string"},
                    "namespace": {"type": "string"},
                    "type": {"type": "string", "description": "Normal or Warning"}
                }
            },
            handler=self._get_pod_events
        ))

        # Tool: Check Pod Status
        self.register_tool(MCPTool(
            name="check_pod_status",
            description="Detailed pod status and container states",
            parameters={
                "type": "object",
                "properties": {
                    "pod": {"type": "string"},
                    "namespace": {"type": "string"}
                }
            },
            handler=self._check_pod_status
        ))

        # Tool: Analyze Crash
        self.register_tool(MCPTool(
            name="analyze_crash",
            description="Analyze pod crash and get restart reasons",
            parameters={
                "type": "object",
                "properties": {
                    "pod": {"type": "string"},
                    "namespace": {"type": "string"}
                },
                "required": ["pod"]
            },
            handler=self._analyze_crash
        ))

        # Tool: Check Resources
        self.register_tool(MCPTool(
            name="check_resources",
            description="Check if resource limits are causing issues",
            parameters={
                "type": "object",
                "properties": {
                    "pod": {"type": "string"},
                    "namespace": {"type": "string"}
                }
            },
            handler=self._check_resources
        ))

        # Tool: Test Connectivity
        self.register_tool(MCPTool(
            name="test_connectivity",
            description="Test network connectivity between services",
            parameters={
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "Source pod"},
                    "target": {"type": "string", "description": "Target service:port"},
                    "namespace": {"type": "string"}
                },
                "required": ["source", "target"]
            },
            handler=self._test_connectivity
        ))

        # Tool: Check DNS
        self.register_tool(MCPTool(
            name="check_dns",
            description="Check DNS resolution for services",
            parameters={
                "type": "object",
                "properties": {
                    "service": {"type": "string"},
                    "namespace": {"type": "string"}
                },
                "required": ["service"]
            },
            handler=self._check_dns
        ))

        # Tool: Trace Request
        self.register_tool(MCPTool(
            name="trace_request",
            description="Trace a request through the system",
            parameters={
                "type": "object",
                "properties": {
                    "endpoint": {"type": "string", "description": "API endpoint"},
                    "method": {"type": "string", "description": "HTTP method"}
                },
                "required": ["endpoint"]
            },
            handler=self._trace_request
        ))

        # Tool: Find Root Cause
        self.register_tool(MCPTool(
            name="find_root_cause",
            description="Comprehensive root cause analysis",
            parameters={
                "type": "object",
                "properties": {
                    "symptom": {"type": "string", "description": "Observed problem"},
                    "namespace": {"type": "string"}
                },
                "required": ["symptom"]
            },
            handler=self._find_root_cause
        ))

        # Tool: Suggest Fix
        self.register_tool(MCPTool(
            name="suggest_fix",
            description="Suggest fixes for identified issues",
            parameters={
                "type": "object",
                "properties": {
                    "issue": {"type": "string", "description": "Issue description"},
                    "context": {"type": "object", "description": "Additional context"}
                },
                "required": ["issue"]
            },
            handler=self._suggest_fix
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

        return stdout.decode() + stderr.decode()

    async def _analyze_error(self, error: str, language: str = None, **kwargs) -> Dict:
        analysis = {
            "error": error[:500],
            "type": "unknown",
            "location": None,
            "suggestions": []
        }

        # Identify error type
        error_lower = error.lower()

        if "typeerror" in error_lower:
            analysis["type"] = "TypeError"
            analysis["suggestions"].append("Check variable types and function arguments")
        elif "keyerror" in error_lower or "attributeerror" in error_lower:
            analysis["type"] = "KeyError/AttributeError"
            analysis["suggestions"].append("Verify dictionary keys or object attributes exist")
        elif "connectionerror" in error_lower or "connection refused" in error_lower:
            analysis["type"] = "ConnectionError"
            analysis["suggestions"].append("Check if target service is running")
            analysis["suggestions"].append("Verify network connectivity and port")
        elif "timeout" in error_lower:
            analysis["type"] = "Timeout"
            analysis["suggestions"].append("Increase timeout value")
            analysis["suggestions"].append("Check target service performance")
        elif "permission" in error_lower or "denied" in error_lower:
            analysis["type"] = "PermissionError"
            analysis["suggestions"].append("Check file/directory permissions")
            analysis["suggestions"].append("Verify RBAC settings")
        elif "memory" in error_lower or "oom" in error_lower:
            analysis["type"] = "OutOfMemory"
            analysis["suggestions"].append("Increase memory limits")
            analysis["suggestions"].append("Check for memory leaks")
        elif "not found" in error_lower or "404" in error_lower:
            analysis["type"] = "NotFound"
            analysis["suggestions"].append("Verify endpoint/resource exists")
        elif "unauthorized" in error_lower or "401" in error_lower:
            analysis["type"] = "Unauthorized"
            analysis["suggestions"].append("Check authentication token")
            analysis["suggestions"].append("Verify credentials")
        elif "500" in error_lower or "internal server" in error_lower:
            analysis["type"] = "InternalServerError"
            analysis["suggestions"].append("Check server logs for details")

        # Extract file/line info
        file_line_match = re.search(r'File "([^"]+)", line (\d+)', error)
        if file_line_match:
            analysis["location"] = {
                "file": file_line_match.group(1),
                "line": int(file_line_match.group(2))
            }

        # JS/TS pattern
        js_match = re.search(r'at (\S+) \(([^:]+):(\d+):\d+\)', error)
        if js_match:
            analysis["location"] = {
                "function": js_match.group(1),
                "file": js_match.group(2),
                "line": int(js_match.group(3))
            }

        return analysis

    async def _search_logs(self, pod: str = None, namespace: str = None, pattern: str = None, level: str = "error", since: str = "1h", **kwargs) -> Dict:
        ns = namespace or self.namespace

        if pod:
            cmd = f"kubectl logs -n {ns} deployment/{pod} --since={since}"
        else:
            cmd = f"kubectl logs -n {ns} -l app --since={since}"

        try:
            result = await self._run_cmd(cmd)
            lines = result.strip().split('\n')

            # Filter by level
            level_patterns = {
                "error": ["error", "err", "exception", "fail"],
                "warning": ["warning", "warn"],
                "info": ["info"]
            }

            filtered = []
            patterns = level_patterns.get(level, [level])

            for line in lines:
                line_lower = line.lower()
                if any(p in line_lower for p in patterns):
                    filtered.append(line)
                elif pattern and pattern.lower() in line_lower:
                    filtered.append(line)

            return {
                "logs": filtered[-50:],  # Last 50 matches
                "total_matches": len(filtered),
                "level": level,
                "since": since
            }
        except Exception as e:
            return {"error": str(e)}

    async def _get_pod_events(self, pod: str = None, namespace: str = None, type: str = None, **kwargs) -> List[Dict]:
        ns = namespace or self.namespace

        cmd = f"kubectl get events -n {ns} --sort-by='.lastTimestamp' -o json"

        result = await self._run_cmd(cmd)
        data = json.loads(result)

        events = []
        for item in data.get("items", [])[-30:]:
            event_type = item.get("type")

            if type and event_type != type:
                continue

            if pod and pod not in item.get("involvedObject", {}).get("name", ""):
                continue

            events.append({
                "type": event_type,
                "reason": item.get("reason"),
                "message": item.get("message"),
                "object": item.get("involvedObject", {}).get("name"),
                "count": item.get("count", 1),
                "time": item.get("lastTimestamp")
            })

        return events

    async def _check_pod_status(self, pod: str = None, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        if pod:
            cmd = f"kubectl get pod {pod} -n {ns} -o json"
        else:
            cmd = f"kubectl get pods -n {ns} -o json"

        result = await self._run_cmd(cmd)
        data = json.loads(result)

        if "items" in data:
            pods = data["items"]
        else:
            pods = [data]

        statuses = []
        for p in pods:
            status = p.get("status", {})
            containers = status.get("containerStatuses", [])

            pod_status = {
                "name": p.get("metadata", {}).get("name"),
                "phase": status.get("phase"),
                "conditions": [],
                "containers": []
            }

            for cond in status.get("conditions", []):
                if cond.get("status") != "True":
                    pod_status["conditions"].append({
                        "type": cond.get("type"),
                        "reason": cond.get("reason"),
                        "message": cond.get("message")
                    })

            for c in containers:
                container_info = {
                    "name": c.get("name"),
                    "ready": c.get("ready"),
                    "restarts": c.get("restartCount", 0)
                }

                state = c.get("state", {})
                if "waiting" in state:
                    container_info["state"] = "waiting"
                    container_info["reason"] = state["waiting"].get("reason")
                    container_info["message"] = state["waiting"].get("message")
                elif "terminated" in state:
                    container_info["state"] = "terminated"
                    container_info["reason"] = state["terminated"].get("reason")
                    container_info["exit_code"] = state["terminated"].get("exitCode")
                else:
                    container_info["state"] = "running"

                pod_status["containers"].append(container_info)

            statuses.append(pod_status)

        return {"pods": statuses}

    async def _analyze_crash(self, pod: str, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        analysis = {
            "pod": pod,
            "crash_info": None,
            "previous_logs": None,
            "causes": []
        }

        # Get pod status
        status = await self._check_pod_status(pod=pod, namespace=ns)

        for p in status.get("pods", []):
            for c in p.get("containers", []):
                if c.get("restarts", 0) > 0:
                    analysis["crash_info"] = c

        # Get previous logs
        try:
            logs = await self._run_cmd(f"kubectl logs -n {ns} {pod} --previous --tail=50")
            analysis["previous_logs"] = logs.strip().split('\n')[-20:]
        except:
            analysis["previous_logs"] = ["No previous logs available"]

        # Identify causes
        if analysis["crash_info"]:
            reason = analysis["crash_info"].get("reason", "")
            if "OOMKilled" in reason:
                analysis["causes"].append("Out of Memory - increase memory limits")
            elif "Error" in reason:
                analysis["causes"].append("Application error - check logs for details")
            elif "CrashLoopBackOff" in reason:
                analysis["causes"].append("Repeated crashes - fix root cause before restart")

        return analysis

    async def _check_resources(self, pod: str = None, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        # Get resource metrics
        try:
            metrics = await self._run_cmd(f"kubectl top pods -n {ns}")
        except:
            metrics = "metrics-server not available"

        # Get resource limits
        if pod:
            cmd = f"kubectl get pod {pod} -n {ns} -o json"
        else:
            cmd = f"kubectl get pods -n {ns} -o json"

        result = await self._run_cmd(cmd)
        data = json.loads(result)

        if "items" in data:
            pods = data["items"]
        else:
            pods = [data]

        resources = []
        for p in pods:
            for c in p.get("spec", {}).get("containers", []):
                res = c.get("resources", {})
                resources.append({
                    "pod": p.get("metadata", {}).get("name"),
                    "container": c.get("name"),
                    "limits": res.get("limits", {}),
                    "requests": res.get("requests", {})
                })

        return {
            "metrics": metrics,
            "resources": resources
        }

    async def _test_connectivity(self, source: str, target: str, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        # Get source pod name
        pods = await self._run_cmd(f"kubectl get pods -n {ns} -l app={source} -o jsonpath='{{.items[0].metadata.name}}'")
        pod_name = pods.strip()

        if not pod_name:
            return {"error": f"No pod found for {source}"}

        # Test connectivity
        try:
            result = await self._run_cmd(
                f"kubectl exec -n {ns} {pod_name} -- curl -s -o /dev/null -w '%{{http_code}}' {target} --connect-timeout 5"
            )
            status_code = result.strip()

            return {
                "source": source,
                "target": target,
                "reachable": status_code in ["200", "201", "204", "301", "302"],
                "status_code": status_code
            }
        except Exception as e:
            return {
                "source": source,
                "target": target,
                "reachable": False,
                "error": str(e)
            }

    async def _check_dns(self, service: str, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        try:
            result = await self._run_cmd(f"kubectl run dns-test --rm -it --restart=Never --image=busybox -- nslookup {service}.{ns}.svc.cluster.local")

            return {
                "service": service,
                "fqdn": f"{service}.{ns}.svc.cluster.local",
                "resolved": "Address" in result,
                "output": result
            }
        except Exception as e:
            return {
                "service": service,
                "resolved": False,
                "error": str(e)
            }

    async def _trace_request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict:
        trace = {
            "endpoint": endpoint,
            "method": method,
            "steps": []
        }

        # Parse endpoint
        if endpoint.startswith("http"):
            # External request
            try:
                result = await self._run_cmd(f"curl -s -v {endpoint} 2>&1 | head -30")
                trace["steps"].append({"step": "curl", "result": result})
            except Exception as e:
                trace["steps"].append({"step": "curl", "error": str(e)})
        else:
            # Internal K8s path
            trace["steps"].append({"step": "parse", "path": endpoint})

        return trace

    async def _find_root_cause(self, symptom: str, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        root_cause_analysis = {
            "symptom": symptom,
            "investigation": [],
            "probable_causes": [],
            "recommended_actions": []
        }

        # Step 1: Check pod status
        self.log("Checking pod status...", "step")
        status = await self._check_pod_status(namespace=ns)
        root_cause_analysis["investigation"].append({"step": "pod_status", "result": status})

        for pod in status.get("pods", []):
            if pod.get("phase") != "Running":
                root_cause_analysis["probable_causes"].append(f"Pod {pod['name']} is {pod['phase']}")

            for c in pod.get("containers", []):
                if c.get("restarts", 0) > 5:
                    root_cause_analysis["probable_causes"].append(f"Container {c['name']} has high restarts ({c['restarts']})")

        # Step 2: Check events
        self.log("Checking events...", "step")
        events = await self._get_pod_events(namespace=ns, type="Warning")
        root_cause_analysis["investigation"].append({"step": "events", "count": len(events)})

        for event in events[-5:]:
            root_cause_analysis["probable_causes"].append(f"Event: {event['reason']} - {event['message']}")

        # Step 3: Check logs for errors
        self.log("Checking logs...", "step")
        logs = await self._search_logs(namespace=ns, level="error", since="30m")
        root_cause_analysis["investigation"].append({"step": "logs", "error_count": logs.get("total_matches", 0)})

        # Generate recommended actions
        if "OOMKilled" in str(root_cause_analysis["probable_causes"]):
            root_cause_analysis["recommended_actions"].append("Increase memory limits for affected containers")

        if "CrashLoopBackOff" in str(root_cause_analysis["probable_causes"]):
            root_cause_analysis["recommended_actions"].append("Check application logs for startup errors")

        if "connection" in symptom.lower():
            root_cause_analysis["recommended_actions"].append("Verify service endpoints and network policies")

        if not root_cause_analysis["recommended_actions"]:
            root_cause_analysis["recommended_actions"].append("Review logs in detail")
            root_cause_analysis["recommended_actions"].append("Check resource metrics")

        return root_cause_analysis

    async def _suggest_fix(self, issue: str, context: Dict = None, **kwargs) -> Dict:
        fixes = {
            "suggestions": [],
            "commands": []
        }

        issue_lower = issue.lower()

        if "crash" in issue_lower or "restart" in issue_lower:
            fixes["suggestions"].append("Check container logs for errors before crash")
            fixes["suggestions"].append("Increase resource limits if OOMKilled")
            fixes["commands"].append("kubectl logs <pod> --previous")
            fixes["commands"].append("kubectl describe pod <pod>")

        if "connection" in issue_lower or "network" in issue_lower:
            fixes["suggestions"].append("Verify target service is running")
            fixes["suggestions"].append("Check network policies")
            fixes["commands"].append("kubectl get svc -n <namespace>")
            fixes["commands"].append("kubectl get networkpolicies -n <namespace>")

        if "memory" in issue_lower or "oom" in issue_lower:
            fixes["suggestions"].append("Increase memory limits in deployment")
            fixes["suggestions"].append("Check for memory leaks in application")
            fixes["commands"].append("kubectl top pods")
            fixes["commands"].append("kubectl edit deployment <name>")

        if "permission" in issue_lower or "rbac" in issue_lower:
            fixes["suggestions"].append("Check ServiceAccount permissions")
            fixes["suggestions"].append("Review RBAC role bindings")
            fixes["commands"].append("kubectl auth can-i --list --as=system:serviceaccount:<ns>:<sa>")

        if "dns" in issue_lower:
            fixes["suggestions"].append("Verify CoreDNS is running")
            fixes["suggestions"].append("Check service name and namespace")
            fixes["commands"].append("kubectl get pods -n kube-system -l k8s-app=kube-dns")

        return fixes

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
        if "error" in query:
            return await self._analyze_error(error="Generic error check")
        elif "log" in query:
            return await self._search_logs()
        elif "event" in query:
            return await self._get_pod_events()
        elif "pod" in query and "status" in query:
            return await self._check_pod_status()
        elif "crash" in query:
            return await self._analyze_crash()
        elif "resource" in query:
            return await self._check_resources()
        elif "connectivity" in query or "connection" in query:
            return await self._test_connectivity()
        elif "dns" in query:
            return await self._check_dns()
        elif "root" in query or "cause" in query:
            return await self._find_root_cause()
        elif "fix" in query or "suggest" in query:
            return await self._suggest_fix()

        return {"status": "no action taken", "query": query}
