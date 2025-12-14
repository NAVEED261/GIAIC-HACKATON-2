# Phase 2D - Testing Baby Steps Guide
## Roman Urdu Main

---

## 🎯 **5 MINUTE SETUP**

### **Step 1: Backend Server Shuru Karo (2 min)**

```bash
cd Phase-2/backend
pip install fastapi uvicorn sqlmodel pyjwt bcrypt
python -m uvicorn main:app --reload
```

**Dekhna:**
```
Uvicorn running on http://127.0.0.1:8000
```

✅ **Server chal gaya!**

---

## ⚡ **10 SIMPLE TESTS**

### **Test 1: Server Zinda Hai? (Health Check)**

```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{"status": "healthy"}
```

✅ **Server kaaam kar raha hai!**

---

### **Test 2: User Banao (Signup)**

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#"}'
```

**Response mein:**
```json
{
  "access_token": "eyJhbG...",
  "user": {"email": "test@example.com"}
}
```

TOKEN ko save karo! (Agle tests k liye)

✅ **User ban gaya!**

---

### **Test 3: Login Karo**

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#"}'
```

**Response mein TOKEN milega:**
```json
{"access_token": "eyJhbG..."}
```

**Neeche `YOUR_TOKEN_HERE` ko replace karo is TOKEN se**

✅ **Login successful!**

---

### **Test 4: Mera User Dekho (Get Me)**

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

✅ **Authentication kaaam kar raha hai!**

---

### **Test 5: Task Banao (CREATE)**

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"title":"Doodh Khareed Lo","description":"2 liters","priority":"high"}'
```

**Response:**
```json
{
  "id": 1,
  "title": "Doodh Khareed Lo",
  "status": "pending",
  "priority": "high"
}
```

✅ **Task ban gaya!**

---

### **Test 6: Sub Tasks Dekho (READ)**

```bash
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Doodh Khareed Lo",
    "status": "pending",
    "priority": "high"
  }
]
```

✅ **Task mil gaya!**

---

### **Test 7: Task Ko Update Karo (UPDATE)**

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"title":"Doodh Aur Bread Khareed Lo"}'
```

**Response:**
```json
{
  "id": 1,
  "title": "Doodh Aur Bread Khareed Lo",
  "status": "pending"
}
```

✅ **Task update ho gaya!**

---

### **Test 8: Task Ko Complete Karo (COMPLETE)**

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

✅ **Task complete ho gaya!**

---

### **Test 9: Task Ko Delete Karo (DELETE)**

```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
{"message": "Task deleted successfully"}
```

✅ **Task delete ho gaya!**

---

### **Test 10: Security Test (Bina Token)**

```bash
curl http://localhost:8000/api/tasks
```

**Expected Response:**
```json
{"detail": "Not authenticated"}
```

✅ **Security kaaam kar rahi hai!**

---

## 🎯 **QUICK SUMMARY**

| Test | Command | Expected | Status |
|------|---------|----------|--------|
| Health | GET /health | 200 OK | ✅ |
| Signup | POST /auth/signup | 201 Created | ✅ |
| Login | POST /auth/login | 200 OK | ✅ |
| Mera Data | GET /auth/me | 200 OK | ✅ |
| Task Banao | POST /tasks | 201 Created | ✅ |
| Sub Tasks | GET /tasks | 200 OK | ✅ |
| Update | PUT /tasks/1 | 200 OK | ✅ |
| Complete | PATCH /tasks/1/complete | 200 OK | ✅ |
| Delete | DELETE /tasks/1 | 200 OK | ✅ |
| No Auth | GET /tasks (no token) | 403 Forbidden | ✅ |

---

## 📱 **Frontend Testing (Browser mein)**

### **Step 1: Frontend Shuru Karo**

```bash
cd Phase-2/frontend
npm install
npm run dev
```

Browser kholo: `http://localhost:3000`

### **Step 2: Manual Testing**

1. **Landing Page**: Sub load ho raha hai? ✅
2. **Signup**: Email & password enter karo → "Signup" click → Dashboard jaye? ✅
3. **Login**: Phir se login karo → Task page dikhe? ✅
4. **Task Banao**: "New Task" → title likho → "Create" click → List mein aaye? ✅
5. **Edit Task**: Task par click karo → Title change karo → Save → Update ho jaye? ✅
6. **Complete**: "Complete" button click → Status change ho? ✅
7. **Delete**: "Delete" → Confirm → Task gone? ✅
8. **Logout**: "Logout" → Login page aaye? ✅

---

## ✅ **COMPLETE CHECKLIST**

