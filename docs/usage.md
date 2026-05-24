# NetPlanIQ Usage Guide

## Installation

Clone the repository:

git clone https://github.com/SamadAdebimpe/NetPlanIQ.git
cd NetPlanIQ

Create and activate a virtual environment:

python -m venv .venv

On Windows:

.venv\Scripts\activate

On macOS/Linux:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

## Run NetPlanIQ

Start the CLI:

python subnet.py

You will see:

IP Network Planner
1. Host-Based Allocation
2. Point-to-Point Calculator
3. Exit

## Host-Based Allocation Example

Choose:

1. Host-Based Allocation

Example base network:

192.168.1.0/24

Example requirements:

Core Services: 50 hosts, growth-friendly
User VLAN: 15 hosts, auto

NetPlanIQ will:

- show base network information
- sort allocation requirements by subnet size
- calculate suggested prefixes
- validate capacity before allocation
- allocate valid CIDR-aligned subnets
- show remaining unallocated CIDR blocks
- export an Excel report

## Planning Preferences

NetPlanIQ supports four planning preferences:

tight
balanced
growth
auto

### Tight

Uses the requested host count directly.

Best when IP conservation is the priority.

### Balanced

Adds moderate growth room.

Useful for networks expected to grow slightly.

### Growth-Friendly

Adds more growth room.

Useful for departments, sites, or VLANs expected to expand.

### Auto

Applies different growth logic based on the requested host count.

Smaller networks receive more growth room, while larger networks avoid excessive address waste.

## Excel Export

For host-based planning, NetPlanIQ can export:

- Plan Summary
- Allocations
- Remaining Blocks
- optional detailed IP assignment sheets

The optional IP assignment sheets help teams track:

- network address
- default gateway
- available host IPs
- broadcast address
- notes for implementation

## Point-to-Point Calculator

Choose:

2. Point-to-Point Calculator

Supported networks:

/30
/31

Example:

192.168.1.4/30

NetPlanIQ will show:

- network address
- prefix
- subnet mask
- wildcard
- broadcast address
- usable point-to-point IPs

You can also export the point-to-point result to Excel.

## Testing

Run tests:

pytest

Expected result:

11 passed