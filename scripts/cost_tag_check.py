import json
import sys

BILLING_TAG = "landlord_account_id"


def check_plan(plan_path: str) -> int:
    with open(plan_path, "r", encoding="utf-8") as file:
        plan = json.load(file)

    missing = []

    for resource in plan.get("resource_changes", []):
        change = resource.get("change") or {}
        actions = change.get("actions", [])

        # Skip resources that are not being created or changed.
        if not any(action in ("create", "update") for action in actions):
            continue

        after = change.get("after") or {}
        tags = after.get("tags") or {}

        if not tags.get(BILLING_TAG):
            missing.append(resource.get("address", "<unknown>"))

    if missing:
        for address in sorted(missing):
            print(f"Missing {BILLING_TAG}: {address}")
        return 1

    print("All changed resources have the required billing tag.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <terraform-plan.json>")
        sys.exit(2)

    sys.exit(check_plan(sys.argv[1]))