# OT incident response: segmentation compromise — template

**Safety and process stability take precedence.** An analyst must not indiscriminately disconnect PLCs, block plant protocols, restart devices or scan impacted subnets.

1. Detect and triage with passive telemetry, existing logs, operator reports and approved evidence.
2. Notify control room / process owner, incident commander, engineering, safety team and relevant reporting contacts.
3. Establish impact on human safety, production availability, critical control functions and regulatory reporting.
4. Identify safe containment options with operations: disable specific remote session, isolate enterprise-access boundary, revoke tokens, switch to established manual mode where authorized.
5. Require onsite operational authorization before implementing network isolation affecting control equipment.
6. Preserve time-synchronized logs and immutable evidence without disturbing live controllers.
7. Restore through documented approved runbooks, validate process state and reconcile emergency access changes.
8. Conduct post-event review, detection tuning and change-control closeout.

Escalation, safety thresholds and reporting deadlines are site-specific and must be populated before use.

