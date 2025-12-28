"""
Optimizer Agent - POWERFUL Performance Optimization Expert
Resource optimization, scaling, performance tuning

@author: Phase-4 Multi-Agent System
"""

import asyncio
import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class OptimizerAgent(BaseAgent):
    """
    POWERFUL Performance Optimizer Expert Agent
    - Resource optimization
    - Scaling recommendations
    - Performance tuning
    - Cost optimization
    - Efficiency analysis
    """

    KEYWORDS = [
        'optimize', 'performance', 'speed', 'slow', 'fast', 'scale',
        'resource', 'cpu', 'memory', 'efficient', 'cost', 'tune',
        'bottleneck', 'latency', 'throughput', 'capacity'
    ]

    def __init__(self, namespace: str = "todo"):
        super().__init__("Optimizer", "Performance optimization expert - scaling, tuning, efficiency")
        self.namespace = namespace
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all MCP tools for optimization operations"""

        # Tool: Analyze Resource Usage
        self.register_tool(MCPTool(
            name="analyze_resources",
            description="Analyze current resource usage and identify inefficiencies",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "deployment": {"type": "string"}
                }
            },
            handler=self._analyze_resources
        ))

        # Tool: Get Scaling Recommendations
        self.register_tool(MCPTool(
            name="get_scaling_recommendations",
            description="Get recommendations for scaling deployments",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "deployment": {"type": "string"}
                }
            },
            handler=self._get_scaling_recommendations
        ))

        # Tool: Optimize Resource Limits
        self.register_tool(MCPTool(
            name="optimize_limits",
            description="Calculate optimal resource limits based on usage",
            parameters={
                "type": "object",
                "properties": {
                    "deployment": {"type": "string"},
                    "namespace": {"type": "string"},
                    "buffer_percent": {"type": "integer", "description": "Buffer percentage (default 20)"}
                },
                "required": ["deployment"]
            },
            handler=self._optimize_limits
        ))

        # Tool: Apply HPA
        self.register_tool(MCPTool(
            name="apply_hpa",
            description="Apply Horizontal Pod Autoscaler",
            parameters={
                "type": "object",
                "properties": {
                    "deployment": {"type": "string"},
                    "namespace": {"type": "string"},
                    "min_replicas": {"type": "integer"},
                    "max_replicas": {"type": "integer"},
                    "cpu_percent": {"type": "integer", "description": "Target CPU utilization"}
                },
                "required": ["deployment"]
            },
            handler=self._apply_hpa
        ))

        # Tool: Check HPA Status
        self.register_tool(MCPTool(
            name="check_hpa",
            description="Check HPA status and metrics",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            },
            handler=self._check_hpa
        ))

        # Tool: Find Bottlenecks
        self.register_tool(MCPTool(
            name="find_bottlenecks",
            description="Identify performance bottlenecks",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            },
            handler=self._find_bottlenecks
        ))

        # Tool: Optimize Deployment
        self.register_tool(MCPTool(
            name="optimize_deployment",
            description="Optimize deployment configuration",
            parameters={
                "type": "object",
                "properties": {
                    "deployment": {"type": "string"},
                    "namespace": {"type": "string"},
                    "optimization_type": {"type": "string", "description": "resources, replicas, or all"}
                },
                "required": ["deployment"]
            },
            handler=self._optimize_deployment
        ))

        # Tool: Cost Analysis
        self.register_tool(MCPTool(
            name="cost_analysis",
            description="Analyze resource costs and suggest savings",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            },
            handler=self._cost_analysis
        ))

        # Tool: Right-size Containers
        self.register_tool(MCPTool(
            name="right_size",
            description="Calculate right-sized resource requests",
            parameters={
                "type": "object",
                "properties": {
                    "deployment": {"type": "string"},
                    "namespace": {"type": "string"}
                }
            },
            handler=self._right_size
        ))

        # Tool: Performance Report
        self.register_tool(MCPTool(
            name="performance_report",
            description="Generate comprehensive performance report",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            },
            handler=self._performance_report
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

        return stdout.decode()

    async def _analyze_resources(self, namespace: str = None, deployment: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        analysis = {
            "namespace": ns,
            "pods": [],
            "summary": {
                "total_cpu_requests": "0m",
                "total_memory_requests": "0Mi",
                "efficiency": "unknown"
            }
        }

        # Get pod metrics
        try:
            result = await self._run_cmd(f"kubectl top pods -n {ns}")
            lines = result.strip().split('\n')

            for line in lines[1:]:  # Skip header
                parts = line.split()
                if len(parts) >= 3:
                    pod_name = parts[0]

                    if deployment and deployment not in pod_name:
                        continue

                    analysis["pods"].append({
                        "name": pod_name,
                        "cpu_usage": parts[1],
                        "memory_usage": parts[2]
                    })
        except:
            analysis["metrics_error"] = "metrics-server not available"

        # Get resource requests/limits
        if deployment:
            cmd = f"kubectl get deployment {deployment} -n {ns} -o json"
        else:
            cmd = f"kubectl get deployments -n {ns} -o json"

        result = await self._run_cmd(cmd)
        data = json.loads(result)

        if "items" in data:
            deployments = data["items"]
        else:
            deployments = [data]

        for d in deployments:
            name = d.get("metadata", {}).get("name")
            for c in d.get("spec", {}).get("template", {}).get("spec", {}).get("containers", []):
                resources = c.get("resources", {})
                analysis["pods"].append({
                    "deployment": name,
                    "container": c.get("name"),
                    "requests": resources.get("requests", {}),
                    "limits": resources.get("limits", {})
                })

        return analysis

    async def _get_scaling_recommendations(self, namespace: str = None, deployment: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        recommendations = {
            "namespace": ns,
            "recommendations": []
        }

        # Analyze current state
        resources = await self._analyze_resources(namespace=ns, deployment=deployment)

        for pod in resources.get("pods", []):
            if "cpu_usage" in pod:
                # Parse CPU usage
                cpu_str = pod.get("cpu_usage", "0m")
                cpu_m = int(cpu_str.replace("m", "")) if cpu_str.endswith("m") else int(cpu_str) * 1000

                if cpu_m > 800:  # > 800m
                    recommendations["recommendations"].append({
                        "pod": pod["name"],
                        "type": "scale_up",
                        "reason": f"High CPU usage: {cpu_str}",
                        "action": "Consider increasing replicas or CPU limits"
                    })
                elif cpu_m < 100:  # < 100m
                    recommendations["recommendations"].append({
                        "pod": pod["name"],
                        "type": "scale_down",
                        "reason": f"Low CPU usage: {cpu_str}",
                        "action": "Consider reducing CPU requests"
                    })

        # Check deployment replicas
        result = await self._run_cmd(f"kubectl get deployments -n {ns} -o json")
        data = json.loads(result)

        for d in data.get("items", []):
            name = d.get("metadata", {}).get("name")
            replicas = d.get("spec", {}).get("replicas", 1)
            available = d.get("status", {}).get("availableReplicas", 0)

            if replicas == 1:
                recommendations["recommendations"].append({
                    "deployment": name,
                    "type": "high_availability",
                    "reason": "Single replica deployment",
                    "action": "Increase to at least 2 replicas for HA"
                })

        return recommendations

    async def _optimize_limits(self, deployment: str, namespace: str = None, buffer_percent: int = 20, **kwargs) -> Dict:
        ns = namespace or self.namespace

        optimization = {
            "deployment": deployment,
            "current": {},
            "recommended": {}
        }

        # Get current usage
        try:
            result = await self._run_cmd(f"kubectl top pods -n {ns} -l app={deployment}")
            lines = result.strip().split('\n')

            total_cpu = 0
            total_mem = 0
            count = 0

            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 3:
                    cpu_str = parts[1]
                    mem_str = parts[2]

                    cpu_m = int(cpu_str.replace("m", "")) if cpu_str.endswith("m") else int(cpu_str) * 1000
                    mem_mi = int(mem_str.replace("Mi", "")) if "Mi" in mem_str else int(mem_str.replace("Gi", "")) * 1024

                    total_cpu += cpu_m
                    total_mem += mem_mi
                    count += 1

            if count > 0:
                avg_cpu = total_cpu // count
                avg_mem = total_mem // count

                optimization["current"]["avg_cpu"] = f"{avg_cpu}m"
                optimization["current"]["avg_memory"] = f"{avg_mem}Mi"

                # Recommend with buffer
                rec_cpu = int(avg_cpu * (1 + buffer_percent / 100))
                rec_mem = int(avg_mem * (1 + buffer_percent / 100))

                optimization["recommended"]["cpu_request"] = f"{rec_cpu}m"
                optimization["recommended"]["cpu_limit"] = f"{rec_cpu * 2}m"
                optimization["recommended"]["memory_request"] = f"{rec_mem}Mi"
                optimization["recommended"]["memory_limit"] = f"{rec_mem * 2}Mi"

        except Exception as e:
            optimization["error"] = str(e)

        return optimization

    async def _apply_hpa(self, deployment: str, namespace: str = None, min_replicas: int = 2, max_replicas: int = 10, cpu_percent: int = 70, **kwargs) -> Dict:
        ns = namespace or self.namespace

        hpa = {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {
                "name": f"{deployment}-hpa",
                "namespace": ns
            },
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": deployment
                },
                "minReplicas": min_replicas,
                "maxReplicas": max_replicas,
                "metrics": [
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "cpu",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": cpu_percent
                            }
                        }
                    }
                ]
            }
        }

        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(hpa, f)
            temp_path = f.name

        try:
            await self._run_cmd(f"kubectl apply -f {temp_path}")
            return {
                "status": "applied",
                "hpa_name": f"{deployment}-hpa",
                "min_replicas": min_replicas,
                "max_replicas": max_replicas,
                "target_cpu": f"{cpu_percent}%"
            }
        finally:
            os.unlink(temp_path)

    async def _check_hpa(self, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        result = await self._run_cmd(f"kubectl get hpa -n {ns} -o json")
        data = json.loads(result)

        hpas = []
        for item in data.get("items", []):
            status = item.get("status", {})
            spec = item.get("spec", {})

            hpas.append({
                "name": item.get("metadata", {}).get("name"),
                "target": spec.get("scaleTargetRef", {}).get("name"),
                "min_replicas": spec.get("minReplicas"),
                "max_replicas": spec.get("maxReplicas"),
                "current_replicas": status.get("currentReplicas"),
                "desired_replicas": status.get("desiredReplicas"),
                "current_cpu": status.get("currentMetrics", [{}])[0].get("resource", {}).get("current", {}).get("averageUtilization")
            })

        return {"hpas": hpas}

    async def _find_bottlenecks(self, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        bottlenecks = {
            "namespace": ns,
            "issues": [],
            "severity": "low"
        }

        # Check resource usage
        try:
            result = await self._run_cmd(f"kubectl top pods -n {ns}")
            lines = result.strip().split('\n')

            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 3:
                    cpu_str = parts[1]
                    mem_str = parts[2]

                    cpu_m = int(cpu_str.replace("m", "")) if cpu_str.endswith("m") else int(cpu_str) * 1000

                    if cpu_m > 900:
                        bottlenecks["issues"].append({
                            "type": "cpu_saturation",
                            "pod": parts[0],
                            "value": cpu_str,
                            "severity": "high"
                        })
                        bottlenecks["severity"] = "high"

                    if "Gi" in mem_str:
                        mem_gi = float(mem_str.replace("Gi", ""))
                        if mem_gi > 1:
                            bottlenecks["issues"].append({
                                "type": "high_memory",
                                "pod": parts[0],
                                "value": mem_str,
                                "severity": "medium"
                            })
                            if bottlenecks["severity"] == "low":
                                bottlenecks["severity"] = "medium"

        except:
            bottlenecks["metrics_unavailable"] = True

        # Check for pending pods
        result = await self._run_cmd(f"kubectl get pods -n {ns} --field-selector=status.phase=Pending -o json")
        data = json.loads(result)

        if data.get("items"):
            bottlenecks["issues"].append({
                "type": "pending_pods",
                "count": len(data["items"]),
                "severity": "high"
            })
            bottlenecks["severity"] = "high"

        return bottlenecks

    async def _optimize_deployment(self, deployment: str, namespace: str = None, optimization_type: str = "all", **kwargs) -> Dict:
        ns = namespace or self.namespace

        optimizations_applied = []

        if optimization_type in ["resources", "all"]:
            # Get optimal limits
            limits = await self._optimize_limits(deployment=deployment, namespace=ns)

            if "recommended" in limits and limits["recommended"]:
                optimizations_applied.append({
                    "type": "resource_limits",
                    "recommended": limits["recommended"]
                })

        if optimization_type in ["replicas", "all"]:
            # Check if HPA exists
            hpa_status = await self._check_hpa(namespace=ns)

            hpa_exists = any(h["target"] == deployment for h in hpa_status.get("hpas", []))

            if not hpa_exists:
                optimizations_applied.append({
                    "type": "hpa",
                    "recommendation": "Apply HPA for auto-scaling",
                    "suggested_config": {
                        "min_replicas": 2,
                        "max_replicas": 10,
                        "target_cpu": "70%"
                    }
                })

        return {
            "deployment": deployment,
            "optimizations": optimizations_applied
        }

    async def _cost_analysis(self, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        analysis = {
            "namespace": ns,
            "resources": [],
            "potential_savings": []
        }

        # Get all deployments with resources
        result = await self._run_cmd(f"kubectl get deployments -n {ns} -o json")
        data = json.loads(result)

        for d in data.get("items", []):
            name = d.get("metadata", {}).get("name")
            replicas = d.get("spec", {}).get("replicas", 1)

            for c in d.get("spec", {}).get("template", {}).get("spec", {}).get("containers", []):
                resources = c.get("resources", {})
                requests = resources.get("requests", {})

                if requests:
                    analysis["resources"].append({
                        "deployment": name,
                        "container": c.get("name"),
                        "replicas": replicas,
                        "cpu_request": requests.get("cpu", "0"),
                        "memory_request": requests.get("memory", "0")
                    })

        # Check for over-provisioning
        resources_analysis = await self._analyze_resources(namespace=ns)

        for pod in resources_analysis.get("pods", []):
            if "cpu_usage" in pod and "requests" in pod:
                cpu_usage = pod.get("cpu_usage", "0m")
                cpu_request = pod.get("requests", {}).get("cpu", "0m")

                usage_m = int(cpu_usage.replace("m", "")) if cpu_usage.endswith("m") else 0
                request_m = int(cpu_request.replace("m", "")) if cpu_request.endswith("m") else 0

                if request_m > 0 and usage_m < request_m * 0.3:
                    analysis["potential_savings"].append({
                        "resource": pod.get("name", pod.get("deployment")),
                        "type": "cpu_over_provisioned",
                        "current": cpu_request,
                        "actual_usage": cpu_usage,
                        "recommendation": f"Reduce CPU request to {int(usage_m * 1.5)}m"
                    })

        return analysis

    async def _right_size(self, deployment: str = None, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        right_sizing = {
            "namespace": ns,
            "containers": []
        }

        # Get metrics
        try:
            result = await self._run_cmd(f"kubectl top pods -n {ns}")
            metrics = {}

            for line in result.strip().split('\n')[1:]:
                parts = line.split()
                if len(parts) >= 3:
                    pod_name = parts[0]

                    if deployment and deployment not in pod_name:
                        continue

                    cpu_str = parts[1]
                    mem_str = parts[2]

                    cpu_m = int(cpu_str.replace("m", "")) if cpu_str.endswith("m") else int(cpu_str) * 1000
                    mem_mi = int(mem_str.replace("Mi", "")) if "Mi" in mem_str else int(mem_str.replace("Gi", "")) * 1024

                    metrics[pod_name] = {"cpu": cpu_m, "memory": mem_mi}

            # Calculate right-sized values
            for pod, values in metrics.items():
                right_sizing["containers"].append({
                    "pod": pod,
                    "current_usage": {
                        "cpu": f"{values['cpu']}m",
                        "memory": f"{values['memory']}Mi"
                    },
                    "recommended_requests": {
                        "cpu": f"{int(values['cpu'] * 1.2)}m",
                        "memory": f"{int(values['memory'] * 1.2)}Mi"
                    },
                    "recommended_limits": {
                        "cpu": f"{int(values['cpu'] * 2)}m",
                        "memory": f"{int(values['memory'] * 2)}Mi"
                    }
                })

        except Exception as e:
            right_sizing["error"] = str(e)

        return right_sizing

    async def _performance_report(self, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        report = {
            "namespace": ns,
            "timestamp": None,
            "summary": {},
            "details": {}
        }

        # Resource analysis
        self.log("Analyzing resources...", "step")
        report["details"]["resources"] = await self._analyze_resources(namespace=ns)

        # Bottlenecks
        self.log("Finding bottlenecks...", "step")
        report["details"]["bottlenecks"] = await self._find_bottlenecks(namespace=ns)

        # Scaling recommendations
        self.log("Getting scaling recommendations...", "step")
        report["details"]["scaling"] = await self._get_scaling_recommendations(namespace=ns)

        # Cost analysis
        self.log("Analyzing costs...", "step")
        report["details"]["cost"] = await self._cost_analysis(namespace=ns)

        # Generate summary
        bottleneck_count = len(report["details"]["bottlenecks"].get("issues", []))
        recommendation_count = len(report["details"]["scaling"].get("recommendations", []))
        savings_count = len(report["details"]["cost"].get("potential_savings", []))

        report["summary"] = {
            "health": "healthy" if bottleneck_count == 0 else "needs_attention",
            "bottlenecks_found": bottleneck_count,
            "scaling_recommendations": recommendation_count,
            "cost_optimization_opportunities": savings_count,
            "overall_score": 100 - (bottleneck_count * 10) - (savings_count * 5)
        }

        return report

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
        if "resource" in query or "analyze" in query:
            return await self._analyze_resources()
        elif "scaling" in query or "recommendation" in query:
            return await self._get_scaling_recommendations()
        elif "limit" in query:
            return await self._optimize_limits()
        elif "hpa" in query:
            return await self._check_hpa()
        elif "bottleneck" in query:
            return await self._find_bottlenecks()
        elif "optimize" in query and "deployment" in query:
            return await self._optimize_deployment()
        elif "cost" in query:
            return await self._cost_analysis()
        elif "size" in query or "right" in query:
            return await self._right_size()
        elif "performance" in query or "report" in query:
            return await self._performance_report()

        return {"status": "no action taken", "query": query}
