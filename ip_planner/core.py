import math
from netaddr import IPNetwork, IPAddress, IPRange
from rich import print

# Adjust host for preference
def adjust_hosts_for_preference(hosts_needed, preference):
    if preference == "tight":
        return hosts_needed
    elif preference == "balanced":
        return math.ceil(hosts_needed * 1.2)
    elif preference == "growth":
        return math.ceil(hosts_needed * 1.5)
    elif preference == "auto":
        if hosts_needed <= 30:
            return math.ceil(hosts_needed * 1.5)  # Small networks grow unpredictably
        elif hosts_needed <= 100:
            return math.ceil(hosts_needed * 1.3)  # Medium networks get moderate growth room
        else:
            return math.ceil(hosts_needed * 1.2)  # Large networks avoid excessive IP waste
    else:
        raise ValueError("Invalid planning preference.")
    

# Calculate prefix

def calculate_prefix(hosts_needed, preference="tight"):
    if not isinstance(hosts_needed, int):
        raise ValueError("Hosts needed must be a whole number.")

    if hosts_needed <= 0:
        raise ValueError("Hosts needed must be greater than 0.")

    adjusted_hosts = adjust_hosts_for_preference(hosts_needed, preference)

    if adjusted_hosts <= 0:
        raise ValueError("Adjusted host requirement must be greater than 0.")

    needed_addresses = adjusted_hosts + 2

    if needed_addresses > 2 ** 32:
        raise ValueError(
            "Host requirement is too large for IPv4. Use a smaller host count or split the design."
        )

    host_bits = math.ceil(math.log2(needed_addresses))
    prefix_length = 32 - host_bits

    if prefix_length < 0 or prefix_length > 30:
        raise ValueError(
            f"Calculated prefix /{prefix_length} is not valid for host allocation."
        )

    return prefix_length

#Sort allocation by hosts 

def sort_allocations_by_hosts(allocations):
    return sorted(
        allocations,
        key=lambda allocation: (
            calculate_prefix(allocation["hosts"], allocation["preference"]),
            -adjust_hosts_for_preference(allocation["hosts"], allocation["preference"])
        )
    )