### Backend API Tests
```
[✅] Server Health Check
[✅] User Signup
[✅] User Login
[✅] Mera User Data
[✅] Task Banao
[✅] Sub Tasks
[✅] Task Update
[✅] Task Complete
[✅] Task Delete
[✅] Security Check
```

### Frontend Manual Tests
```
[✅] Landing Page Load
[✅] Signup Flow
[✅] Login Flow
[✅] Task Create
[✅] Task Edit
[✅] Task Complete
[✅] Task Delete
[✅] Logout
[✅] Mobile Responsive
[✅] Error Handling
```

---

## 🚀 **QUICK COMMANDS**

### **All at Once**

```bash
# Terminal 1: Backend Shuru Karo
cd Phase-2/backend && python -m uvicorn main:app --reload

# Terminal 2: Health Check
curl http://localhost:8000/health

# Terminal 3: Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!@#"}'

# Terminal 3: Login (TOKEN copy karo response se)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!@#"}'

# Terminal 3: Task Banao
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title":"Kaam Karo"}'

# Terminal 3: Sub Tasks Dekho
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🎯 **WHAT EACH TEST CHECKS**

### **Health Check**
- ✅ Server chal raha hai?
- ✅ Database connected hai?

### **Signup**
- ✅ Naya user ban sakta hai?
- ✅ Email unique hai?
- ✅ Password strong hai?
- ✅ Token generate hua?

### **Login**
- ✅ Sahi email-password se login ho?
- ✅ Galat password reject ho?
- ✅ Token valid hai?

### **Create Task**
- ✅ Task ban sakta hai?
- ✅ Title required hai?
- ✅ Task user ko assign hota hai?

### **List Tasks**
- ✅ Sub tasks dikhte hain?
- ✅ Sirf apne tasks dikhte hain (security)?
- ✅ Filtering kaam karti hai?

### **Update Task**
- ✅ Task update ho sakta hai?
- ✅ Doosre ka task update nahi ho sakta?

### **Delete Task**
- ✅ Task delete ho sakta hai?
- ✅ Delete ke baad gone?

### **Security**
- ✅ Bina token access nahi?
- ✅ Invalid token reject ho?
- ✅ Doosre ka data access nahi?

---

## 💡 **TIPS & TRICKS**

### **Token ko Save Karo**

```bash
# Signup karte wakt token save karo
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!@#"}' | \
  grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo $TOKEN  # Token dekho

# Ab har request mein yah token use karo
curl http://localhost:8000/api/tasks -H "Authorization: Bearer $TOKEN"
```

### **Response ko Pretty Print Karo**

```bash
# jq install karo
pip install jq

# Pretty output dekho
curl http://localhost:8000/health | jq
```

### **Error Debugging Karo**

```bash
# Verbose mode (sub details dekho)
curl -v http://localhost:8000/health

# Headers dekho
curl -i http://localhost:8000/health
```

---

## 🎊 **SUCCESS CRITERIA**

**Sub tests pass karne ka matlab:**

✅ **Backend API 100% kaam kar raha hai**
✅ **Authentication secure hai**
✅ **Database connection achhha hai**
✅ **Multi-user data isolated hai**
✅ **Error handling sahi hai**
✅ **Ready for deployment hai**

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
  ├─ ✅ Signup ban sake
  ├─ ✅ Login kaam kare
  ├─ ✅ Token valid ho
  └─ ✅ Logout kaam kare

Test Tasks
  ├─ ✅ Create task
  ├─ ✅ List sub tasks
  ├─ ✅ Update task
  ├─ ✅ Complete karo
  └─ ✅ Delete karo

Test Security
  ├─ ✅ No token = Forbidden
  ├─ ✅ Invalid token = Forbidden
  ├─ ✅ Other user's task = Forbidden
  └─ ✅ Password hashed hai

Test Frontend
  ├─ ✅ Signup kaam kare
  ├─ ✅ Login kaam kare
  ├─ ✅ Task CRUD kaam kare
  └─ ✅ Mobile responsive ho

RESULT: ✅ ALL TESTS PASS!
```

---

## 📚 **RELATED FILES**

- `PHASE-2D-COMPLETE.md` - Detailed testing guide
- `PHASE-2D-MANUAL-TESTING-GUIDE.md` - Step-by-step with expected responses
- `PHASE-2D-TEST-RESULTS.md` - Complete test summary
- `PHASE-2D-SUMMARY-URDU.md` - Urdu summary

---

**Created:** 2025-12-14
**Time:** 15-20 minutes
**Difficulty:** Baby steps - Bilkul easy!

🎉 **Phase 2D Testing - Baby Steps Complete!** 🎉

**Bilkul Short aur Simple - Bas Copy-Paste Karo!**

