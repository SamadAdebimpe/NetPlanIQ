from netaddr import IPNetwork, IPAddress, AddrFormatError, IPRange
from rich import print
from rich.table import Table

from ip_planner.core import (
    adjust_hosts_for_preference,
    calculate_prefix,
    sort_allocations_by_hosts,
    validate_capacity_before_allocation,
    allocate_subnets,
)

from ip_planner.exporters import export_to_excel, export_p2p_to_excel

# GET HOST BASED NETWORK
def get_host_base_network():
    while True:
        network_input = input("Enter base network (e.g: 192.168.1.0/24): ").strip()

        try:
            network = IPNetwork(network_input)

            if str(network.ip) != str(network.network):
                print(
                    f"[bold yellow]Note:[/bold yellow] {network_input} was normalized to "
                    f"{network.network}/{network.prefixlen} because the entered IP is not "
                    f"the actual network address for this prefix."
                )

            network = IPNetwork(f"{network.network}/{network.prefixlen}")
            if network.prefixlen >= 31:
                print("[bold red]Base network for host allocation must be larger than /31.[/bold red]")
                continue

            return network

        except AddrFormatError:
            print("[bold red]Invalid network format. Please try again.[/bold red]")
        except ValueError:
            print("[bold red]Invalid value entered. Please try again.[/bold red]")

# GET YES OR NO CHOICE
def get_yes_no_choice(prompt):
    while True:
        choice = input(prompt).strip().lower()

        if choice in ("y", "yes"):
            return True

        if choice in ("n", "no"):
            return False

        print("[bold red]Invalid choice. Please enter y or n.[/bold red]")

# GET P2P NETWORK
def get_p2p_network():
    while True:
        network_input = input("Enter point-to-point network (e.g: 192.168.1.0/31 or 192.168.1.0/30): ").strip()

        try:
            network = IPNetwork(network_input)

            if str(network.ip) != str(network.network):
                print(
                    f"[bold yellow]Note:[/bold yellow] {network_input} was normalized to "
                    f"{network.network}/{network.prefixlen} because the entered IP is not "
                    f"the actual network address for this prefix."
                )

            network = IPNetwork(f"{network.network}/{network.prefixlen}")

            if network.prefixlen not in (30, 31):
                print("[bold red]Point-to-point network must be /30 or /31.[/bold red]")
                continue

            return network
        
        except AddrFormatError:
            print("[bold red]Invalid network format. Please try again.[/bold red]")
        except ValueError:
            print("[bold red]Invalid value entered. Please try again.[/bold red]")

# Show network information
def show_network_info(network):
    total_addresses = network.size
    usable_hosts = total_addresses - 2 if network.prefixlen < 31 else total_addresses

    print("\n[bold green]Network Information[/bold green]")
    print(f"Network Address: {network.network}")
    print(f"CIDR Prefix: /{network.prefixlen}")
    print(f"Subnet Mask: {network.netmask}")
    print(f"Wildcard: {network.hostmask}")
    print(f"Broadcast Address: {network.broadcast}")
    print(f"Total Addresses: {total_addresses}")
    print(f"Usable Hosts: {usable_hosts}")

    if network.prefixlen < 31:
        print(f"First Usable IP: {network[1]}")
        print(f"Last Usable IP: {network[-2]}")
    elif network.prefixlen == 31:
        print(f"Usable IP 1: {network[0]}")
        print(f"Usable IP 2: {network[1]}")
    else:
        print("[bold yellow]This subnet does not have a traditional usable host range.[/bold yellow]")

