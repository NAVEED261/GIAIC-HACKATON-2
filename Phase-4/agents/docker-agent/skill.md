# Docker Agent - Expertise & Skills

## Agent Identity

**Name**: Docker Agent
**Domain**: Containerization & Docker Operations
**Phase**: Phase-4 (Kubernetes Deployment)

---

## Core Expertise

### 1. Dockerfile Creation

#### Multi-Stage Builds
```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
EXPOSE 3000
CMD ["npm", "start"]
```

#### Best Practices
- Use specific base image tags (not `latest`)
- Minimize layers with combined RUN commands
- Use `.dockerignore` to exclude unnecessary files
- Copy dependency files first for better caching
- Use non-root users for security
- Add health checks

### 2. Image Optimization

#### Size Reduction Techniques
- Use Alpine-based images
- Multi-stage builds to exclude dev dependencies
- Remove cache after package installation
- Use `--no-cache` for apk/apt

#### Layer Optimization
```dockerfile
# Bad: Multiple layers
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get clean

# Good: Single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Docker Compose

#### Development Configuration
```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 4. Docker AI (Gordon) Integration

#### Common Commands
```bash
# Generate Dockerfile
docker ai "create a Dockerfile for Next.js production app"

# Optimize existing Dockerfile
docker ai "optimize this Dockerfile for smaller image size"

# Troubleshoot build
docker ai "why is my Docker build failing with this error"

# Security scan
docker ai "check this image for security vulnerabilities"
```

---

## Specialized Knowledge

### Frontend Containerization (Next.js)

```dockerfile
# Optimized Next.js Dockerfile
FROM node:18-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
```

### Backend Containerization (FastAPI/Python)

```dockerfile
# Optimized FastAPI Dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Security: non-root user
RUN adduser --disabled-password --gecos "" appuser

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Common Patterns

### Health Checks
```dockerfile
# HTTP health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Process health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD pgrep -x node || exit 1
```

### Environment Variables
```dockerfile
# Build-time variables
ARG NODE_ENV=production
ARG API_URL

# Runtime variables
ENV NODE_ENV=${NODE_ENV}
ENV NEXT_PUBLIC_API_URL=${API_URL}
```

### Volume Mounts (Development)
```yaml
volumes:
  - ./src:/app/src           # Source code
  - /app/node_modules        # Prevent overwrite
  - ./public:/app/public     # Static assets
```

---

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Build fails on npm install | Missing deps | Add build tools to base image |
| Large image size | Dev dependencies | Use multi-stage builds |
| Container crashes | Missing env vars | Define all required ENV |
| Port not accessible | Wrong EXPOSE | Match EXPOSE with CMD port |
| Permission denied | Root user issues | Use non-root user |

### Debug Commands
```bash
# Check image layers
docker history <image>

# Inspect image
docker inspect <image>

# Run shell in container
docker run -it --rm <image> sh

# View build logs
docker build --progress=plain .

# Check container logs
docker logs <container>
```

---

## Integration with Phase-4

### Responsibilities
1. Create Dockerfiles for frontend and backend
2. Optimize images for Kubernetes deployment
3. Configure health checks for K8s probes
4. Set up environment variable handling
5. Integrate with Docker AI (Gordon)

### Handoff to Kubernetes Agent
- Provide image names and tags
- Document exposed ports
- Document health check endpoints
- Document required environment variables

---

## References

- Docker Documentation: https://docs.docker.com
- Dockerfile Best Practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- Docker Compose: https://docs.docker.com/compose/
- Docker AI (Gordon): https://docs.docker.com/ai/

---

**Status**: Active
**Last Updated**: Phase-4 Initialization
