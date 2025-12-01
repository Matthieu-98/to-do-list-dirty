import json
import yaml

YAML_FILE = "test_list.yaml"
JSON_FILE = "result_test_auto.json"


def load_yaml():
    with open(YAML_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data["tests"]


def load_json():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠ Aucun fichier JSON '{JSON_FILE}' trouvé.")
        return None


def main():
    print("Lecture des tests auto via result_test_auto.json…")
    json_data = load_json()
    print("OK\n")

    # Extraire les tests auto via leur test_case_id
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
        num = test["numero"]
        type_test = test["type"]
        test_id = f"TC{num:03d}"
        total += 1

        if type_test == "manuel":
            status = "🫱Manual test needed"
            manual += 1
        elif type_test == "visuel":
            status = "🫣Visual test needed"
            manual += 1
        else:  # auto-unittest
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
        return round((value / total) * 100, 1)

    print("\n=== Rapport global ===")
    print(f"Number of tests: {total}")
    print(f"✅Passed tests: {passed} ({pct(passed)}%)")
    print(f"❌Failed tests: {failed} ({pct(failed)}%)")
    print(f"🕳Not found tests: {not_found} ({pct(not_found)}%)")
    print(f"🫱Test to pass manually: {manual} ({pct(manual)}%)")
    print(f"✅Passed + 🫱Manual: {passed + manual} ({pct(passed + manual)}%)")


if __name__ == "__main__":
    main()
