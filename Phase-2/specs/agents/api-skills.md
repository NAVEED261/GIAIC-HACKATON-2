# API Agent Skills

**Agent Name**: API Agent (REST API Design Specialist)
**Domain**: API - REST Endpoint Architecture & Contracts
**Total Skills**: 10 Core + 7 Advanced

---

## Core Skills (Essential for Phase-2)

### 1. REST Principles & Design

**Purpose**: Design APIs following REST principles and best practices

**Example Query**: "Design endpoints for task resource following REST"

**Expected Action**:
- Use resource-based URLs (/api/tasks, /api/users)
- Map HTTP methods correctly (GET, POST, PUT, PATCH, DELETE)
- Design for consistency
- Follow naming conventions
- Document principles

**Technical Skills**:
- REST principles
- Resource modeling
- HTTP method mapping
- URL design
- Consistency patterns

---

### 2. HTTP Status Code Selection

**Purpose**: Return appropriate HTTP status codes for different scenarios

**Example Query**: "What status code for task creation?"

**Expected Action**:
- Return 201 for resource creation
- Return 200 for successful GET/PUT
- Return 204 for DELETE
- Return 400 for bad request
- Return 401 for unauthorized
- Return 403 for forbidden
- Return 404 for not found
- Return 422 for validation errors
- Return 500 for server errors

**Technical Skills**:
- Status code semantics
- Success responses (2xx)
- Client errors (4xx)
- Server errors (5xx)
- Proper selection

---

### 3. Request & Response Formatting

**Purpose**: Define consistent request and response formats

**Example Query**: "Define request/response format for task creation"

**Expected Action**:
- Define request body structure
- Define response body structure
- Use JSON format
- Include metadata
- Document examples

**Technical Skills**:
- JSON structure
- Request body design
- Response body design
- Field naming conventions
- Data structure examples

---

### 4. Error Response Standardization

**Purpose**: Return consistent error responses

**Example Query**: "Define error response format"

**Expected Action**:
- Include error code
- Include error message
- Include error details
- Include timestamp
- Include request ID

**Technical Skills**:
- Error schema design
- Error codes
- Error messages
- Structured errors
- Error documentation

---

### 5. Pagination Design

**Purpose**: Design pagination for list endpoints

**Example Query**: "Design pagination for task list"

**Expected Action**:
- Support page and limit parameters
- Return total count
- Return page info
- Support different sort orders
- Document pagination

**Technical Skills**:
- Pagination parameters
- Offset/limit
- Cursor pagination (optional)
- Sort parameters
- Response metadata

---

### 6. Query Parameter Design

**Purpose**: Design query parameters for filtering and sorting

**Example Query**: "Design query parameters for task filtering"

**Expected Action**:
- Support status filter
- Support sorting (created_at, title)
- Support search
- Validate parameters
- Document all parameters

**Technical Skills**:
- Filter parameters
- Sort parameters
- Search parameters
- Parameter validation
- Documentation

---

### 7. Path Parameter Design

**Purpose**: Design path parameters for resource identification

**Example Query**: "Design path for getting specific task"

**Expected Action**:
- Use resource ID in path
- Use resource hierarchy
- Keep paths simple
- Validate path parameters
- Document examples

**Technical Skills**:
- Path design
- ID handling
- Path hierarchy
- Validation
- Examples

---

### 8. Authentication Header Design

**Purpose**: Define how to pass authentication tokens

**Example Query**: "How should clients send JWT tokens?"

**Expected Action**:
- Use Authorization header
- Use Bearer token format
- Document token format
- Handle missing/invalid tokens
- Provide examples

**Technical Skills**:
- Header design
- Bearer tokens
- Token format
- Examples
- Error handling

---

### 9. API Documentation with OpenAPI

**Purpose**: Generate machine-readable API documentation

**Example Query**: "Generate OpenAPI documentation for all endpoints"

**Expected Action**:
- Create OpenAPI spec
- Document all endpoints
- Document request/response
- Include examples
- Enable Swagger UI

**Technical Skills**:
- OpenAPI 3.0 spec
- Endpoint documentation
- Schema definitions
- Examples
- Swagger UI integration

---

### 10. Versioning Strategy

**Purpose**: Plan API versioning for future compatibility

**Example Query**: "Plan API versioning strategy"

**Expected Action**:
- Choose versioning approach (URL or header)
- Document versioning policy
- Plan deprecation
- Support multiple versions
- Provide migration guide

**Technical Skills**:
- Versioning approaches
- URL versioning (v1, v2)
- Header versioning
- Deprecation planning
- Backward compatibility

---

## Advanced Skills (Optional for Phase-2)

### 11. Rate Limiting Policy

**Purpose**: Design rate limiting to prevent abuse

**Example Query**: "Design rate limits for different endpoints"

**Technical Skills**: Rate limit rules, header design, quota management

---

### 12. HATEOAS Links (Hypermedia)

**Purpose**: Include links in responses for discoverability

**Example Query**: "Add HATEOAS links to task response"

**Technical Skills**: Link design, self-links, related resources, navigation

---

### 13. Content Negotiation

**Purpose**: Support multiple content types (JSON, XML, etc.)

**Example Query**: "Support both JSON and XML responses"

**Technical Skills**: Content-Type handling, Accept headers, format negotiation

---

### 14. Caching Headers

**Purpose**: Include cache control headers for optimization

**Example Query**: "Add cache headers to task list endpoint"