#Get HOST ALLOCATION
def get_host_allocations():
    allocations = []

    while True:
        try:
            number_of_allocations = int(
                input("\nHow many departments/sections/blocks do you want to plan for? ").strip()
            )
            if number_of_allocations <= 0:
                print("[bold red]Please enter a number greater than 0.[/bold red]")
                continue
            break
        except ValueError:
            print("[bold red]Please enter a valid number.[/bold red]")

    for i in range(number_of_allocations):
        print(f"\nAllocation {i + 1}")

        while True:
            entry_name = input("Enter department/section/block name: ").strip()

            if not entry_name:
                print("[bold red]Name cannot be empty. Please enter a valid name.[/bold red]")
                continue

            existing_names = [
                allocation["name"].lower()
                for allocation in allocations
            ]

            if entry_name.lower() in existing_names:
                print(
                    "[bold red]This name has already been used. "
                    "Please enter a unique department/section/block name.[/bold red]"
                )
                continue

            break

        while True:
            try:
                hosts_needed = int(input("Enter the number of hosts needed: ").strip())
                if hosts_needed <= 0:
                    print("[bold red]Hosts must be greater than 0.[/bold red]")
                    continue
                break
            except ValueError:
                print("[bold red]Please enter a valid number of hosts.[/bold red]")

        while True:
            preference_choice = input(
                "Select planning preference (1: Tight, 2: Balanced, 3: Growth-friendly, 4: Auto): "
            ).strip()

            if preference_choice == "1":
                preference = "tight"
                break
            elif preference_choice == "2":
                preference = "balanced"
                break
            elif preference_choice == "3":
                preference = "growth"
                break
            elif preference_choice == "4":
                preference = "auto"
                break
            else:
                print("[bold red]Invalid choice. Enter 1, 2, 3, or 4.[/bold red]")

        allocation = {
            "name": entry_name,
            "hosts": hosts_needed,
            "type": "host",
            "preference": preference,
        }

        allocations.append(allocation)

    return allocations


# SHOW ALLOCATIONS
def show_allocations(allocations):
    print("\n[bold cyan]Allocation Requirements[/bold cyan]")

    for allocation in allocations:
        adjusted_hosts = adjust_hosts_for_preference(
            allocation["hosts"], allocation["preference"]
        )

        print(
            f"Name: {allocation['name']} | "
            f"Type: {allocation['type']} | "
            f"Hosts Needed: {allocation['hosts']} | "
            f"Preference: {allocation['preference']} | "
            f"Adjusted Hosts: {adjusted_hosts}"
        )


# SHOW ALLOCATION PREFIXES
def show_allocation_prefixes(allocations):
    print("\n[bold cyan]Allocation Subnet Sizes[/bold cyan]")

    for allocation in allocations:
        try:
            prefix = calculate_prefix(allocation["hosts"], allocation["preference"])
            print(
                f"Name: {allocation['name']} | "
                f"Hosts Needed: {allocation['hosts']} | "
                f"Preference: {allocation['preference']} | "
                f"Suggested Prefix: /{prefix}"
            )
        except ValueError as e:
            print(
                f"[bold red]Cannot calculate subnet size for {allocation['name']}: "
                f"{e}[/bold red]"
            )

# SHOW PLANNED SUBNETS
def show_planned_subnets(planned_subnets):
    table = Table(title="HOST-BASED ALLOCATION RESULT")
    
    table.add_column("Name", justify="left")
    table.add_column("Hosts Needed", justify="right")
    table.add_column("Network", justify="left")
    table.add_column("Prefix", justify="left")
    table.add_column("Subnet Mask", justify="left")
    table.add_column("Wildcard", justify="left")
    table.add_column("Broadcast", justify="left")
    table.add_column("Usable Hosts", justify="right")
    table.add_column("First IP", justify="left")
    table.add_column("Last IP", justify="left")
    table.add_column("suggested Gateway", justify="left")
    table.add_column("Unused Hosts", justify="right")
    table.add_column("Preference", justify="left")
    table.add_column("Adjusted Hosts", justify="right")
    table.add_column("Efficiency %", justify="right")
    table.add_column("Recommendation", justify="left")

    for subnet_info in planned_subnets:
        table.add_row(
            subnet_info["name"],
            str(subnet_info["hosts_needed"]),
            str(subnet_info["network"]),
            f"/{subnet_info['prefix']}",
            str(subnet_info["subnet_mask"]),
            str(subnet_info["wildcard"]),
            str(subnet_info["broadcast"]),
            str(subnet_info["usable_hosts"]),
            str(subnet_info["first_ip"]),
            str(subnet_info["last_ip"]),
            str(subnet_info["suggested_gateway"]),
            str(subnet_info["unused_hosts"]),
            subnet_info["preference"],
            str(subnet_info["adjusted_hosts"]),
            f"{subnet_info['efficiency']}%" if subnet_info["efficiency"] != "N/A" else "N/A",
            str(subnet_info["recommendation"]),
        )

    print(table)


