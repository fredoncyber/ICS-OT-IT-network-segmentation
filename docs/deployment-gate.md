# Production deployment gate (human-controlled)

**STOP:** the public repository and its examples are not approved production changes.

## Before deployment

- [ ] Facility and safety owners sign off on process hazard, failure modes, OT operational constraints and maintenance window.
- [ ] Asset inventory, protocol dependencies, vendor restrictions and safety-zone independence reviewed.
- [ ] Bidirectional dependency and stateful return traffic assessed; address translation, routing, QoS, multicast and redundancy verified.
- [ ] Site-specific platform syntax and effective rule order independently peer reviewed; secure management plane separated.
- [ ] Restore-tested configuration backup, out-of-band console access and staged rollback plan available.
- [ ] Change ticket, operator communication, onsite support, spare parts and escalation bridge confirmed.
- [ ] Rules reviewed in lab with representative timing, failover and functionality tests.
- [ ] Passive visibility or vendor-approved non-disruptive test plan signed off.
- [ ] Window, stop criteria, decision authority and rollback trigger recorded.

## During and after

Record approved scope and device versions; capture config checksums pre/post; monitor plant signals, process latency, failover and relevant alerts. **Do not proactively scan sensitive controllers to prove segmentation.** Validate boundaries by read-only configuration inspection, passive captures and isolated test nodes where authorized. Reconcile exceptions and evidence to tickets. Roll back with the process owner upon abnormal operation.

## Guarded Ansible reference

\`configure-firewalls.yml\` defaults to creating a review artifact. Activation needs \`apply_firewall=true\`, \`change_approved=true\` and \`out_of_band_recovery=true\`. Even then, it is a generic Linux laboratory reference, **not supported on industrial firewalls**; invoke only on an isolated test VM. It does not solve remote-access lockout or plant safety risks.

