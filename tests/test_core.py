from netaddr import IPNetwork

from ip_planner.core import (
    adjust_hosts_for_preference,
    calculate_prefix,
    sort_allocations_by_hosts,
    validate_capacity_before_allocation,
    allocate_subnets,
    get_remaining_cidr_blocks,
)


def test_adjust_hosts_for_preference():
    assert adjust_hosts_for_preference(100, "tight") == 100
    assert adjust_hosts_for_preference(100, "balanced") == 120
    assert adjust_hosts_for_preference(100, "growth") == 150
    assert adjust_hosts_for_preference(15, "auto") == 23
    assert adjust_hosts_for_preference(80, "auto") == 104
    assert adjust_hosts_for_preference(1000, "auto") == 1200


def test_calculate_prefix():
    assert calculate_prefix(12, "tight") == 28
    assert calculate_prefix(50, "tight") == 26
    assert calculate_prefix(102, "tight") == 25
    assert calculate_prefix(15, "auto") == 27


def test_sort_allocations_by_prefix_size():
    allocations = [
        {"name": "small", "hosts": 12, "type": "host", "preference": "tight"},
        {"name": "large", "hosts": 102, "type": "host", "preference": "tight"},
        {"name": "medium", "hosts": 50, "type": "host", "preference": "tight"},
    ]

    sorted_allocations = sort_allocations_by_hosts(allocations)

    assert [allocation["name"] for allocation in sorted_allocations] == [
        "large",
        "medium",
        "small",
    ]


def test_allocate_subnets():
    base_network = IPNetwork("192.168.1.0/24")
    allocations = [
        {"name": "large", "hosts": 102, "type": "host", "preference": "tight"},
        {"name": "small", "hosts": 12, "type": "host", "preference": "tight"},
    ]

    planned_subnets, next_free_ip = allocate_subnets(base_network, allocations)

    assert str(planned_subnets[0]["network"]) == "192.168.1.0"
    assert planned_subnets[0]["prefix"] == 25
    assert str(planned_subnets[1]["network"]) == "192.168.1.128"
    assert planned_subnets[1]["prefix"] == 28
    assert next_free_ip == int(IPNetwork("192.168.1.128/28").broadcast) + 1


def test_capacity_validation_fails_when_base_is_too_small():
    base_network = IPNetwork("192.168.1.0/24")
    allocations = [
        {"name": "A", "hosts": 100, "type": "host", "preference": "tight"},
        {"name": "B", "hosts": 100, "type": "host", "preference": "tight"},
        {"name": "C", "hosts": 50, "type": "host", "preference": "tight"},
    ]

    assert validate_capacity_before_allocation(base_network, allocations) is False


def test_remaining_cidr_blocks():
    base_network = IPNetwork("192.168.1.0/24")
    next_free_ip = int(IPNetwork("192.168.1.128/28").broadcast) + 1

    remaining_blocks = get_remaining_cidr_blocks(base_network, next_free_ip)

    assert [str(block) for block in remaining_blocks] == [
        "192.168.1.144/28",
        "192.168.1.160/27",
        "192.168.1.192/26",
    ]