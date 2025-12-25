# Helm Agent - Expertise & Skills

## Agent Identity

**Name**: Helm Agent
**Domain**: Kubernetes Package Management
**Phase**: Phase-4 (Kubernetes Deployment)

---

## Core Expertise

### 1. Helm Architecture

#### Components
```
┌─────────────────────────────────────────────────────────┐
│                      Helm Client                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ helm install│  │ helm upgrade │  │ helm rollback │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    Kubernetes API                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Release Management                  │   │
│  │  (Stored as Secrets in cluster)                 │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 2. Chart Structure

```
my-chart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── charts/             # Dependent charts
├── templates/          # Kubernetes manifest templates
│   ├── NOTES.txt       # Post-install instructions
│   ├── _helpers.tpl    # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
├── .helmignore         # Files to ignore
└── README.md           # Chart documentation
```

---

## Chart Configuration

### Chart.yaml
```yaml
apiVersion: v2
name: todo-frontend
description: Todo Application Frontend
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - frontend
  - nextjs
maintainers:
  - name: Phase-4 Team
    email: team@example.com
dependencies: []
```

### values.yaml (Frontend)
```yaml
# Image configuration
image:
  repository: todo-frontend
  tag: "v1"
  pullPolicy: IfNotPresent

# Replica count
replicaCount: 2

# Container port
containerPort: 3000

# Service configuration
service:
  type: NodePort
  port: 80
  nodePort: 30080

# Resource limits
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"

# Environment configuration
config:
  nodeEnv: "production"
  apiUrl: "http://todo-backend-service:8000"

# Health checks
healthCheck:
  path: "/"
  initialDelaySeconds: 30
  periodSeconds: 10
```

### values.yaml (Backend)
```yaml
# Image configuration
image:
  repository: todo-backend
  tag: "v1"
  pullPolicy: IfNotPresent

# Replica count
replicaCount: 2

# Container port
containerPort: 8000

# Service configuration
service:
  type: NodePort
  port: 8000
  nodePort: 30800

# Resource limits
resources:
  requests:
    cpu: "100m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"

# Environment configuration
config:
  pythonEnv: "production"
  corsOrigins: "*"

# Secrets (provide at install time)
secrets:
  anthropicApiKey: ""
  openaiApiKey: ""

# Health checks
healthCheck:
  path: "/health"
  initialDelaySeconds: 15
  periodSeconds: 10
```

---

## Template Patterns

### _helpers.tpl
```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "todo.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo.labels" -}}
helm.sh/chart: {{ include "todo.chart" . }}
{{ include "todo.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Chart name and version
*/}}
{{- define "todo.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}
```

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo.fullname" . }}
  labels:
    {{- include "todo.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "todo.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.containerPort }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: {{ .Values.healthCheck.path }}
              port: http
            initialDelaySeconds: {{ .Values.healthCheck.initialDelaySeconds }}
            periodSeconds: {{ .Values.healthCheck.periodSeconds }}
          readinessProbe:
            httpGet:
              path: {{ .Values.healthCheck.path }}
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          envFrom:
            - configMapRef:
                name: {{ include "todo.fullname" . }}-config
            {{- if .Values.secrets }}
            - secretRef:
                name: {{ include "todo.fullname" . }}-secrets
            {{- end }}
```

### service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo.fullname" . }}-service
  labels:
    {{- include "todo.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
      {{- if and (eq .Values.service.type "NodePort") .Values.service.nodePort }}
      nodePort: {{ .Values.service.nodePort }}
      {{- end }}
  selector:
    {{- include "todo.selectorLabels" . | nindent 4 }}
```

### configmap.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "todo.fullname" . }}-config
  labels:
    {{- include "todo.labels" . | nindent 4 }}
data:
  {{- range $key, $value := .Values.config }}
  {{ $key | upper }}: {{ $value | quote }}
  {{- end }}
```

### secret.yaml
```yaml
{{- if .Values.secrets }}
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "todo.fullname" . }}-secrets
  labels:
    {{- include "todo.labels" . | nindent 4 }}
type: Opaque
data:
  {{- range $key, $value := .Values.secrets }}
  {{- if $value }}
  {{ $key | upper }}: {{ $value | b64enc | quote }}
  {{- end }}
  {{- end }}
{{- end }}
```

---

## Helm Commands

### Chart Development
```bash
# Create new chart
helm create todo-frontend

# Lint chart
helm lint ./todo-frontend

# Template (dry run)
helm template my-release ./todo-frontend

# Package chart
helm package ./todo-frontend
```

### Chart Installation
```bash
# Install chart
helm install todo-frontend ./helm-charts/todo-frontend -n todo

# Install with values
helm install todo-frontend ./helm-charts/todo-frontend \
  -n todo \
  --set replicaCount=3 \
  --set image.tag=v2

# Install from values file
helm install todo-frontend ./helm-charts/todo-frontend \
  -n todo \
  -f custom-values.yaml
```

### Release Management
```bash
# List releases
helm list -n todo

# Get release status
helm status todo-frontend -n todo

# Upgrade release
helm upgrade todo-frontend ./helm-charts/todo-frontend -n todo

# Rollback
helm rollback todo-frontend 1 -n todo

# Uninstall
helm uninstall todo-frontend -n todo
```

### Debugging
```bash
# Dry run with debug
helm install todo-frontend ./helm-charts/todo-frontend \
  -n todo \
  --dry-run \
  --debug

# Get release history
helm history todo-frontend -n todo

# Get values used
helm get values todo-frontend -n todo

# Get all release info
helm get all todo-frontend -n todo
```

---

## Best Practices

### 1. Version Management
```yaml
# Chart.yaml
version: 1.0.0      # Chart version (update on chart changes)
appVersion: "1.0.0" # App version (update on app changes)
```

### 2. Default Values
- Provide sensible defaults in values.yaml
- Document all values
- Use comments for clarification

### 3. Template Safety
```yaml
# Always quote strings
value: {{ .Values.name | quote }}

# Use default for optional values
value: {{ .Values.optional | default "default-value" }}

# Check if value exists
{{- if .Values.ingress.enabled }}
# ingress config
{{- end }}
```

### 4. Resource Naming
```yaml
# Use release name in resource names
name: {{ include "todo.fullname" . }}

# Truncate to 63 chars (K8s limit)
name: {{ .Release.Name | trunc 63 }}
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Template error | Invalid YAML | Use `helm lint` |
| Values not applied | Wrong path | Check values structure |
| Release stuck | Failed hooks | `helm rollback` |
| Resource exists | Previous release | Use `--replace` |

### Debug Commands
```bash
# Check template output
helm template test ./chart --debug

# Lint with strict
helm lint ./chart --strict

# Check release status
helm status release-name -n namespace

# Get manifest
helm get manifest release-name -n namespace
```

---

## Integration with Phase-4

### Responsibilities
1. Create Helm charts for frontend and backend
2. Configure values.yaml with proper defaults
3. Create reusable templates
4. Handle secrets securely
5. Enable easy upgrades and rollbacks

### Input from Kubernetes Agent
- Resource specifications
- Health check paths
- Service types

### Output
- Deployable Helm charts
- values.yaml for customization
- Installation instructions

---

## References

- Helm Documentation: https://helm.sh/docs
- Chart Best Practices: https://helm.sh/docs/chart_best_practices/
- Template Functions: https://helm.sh/docs/chart_template_guide/function_list/
- Helm Hub: https://artifacthub.io

---

**Status**: Active
**Last Updated**: Phase-4 Initialization
