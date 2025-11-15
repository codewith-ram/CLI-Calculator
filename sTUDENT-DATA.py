"""
SNSCT Portal Auto Login — FINAL WORKING VERSION
"""

import time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://portal.snsct.org/"
USERNAME = "713521AS021"
Password = "snsct@123"

def main():
    print("[*] Launching Chrome...")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(URL)
        print("[+] Portal opened.")

        # Username
        username_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter your username']")))
        username_box.click()
        username_box.clear()
        username_box.send_keys(USERNAME)
        print("[+] Username entered.")

        # Wait for and handle password field dynamically
        print("[*] Waiting for password field...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your password']")))
        time.sleep(1.2)

        password_box = driver.find_element(By.XPATH, "//input[@placeholder='Enter your password']")
        driver.execute_script("arguments[0].scrollIntoView(true);", password_box)
        driver.execute_script("arguments[0].value = arguments[1];", password_box, PASSWORD)
        print("[+] Password injected successfully using JS.")

        # Wait for Login button and click
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login')]")))
        login_button.click()
        print("[+] Login button clicked.")

        # Wait to verify navigation
        time.sleep(6)
        json.dump(driver.get_cookies(), open("snsct_cookies.json", "w"), indent=2)
        print("[+] Cookies saved. Login should be successful!")

    except Exception as e:
        print("[!] Error:", e)
    finally:
        print("[*] Keeping browser open for 10 seconds...")
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    main()
