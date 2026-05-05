from ml_model import ElementMatcher


class SelfHealingEngine:
    def __init__(self):
        self.ml = ElementMatcher()

    # ---------------------------------------
    # 1. RULE-BASED HEALING (Primary attempt)
    # ---------------------------------------
    def rule_based(self, driver, locator_type, value):
        try:
            if locator_type == "id":
                return driver.find_element("id", value)

            elif locator_type == "xpath":
                return driver.find_element("xpath", value)

            elif locator_type == "css":
                return driver.find_element("css selector", value)

            elif locator_type == "name":
                return driver.find_element("name", value)

        except Exception:
            return None

        return None

    # ---------------------------------------
    # 2. DOM-BASED CANDIDATE GENERATION
    # (REALISTIC SELF-HEALING INPUT SOURCE)
    # ---------------------------------------
    def get_dom_candidates(self, driver):
        elements = driver.find_elements("xpath", "//*")

        candidates = []

        for el in elements:
            try:
                tag = el.tag_name
                text = el.text.strip()

                # Focus only on useful interactive elements
                if tag in ["input", "button", "a"]:

                    features = [
                        1 if tag == "input" else 0,
                        1 if tag == "button" else 0,
                        1 if text != "" else 0
                    ]

                    candidates.append({
                        "type": "xpath",
                        "value": f"//{tag}",
                        "features": features
                    })

            except Exception:
                continue

        return candidates

    # ---------------------------------------
    # 3. ML-BASED HEALING (SAFE VERSION)
    # ---------------------------------------
    def ml_based(self, driver, candidates):
        for c in candidates:
            try:
                prediction = self.ml.predict(c["features"])

                if prediction == 1:
                    elements = driver.find_elements(c["type"], c["value"])

                    if len(elements) > 0:
                        return elements[0]

            except Exception:
                continue

        return None

    # ---------------------------------------
    # 4. MAIN HEALING PIPELINE
    # ---------------------------------------
    def heal(self, driver, locator_type, value, candidates=None):

        print("\n🔍 Healing triggered...")

        # STEP 1: Try original locator
        element = self.rule_based(driver, locator_type, value)

        if element:
            print("✅ Rule-based success")
            return element, "Rule-Based Success"

        # STEP 2: Generate DOM candidates if not provided
        if candidates is None:
            candidates = self.get_dom_candidates(driver)

        # STEP 3: Try ML-based recovery
        element = self.ml_based(driver, candidates)

        if element:
            print("✅ ML-based success")
            return element, "ML-Based Success"

        # STEP 4: FAIL SAFE
        print("❌ Healing failed - no valid match found")
        return None, "Failed to Heal"