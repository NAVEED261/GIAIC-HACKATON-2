# Phase 2D - Quick Testing Guide
## Baby Steps में Short तरीका

---

## 🎯 **5 MINUTE SETUP**

### **Step 1: Backend Server शुरू करो (2 min)**

```bash
cd Phase-2/backend
pip install fastapi uvicorn sqlmodel pyjwt bcrypt
python -m uvicorn main:app --reload
```

**Output देखो:**
```
Uvicorn running on http://127.0.0.1:8000
```

✅ **Server चल गया!**

---

## ⚡ **10 SIMPLE TESTS**

### **Test 1: Server Alive है? (Health Check)**

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "healthy"}
```

✅ **Server काम कर रहा है!**

---

### **Test 2: User बनाओ (Signup)**

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#"}'
```

**Response में देखो:**
```json
{
  "access_token": "eyJhbG...",
  "user": {"email": "test@example.com"}
}
```

Token को सेव करो! (अगले tests के लिए)

✅ **User बन गया!**

---

### **Test 3: Login करो**

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#"}'
```

**Response में TOKEN मिलेगा**
```json
{"access_token": "eyJhbG..."}
```

**नीचे `YOUR_TOKEN_HERE` को इस TOKEN से replace करो**

✅ **Login successful!**

---

### **Test 4: Current User देखो**

```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
{
  "id": "user_123",
  "email": "test@example.com",
  "is_active": true
}
```

✅ **Authentication काम कर रहा है!**

---

### **Test 5: Task बनाओ (CREATE)**

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"title":"Buy Milk","description":"2 liters","priority":"high"}'
```

**Response:**
```json
{
  "id": 1,
  "title": "Buy Milk",
  "status": "pending",
  "priority": "high"
}
```

✅ **Task बन गया!**

---

### **Test 6: सब Tasks देखो (READ)**

```bash
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Buy Milk",
    "status": "pending",
    "priority": "high"
  }
]
```

✅ **Task मिल गया!**

---

### **Test 7: Task update करो (UPDATE)**

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"title":"Buy Milk and Bread"}'
```

**Response:**
```json
{
  "id": 1,
  "title": "Buy Milk and Bread",
  "status": "pending"
}
```

✅ **Task update हो गया!**

---

### **Test 8: Task को Complete करो (COMPLETE)**

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/complete \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
{
  "id": 1,
  "status": "completed",
  "completed_at": "2025-12-14T10:30:00Z"
}
```

✅ **Task complete हो गया!**

---

### **Test 9: Task delete करो (DELETE)**

```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
{"message": "Task deleted successfully"}
```

✅ **Task delete हो गया!**

---

### **Test 10: Security Test (बिना Token)**

```bash
curl http://localhost:8000/api/tasks
```

**Expected Response:**
```json
{"detail": "Not authenticated"}
```

✅ **Security काम कर रही है!**

---

## 🎯 **QUICK SUMMARY**

| Test | Command | Expected | Status |
|------|---------|----------|--------|
| Health | GET /health | 200 OK | ✅ |
| Signup | POST /auth/signup | 201 Created | ✅ |
| Login | POST /auth/login | 200 OK | ✅ |
| Me | GET /auth/me | 200 OK | ✅ |
| Create Task | POST /tasks | 201 Created | ✅ |
| List Tasks | GET /tasks | 200 OK | ✅ |
| Update Task | PUT /tasks/1 | 200 OK | ✅ |
| Complete Task | PATCH /tasks/1/complete | 200 OK | ✅ |
| Delete Task | DELETE /tasks/1 | 200 OK | ✅ |
| No Auth | GET /tasks (no token) | 403 Forbidden | ✅ |

---

## 📱 **Frontend Testing (Browser)**

### **Step 1: Frontend शुरू करो**

```bash
cd Phase-2/frontend
npm install
npm run dev
```

Browser खोलो: `http://localhost:3000`

### **Step 2: Manual Testing**

1. **Landing Page**: सब कुछ load हो रहा है? ✅
2. **Signup**: Email & password enter करो → "Signup" click → Dashboard जाए? ✅
3. **Login**: फिर से login करो → Task page दिखे? ✅
4. **Create Task**: "New Task" → title भरो → "Create" click → List में आए? ✅
5. **Edit Task**: Task पर click → Title change करो → Save → Update हो जाए? ✅
6. **Complete**: "Complete" button click → Status change हो? ✅
7. **Delete**: "Delete" → Confirm → Task gone? ✅
8. **Logout**: "Logout" → Login page आए? ✅

---

## ✅ **COMPLETE CHECKLIST**

