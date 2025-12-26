"""
مکمل Auth Flow Test: Signup → Login → Dashboard
"""
import asyncio
from playwright.async_api import async_playwright
import json

async def test_complete_flow():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("\n" + "="*60)
        print("🚀 مکمل Auth Flow Test شروع")
        print("="*60 + "\n")
        
        # Step 1: Home Page
        print("📍 Step 1: Home Page پر جا رہے ہیں...")
        await page.goto('http://localhost:3001')
        await page.wait_for_timeout(2000)
        title = await page.title()
        print(f"✅ Home Page لوڈ ہوا: {title}\n")
        
        # Step 2: Signup Page
        print("📍 Step 2: Signup Page پر جا رہے ہیں...")
        await page.click('a:has-text("Sign Up")')
        await page.wait_for_timeout(2000)
        print("✅ Signup Page لوڈ ہوا\n")
        
        # Step 3: Form Fill
        print("📍 Step 3: Signup Form بھر رہے ہیں...")
        test_data = {
            "name": "Complete Flow Test",
            "email": f"flowtest{int(__import__('time').time())}@example.com",
            "password": "FlowTest12345"
        }
        
        await page.fill('input[placeholder="John Doe"]', test_data["name"])
        await page.fill('input[placeholder="you@example.com"]', test_data["email"])
        await page.fill('input[placeholder="••••••••"]', test_data["password"])
        
        print(f"  ✓ نام: {test_data['name']}")
        print(f"  ✓ ای میل: {test_data['email']}")
        print(f"  ✓ پاس ورڈ: {test_data['password']}\n")
        
        # Step 4: Submit Signup
        print("📍 Step 4: Signup بھجا رہے ہیں...")
        await page.click('button:has-text("Sign Up")')
        await page.wait_for_timeout(3000)
        
        # Check for success message
        success_text = await page.text_content('text=Account created successfully')
        if success_text:
            print(f"✅ Signup کامیاب: {success_text}\n")
        else:
            print("❌ Signup ناکام!")
            await browser.close()
            return False
        
        # Wait for redirect to login
        await page.wait_for_url('**/auth/login', timeout=5000)
        await page.wait_for_timeout(1000)
        print("✅ Automatically Login Page پر آگیا\n")
        
        # Step 5: Login Form
        print("📍 Step 5: Login Form بھر رہے ہیں...")
        await page.fill('input[placeholder="you@example.com"]', test_data["email"])
        await page.fill('input[placeholder="••••••••"]', test_data["password"])
        print(f"  ✓ ای میل: {test_data['email']}")
        print(f"  ✓ پاس ورڈ: {test_data['password']}\n")
        
        # Step 6: Submit Login
        print("📍 Step 6: Login بھجا رہے ہیں...")
        await page.click('button:has-text("Sign In")')
        await page.wait_for_timeout(3000)
        
        # Check if redirected to dashboard
        current_url = page.url
        print(f"  URL: {current_url}\n")
        
        if '/dashboard' in current_url:
            print("✅ Dashboard پر پہنچ گیا!\n")
            
            # Check for user greeting
            try:
                welcome = await page.text_content('text=Welcome')
                if welcome:
                    print(f"✅ {welcome}\n")
            except:
                pass
            
            # Check localStorage
            print("📍 Step 7: localStorage چیک کر رہے ہیں...")
            storage = await page.evaluate("""
                () => {
                    const storage = {};
                    for (let i = 0; i < localStorage.length; i++) {
                        const key = localStorage.key(i);
                        if (key) {
                            const value = localStorage.getItem(key);
                            storage[key] = value.substring(0, 50) + '...';
                        }
                    }
                    return storage;
                }
            """)
            
            print("✅ localStorage میں موجود:")
            for key, value in storage.items():
                print(f"  • {key}: {value}")
            print()
            
            # Screenshot
            await page.screenshot(path='dashboard_success.png')
            print("📸 Screenshot: dashboard_success.png\n")
            
            print("="*60)
            print("✅ مکمل Flow کامیاب!")
            print("="*60 + "\n")
            
            await browser.close()
            return True
        else:
            print(f"❌ Dashboard پر نہیں پہنچے۔ URL: {current_url}\n")
            await browser.close()
            return False

if __name__ == '__main__':
    result = asyncio.run(test_complete_flow())
    exit(0 if result else 1)
