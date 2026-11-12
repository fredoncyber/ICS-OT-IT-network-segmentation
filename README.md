# IT/OT/ICS Network Segmentation Management

[![CI](https://github.com/fredoncyber/ICS-OT-IT-network-segmentation/actions/workflows/validate.yml/badge.svg)](https://github.com/fredoncyber/ICS-OT-IT-network-segmentation/actions/workflows/validate.yml)

A **policy-as-code and operational governance reference** for network-security analysts, engineers, and OT owners. It models industrial zones, approved conduits, rule lifecycle and audit evidence across basic, plant and multi-site architectures. This is a **review-ready reference implementation, not a production-certified firewall solution**.

## Safety boundaries

- **Offline CI only:** checks schema, policy conflicts, restricted paths and documentation; no packet probing of OT assets.
- Firewall changes are **not automatic**. Ansible playbooks are dry-run rendering by default; installing rules requires explicit opt-in, change approval and an out-of-band recovery plan.
- Never scan or actively test live PLCs, RTUs, safety systems or process networks without facility-owner permission and an approved maintenance procedure.
- No credentials, facility IPs, internal diagrams, operational logs or production evidence belong in this public repository.
- An approved flow is **not automatically deployed**; actual enforcement must be independently inspected at switches, routers, firewalls, hosts and remote-access systems.
- No claim of NERC CIP, IEC 62443 or NIST certification, conformity, or complete coverage is made.

## Quick start (Python 3.11+; standard library only)

\`\`\`sh
python3 -m unittest discover -s tests -v
python3 -m segmentation validate --policy examples/basic/policy.json
python3 -m segmentation validate --policy examples/plant/policy.json
python3 -m segmentation validate --policy examples/enterprise/policy.json
python3 -m segmentation report --policy examples/plant/policy.json --output /tmp/segmentation-report.json
python3 -m segmentation render --policy examples/plant/policy.json --output /tmp/segmentation.nft
\`\`\`

Rendering generates a **review artifact only**; it does not activate a firewall. Do not treat synthetic test results as real network measurements. See [Getting Started](docs/getting-started.md), [Design](docs/architecture.md), [Deployment Gate](docs/deployment-gate.md) and [Assurance](docs/assurance.md).

## Scale profiles

| Profile | Scope | Typical controls |
| --- | --- | --- |
| Basic | One lab / isolated production cell | Separate trust zones, local firewall, documented conduits |
| Plant | Several cells / one site | Two-boundary IDMZ, managed jump access, OT-aware visibility |
| Enterprise | Multi-site / critical infrastructure | Site-specific boundaries, HA and recovery, centralized evidence and monitoring |

Profiles are **illustrative**, not vendor-certified topologies. IEC 62443 zones and conduits are risk-driven; Purdue levels are a useful reference and are not substitutes for asset inventory and risk assessment.

## Repository map

- \`segmentation/\`: offline zone/conduit validation, reachability assessment, JSON evidence report and *illustrative* nftables rendering
- \`examples/\`: synthetic basic, plant and enterprise profiles with no real facilities
- \`docs/\`: architecture, threat model, operating model, lifecycle, assurance and mapping caveats
- \`policies/\`: access, change, remote access and OT incident response
- \`infrastructure/ansible/\`: sample firewall render / guarded installation and jump host baseline
- \`infrastructure/terraform/\`: **AWS simulation only**, not physical ICS enforcement
- \`tests/\`: positive and negative unit tests; CI enforces regression checks

## Program operating cycle

**Discover → classify criticality/safety → partition zones → approve directional flows → stage rules → review change → deploy under change window → passively verify → collect evidence → periodically recertify.**

Owner roles: facility/process owner approves safety impacts; network engineer designs and deploys; security analyst assesses threat paths and monitoring; change authority approves implementation; independent reviewer reconciles evidence. Keep duties separated when feasible.

## Limitations

The validator tests **declared logical policy** only. It cannot determine actual network reachability, asymmetric routing, NAT, protocol semantics, time synchronization, firewall ordering on a real platform, safety consequences or regulatory applicability. RFC1918/example addresses are synthetic. Real use requires vendor-specific engineering, tabletop exercises, site acceptance testing, backups, rollback and process-safety review.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [LICENSE](LICENSE) and [Roadmap](docs/roadmap.md).

