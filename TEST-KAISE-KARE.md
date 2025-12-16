# Test Kaise Kare - Step by Step

## 🎯 Bilkul Simple Treqa

---

## **Step 1: Python Install Karo**

### Python 3.11 Download Karo:
1. https://www.python.org/downloads/ kholo
2. "Python 3.11" search karo
3. Download karo
4. Install karo (Next > Next > Finish)

✅ Done!

---

## **Step 2: Backend Shuru Karo**

### Terminal 1 kholo aur yeh type karo:

```bash
cd Phase-2/backend
python -m uvicorn main:app --reload
```

**Dekhna:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ Server chal gaya!

---

## **Step 3: Naya Terminal Kholo**

### Terminal 2 mein yeh commands chalao:

---

## **TEST 1: Server Alive?**

```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{"status": "healthy"}
```

✅ **Server sahi hai!**

---

## **TEST 2: User Banao (Signup)**

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!@#"}'
```

**Response mein TOKEN milega:**
```json
{
  "access_token": "eyJhbG...",
  "refresh_token": "eyJ...",
  "user": {"email": "test@test.com"}
}
```

**TOKEN ko Copy Karo** (neeche wali 10-15 lines)
```
eyJhbG...
```

✅ **User ban gaya!**

---

## **TEST 3: Login Karo**

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!@#"}'
```

**Response:**
```json
{"access_token": "eyJhbG..."}
```

✅ **Login successful!**

---

## **TEST 4: Mera User Dekho**

**TOKEN ko yahan paste karo** (jo TEST 2 mein copy kiya tha)

```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer PASTE_TOKEN_HERE"
```

**Example:**
```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer eyJhbG..."
```

**Response:**
```json
{
  "id": "user_123",
  "email": "test@test.com",
  "is_active": true
}
```

✅ **User mil gaya!**

---

## **TEST 5: Task Banao (CREATE)**

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
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

## **TEST 6: Sub Tasks Dekho (LIST)**

```bash
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN"
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

✅ **Task list mil gaya!**

---

## **TEST 7: Task Update Karo**

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
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

## **TEST 8: Task Complete Karo**

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/complete \
  -H "Authorization: Bearer YOUR_TOKEN"
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

## **TEST 9: Task Delete Karo**

```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{"message": "Task deleted successfully"}
```

✅ **Task delete ho gaya!**

---

## **TEST 10: Security Test (Bina Token)**

```bash
curl http://localhost:8000/api/tasks
```

**Expected:**
```json
{"detail": "Not authenticated"}
```

✅ **Security sahi hai!**

---

## ✅ **TESTING COMPLETE!**

```
[✅] Test 1: Server Health
[✅] Test 2: User Signup
[✅] Test 3: User Login
[✅] Test 4: Get Current User
[✅] Test 5: Create Task
[✅] Test 6: List Tasks
[✅] Test 7: Update Task
[✅] Test 8: Complete Task
[✅] Test 9: Delete Task
[✅] Test 10: Security Check

RESULT: ✅ ALL TESTS PASSED!
```

---

## 🎯 **QUICK REFERENCE**

| Step | Command | Time |
|------|---------|------|
| Python Install | Download & Install | 5 min |
| Server Start | `python -m uvicorn main:app --reload` | 1 min |
| Test 1-10 | Copy-paste commands | 10 min |
| **Total** | | **16 min** |

---

## 💡 **TIPS**

### **TOKEN Copy Kaise Kare?**
1. Test 2 ko run karo
2. Response mein `"access_token": "..."` dikhe
3. `"..."` wala part copy karo
4. Agle tests mein `Bearer YOUR_TOKEN` ki jagah paste karo

### **Copy-Paste Mein Problem?**
Agar copy-paste mein issue ho to manually type karo. Bilkul same result hoga.

### **Windows mein curl nahi hai?**
Windows 10+ mein built-in curl hai. PowerShell kholo aur command type karo.

Agar nahi chalegi to:
```bash
pip install curl-windows
```

---

## 🚀 **FRONTEND Testing (Optional)**

Agar Backend tests pass ho gaye to ab Frontend test kar sakte ho:

```bash
cd Phase-2/frontend
npm install
npm run dev
```

Browser mein: `http://localhost:3000`

Signup → Login → Task banao → Success!

---

## ❌ **Agar Error Aaye?**

### **Error 1: Python nahi hai**
- Python 3.11 install karo: https://www.python.org/downloads/

### **Error 2: pydantic error**
- Python 3.14 hai to 3.11 install karo
- Phir try karo

### **Error 3: "Connection refused"**
- Check karo server Terminal 1 mein chal raha hai
- `Uvicorn running on http://127.0.0.1:8000` likha ho

### **Error 4: "Not authenticated"**
- Token galat hai
- Test 2 se TOKEN dobara copy karo
- Aur sahi se paste karo

---

## 📝 **Notes**

- Har test independent hai
- Order mein karna zaroori hai (Test 1 → 10)
- TOKEN bohot important hai (Test 2 se copy karo)
- Response mein exact yeh likha hona chahiye

---

## 🎊 **FINAL RESULT**

Agar 10 tests sab pass ho jaye to:

✅ **Backend 100% working**
✅ **Authentication 100% working**
✅ **Task management 100% working**
✅ **Security 100% working**

**Phase 2D Testing COMPLETE!** 🎉

---

**Time Required:** 15-20 minutes
**Difficulty:** Bilkul easy (copy-paste!)
**Expected Result:** 100% pass rate

Bilkul tayyar! Shuru kar dou testing! 🚀

