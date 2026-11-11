"""Fail-closed evaluation of declarative, synthetic zone/conduit policies.

This module does not contact any network devices. Only TCP/UDP are rendered.
Every intended allowed conduit requires a dedicated approved change ID.
"""
import ipaddress
import json
import re
from collections import defaultdict
from datetime import date
from itertools import combinations

NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,47}$")
CHANGE = re.compile(r"^[A-Z][A-Z0-9_-]{3,63}$")
PROTOCOLS = {"tcp", "udp"}
ROLES = {"enterprise", "idmz", "operations", "supervisory", "control", "safety", "other"}
OT_ROLES = {"operations", "supervisory", "control", "safety"}
VALID_STATUSES = {"approved"}
MAX_ZONES = 256
MAX_CONDUITS = 4096

def evaluate(policy):
    issues = []
    if not isinstance(policy, dict):
        return ["policy must be a JSON object"]
    if policy.get("schema_version") != "1.0":
        issues.append("schema_version must be 1.0")
    zones, conduits = policy.get("zones"), policy.get("conduits")
    if not isinstance(zones, list) or not zones or len(zones) > MAX_ZONES:
        return issues + ["zones must be a nonempty list of at most 256 entries"]
    if not isinstance(conduits, list) or len(conduits) > MAX_CONDUITS:
        return issues + ["conduits must be a list of at most 4096 entries"]
    index = {}
    networks = {}
    for z in zones:
        if not isinstance(z, dict):
            issues.append("zone entries must be objects")
            continue
        name = z.get("id")
        if not isinstance(name, str) or not NAME.fullmatch(name):
            issues.append(f"invalid zone id: {name!r}")
            continue
        if name in index:
            issues.append(f"duplicate zone id: {name}")
        index[name] = z
        if z.get("role") not in ROLES:
            issues.append(f"{name}: invalid zone role")
        if not isinstance(z.get("owner"), str) or not z["owner"].strip():
            issues.append(f"{name}: missing accountable owner")
        cidr = z.get("cidr")
        try:
            if not isinstance(cidr, str):
                raise ValueError("CIDR is required")
            network = ipaddress.ip_network(cidr, strict=True)
            if network.version != 4:
                raise ValueError("IPv4 only in renderer")
            networks[name] = network
        except ValueError:
            issues.append(f"{name}: invalid canonical IPv4 CIDR")
    for a, b in combinations(networks, 2):
        if networks[a].overlaps(networks[b]):
            issues.append(f"overlapping zone networks: {a}, {b}")
    keys = set()
    graph = defaultdict(set)
    for idx, c in enumerate(conduits):
        prefix = f"conduit[{idx}]"
        if not isinstance(c, dict):
            issues.append(f"{prefix}: must be object")
            continue
        source, dest = c.get("source"), c.get("destination")
        if source not in index or dest not in index or source == dest:
            issues.append(f"{prefix}: source and destination must be distinct defined zones")
            continue
        proto, port = c.get("protocol"), c.get("port")
        if proto not in PROTOCOLS or type(port) is not int or not 1 <= port <= 65535:
            issues.append(f"{prefix}: protocol must be tcp/udp and port 1..65535")
            continue
        key = (source, dest, proto, port)
        if key in keys:
            issues.append(f"{prefix}: duplicate flow {key}")
        keys.add(key)
        if c.get("status") not in VALID_STATUSES:
            issues.append(f"{prefix}: status must be approved")
        if not isinstance(c.get("change_id"), str) or not CHANGE.fullmatch(c["change_id"]):
            issues.append(f"{prefix}: missing/invalid change_id")
        if not isinstance(c.get("justification"), str) or len(c["justification"].strip()) < 12:
            issues.append(f"{prefix}: justification must be at least 12 characters")
        expires = c.get("review_by")
        try:
            if not isinstance(expires, str):
                raise ValueError("review date missing")
            review = date.fromisoformat(expires)
            if review < date.today():
                issues.append(f"{prefix}: overdue review_by {expires}")
        except ValueError:
            issues.append(f"{prefix}: invalid review_by ISO date")
        if index[source].get("role") == "enterprise" and index[dest].get("role") in OT_ROLES:
            issues.append(f"{prefix}: direct enterprise-to-OT conduit prohibited")
        if index[dest].get("role") == "enterprise" and index[source].get("role") in OT_ROLES:
            issues.append(f"{prefix}: direct OT-to-enterprise conduit prohibited")
        if index[source].get("role") == "enterprise" and index[dest].get("role") in {"control", "safety"}:
            issues.append(f"{prefix}: direct enterprise-to-control/safety prohibited")
        if index[dest].get("role") == "safety" and index[source].get("role") != "safety":
            issues.append(f"{prefix}: safety zone must not accept other-zone conduits")
        graph[source].add(dest)
    # Conservative graph policy: reject *any* logical multi-hop path from enterprise to control/safety.
    # This is stricter than an engineered application relay; exceptions require separate architecture.
    enterprise = [n for n,z in index.items() if z.get("role") == "enterprise"]
    protected = {n for n,z in index.items() if z.get("role") in {"control", "safety"}}
    for start in enterprise:
        found = {start}
        frontier = [start]
        while frontier:
            node = frontier.pop()
            for neighbor in graph[node] - found:
                found.add(neighbor)
                frontier.append(neighbor)
        for end in sorted(found & protected):
            issues.append(f"transitive enterprise-to-control/safety path: {start} -> {end}")
    return issues

def report(policy):
    return {
        "schema_version": policy["schema_version"],
        "site": policy.get("site", "unspecified"),
        "mode": "offline-declared-policy-only",
        "verified_live": False,
        "zones": len(policy["zones"]),
        "approved_conduits": len(policy["conduits"]),
        "default_action": "drop",
        "finding_count": 0,
        "warning": "No live configuration or network enforcement has been validated."
    }

def render_nftables(policy):
    """Generate a REVIEW-ONLY inet forward chain; no output/input hooks touched."""
    if evaluate(policy):
        raise ValueError("Policy invalid; refusing to render")
    zone = {z["id"]: z for z in policy["zones"]}
    lines = [
        "# ILLUSTRATIVE ONLY: review interface direction, NAT, routing and rule order.",
        "# NOT an industrial firewall deployment package.",
        "table inet segmentation_reference {",
        "  chain forward {",
        "    type filter hook forward priority 0; policy drop;",
        "    ct state established,related accept",
        "    ct state invalid drop",
    ]
    for c in sorted(policy["conduits"], key=lambda x:(x["source"],x["destination"],x["protocol"],x["port"])):
        src = zone[c["source"]]["cidr"]
        dst = zone[c["destination"]]["cidr"]
        lines.append(
            f'    ip saddr {src} ip daddr {dst} {c["protocol"]} dport {c["port"]} ct state new accept'
        )
    lines += ["  }", "}", ""]
    return "\n".join(lines)