# Align to prefix
def align_to_prefix_boundary(ip_as_int, prefix):
    block_size = 2 ** (32 - prefix)
    return((ip_as_int + block_size - 1 ) // block_size) * block_size

# Get recommendation
def get_recommendation(allocation_type, efficiency):
    if allocation_type != "host" or efficiency == "N/A":
        return "N/A"

    if efficiency >= 80:
        return "High utilization"
    elif efficiency >= 60:
        return "Moderate utilization"
    elif efficiency >= 40:
        return "Growth capacity available"
    else:
        return "Large spare capacity"
    
    #GET EXPLANATION

def get_explanation(hosts_needed, adjusted_hosts, prefix, usable_hosts, unused_hosts, efficiency, allocation_type, preference):
    if allocation_type != "host":
        return "Point-to-point allocation does not use host-based efficiency analysis."

    if efficiency >= 80:
        label = "high utilization"
    elif efficiency >= 60:
        label = "moderate utilization"
    elif efficiency >= 40:
        label = "available growth capacity"
    else:
        label = "large spare capacity"

    if preference == "auto":
        preference_sentence = (
            f"/{prefix} was selected for {hosts_needed} requested hosts using "
            f"the auto planning preference. Auto added growth room, increasing "
            f"the planning requirement to {adjusted_hosts} hosts."
        )
    else:
        preference_sentence = (
            f"/{prefix} was selected for {hosts_needed} requested hosts using "
            f"the {preference} planning preference. The planning requirement is "
            f"{adjusted_hosts} hosts."
        )

    return (
        f"{preference_sentence} "
        f"This subnet provides {usable_hosts} usable addresses "
        f"and leaves {unused_hosts} extra addresses. "
        f"Utilization efficiency is {round(efficiency, 2)}%, "
        f"indicating {label}."
    )

# VALIDATE CAPACITY BEFORE ALLOCATION
def validate_capacity_before_allocation(base_network, allocations):
    current_ip = int(base_network.network)
    base_end_ip = int(base_network.broadcast)

    total_required_addresses = 0
    total_alignment_gap = 0

    for allocation in allocations:
        try:
            prefix = calculate_prefix(allocation["hosts"], allocation["preference"])
        except ValueError as e:
            print("\n[bold red]Capacity Check Failed[/bold red]")
            print(f"[bold red]{allocation['name']}: {e}[/bold red]")
            return False

        block_size = 2 ** (32 - prefix)

        aligned_ip = align_to_prefix_boundary(current_ip, prefix)

        if aligned_ip > current_ip:
            total_alignment_gap += aligned_ip - current_ip

        subnet_end_ip = aligned_ip + block_size - 1
        total_required_addresses += block_size

        if subnet_end_ip > base_end_ip:
            print("\n[bold red]Capacity Check Failed[/bold red]")
            print(f"Base Network: {base_network}")
            print(f"Total Addresses Available: {base_network.size}")
            print(f"Required Subnet Block Size: {block_size}")
            print(
                f"[bold red]{allocation['name']} needs a /{prefix} subnet "
                f"({block_size} total addresses), but the base network only has "
                f"{base_network.size} total addresses.[/bold red]"
            )
            print(
                "[bold yellow]Use a larger base network or reduce the host requirements.[/bold yellow]"
            )
            return False

        current_ip = subnet_end_ip + 1

    print("\n[bold green]Capacity Check Passed[/bold green]")
    print(f"Base Network: {base_network}")
    print(f"Total Addresses Available: {base_network.size}")
    print(f"Total Required Subnet Blocks: {total_required_addresses}")

    # if total_alignment_gap > 0:
    #     print(f"Alignment Gap: {total_alignment_gap} addresses")

    return True


# Allocate subnets
def allocate_subnets(base_network, allocations):
    planned_subnets = []
    current_ip = int(base_network.network)

    for allocation in allocations:
        print(f"Allocating subnet for {allocation['name']}...")

        try:
            prefix = calculate_prefix(allocation["hosts"], allocation["preference"])
        except ValueError as e:
            print(f"[bold red]Cannot allocate subnet for {allocation['name']}: {e}[/bold red]")
            return [], None

        aligned_ip = align_to_prefix_boundary(current_ip, prefix)

        if aligned_ip != current_ip:
            print(
                f"[bold yellow]Adjusted start address from "
                f"{IPAddress(current_ip)} to {IPAddress(aligned_ip)} "
                f"to match /{prefix} subnet boundary.[/bold yellow]"
            )

        subnet = IPNetwork(f"{IPAddress(aligned_ip)}/{prefix}")

        if base_network.broadcast is None:
            print("[bold red]Base network has no usable broadcast address for planning.[/bold red]")
            return [], None

        if int(subnet.broadcast) > int(base_network.broadcast):
            print(f"[bold red]Not enough address space for {allocation['name']}[/bold red]")
            return [], None

        print(f"Subnet created: {subnet}")

        usable_hosts = subnet.size - 2 if subnet.prefixlen < 31 else subnet.size
        first_ip = subnet[1] if subnet.prefixlen < 31 else "N/A"
        last_ip = subnet[-2] if subnet.prefixlen < 31 else "N/A"

        if allocation["type"] == "host" and subnet.prefixlen < 31:
            suggested_gateway = first_ip
        else:
            suggested_gateway = "N/A"

        adjusted_hosts = adjust_hosts_for_preference(
            allocation["hosts"], allocation["preference"]
        )


        if allocation["type"] == "host" and usable_hosts > 0:
            unused_hosts = usable_hosts - adjusted_hosts
            efficiency = (adjusted_hosts / usable_hosts) * 100
        else:
            unused_hosts = "N/A"
            efficiency = "N/A"

        recommendation = get_recommendation(allocation["type"], efficiency)

        explanation = get_explanation(
            hosts_needed = allocation["hosts"],
            adjusted_hosts = adjusted_hosts,
            prefix = subnet.prefixlen,
            usable_hosts = usable_hosts,
            unused_hosts = unused_hosts,
            efficiency = efficiency,
            allocation_type = allocation["type"],
            preference = allocation["preference"]
        )


        subnet_info = {
            "name": allocation["name"],
            "type": allocation["type"],
            "preference": allocation["preference"],
            "hosts_needed": allocation["hosts"],
            "adjusted_hosts": adjusted_hosts,
            "total_addresses": subnet.size,
            "usable_hosts": usable_hosts,
            "unused_hosts": unused_hosts,
            "efficiency": round(efficiency, 2) if isinstance(efficiency, float) else efficiency,
            "recommendation": recommendation,
            "explanation": explanation,
            "network": subnet.network,
            "first_ip": first_ip,
            "last_ip": last_ip,
            "suggested_gateway": suggested_gateway,
            "prefix": subnet.prefixlen,
            "subnet_mask": subnet.netmask,
            "wildcard": IPAddress(int(subnet.hostmask)),
            "broadcast": subnet.broadcast,
        }

        planned_subnets.append(subnet_info)

        current_ip = int(subnet.broadcast) + 1
        print(f"Next Network Address: {IPAddress(current_ip)}")

    return planned_subnets, current_ip


# Remaining CIDR
def get_remaining_cidr_blocks(base_network, next_free_ip):
    if next_free_ip is None:
        return []

    if next_free_ip > int(base_network.broadcast):
        return []

    start_ip = IPAddress(next_free_ip)
    end_ip = base_network.broadcast

    return list(IPRange(start_ip, end_ip).cidrs())