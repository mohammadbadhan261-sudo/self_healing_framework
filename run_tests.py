from selenium import webdriver
from selenium.webdriver.common.by import By
from self_healing import SelfHealingEngine
from explain import explain
import time

engine = SelfHealingEngine()

# -----------------------------
# OPEN REAL LOGIN PAGE
# -----------------------------
driver = webdriver.Chrome()
driver.get("https://opensource-demo.orangehrmlive.com/")

time.sleep(3)

# -----------------------------
# INTENTIONALLY WRONG LOCATOR
# (to trigger self-healing)
# -----------------------------
locator_type = "id"
locator_value = "wrong-username-field"

# -----------------------------
# RUN SELF-HEALING
# -----------------------------
element, method = engine.heal(driver, "id", "wrong-username")

print("\nRESULT:", method)

# -----------------------------
# ACTION (if recovered)
# -----------------------------
if element:
    print(explain("Username field not found", method))
    try:
        element.send_keys("Admin")
    except:
        print("⚠ Element found but not interactable")

else:
    print("❌ Could not recover element")

time.sleep(5)
driver.quit()