# show_explanations
def show_explanations(planned_subnets):
    print("\n[bold cyan]Allocation Explanations [/bold cyan]")

    for subnet_info in planned_subnets:
        print(f"\n[bold yellow]{subnet_info['name']} [/bold yellow]")
        print(subnet_info["explanation"])

# show_summary

def show_summary(base_network, planned_subnets, next_free_ip=None):
    available_addresses = base_network.size

    if next_free_ip is not None:
        used_addresses = next_free_ip - int(base_network.network)
    else:
        used_addresses = sum(subnet["total_addresses"] for subnet in planned_subnets)

    remaining_addresses = available_addresses - used_addresses

    print("\n[bold blue]Allocation Summary[/bold blue]")
    print(f"Allocations Planned: {len(planned_subnets)}")
    print(f"Total Addresses Available: {available_addresses}")
    print(f"Total Address Space Consumed: {used_addresses}")
    print(f"Remaining Addresses: {remaining_addresses}")


# show_remaining_range
def show_remaining_range(base_network, next_free_ip):
    if next_free_ip is None:
        return

    if next_free_ip > int(base_network.broadcast):
        print("\n[bold yellow]No unallocated address space remains.[/bold yellow]")
        return

    start_ip = IPAddress(next_free_ip)
    end_ip = base_network.broadcast

    print("\n[bold cyan]Remaining Unallocated Range[/bold cyan]")
    print(f"Start: {start_ip}")
    print(f"End: {end_ip}")

    remaining_blocks = list(IPRange(start_ip, end_ip).cidrs())

    print("\n[bold cyan]Remaining Available CIDR Blocks[/bold cyan]")
    for block in remaining_blocks:
        usable_hosts = block.size - 2 if block.prefixlen < 31 else block.size
        print(
            f"{block} | Total Addresses: {block.size} | "
            f"Usable Hosts: {usable_hosts}"
        )

# show_p2p_result
def show_p2p_result(network):
    print("\n[bold green]POINT-TO-POINT RESULT[/bold green]")
    print(f"Network Address: {network.network}")
    print(f"CIDR Prefix: /{network.prefixlen}")
    print(f"Subnet Mask: {network.netmask}")
    print(f"Wildcard: {network.hostmask}")
    print(f"Broadcast Address: {network.broadcast}")
    print(f"Total Addresses: {network.size}")

    if network.prefixlen == 31:
        print(f"Usable IP 1: {network[0]}")
        print(f"Usable IP 2: {network[1]}")
        print("Usable Hosts: 2")
    elif network.prefixlen == 30:
        print(f"First Usable IP: {network[1]}")
        print(f"Last Usable IP: {network[-2]}")
        print("Usable Hosts: 2")

# MAIN
def main():
    while True:
        print("\n[bold cyan]IP Network Planner[/bold cyan]")
        print("1. Host-Based Allocation")
        print("2. Point-to-Point Calculator")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            base_network = get_host_base_network()
            show_network_info(base_network)

            allocations = get_host_allocations()
            sorted_allocations = sort_allocations_by_hosts(allocations)

            print("\n[bold magenta]Sorted Allocation Requirements[/bold magenta]")
            show_allocations(sorted_allocations)
            show_allocation_prefixes(sorted_allocations)

            if validate_capacity_before_allocation(base_network, sorted_allocations):
                planned_subnets, next_free_ip = allocate_subnets(base_network, sorted_allocations)

                if planned_subnets:
                    show_planned_subnets(planned_subnets)
                    show_explanations(planned_subnets)
                    show_summary(base_network, planned_subnets, next_free_ip)
                    show_remaining_range(base_network, next_free_ip)

                    include_ip_sheets = get_yes_no_choice(
                        "Include detailed IP assignment sheets in Excel? (y/n): "
                    )

                    export_to_excel(
                        planned_subnets,
                        base_network,
                        next_free_ip,
                        include_ip_sheets=include_ip_sheets
                    )

        elif choice == "2":
            p2p_network = get_p2p_network()
            show_p2p_result(p2p_network)

            if get_yes_no_choice("Export point-to-point result to Excel? (y/n): "):
                export_p2p_to_excel(p2p_network)

        elif choice == "3":
            print("[bold green]Goodbye![/bold green]")
            break

        else:
            print("[bold red]Invalid choice. Please try again.[/bold red]")