### Backend API Tests
```
[✅] Server Health Check
[✅] User Signup
[✅] User Login
[✅] Get Current User
[✅] Create Task
[✅] List Tasks
[✅] Update Task
[✅] Complete Task
[✅] Delete Task
[✅] Authentication Security
```

### Frontend Manual Tests
```
[✅] Landing Page Load
[✅] Signup Flow
[✅] Login Flow
[✅] Create Task
[✅] Edit Task
[✅] Complete Task
[✅] Delete Task
[✅] Logout
[✅] Responsive Design
[✅] Error Handling
```

---

## 🚀 **ONE-LINER TESTS** (Fastest)

Agar सब एक साथ करना है:

```bash
# Terminal 1: Backend शुरू करो
cd Phase-2/backend && python -m uvicorn main:app --reload

# Terminal 2: सब tests run करो (copy-paste करो)
curl http://localhost:8000/health && \
curl -X POST http://localhost:8000/api/auth/signup -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"Test123!@#"}' && \
curl http://localhost:8000/api/tasks -H "Authorization: Bearer TOKEN_HERE"
```

---

## 🎯 **WHAT EACH TEST CHECKS**

### **Health Check**
- ✅ Server चल रहा है?
- ✅ Database connected है?

### **Signup**
- ✅ नया user बन सकता है?
- ✅ Email unique है?
- ✅ Password strong है?
- ✅ Token generate हुआ?

### **Login**
- ✅ सही email-password से login हो?
- ✅ गलत password reject हो?
- ✅ Token valid है?

### **Create Task**
- ✅ Task बन सकता है?
- ✅ Title required है?
- ✅ Task user को assign होता है?

### **List Tasks**
- ✅ सब tasks दिखते हैं?
- ✅ सिर्फ अपने tasks दिखते हैं (security)?
- ✅ Filtering काम करती है?

### **Update Task**
- ✅ Task update हो सकता है?
- ✅ दूसरे का task update नहीं हो सकता?

### **Delete Task**
- ✅ Task delete हो सकता है?
- ✅ Delete के बाद gone?

### **Security**
- ✅ बिना token access नहीं?
- ✅ Invalid token reject हो?
- ✅ दूसरे का data access नहीं?

---

## 💡 **TIPS & TRICKS**

### **Token को आसानी से सेव करो**

```bash
# Signup करते समय token सेव करो
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!@#"}' | \
  grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo $TOKEN  # Token देखो

# अब हर request में यह token use करो
curl http://localhost:8000/api/tasks -H "Authorization: Bearer $TOKEN"
```

### **Response को Pretty Print करो**

```bash
# jq install करो (अगर नहीं है)
pip install jq

# Pretty output देखो
curl http://localhost:8000/health | jq
```

### **Error Debugging करो**

```bash
# Verbose mode (सब details देखो)
curl -v http://localhost:8000/health

# Headers देखो
curl -i http://localhost:8000/health
```

---

## 🎊 **SUCCESS CRITERIA**

**सब tests pass करने का मतलब:**

✅ **Backend API 100% काम कर रहा है**
✅ **Authentication secure है**
✅ **Database connection अच्छा है**
✅ **Multi-user data isolated है**
✅ **Error handling सही है**
✅ **Ready for deployment है**

---

## 📝 **EXPECTED TIME**

- **Health Check**: 30 seconds
- **Signup + Login**: 1 minute
- **All 10 tests**: 5-10 minutes
- **Frontend testing**: 5-10 minutes
- **Total**: **15-20 minutes**

---

## 🎯 **FINAL CHECKLIST**

```
Start Backend Server
  └─ ✅ http://localhost:8000/health returns 200

Test Authentication
  ├─ ✅ Signup बन सके
  ├─ ✅ Login काम करे
  ├─ ✅ Token valid हो
  └─ ✅ Logout काम करे

Test Tasks
  ├─ ✅ Create टास्क
  ├─ ✅ List सब टास्क
  ├─ ✅ Update टास्क
  ├─ ✅ Complete करो
  └─ ✅ Delete करो

Test Security
  ├─ ✅ No token = Forbidden
  ├─ ✅ Invalid token = Forbidden
  ├─ ✅ Other user's task = Forbidden
  └─ ✅ Password हashed है

Test Frontend
  ├─ ✅ Signup काम करे
  ├─ ✅ Login काम करे
  ├─ ✅ Task CRUD काम करे
  └─ ✅ Mobile responsive हो

RESULT: ✅ ALL TESTS PASS!
```

---

**Created:** 2025-12-14
**Time:** 15-20 minutes
**Difficulty:** Beginner-friendly

🎉 **Phase 2D Testing - Quick Guide Complete!** 🎉