**Technical Skills**: Cache-Control, ETag, Last-Modified, Conditional requests

---

### 15. CORS Configuration

**Purpose**: Configure Cross-Origin Resource Sharing

**Example Query**: "Allow frontend at localhost:3000 to call API"

**Technical Skills**: CORS headers, origin validation, preflight requests

---

### 16. Webhook Design

**Purpose**: Design webhooks for event notifications

**Example Query**: "Design webhook for task completion events"

**Technical Skills**: Webhook payload design, delivery retry, signature verification

---

### 17. GraphQL Design (Optional)

**Purpose**: Design GraphQL alternative to REST

**Example Query**: "Design GraphQL schema for tasks"

**Technical Skills**: GraphQL schema, resolvers, queries, mutations

---

## Skill Composition Example

### Task List Endpoint Design
```
1. Design endpoint path (Skill #7: /api/tasks)
2. Select HTTP method (Skill #1: GET)
3. Design query parameters (Skill #6: page, limit, status, sort)
4. Design response format (Skill #3: data array + pagination)
5. Select status codes (Skill #2: 200, 400, 401, 403)
6. Design pagination (Skill #5: page, limit, total)
7. Design error response (Skill #4: error code, message)
8. Document in OpenAPI (Skill #9: Swagger docs)
9. Test endpoint (Skill #18: Testing)
```

### Task Creation Endpoint Design
```
1. Design endpoint (Skill #7: POST /api/tasks)
2. Design request body (Skill #3: title, description)
3. Design response (Skill #3: created task)
4. Select status code (Skill #2: 201 Created)
5. Design validation errors (Skill #4: 422)
6. Add auth header (Skill #8: Bearer token)
7. Include error handling (Skill #4: 400, 401, 403)
8. Document in OpenAPI (Skill #9: Swagger)
9. Test endpoint (Skill #18: Testing)
```

---

## Skill Dependencies

```
REST Principles (#1)
    ├─ Path Parameter Design (#7)
    ├─ Request/Response Format (#3)
    └─ Documentation (#9)

HTTP Status Codes (#2)
    ├─ Error Responses (#4)
    ├─ Success Responses
    └─ Documentation (#9)

Request/Response Format (#3)
    ├─ Pagination Design (#5)
    ├─ Query Parameters (#6)
    ├─ Error Responses (#4)
    └─ Documentation (#9)

Error Responses (#4)
    ├─ Status Codes (#2)
    ├─ Documentation (#9)
    └─ Testing

Pagination Design (#5)
    ├─ Query Parameters (#6)
    ├─ Request/Response Format (#3)
    └─ Documentation (#9)

Query Parameters (#6)
    ├─ Validation
    ├─ Documentation (#9)
    └─ Examples

Path Parameters (#7)
    ├─ REST Principles (#1)
    ├─ Validation
    └─ Documentation (#9)

Authentication (#8)
    ├─ Documentation (#9)
    ├─ Examples
    └─ Testing

OpenAPI Documentation (#9)
    ├─ REST Principles (#1)
    ├─ All other skills
    └─ Swagger UI

Versioning (#10)
    ├─ Backward Compatibility
    ├─ Migration Guide
    └─ Documentation (#9)
```

---

## Guardrails

### Must Do
- ✅ Use resource-based URLs
- ✅ Map HTTP methods correctly
- ✅ Return appropriate status codes
- ✅ Return consistent error responses
- ✅ Document all endpoints
- ✅ Support pagination for lists
- ✅ Require authentication for protected endpoints
- ✅ Include timestamps in responses

### Must Not Do
- ❌ Use verbs in URLs (use nouns)
- ❌ Use GET for mutating operations
- ❌ Return inconsistent error formats
- ❌ Expose internal error messages
- ❌ Leave endpoints undocumented
- ❌ Hardcode API URLs in client
- ❌ Return sensitive data in responses
- ❌ Use lowercase only (use camelCase or snake_case consistently)

### Out of Scope
- SOAP/XML APIs (REST only)
- Custom binary protocols
- Protocol Buffers (Phase-3+)
- Extremely high-performance RPC (Phase-5+)

---

## API Design Checklist

- [ ] All endpoints follow REST principles
- [ ] Correct HTTP methods used
- [ ] Appropriate status codes returned
- [ ] Error responses consistent
- [ ] Pagination implemented for lists
- [ ] Query parameters documented
- [ ] Path parameters validated
- [ ] Authentication required on protected routes
- [ ] OpenAPI spec generated
- [ ] Swagger UI accessible
- [ ] All endpoints in documentation
- [ ] Examples provided
- [ ] Versioning strategy defined
- [ ] Rate limiting policy defined
- [ ] CORS configured

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **API Documentation** | 100% of endpoints documented |
| **OpenAPI Compliance** | 100% |
| **Endpoint Consistency** | High (naming, format, codes) |
| **Error Response Format** | Consistent |
| **Test Coverage** | ≥ 80% of endpoints |
| **Response Time** | < 500ms (p95) |

---

## Configuration Reference

### OpenAPI/Swagger URL
```
/docs - Swagger UI
/redoc - ReDoc UI
/openapi.json - OpenAPI specification
```

### Bearer Token Example
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Pagination Example
```
GET /api/tasks?page=1&limit=50&sort=created_at&order=desc
```

---

**Skill Status**: Ready for use by API Agent

**Related**: api-agent.md, api-agent tasks
