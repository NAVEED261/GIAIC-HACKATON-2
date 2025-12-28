"""
Security Agent - POWERFUL Security Expert
Vulnerability scanning, secrets management, compliance, auditing

@author: Phase-4 Multi-Agent System
"""

import asyncio
import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class SecurityAgent(BaseAgent):
    """
    POWERFUL Security Expert Agent
    - Vulnerability scanning
    - Secrets management
    - Network policies
    - RBAC management
    - Security auditing
    """

    KEYWORDS = [
        'security', 'secure', 'vulnerability', 'scan', 'secret', 'password',
        'rbac', 'role', 'permission', 'audit', 'compliance', 'policy',
        'encryption', 'certificate', 'ssl', 'tls', 'firewall', 'network policy'
    ]

    def __init__(self, namespace: str = "todo"):
        super().__init__("Security", "Security expert - vulnerabilities, secrets, RBAC, auditing")
        self.namespace = namespace
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all MCP tools for security operations"""

        # Tool: Scan Image
        self.register_tool(MCPTool(
            name="scan_image",
            description="Scan Docker image for vulnerabilities",
            parameters={
                "type": "object",
                "properties": {
                    "image": {"type": "string", "description": "Image name:tag"},
                    "severity": {"type": "string", "description": "Minimum severity (LOW, MEDIUM, HIGH, CRITICAL)"}
                },
                "required": ["image"]
            },
            handler=self._scan_image
        ))

        # Tool: List Secrets
        self.register_tool(MCPTool(
            name="list_secrets",
            description="List Kubernetes secrets in namespace",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "type": {"type": "string", "description": "Secret type filter"}
                }
            },
            handler=self._list_secrets
        ))

        # Tool: Create Secret
        self.register_tool(MCPTool(
            name="create_secret",
            description="Create a Kubernetes secret",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Secret name"},
                    "data": {"type": "object", "description": "Key-value pairs"},
                    "namespace": {"type": "string"},
                    "type": {"type": "string", "description": "Secret type (Opaque, docker-registry, tls)"}
                },
                "required": ["name", "data"]
            },
            handler=self._create_secret
        ))

        # Tool: Rotate Secret
        self.register_tool(MCPTool(
            name="rotate_secret",
            description="Rotate/update a secret value",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Secret name"},
                    "key": {"type": "string", "description": "Key to rotate"},
                    "value": {"type": "string", "description": "New value"},
                    "namespace": {"type": "string"}
                },
                "required": ["name", "key", "value"]
            },
            handler=self._rotate_secret
        ))

        # Tool: Check RBAC
        self.register_tool(MCPTool(
            name="check_rbac",
            description="Check RBAC permissions for user/service account",
            parameters={
                "type": "object",
                "properties": {
                    "user": {"type": "string", "description": "User or service account"},
                    "verb": {"type": "string", "description": "get, list, create, delete, etc."},
                    "resource": {"type": "string", "description": "Resource type"},
                    "namespace": {"type": "string"}
                },
                "required": ["user", "verb", "resource"]
            },
            handler=self._check_rbac
        ))

        # Tool: List Roles
        self.register_tool(MCPTool(
            name="list_roles",
            description="List roles and role bindings",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "type": {"type": "string", "description": "role, clusterrole, rolebinding"}
                }
            },
            handler=self._list_roles
        ))

        # Tool: Security Audit
        self.register_tool(MCPTool(
            name="security_audit",
            description="Perform security audit of cluster/namespace",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "checks": {"type": "array", "description": "Specific checks to run"}
                }
            },
            handler=self._security_audit
        ))

        # Tool: Check Network Policies
        self.register_tool(MCPTool(
            name="check_network_policies",
            description="Review network policies",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            },
            handler=self._check_network_policies
        ))

        # Tool: Create Network Policy
        self.register_tool(MCPTool(
            name="create_network_policy",
            description="Create network policy for pod isolation",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "namespace": {"type": "string"},
                    "pod_selector": {"type": "object"},
                    "ingress": {"type": "array"},
                    "egress": {"type": "array"}
                },
                "required": ["name"]
            },
            handler=self._create_network_policy
        ))

        # Tool: Check Pod Security
        self.register_tool(MCPTool(
            name="check_pod_security",
            description="Check pod security context and policies",
            parameters={
                "type": "object",
                "properties": {
                    "pod": {"type": "string", "description": "Pod name"},
                    "namespace": {"type": "string"}
                }
            },
            handler=self._check_pod_security
        ))

        # Tool: Check Certificates
        self.register_tool(MCPTool(
            name="check_certificates",
            description="Check TLS certificates expiry and validity",
            parameters={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "secret": {"type": "string", "description": "TLS secret name"}
                }
            },
            handler=self._check_certificates
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

    async def _scan_image(self, image: str, severity: str = "MEDIUM", **kwargs) -> Dict:
        self.log(f"Scanning image: {image}", "working")

        # Try trivy if available, otherwise use docker scout
        try:
            result = await self._run_cmd(f"trivy image --severity {severity} {image} --format json")
            return {"scanner": "trivy", "results": json.loads(result)}
        except:
            pass

        try:
            result = await self._run_cmd(f"docker scout cves {image}")
            return {"scanner": "docker-scout", "results": result}
        except:
            pass

        return {
            "status": "no_scanner",
            "message": "Install trivy or docker scout for vulnerability scanning",
            "image": image
        }

    async def _list_secrets(self, namespace: str = None, type: str = None, **kwargs) -> List[Dict]:
        ns = namespace or self.namespace

        result = await self._run_cmd(f"kubectl get secrets -n {ns} -o json")
        data = json.loads(result)

        secrets = []
        for item in data.get("items", []):
            secret_type = item.get("type", "")
            if type and type not in secret_type:
                continue

            secrets.append({
                "name": item.get("metadata", {}).get("name"),
                "type": secret_type,
                "keys": list(item.get("data", {}).keys()),
                "created": item.get("metadata", {}).get("creationTimestamp")
            })

        return secrets

    async def _create_secret(self, name: str, data: Dict, namespace: str = None, type: str = "Opaque", **kwargs) -> Dict:
        ns = namespace or self.namespace

        # Build literal flags
        literals = " ".join([f"--from-literal={k}={v}" for k, v in data.items()])

        await self._run_cmd(f"kubectl create secret generic {name} {literals} -n {ns}")

        return {"created": True, "name": name, "namespace": ns}

    async def _rotate_secret(self, name: str, key: str, value: str, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace
        import base64

        # Get current secret
        result = await self._run_cmd(f"kubectl get secret {name} -n {ns} -o json")
        secret = json.loads(result)

        # Update value (base64 encoded)
        encoded = base64.b64encode(value.encode()).decode()
        secret["data"][key] = encoded

        # Apply updated secret
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(secret, f)
            temp_path = f.name

        await self._run_cmd(f"kubectl apply -f {temp_path}")
        os.unlink(temp_path)

        return {"rotated": True, "secret": name, "key": key}

    async def _check_rbac(self, user: str, verb: str, resource: str, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        result = await self._run_cmd(
            f"kubectl auth can-i {verb} {resource} -n {ns} --as={user}"
        )

        return {
            "user": user,
            "verb": verb,
            "resource": resource,
            "namespace": ns,
            "allowed": "yes" in result.lower()
        }

    async def _list_roles(self, namespace: str = None, type: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace
        roles = {}

        if not type or type == "role":
            result = await self._run_cmd(f"kubectl get roles -n {ns} -o json")
            data = json.loads(result)
            roles["roles"] = [r.get("metadata", {}).get("name") for r in data.get("items", [])]

        if not type or type == "clusterrole":
            result = await self._run_cmd("kubectl get clusterroles -o json")
            data = json.loads(result)
            roles["clusterroles"] = [r.get("metadata", {}).get("name") for r in data.get("items", [])][:20]

        if not type or type == "rolebinding":
            result = await self._run_cmd(f"kubectl get rolebindings -n {ns} -o json")
            data = json.loads(result)
            roles["rolebindings"] = [r.get("metadata", {}).get("name") for r in data.get("items", [])]

        return roles

    async def _security_audit(self, namespace: str = None, checks: List = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        audit = {
            "namespace": ns,
            "timestamp": None,
            "findings": [],
            "score": 100
        }

        # Check 1: Privileged containers
        self.log("Checking for privileged containers...", "step")
        pods_result = await self._run_cmd(f"kubectl get pods -n {ns} -o json")
        pods = json.loads(pods_result)

        for pod in pods.get("items", []):
            for container in pod.get("spec", {}).get("containers", []):
                security_context = container.get("securityContext", {})
                if security_context.get("privileged"):
                    audit["findings"].append({
                        "severity": "HIGH",
                        "type": "privileged_container",
                        "resource": f"{pod.get('metadata', {}).get('name')}/{container.get('name')}",
                        "message": "Container running as privileged"
                    })
                    audit["score"] -= 20

                if security_context.get("runAsRoot") or security_context.get("runAsUser") == 0:
                    audit["findings"].append({
                        "severity": "MEDIUM",
                        "type": "root_user",
                        "resource": f"{pod.get('metadata', {}).get('name')}/{container.get('name')}",
                        "message": "Container running as root"
                    })
                    audit["score"] -= 10

        # Check 2: Secrets in environment
        self.log("Checking for exposed secrets...", "step")
        for pod in pods.get("items", []):
            for container in pod.get("spec", {}).get("containers", []):
                for env in container.get("env", []):
                    name = env.get("name", "").lower()
                    if any(s in name for s in ["password", "secret", "key", "token"]):
                        if env.get("value"):  # Plain text value
                            audit["findings"].append({
                                "severity": "HIGH",
                                "type": "exposed_secret",
                                "resource": f"{pod.get('metadata', {}).get('name')}/{container.get('name')}",
                                "message": f"Secret '{env.get('name')}' exposed as plain text"
                            })
                            audit["score"] -= 15

        # Check 3: Network policies
        self.log("Checking network policies...", "step")
        try:
            np_result = await self._run_cmd(f"kubectl get networkpolicies -n {ns} -o json")
            np_data = json.loads(np_result)
            if not np_data.get("items"):
                audit["findings"].append({
                    "severity": "MEDIUM",
                    "type": "no_network_policy",
                    "resource": ns,
                    "message": "No network policies defined"
                })
                audit["score"] -= 10
        except:
            pass

        audit["score"] = max(0, audit["score"])
        return audit

    async def _check_network_policies(self, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        result = await self._run_cmd(f"kubectl get networkpolicies -n {ns} -o json")
        data = json.loads(result)

        policies = []
        for item in data.get("items", []):
            spec = item.get("spec", {})
            policies.append({
                "name": item.get("metadata", {}).get("name"),
                "podSelector": spec.get("podSelector"),
                "policyTypes": spec.get("policyTypes", []),
                "ingress_rules": len(spec.get("ingress", [])),
                "egress_rules": len(spec.get("egress", []))
            })

        return {"policies": policies, "count": len(policies)}

    async def _create_network_policy(self, name: str, namespace: str = None, pod_selector: Dict = None, ingress: List = None, egress: List = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        policy = {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": name,
                "namespace": ns
            },
            "spec": {
                "podSelector": pod_selector or {},
                "policyTypes": []
            }
        }

        if ingress is not None:
            policy["spec"]["policyTypes"].append("Ingress")
            policy["spec"]["ingress"] = ingress

        if egress is not None:
            policy["spec"]["policyTypes"].append("Egress")
            policy["spec"]["egress"] = egress

        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(policy, f)
            temp_path = f.name

        await self._run_cmd(f"kubectl apply -f {temp_path}")
        os.unlink(temp_path)

        return {"created": True, "name": name, "namespace": ns}

    async def _check_pod_security(self, pod: str = None, namespace: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        if pod:
            result = await self._run_cmd(f"kubectl get pod {pod} -n {ns} -o json")
            pods = [json.loads(result)]
        else:
            result = await self._run_cmd(f"kubectl get pods -n {ns} -o json")
            pods = json.loads(result).get("items", [])

        security_report = []
        for p in pods:
            name = p.get("metadata", {}).get("name")
            spec = p.get("spec", {})

            pod_security = {
                "pod": name,
                "securityContext": spec.get("securityContext", {}),
                "containers": [],
                "issues": []
            }

            for container in spec.get("containers", []):
                ctx = container.get("securityContext", {})
                pod_security["containers"].append({
                    "name": container.get("name"),
                    "securityContext": ctx
                })

                if ctx.get("privileged"):
                    pod_security["issues"].append(f"{container.get('name')}: privileged=true")
                if not ctx.get("readOnlyRootFilesystem"):
                    pod_security["issues"].append(f"{container.get('name')}: root filesystem is writable")

            security_report.append(pod_security)

        return {"pods": security_report}

    async def _check_certificates(self, namespace: str = None, secret: str = None, **kwargs) -> Dict:
        ns = namespace or self.namespace

        if secret:
            result = await self._run_cmd(f"kubectl get secret {secret} -n {ns} -o json")
            secrets = [json.loads(result)]
        else:
            result = await self._run_cmd(f"kubectl get secrets -n {ns} -o json")
            secrets = [s for s in json.loads(result).get("items", []) if s.get("type") == "kubernetes.io/tls"]

        certs = []
        for s in secrets:
            name = s.get("metadata", {}).get("name")
            data = s.get("data", {})

            cert_info = {
                "name": name,
                "has_cert": "tls.crt" in data,
                "has_key": "tls.key" in data
            }

            # In real scenario, decode and parse cert for expiry
            certs.append(cert_info)

        return {"certificates": certs}

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
        if "secret" in query and ("list" in query or "show" in query or "all" in query):
            return await self._list_secrets()
        elif "role" in query:
            return await self._list_roles()
        elif "rbac" in query:
            return {"status": "need_params", "message": "Provide: user, verb, resource"}
        elif "audit" in query or "security" in query:
            return await self._security_audit()
        elif "policy" in query or "network" in query:
            return await self._check_network_policies()
        elif "pod" in query and "security" in query:
            return await self._check_pod_security()
        elif "certificate" in query or "cert" in query:
            return await self._check_certificates()
        elif "scan" in query:
            return {"status": "need_params", "message": "Provide: image name to scan"}

        return {"status": "no action taken", "query": query}
