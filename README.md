# NetPlanIQ

NetPlanIQ is a Python-based network planning tool for IPv4 subnet allocation, capacity validation, point-to-point link calculation, and Excel reporting.

It is designed to help network engineers and infrastructure teams produce accurate, documented IP addressing plans with clear subnet details, gateway recommendations, remaining address blocks, and implementation-ready reports.

## Features

- Host-based IPv4 subnet planning
- VLSM-style allocation from largest subnet to smallest subnet
- Tight, balanced, growth-friendly, and automatic planning preferences
- Subnet boundary alignment
- Capacity validation before allocation
- Base network normalization warnings
- Remaining unallocated CIDR block reporting
- Point-to-point `/30` and `/31` calculator
- Excel export with:
  - Plan Summary
  - Allocations
  - Remaining Blocks
  - Optional detailed IP assignment sheets
- Safe Excel worksheet naming
- Automated tests for core subnet logic and exporter helpers

## Project Structure

```text
IP-Planner/
  ip_planner/
    core.py
    cli.py
    exporters.py
    formatting.py
  tests/
    test_core.py
    test_exporters.py
  subnet.py
  requirements.txt
  pytest.ini
  README.md