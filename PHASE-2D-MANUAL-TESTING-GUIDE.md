# Phase 2D - Manual Testing Guide (Baby Steps)

Agar aap Python compatibility issues se baachna chahte ho, to **manual testing** kro.

---

## 🚀 Step 1: Backend Server Start Karo

```bash
cd Phase-2/backend
pip install fastapi sqlmodel uvicorn python-multipart pyjwt bcrypt

# Server shuru karo
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server running hoga: `http://localhost:8000`

---

## 📋 Step 2: API Testing (Using cURL or Postman)

### **Test 1: User Registration (Signup)**

```bash
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "Test123!@#"
  }'
```

**Expected Response (201):**
```json
{
  "access_token": "eyJhbG...",
  "refresh_token": "eyJhbG...",
  "user": {
    "id": "user_123",
    "email": "testuser@example.com",
    "name": null
  }
}
```

---

### **Test 2: User Login**

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "Test123!@#"
  }'
```

**Expected Response (200):**
```json
{
  "access_token": "eyJhbG...",
  "refresh_token": "eyJhbG...",
  "user": {
    "id": "user_123",
    "email": "testuser@example.com"
  }
}
```

Save `access_token` for next tests.

---

### **Test 3: Get Current User**

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**Expected Response (200):**
```json
{
  "id": "user_123",
  "email": "testuser@example.com",
  "is_active": true
}
```

---

### **Test 4: Create Task**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "high",
    "due_date": "2025-12-25"
  }'
```

**Expected Response (201):**
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high",
  "status": "pending",
  "created_at": "2025-12-14T10:00:00Z"
}
```

---

### **Test 5: Get All Tasks**

```bash
curl -X GET "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**Expected Response (200):**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "status": "pending",
    "priority": "high"
  }
]
```

---

### **Test 6: Update Task**

```bash
curl -X PUT "http://localhost:8000/api/tasks/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -d '{
    "title": "Buy groceries and cook",
    "priority": "medium"
  }'
```

**Expected Response (200):**
```json
{
  "id": 1,
  "title": "Buy groceries and cook",
  "priority": "medium",
  "status": "pending"
}
```

---

### **Test 7: Complete Task**

```bash
curl -X PATCH "http://localhost:8000/api/tasks/1/complete" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**Expected Response (200):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "status": "completed",
  "completed_at": "2025-12-14T10:30:00Z"
}
```

---

### **Test 8: Delete Task**

```bash
curl -X DELETE "http://localhost:8000/api/tasks/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**Expected Response (200):**
```json
{
  "message": "Task deleted successfully"
}
```

---

### **Test 9: Health Check**

```bash
curl -X GET "http://localhost:8000/health"
```

**Expected Response (200):**
```json
{
  "status": "healthy"
}
```

---

### **Test 10: Database Health**

```bash
curl -X GET "http://localhost:8000/health/db"
```

**Expected Response (200):**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## 🧪 Step 3: Frontend Testing

### **Start Frontend Server**

```bash
cd Phase-2/frontend
npm install
npm run dev
```

Frontend running hoga: `http://localhost:3000`

---

### **Manual Flow Testing**

1. **Landing Page Test:**
   - URL: `http://localhost:3000/`
   - Check: Landing page loads properly
   - Check: Signup/Login buttons visible

2. **Signup Flow:**
   - Go to: `http://localhost:3000/signup`
   - Fill email: `testuser@example.com`
   - Fill password: `Test123!@#`
   - Click: Signup button
   - Expected: Redirects to dashboard

3. **Login Flow:**
   - Go to: `http://localhost:3000/login`
   - Fill email: `testuser@example.com`
   - Fill password: `Test123!@#`
   - Click: Login button
   - Expected: Redirects to dashboard

4. **Dashboard Test:**
   - Go to: `http://localhost:3000/dashboard`
   - Check: User is logged in
   - Check: Welcome message shows

5. **Create Task Test:**
   - Go to: `http://localhost:3000/tasks/new`
   - Fill title: `Buy groceries`
   - Fill description: `Milk, eggs, bread`
   - Select priority: `High`
   - Click: Create button
   - Expected: Task added to list

6. **Task List Test:**
   - Go to: `http://localhost:3000/tasks`
   - Check: All tasks visible
   - Check: Filter by status works
   - Check: Can click to edit task

7. **Edit Task Test:**
   - Click: Edit button on any task
   - Change title: `Buy groceries and cook`
   - Click: Save button
   - Expected: Task updated in list

8. **Complete Task Test:**
   - Click: Complete button on task
   - Expected: Task marked as completed
   - Check: Status changes to "Completed"

9. **Delete Task Test:**
   - Click: Delete button on task
   - Confirm: Delete confirmation dialog
   - Expected: Task removed from list

10. **Logout Test:**
    - Click: Logout button
    - Expected: Redirects to login page

---

## ✅ Checklist for Manual Testing

### Backend (API) Testing
- [ ] Signup with valid email/password → 201 ✅
- [ ] Signup with duplicate email → 400 ❌
- [ ] Signup with invalid email → 422 ❌
- [ ] Login with correct credentials → 200 ✅
- [ ] Login with wrong password → 401 ❌
- [ ] Get current user → 200 ✅
- [ ] Get current user without token → 403 ❌
- [ ] Create task → 201 ✅
- [ ] Get all tasks → 200 ✅
- [ ] Update task → 200 ✅
- [ ] Update non-existent task → 404 ❌
- [ ] Delete task → 200 ✅
- [ ] Complete task → 200 ✅
- [ ] Health check → 200 ✅
- [ ] Database health → 200 ✅

### Frontend Testing
- [ ] Landing page loads → ✅
- [ ] Signup flow works → ✅
- [ ] Login flow works → ✅
- [ ] Dashboard shows → ✅
- [ ] Create task → ✅
- [ ] List tasks → ✅
- [ ] Edit task → ✅
- [ ] Complete task → ✅
- [ ] Delete task → ✅
- [ ] Logout works → ✅

### Responsive Design (Frontend)
- [ ] Mobile (320px) → Responsive ✅
- [ ] Tablet (768px) → Responsive ✅
- [ ] Desktop (1024px) → Responsive ✅
- [ ] Touch-friendly buttons → ✅

### Security Testing
- [ ] Can't access tasks without auth → 403 ✅
- [ ] Can't access other user's tasks → 403 ✅
- [ ] Can't update other user's tasks → 403 ✅
- [ ] Can't delete other user's tasks → 403 ✅
- [ ] Password is hashed → ✅
- [ ] Tokens expire → ✅

---

## 🎯 Quick Testing Commands

### All at Once (Using Postman Collection)

Create a Postman collection with these requests:
1. POST /api/auth/signup
2. POST /api/auth/login
3. GET /api/auth/me
4. POST /api/tasks
5. GET /api/tasks
6. PUT /api/tasks/1
7. PATCH /api/tasks/1/complete
8. DELETE /api/tasks/1
9. GET /health
10. GET /health/db

---

## 📊 Test Results Summary

**Total Tests:** 33 test cases created
- **Auth Tests:** 15 cases (signup, login, logout, refresh, me)
- **Task Tests:** 16 cases (CRUD, filtering, multi-user isolation)
- **Health Tests:** 2 cases

**Status:** ✅ Ready for manual execution

**Expected Results:** 100% pass rate for all manual tests

---

**Created:** 2025-12-14
**For:** Manual testing without pytest setup
**Difficulty:** Beginner-friendly (just copy-paste commands)
