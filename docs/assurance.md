# Segmentation assurance and evidence catalog

Evidence streams: inventory snapshots with asset/system owners; diagram version and zone definitions; approved conduit register; change tickets; platform policy exports, effective rule order and NAT; approved exception register; rule-hit and passive IDS metadata; backup and rollback proof; recertification records; process-owner acceptance.

| Check | Cadence | Owner | Evidence | Outcome |
| --- | --- | --- | --- | --- |
| New path approval | Every change | OT owner + change authority | ticket, risk, peers | approved/rejected |
| Offline model regression | Every PR | security engineering | CI result | pass/fail |
| Drift reconciliation | Monthly or after major change | network engineer | config export/diff | exception/remediation |
| Stale unused rule review | Quarterly (risk-based) | control owner | hit counters plus protocol dependency | retained/removed |
| Remote vendor access review | Each session and quarterly | access owner | identity, MFA, session approval/logs | closed/exceptions |
| Safety and failover acceptance | Before deployment | process/safety owner | test sign-off | safe to proceed |
| Monitoring coverage review | Quarterly | SOC/OT lead | passive sensor map, alerts | gaps |
| Policy recertification | At least annually or per local risk | zone owners | signed conduit register | updated |

## Evidence quality

Evidence must be dated, attributable, tamper-evident where practical, tied to a known asset/configuration revision, and retained under the organization's record schedule. Hash reports and link to change IDs in a secured evidence store; avoid exposing internal addresses to this public GitHub project. Policy checks in this repo **do not prove deployed enforcement or standards compliance**.

