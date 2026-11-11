# Getting started: analyst and engineer workflow

1. Create a site inventory in an **internal secured system**: assets, functions, owner, criticality, safety consequence, OEM, lifecycle, protocols and maintenance windows. Public examples contain synthetic addresses only.
2. Copy an example JSON policy and change only synthetic lab data. Assign uniquely named zones with canonical IPv4 CIDRs, roles and accountable owners.
3. Add each required **directional** TCP/UDP conduit with unique protocol/port pairing, business justification, approved change ID and future review date. If a protocol is not representable in this model, track it outside the renderer.
4. Run unit tests, validation and report locally. Resolve any finding; never edit the validator to bypass denied paths.
5. Convene facility-owner, OT engineer, security and change-authority review. See deployment gate.
6. Generate rules for **offline comparison only**. An actual deployment requires rule translation and platform-specific review for NAT, object groups, interface scoping and high availability.
7. Schedule recertification and reconcile declared vs device configurations, session logs, monitoring evidence and change approvals.

## Tool syntax
\`\`\`sh
python3 -m segmentation validate --policy examples/plant/policy.json
python3 -m segmentation report --policy examples/plant/policy.json --output /tmp/site-report.json
python3 -m segmentation render --policy examples/plant/policy.json --output /tmp/reference.nft
\`\`\`

Validation exits 0 on policy success, 1 on policy findings, 2 on malformed input or IO errors. CLI does not actively test destination hosts. Never interpret a TCP refusal, ping failure or timeout as affirmative firewall enforcement evidence.

