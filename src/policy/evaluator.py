from __future__ import annotations
import json
from pathlib import Path


class PolicyEvaluator:
    def __init__(self, policy_path: str = "policy/policies.json"):
        self.policy_path = Path(policy_path)
        self.doc = json.loads(self.policy_path.read_text())

    def evaluate(self, action: str, role: str) -> tuple[bool, str]:
        for rule in self.doc.get("rules", []):
            if rule.get("action") != action:
                continue
            if rule.get("effect") == "allow":
                return True, rule["id"]
            if rule.get("effect") == "deny":
                if rule.get("unless_role") != role:
                    return False, rule["id"]
                return True, f"{rule['id']}_unless_pass"
        return False, "default_deny"
