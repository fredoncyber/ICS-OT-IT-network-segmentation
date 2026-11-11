# Informative standards crosswalk (not compliance certification)

Applicability, editions, effective dates, asset impact categories and exact evidence expectations must be established by qualified compliance owners; the list is illustrative rather than exhaustive.

| Framework | Relevant topic | Repository artifact | Evidence still needed |
| --- | --- | --- | --- |
| NIST SP 800-82 Rev. 3 | OT architecture, segmentation, remote access, monitoring | architecture, deployment gate, assurance | deployed design and operational testing |
| IEC 62443-3-2 | Risk assessment; defining zones/conduits and target security levels | threat model, site inventory guidance | formal risk and target SL decisions |
| IEC 62443-3-3 | System security requirements / foundational requirements | access policy, declared conduits | platform/system test and requirement assessment |
| NERC CIP-005 | Applicable electronic security perimeters and electronic access points | trust boundary design and change policy | registered entity applicability, diagrams, access-point evidence |
| NERC CIP-007 | Applicable system security management | hardening reference and access policies | inventory, patch/malware/account management evidence |
| NERC CIP-015-1 | Internal Network Security Monitoring in applicable scope | monitoring and evidence guidance | effective-date / applicability evaluation and deployed capability evidence |

**Avoid conflating** generic IT/OT segmentation with a formal NERC Electronic Security Perimeter. A CIP compliance claim cannot be inferred from zone naming or generic firewall rules. Security levels (SLs) must be determined through IEC 62443 risk analysis rather than mapped mechanically to Purdue levels.

Primary public references:
- NIST: https://csrc.nist.gov/pubs/sp/800/82/r3/final
- IEC 62443 overview: https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards
- NERC standards: https://www.nerc.com/pa/Stand/Pages/ReliabilityStandards.aspx
- MITRE ATT&CK for ICS: https://attack.mitre.org/matrices/ics/

