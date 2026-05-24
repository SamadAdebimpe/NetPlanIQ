# NetPlanIQ Roadmap

NetPlanIQ is being developed as a practical network engineering and automation project. The roadmap focuses on improving subnet planning accuracy, reducing IP address management errors, supporting real-world implementation workflows, and demonstrating continued technical development.

## Current Version

NetPlanIQ currently supports:

- IPv4 host-based subnet planning
- VLSM-style allocation
- subnet boundary alignment
- capacity validation before allocation
- planning preferences: tight, balanced, growth-friendly, and auto
- remaining CIDR block reporting
- point-to-point `/30` and `/31` calculation
- Excel export with plan summary, allocation table, remaining blocks, and optional IP assignment sheets
- automated tests with GitHub Actions

## Short-Term Improvements

These improvements focus on making NetPlanIQ easier to use in practical network planning workflows.

- CSV import for bulk subnet requirements
- CSV export for allocation results
- improved Excel report styling
- improved CLI command structure
- packaged CLI command, for example `netplaniq`
- more automated tests for CLI and exporters
- example enterprise and campus network planning scenarios

## Medium-Term Improvements

These improvements focus on strengthening NetPlanIQ as an IP planning and implementation support tool.

- DHCP range planning
- reserved IP role support
- subnet conflict detection
- PDF report export
- JSON export for automation workflows
- Ansible inventory export
- support for importing existing IP allocation data
- better documentation for operational deployment use cases

## Long-Term Improvements

These improvements focus on expanding NetPlanIQ into a broader network automation and IP address management toolkit.

- IPv6 subnet planning
- live network discovery
- DHCP lease import
- ARP table import
- Nmap integration for permitted discovery scans
- router, switch, firewall, or IPAM API integration
- web dashboard
- multi-site planning
- cloud VPC/subnet planning support

## Future Discovery Feature

A future discovery module may help identify active IP addresses on reachable networks.

Possible methods include:

- ping sweep
- ARP table lookup
- DHCP lease import
- Nmap integration
- network device API/SNMP integration

This feature will require clear permission warnings because active scanning should only be performed on networks the user owns or is authorized to assess.

## Development Direction

NetPlanIQ is designed to support engineers and infrastructure teams who need to produce accurate IP plans, reduce subnetting errors, track address usage, and document remaining address capacity.

Future development will focus on making the tool more useful in operational environments by adding bulk imports, conflict detection, DHCP planning, live discovery, automation exports, and integrations with network infrastructure data sources.

The project reflects a practical approach to network engineering: solving a real operational problem with repeatable automation, clear reporting, and testable logic.