# Architecture and zone / conduit design

## Non-negotiable design principles

Safety, reliability, recoverability and operational continuity take precedence over convenience. Inventory physical and logical assets (including non-IP protocols), safety dependencies, vendor support, critical services and maintenance paths before partitioning. Pursue least-functionality flows, segmentation of management planes, monitoring visibility, and independence of safety protection systems as determined by engineering analysis.

## Purdue and IEC 62443

Purdue Level 0: physical process. Level 1: controllers/sensors/actuators. Level 2: HMI and supervisory systems. Level 3: site operations. Level 3.5: an *informal* term for the industrial DMZ, not an official Purdue level. Level 4/5: enterprise business and connectivity. Actual installations often cross levels; classify by trust, functionality and consequence rather than labels alone.

IEC 62443-3-2 engineering uses risk assessment to define zones, conduits and target security levels. An IDMZ may hold brokers, replicated historians, patch staging and managed jump hosts; a dual-boundary design is common but not universally required. The sample policy rejects any declared enterprise-to-control path, even via multiple hops. An engineered application relay may need a richer model describing termination, identity, protocol break and data direction; do not weaken this restriction solely to make a check pass.

## Trust-boundary diagram

\`\`\`mermaid
flowchart LR
  IT[Enterprise IT L4/5] -->|approved web service| IDMZ[Industrial DMZ]
  IDMZ -.->|No implicit routing or forwarding| OPS[Site Operations L3]
  OPS -->|approved application| HMI[Supervisory L2]
  HMI -->|controlled process protocol| PLC[Control L1]
  SIS[Independent Safety Zone]:::safety
  classDef safety fill:#fff0e0,stroke:#9a4800
\`\`\`

The diagram is *logical*. Firewall rules must be applied to the correct interfaces and direction. VLANs by themselves do not enforce L3/L4 separation if routing is available. Multicast/broadcast and L2 protocols (e.g., GOOSE, PROFINET real-time) demand switch-level engineering, not just IPv4 access rules. Consult vendor design limits and functional-safety requirements.

## Multi-site

Model each site separately with per-site owners, routable overlap checks, third-party demarcations, remote operations centers, WAN redundancy, time sources and evidence retention. Enterprise management must not become an unreviewed transitive path into control environments. Adopt per-site change approval and compensating controls for legacy devices. Cloud or AWS topologies are educational simulations only; not a substitute for physical plant enforcement.

