import copy
import json
import unittest
from pathlib import Path
from segmentation.core import evaluate, render_nftables, report

ROOT = Path(__file__).resolve().parents[1]

def fixture(name="plant"):
    return json.loads((ROOT / "examples" / name / "policy.json").read_text())

class PolicyTests(unittest.TestCase):
    def test_profiles(self):
        for profile in ("basic", "plant", "enterprise"):
            with self.subTest(profile=profile):
                self.assertEqual([], evaluate(fixture(profile)))
    def test_overlap_rejected(self):
        p = fixture()
        p["zones"][1]["cidr"] = p["zones"][0]["cidr"]
        self.assertTrue(any("overlapping" in i for i in evaluate(p)))
    def test_direct_it_ot_rejected(self):
        p = fixture()
        flow = copy.deepcopy(p["conduits"][0])
        flow["destination"] = "Operations"
        p["conduits"].append(flow)
        self.assertTrue(any("direct enterprise-to-OT" in i for i in evaluate(p)))
    def test_transitive_rejected(self):
        p = fixture()
        p["conduits"].append(dict(source="IDMZ", destination="Operations", protocol="tcp",
                                  port=9000, status="approved", change_id="CHG-2009",
                                  justification="This creates forbidden logical transit",
                                  review_by="2028-01-01"))
        self.assertTrue(any("transitive enterprise-to-control" in i for i in evaluate(p)))
    def test_safety_boundary_rejected(self):
        p = fixture()
        p["conduits"].append(dict(source="Operations", destination="Safety", protocol="tcp",
                                  port=443, status="approved", change_id="CHG-2010",
                                  justification="Synthetic forbidden safety access",
                                  review_by="2028-01-01"))
        self.assertTrue(any("safety zone" in i for i in evaluate(p)))
    def test_duplicate_and_missing_approval(self):
        p = fixture()
        p["conduits"].append(copy.deepcopy(p["conduits"][0]))
        p["conduits"][0]["change_id"] = ""
        issues = evaluate(p)
        self.assertTrue(any("duplicate flow" in i for i in issues))
        self.assertTrue(any("change_id" in i for i in issues))
    def test_port_bool_rejected(self):
        p = fixture()
        p["conduits"][0]["port"] = True
        self.assertTrue(any("port" in i for i in evaluate(p)))
    def test_invalid_expired_review(self):
        p = fixture()
        p["conduits"][0]["review_by"] = "2000-01-01"
        self.assertTrue(any("overdue" in i for i in evaluate(p)))
    def test_cidr_must_be_canonical(self):
        p = fixture()
        p["zones"][0]["cidr"] = "10.100.0.1/24"
        self.assertTrue(any("canonical" in i for i in evaluate(p)))
    def test_render_is_deny_default_and_offline(self):
        rules = render_nftables(fixture())
        self.assertIn("policy drop", rules)
        self.assertIn("ct state established,related accept", rules)
        self.assertIn("ip saddr 10.100.0.0/24 ip daddr 10.200.0.0/24 tcp dport 443", rules)
        self.assertNotIn("flush ruleset", rules)
        self.assertFalse(report(fixture())["verified_live"])

if __name__ == "__main__":
    unittest.main()

