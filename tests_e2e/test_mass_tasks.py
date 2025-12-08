import time
import unittest
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestMassCreateDelete(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # mode headless si tu veux
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(1)

    def tearDown(self):
        self.driver.quit()

    def count_tasks(self):
        return len(self.driver.find_elements(By.CSS_SELECTOR, ".item-row"))

    def test_create_and_delete_10_tasks(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        initial_count = self.count_tasks()
        print("Initial count:", initial_count)

        # --- Création automatique de 10 tâches ---
        for i in range(10):
            input_box = wait.until(EC.presence_of_element_located((By.ID, "task-input")))
            input_box.clear()
            input_box.send_keys(f"AutoTest-{i}")

            add_button = wait.until(EC.element_to_be_clickable((By.ID, "add-button")))
            add_button.click()

            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, f".item-row[data-test-name='AutoTest-{i}']"))
            )
            time.sleep(0.1)

        after_creation = self.count_tasks()
        print("After creation:", after_creation)
        self.assertEqual(after_creation, initial_count + 10)

        # --- Suppression automatique des 10 tâches créées ---
        for i in range(10):
            delete_buttons = wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, ".delete-button"))
            self.assertGreater(len(delete_buttons), 0)
            delete_buttons[-1].click()
            wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".item-row")) == after_creation - 1)
            after_creation -= 1
            time.sleep(0.1)

        after_deletion = self.count_tasks()
        print("After deletion:", after_deletion)
        self.assertEqual(after_deletion, initial_count)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestMassCreateDelete)
    runner = unittest.TextTestRunner(resultclass=unittest.TestResult)
    result = runner.run(suite)

    # JSON compatible avec test_report.py
    results_json = {
        "tests": [
            {
                "test_case_id": "auto-selenium",
                "outcome": "passed" if result.wasSuccessful() else "failed",
                "testsRun": result.testsRun,
                "failures": [{"test": str(f[0]), "reason": str(f[1])} for f in result.failures],
                "errors": [{"test": str(e[0]), "reason": str(e[1])} for e in result.errors]
            }
        ]
    }

    # Sauvegarde dans un fichier JSON
    with open("result_test_selenium.json", "w", encoding="utf-8") as f:
        json.dump(results_json, f, indent=4)
