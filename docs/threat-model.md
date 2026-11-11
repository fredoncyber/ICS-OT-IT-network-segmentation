# Threat model (STRIDE and ATT&CK for ICS informed)

## Assets and consequences
Controller integrity, deterministic control traffic, process availability, operator visibility, engineering workstations, historical records, safety interlocks, remote support and recovery infrastructure. Consequences include unsafe physical actuation, production interruption and loss of visibility.

| Threat | Trust path | Consequence | Defensive control | Verification |
| --- | --- | --- | --- | --- |
| Stolen IT credentials | Enterprise → remote access → OT | Unauthorized changes | MFA, brokered sessions, just-in-time approval, segmentation | identity/session log review |
| Ransomware lateral movement | Shared identity or unfiltered lateral paths | Operations disruption | separate zones, credential boundaries, backups | configuration reconciliation |
| Unauthorized engineering downloads | EWS → controller | Altered logic | engineering change approval, limited workstation access, controller integrity checks | signed change and vendor records |
| Malicious/accidental historian pathway | OT → IDMZ → IT | Data integrity/exfiltration | application relay, protocol termination, restricted directions | data flow inspection |
| Monitoring gaps | East-west control network | Late detection | passive OT IDS / SPAN/TAP engineering | sensor coverage and detection test |
| Availability degradation | Misapplied firewall or high traffic | Process upset | conservative rollout, availability tests, fail-safe rollback | plant acceptance |

STRIDE prompts: spoofing remote support identities, tampering with control messages, repudiation of changes, information disclosure through historians, denial of service at boundaries, privilege escalation from business endpoints. Map observed behaviors to the current MITRE ATT&CK for ICS matrix for detection engineering; do not imply that any synthetic example demonstrates an actual exploit.

Safety-related systems and legacy protocol dependencies must be examined by qualified engineering staff; do not treat generic firewall templates as functional safety controls.

