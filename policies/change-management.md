# Segmentation change management policy — template

Each rule change must identify site, asset owners, source/destination zones, precise direction, protocol, port, application, justification, risk, dependency, requested duration, change ticket, reviewer, maintenance window, verification and rollback plan.

Required review: OT/process owner for safety and availability, network engineer for routing and policy interaction, security analyst for trust paths, independent approver when possible. Emergency changes require explicit emergency authority and retrospective review.

The policy-as-code file is the **intent register**, not evidence of effective production firewall enforcement. Compare it with running configuration, NAT and physical network topology. Remove unnecessary access following confirmed safe functional review; never auto-delete an OT rule solely because logs show low use.

