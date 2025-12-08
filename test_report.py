import json
import yaml

YAML_FILE = "test_list.yaml"
JSON_FILE = "result_test_selenium.json"


def load_yaml():
    """Charge les tests depuis le fichier YAML."""
    with open(YAML_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data.get("tests", [])


def load_json():
    """Charge les résultats des tests auto depuis le JSON."""
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠ Aucun fichier JSON '{JSON_FILE}' trouvé.")
        return None


def main():
    print("Lecture des tests auto via result_test_selenium.json…")
    json_data = load_json()
    print("OK\n")

    # Construire un dictionnaire des résultats auto
    test_results = {}
    if json_data:
        for t in json_data.get("tests", []):
            test_case_id = t.get("test_case_id")
            outcome = t.get("outcome")
            if test_case_id:
                test_results[test_case_id] = outcome

    tests_yaml = load_yaml()

    # Compteurs
    total = 0
    passed = 0
    failed = 0
    not_found = 0
    manual = 0

    for test in tests_yaml:
        num = test.get("numero")
        type_test = test.get("type")

        # Générer test_id
        if type_test == "auto-selenium":
            test_id = "auto-selenium"
        elif num is not None:
            test_id = f"TC{num:03d}"
        else:
            test_id = "unknown"

        total += 1

        if type_test in ["manuel", "visuel"]:
            status = "🫱Manual test needed"
            manual += 1
        else:  # auto-unittest ou auto-selenium
            outcome = test_results.get(test_id)
            if outcome == "passed":
                status = "✅Passed"
                passed += 1
            elif outcome == "failed":
                status = "❌Failed"
                failed += 1
            else:
                status = "🕳Not found"
                not_found += 1

        print(f"{test_id} | {type_test} | {status}")

    # Calcul pourcentages
    def pct(value):
        return round((value / total) * 100, 1) if total else 0

    print("\n=== Rapport global ===")
    print(f"Number of tests: {total}")
    print(f"✅Passed tests: {passed} ({pct(passed)}%)")
    print(f"❌Failed tests: {failed} ({pct(failed)}%)")
    print(f"🕳Not found tests: {not_found} ({pct(not_found)}%)")
    print(f"🫱Test to pass manually: {manual} ({pct(manual)}%)")
    print(f"✅Passed + 🫱Manual: {passed + manual} ({pct(passed + manual)}%)")


if __name__ == "__main__":
    main()
