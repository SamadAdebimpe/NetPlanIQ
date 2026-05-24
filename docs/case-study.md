# NetPlanIQ Case Study

## Problem

Manual IP address planning is a common source of errors in network design and implementation. Network engineers often need to allocate multiple subnets from a shared address block while balancing current host requirements, future growth, and efficient address usage.

Common problems include:

- incorrect subnet sizing
- invalid subnet boundaries
- address overlap
- insufficient capacity discovered too late
- poor documentation of usable ranges
- unclear gateway assignment
- lack of visibility into remaining address space
- inconsistent reporting for implementation teams
- poor visibility into which IP addresses have already been assigned
- accidental IP reuse, which can cause IP conflicts and service disruption

Without a clear IP assignment register, engineers may accidentally assign an address that is already being used by another host. This can lead to difficult troubleshooting during deployment, especially in branch networks, campus networks, labs, or environments with limited documentation.

## Solution

NetPlanIQ is a Python-based network planning tool that automates IPv4 subnet allocation and reporting.

The tool calculates suitable subnet sizes, sorts allocations using VLSM principles, validates capacity before allocation, aligns each subnet to valid CIDR boundaries, and exports structured Excel reports that can be used for review or implementation.

NetPlanIQ also includes optional detailed IP assignment sheets. These sheets allow users to track which addresses are available, reserved, assigned, or used for infrastructure roles such as gateways, servers, printers, access points, and DHCP pools.

This turns the exported plan into a practical IP register that can support implementation and reduce the risk of IP conflicts.

NetPlanIQ supports:

- host-based IPv4 subnet planning
- point-to-point /30 and /31 calculation
- tight, balanced, growth-friendly, and automatic planning preferences
- subnet boundary alignment
- pre-allocation capacity validation
- remaining CIDR block reporting
- optional detailed IP assignment sheets
- Excel reporting for review and implementation
- automated test coverage for core planning logic and export helpers

## Example Scenario

An organization needs to allocate IP address space from:

192.168.1.0/24

The required networks are:

Core Services: 50 hosts, growth-friendly
User VLAN: 15 hosts, auto

NetPlanIQ calculates the required subnet sizes, sorts the larger subnet first, validates that the base network has enough address space, and produces an allocation plan.

Example output:

Core Services -> 192.168.1.0/25
User VLAN     -> 192.168.1.128/27

It also reports the remaining available CIDR blocks:

192.168.1.160/27
192.168.1.192/26

This gives the engineer both the allocated design and the remaining address space available for future use.

## IP Assignment Tracking

NetPlanIQ can generate detailed IP assignment sheets for each planned subnet.

These sheets identify:

- the network address
- the suggested default gateway
- available host addresses
- the broadcast address
- notes for implementation teams

The IP assignment sheet can be used as a working register during deployment. Engineers can update the status of each address as devices are configured.

Example statuses include:

Available
Assigned
Reserved
Default Gateway
DHCP Pool
Server
Printer
Access Point
Firewall
Switch Management

This helps reduce the risk of IP conflict because the implementation team has a clear record of which addresses are planned, available, or already assigned.

## Technical Design Decisions

### VLSM Allocation

NetPlanIQ sorts subnet requests by calculated prefix size so larger subnet blocks are allocated first.

This follows common VLSM planning practice and reduces the chance of fragmentation preventing larger allocations from fitting later.

### Subnet Boundary Alignment

Each subnet must start at a valid boundary for its prefix length.

For example, valid /26 boundaries inside 192.168.1.0/24 are:

192.168.1.0/26
192.168.1.64/26
192.168.1.128/26
192.168.1.192/26

NetPlanIQ aligns each allocation to the correct boundary before creating the subnet.

### Capacity Validation

Before producing an allocation plan, NetPlanIQ checks whether all requested subnet blocks can fit inside the base network.

This prevents partial plans where some departments are allocated successfully but later allocations fail due to insufficient address space.

### Growth Preferences

NetPlanIQ supports four planning preferences:

tight
balanced
growth
auto

These preferences adjust the planning host requirement before the subnet prefix is calculated.

The auto preference gives smaller networks more growth room while avoiding excessive waste for larger networks.

### Utilization Reporting

NetPlanIQ separates user planning preference from utilization status.

For example, a user may choose a growth preference, while the final subnet utilization may be reported as:

Growth capacity available

This avoids confusing the selected planning strategy with the measured utilization of the chosen subnet.

### Remaining CIDR Blocks

After allocation, NetPlanIQ converts the unallocated address range into valid CIDR blocks.

This is more useful than only showing a start and end IP address because engineers can immediately see which valid subnet blocks remain available.

### Excel Reporting

NetPlanIQ exports structured Excel reports with:

- Plan Summary
- Allocations
- Remaining Blocks
- optional detailed IP assignment sheets
- point-to-point report export

The detailed IP assignment sheets mark:

- network address
- default gateway
- available host addresses
- broadcast address
- notes for implementation teams

## Future Network Discovery Feature

A future version of NetPlanIQ may include live network discovery to help identify addresses that are already active on a network.

Possible discovery methods include:

### Ping Sweep

The tool can ping addresses in a subnet and mark responding IPs as active.

This is simple and useful, but some devices block ICMP, so a lack of response does not always mean an address is unused.

### ARP Table Lookup

The tool can inspect ARP table entries after probing a local subnet.

This can improve local network visibility, especially for devices on the same Layer 2 segment.

### Nmap Integration

NetPlanIQ could integrate with Nmap to perform more advanced host discovery.

This would be useful for controlled environments where the engineer has permission to scan the network.

### DHCP Lease Import

The tool could import DHCP lease information to identify addresses currently assigned by a DHCP server.

This would improve accuracy in environments where most hosts receive addresses dynamically.

### Network Device Integration

A longer-term feature could integrate with routers, switches, firewalls, or IPAM systems using APIs, SNMP, or exported tables.

Possible data sources include:

DHCP leases
ARP tables
MAC address tables
router neighbor tables
firewall address objects
existing IPAM exports

This would allow NetPlanIQ to compare planned addresses with observed or documented network usage.

## Testing

NetPlanIQ includes automated tests for:

- host adjustment preferences
- prefix calculation
- VLSM sorting
- subnet allocation
- capacity validation
- remaining CIDR block calculation
- Excel worksheet name sanitization
- safe filename generation

The project uses GitHub Actions to run tests automatically on push and pull requests.

## Current Status

NetPlanIQ currently supports IPv4 planning for host-based networks and point-to-point links.

The codebase has been refactored into separate modules for:

core planning logic
CLI interaction
Excel exporting
tests

This structure makes the project easier to maintain, test, and extend.

## Impact

NetPlanIQ reduces manual subnetting errors and provides a repeatable way to produce documented IP plans for network design and implementation.

It is useful for:

- enterprise network planning
- campus network design
- branch office design
- lab and training environments
- infrastructure documentation
- IP address assignment tracking
- reducing IP conflict risk
- junior and experienced engineers who need reliable subnet planning support

## Roadmap

Planned improvements include:

- CSV import for bulk planning
- IPv6 subnet planning
- subnet conflict detection
- PDF report export
- Ansible inventory export
- DHCP range planning
- reserved address roles
- live network discovery
- DHCP lease import
- router, switch, and firewall integration
- web dashboard
- packaged CLI installation