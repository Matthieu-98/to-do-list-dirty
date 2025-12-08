import json

def pytest_runtest_makereport(item, call):
    """
    Hook pytest : ajoute l'attribut test_case_id dans le rapport
    pour chaque test lors de son exécution.
    """
    outcome = yield
    rep = outcome.get_result()
    if call.when == "call":
        test_case_id = getattr(item.function, "test_case_id", None)
        if test_case_id:
            setattr(rep, "test_case_id", test_case_id)


def pytest_sessionfinish(session, exitstatus):
    """
    À la fin de la session pytest, génère result_test_auto.json
    contenant nodeid, outcome et test_case_id.
    """
    results = []

    for item in session.items:
        rep_call = getattr(item, "rep_call", None)
        if rep_call:
            outcome = getattr(rep_call, "outcome", "unknown")
            test_case_id = getattr(
                rep_call, "test_case_id", getattr(item.function, "test_case_id", None)
            )
            results.append({
                "nodeid": item.nodeid,
                "outcome": outcome,
                "test_case_id": test_case_id
            })

    with open("result_test_auto.json", "w") as f:
        json.dump({"tests": results}, f, indent=2)
