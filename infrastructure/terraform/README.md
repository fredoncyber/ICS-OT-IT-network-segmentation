# Terraform reference: cloud-only IT/OT concept simulation

The supplied blueprint used separate AWS VPCs and an ingress *allow* security group rule with a placeholder ID and labeled it a **deny** control. That cannot implement the claimed perimeter. An AWS VPC represents only a cloud simulation; it is **not an OT safety architecture** or an industrial firewall.

No production Terraform deployment is shipped in v0.1. Future cloud-lab IaC should create isolated VPCs with no transit connectivity by default, with explicit, reviewed route tables and security groups, constrained IAM, budgets, teardown procedures and automated policy validation. Do not connect any simulated network to a facility.

