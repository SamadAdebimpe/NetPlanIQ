from ip_planner.cli import main
# def get_host_base_network():
#     while True:
#         network_input = input("Enter base network (e.g: 192.168.1.0/24): ").strip()

#         try:
#             network = IPNetwork(network_input)

#             if str(network.ip) != str(network.network):
#                 print(
#                     f"[bold yellow]Note:[/bold yellow] {network_input} was normalized to "
#                     f"{network.network}/{network.prefixlen} because the entered IP is not "
#                     f"the actual network address for this prefix."
#                 )

#             network = IPNetwork(f"{network.network}/{network.prefixlen}")
#             if network.prefixlen >= 31:
#                 print("[bold red]Base network for host allocation must be larger than /31.[/bold red]")
#                 continue

#             return network

#         except AddrFormatError:
#             print("[bold red]Invalid network format. Please try again.[/bold red]")
#         except ValueError:
#             print("[bold red]Invalid value entered. Please try again.[/bold red]")

# def get_yes_no_choice(prompt):
#     while True:
#         choice = input(prompt).strip().lower()

#         if choice in ("y", "yes"):
#             return True

#         if choice in ("n", "no"):
#             return False

#         print("[bold red]Invalid choice. Please enter y or n.[/bold red]")

# def get_p2p_network():
#     while True:
#         network_input = input("Enter point-to-point network (e.g: 192.168.1.0/31 or 192.168.1.0/30): ").strip()

#         try:
#             network = IPNetwork(network_input)

#             if str(network.ip) != str(network.network):
#                 print(
#                     f"[bold yellow]Note:[/bold yellow] {network_input} was normalized to "
#                     f"{network.network}/{network.prefixlen} because the entered IP is not "
#                     f"the actual network address for this prefix."
#                 )

#             network = IPNetwork(f"{network.network}/{network.prefixlen}")

#             if network.prefixlen not in (30, 31):
#                 print("[bold red]Point-to-point network must be /30 or /31.[/bold red]")
#                 continue

#             return network
        
#         except AddrFormatError:
#             print("[bold red]Invalid network format. Please try again.[/bold red]")
#         except ValueError:
#             print("[bold red]Invalid value entered. Please try again.[/bold red]")


# def show_network_info(network):
#     total_addresses = network.size
#     usable_hosts = total_addresses - 2 if network.prefixlen < 31 else total_addresses

#     print("\n[bold green]Network Information[/bold green]")
#     print(f"Network Address: {network.network}")
#     print(f"CIDR Prefix: /{network.prefixlen}")
#     print(f"Subnet Mask: {network.netmask}")
#     print(f"Wildcard: {network.hostmask}")
#     print(f"Broadcast Address: {network.broadcast}")
#     print(f"Total Addresses: {total_addresses}")
#     print(f"Usable Hosts: {usable_hosts}")

#     if network.prefixlen < 31:
#         print(f"First Usable IP: {network[1]}")
#         print(f"Last Usable IP: {network[-2]}")
#     elif network.prefixlen == 31:
#         print(f"Usable IP 1: {network[0]}")
#         print(f"Usable IP 2: {network[1]}")
#     else:
#         print("[bold yellow]This subnet does not have a traditional usable host range.[/bold yellow]")


# def get_host_allocations():
#     allocations = []

#     while True:
#         try:
#             number_of_allocations = int(
#                 input("\nHow many departments/sections/blocks do you want to plan for? ").strip()
#             )
#             if number_of_allocations <= 0:
#                 print("[bold red]Please enter a number greater than 0.[/bold red]")
#                 continue
#             break
#         except ValueError:
#             print("[bold red]Please enter a valid number.[/bold red]")

#     for i in range(number_of_allocations):
#         print(f"\nAllocation {i + 1}")

#         while True:
#             entry_name = input("Enter department/section/block name: ").strip()

#             if not entry_name:
#                 print("[bold red]Name cannot be empty. Please enter a valid name.[/bold red]")
#                 continue

#             existing_names = [
#                 allocation["name"].lower()
#                 for allocation in allocations
#             ]

#             if entry_name.lower() in existing_names:
#                 print(
#                     "[bold red]This name has already been used. "
#                     "Please enter a unique department/section/block name.[/bold red]"
#                 )
#                 continue

#             break

#         while True:
#             try:
#                 hosts_needed = int(input("Enter the number of hosts needed: ").strip())
#                 if hosts_needed <= 0:
#                     print("[bold red]Hosts must be greater than 0.[/bold red]")
#                     continue
#                 break
#             except ValueError:
#                 print("[bold red]Please enter a valid number of hosts.[/bold red]")

#         while True:
#             preference_choice = input(
#                 "Select planning preference (1: Tight, 2: Balanced, 3: Growth-friendly, 4: Auto): "
#             ).strip()

#             if preference_choice == "1":
#                 preference = "tight"
#                 break
#             elif preference_choice == "2":
#                 preference = "balanced"
#                 break
#             elif preference_choice == "3":
#                 preference = "growth"
#                 break
#             elif preference_choice == "4":
#                 preference = "auto"
#                 break
#             else:
#                 print("[bold red]Invalid choice. Enter 1, 2, 3, or 4.[/bold red]")

#         allocation = {
#             "name": entry_name,
#             "hosts": hosts_needed,
#             "type": "host",
#             "preference": preference,
#         }

#         allocations.append(allocation)

#     return allocations

# def show_allocations(allocations):
#     print("\n[bold cyan]Allocation Requirements[/bold cyan]")

#     for allocation in allocations:
#         adjusted_hosts = adjust_hosts_for_preference(
#             allocation["hosts"], allocation["preference"]
#         )

#         print(
#             f"Name: {allocation['name']} | "
#             f"Type: {allocation['type']} | "
#             f"Hosts Needed: {allocation['hosts']} | "
#             f"Preference: {allocation['preference']} | "
#             f"Adjusted Hosts: {adjusted_hosts}"
#         )


# def sort_allocations_by_hosts(allocations):
#     return sorted(
#         allocations,
#         key=lambda allocation: (
#             calculate_prefix(allocation["hosts"], allocation["preference"]),
#             -adjust_hosts_for_preference(allocation["hosts"], allocation["preference"])
#         )
#     )

# def adjust_hosts_for_preference(hosts_needed, preference):
#     if preference == "tight":
#         return hosts_needed
#     elif preference == "balanced":
#         return math.ceil(hosts_needed * 1.2)
#     elif preference == "growth":
#         return math.ceil(hosts_needed * 1.5)
#     elif preference == "auto":
#         if hosts_needed <= 30:
#             return math.ceil(hosts_needed * 1.5)  # Small networks grow unpredictably
#         elif hosts_needed <= 100:
#             return math.ceil(hosts_needed * 1.3)  # Medium networks get moderate growth room
#         else:
#             return math.ceil(hosts_needed * 1.2)  # Large networks avoid excessive IP waste
#     else:
#         raise ValueError("Invalid planning preference.")
    
# def calculate_prefix(hosts_needed, preference="tight"):
#     if not isinstance(hosts_needed, int):
#         raise ValueError("Hosts needed must be a whole number.")

#     if hosts_needed <= 0:
#         raise ValueError("Hosts needed must be greater than 0.")

#     adjusted_hosts = adjust_hosts_for_preference(hosts_needed, preference)

#     if adjusted_hosts <= 0:
#         raise ValueError("Adjusted host requirement must be greater than 0.")

#     needed_addresses = adjusted_hosts + 2

#     if needed_addresses > 2 ** 32:
#         raise ValueError(
#             "Host requirement is too large for IPv4. Use a smaller host count or split the design."
#         )

#     host_bits = math.ceil(math.log2(needed_addresses))
#     prefix_length = 32 - host_bits

#     if prefix_length < 0 or prefix_length > 30:
#         raise ValueError(
#             f"Calculated prefix /{prefix_length} is not valid for host allocation."
#         )

#     return prefix_length

# def get_recommendation(allocation_type, efficiency):
#     if allocation_type != "host" or efficiency == "N/A":
#         return "N/A"

#     if efficiency >= 80:
#         return "High utilization"
#     elif efficiency >= 60:
#         return "Moderate utilization"
#     elif efficiency >= 40:
#         return "Growth capacity available"
#     else:
#         return "Large spare capacity"

# def get_explanation(hosts_needed, adjusted_hosts, prefix, usable_hosts, unused_hosts, efficiency, allocation_type, preference):
#     if allocation_type != "host":
#         return "Point-to-point allocation does not use host-based efficiency analysis."

#     if efficiency >= 80:
#         label = "high utilization"
#     elif efficiency >= 60:
#         label = "moderate utilization"
#     elif efficiency >= 40:
#         label = "available growth capacity"
#     else:
#         label = "large spare capacity"

#     if preference == "auto":
#         preference_sentence = (
#             f"/{prefix} was selected for {hosts_needed} requested hosts using "
#             f"the auto planning preference. Auto added growth room, increasing "
#             f"the planning requirement to {adjusted_hosts} hosts."
#         )
#     else:
#         preference_sentence = (
#             f"/{prefix} was selected for {hosts_needed} requested hosts using "
#             f"the {preference} planning preference. The planning requirement is "
#             f"{adjusted_hosts} hosts."
#         )

#     return (
#         f"{preference_sentence} "
#         f"This subnet provides {usable_hosts} usable addresses "
#         f"and leaves {unused_hosts} extra addresses. "
#         f"Utilization efficiency is {round(efficiency, 2)}%, "
#         f"indicating {label}."
#     )
    
    

# def show_allocation_prefixes(allocations):
#     print("\n[bold cyan]Allocation Subnet Sizes[/bold cyan]")

#     for allocation in allocations:
#         try:
#             prefix = calculate_prefix(allocation["hosts"], allocation["preference"])
#             print(
#                 f"Name: {allocation['name']} | "
#                 f"Hosts Needed: {allocation['hosts']} | "
#                 f"Preference: {allocation['preference']} | "
#                 f"Suggested Prefix: /{prefix}"
#             )
#         except ValueError as e:
#             print(
#                 f"[bold red]Cannot calculate subnet size for {allocation['name']}: "
#                 f"{e}[/bold red]"
#             )


# def align_to_prefix_boundary(ip_as_int, prefix):
#     block_size = 2 ** (32 - prefix)
#     return((ip_as_int + block_size - 1 ) // block_size) * block_size

# def validate_capacity_before_allocation(base_network, allocations):
#     current_ip = int(base_network.network)
#     base_end_ip = int(base_network.broadcast)

#     total_required_addresses = 0
#     total_alignment_gap = 0

#     for allocation in allocations:
#         try:
#             prefix = calculate_prefix(allocation["hosts"], allocation["preference"])
#         except ValueError as e:
#             print("\n[bold red]Capacity Check Failed[/bold red]")
#             print(f"[bold red]{allocation['name']}: {e}[/bold red]")
#             return False

#         block_size = 2 ** (32 - prefix)

#         aligned_ip = align_to_prefix_boundary(current_ip, prefix)

#         if aligned_ip > current_ip:
#             total_alignment_gap += aligned_ip - current_ip

#         subnet_end_ip = aligned_ip + block_size - 1
#         total_required_addresses += block_size

#         if subnet_end_ip > base_end_ip:
#             print("\n[bold red]Capacity Check Failed[/bold red]")
#             print(f"Base Network: {base_network}")
#             print(f"Total Addresses Available: {base_network.size}")
#             print(f"Required Subnet Block Size: {block_size}")
#             print(
#                 f"[bold red]{allocation['name']} needs a /{prefix} subnet "
#                 f"({block_size} total addresses), but the base network only has "
#                 f"{base_network.size} total addresses.[/bold red]"
#             )
#             print(
#                 "[bold yellow]Use a larger base network or reduce the host requirements.[/bold yellow]"
#             )
#             return False

#         current_ip = subnet_end_ip + 1

#     print("\n[bold green]Capacity Check Passed[/bold green]")
#     print(f"Base Network: {base_network}")
#     print(f"Total Addresses Available: {base_network.size}")
#     print(f"Total Required Subnet Blocks: {total_required_addresses}")

#     # if total_alignment_gap > 0:
#     #     print(f"Alignment Gap: {total_alignment_gap} addresses")

#     return True


# def allocate_subnets(base_network, allocations):
#     planned_subnets = []
#     current_ip = int(base_network.network)

#     for allocation in allocations:
#         print(f"Allocating subnet for {allocation['name']}...")

#         try:
#             prefix = calculate_prefix(allocation["hosts"], allocation["preference"])
#         except ValueError as e:
#             print(f"[bold red]Cannot allocate subnet for {allocation['name']}: {e}[/bold red]")
#             return [], None

#         aligned_ip = align_to_prefix_boundary(current_ip, prefix)

#         if aligned_ip != current_ip:
#             print(
#                 f"[bold yellow]Adjusted start address from "
#                 f"{IPAddress(current_ip)} to {IPAddress(aligned_ip)} "
#                 f"to match /{prefix} subnet boundary.[/bold yellow]"
#             )

#         subnet = IPNetwork(f"{IPAddress(aligned_ip)}/{prefix}")

#         if base_network.broadcast is None:
#             print("[bold red]Base network has no usable broadcast address for planning.[/bold red]")
#             return [], None

#         if int(subnet.broadcast) > int(base_network.broadcast):
#             print(f"[bold red]Not enough address space for {allocation['name']}[/bold red]")
#             return [], None

#         print(f"Subnet created: {subnet}")

#         usable_hosts = subnet.size - 2 if subnet.prefixlen < 31 else subnet.size
#         first_ip = subnet[1] if subnet.prefixlen < 31 else "N/A"
#         last_ip = subnet[-2] if subnet.prefixlen < 31 else "N/A"

#         if allocation["type"] == "host" and subnet.prefixlen < 31:
#             suggested_gateway = first_ip
#         else:
#             suggested_gateway = "N/A"

#         adjusted_hosts = adjust_hosts_for_preference(
#             allocation["hosts"], allocation["preference"]
#         )


#         if allocation["type"] == "host" and usable_hosts > 0:
#             unused_hosts = usable_hosts - adjusted_hosts
#             efficiency = (adjusted_hosts / usable_hosts) * 100
#         else:
#             unused_hosts = "N/A"
#             efficiency = "N/A"

#         recommendation = get_recommendation(allocation["type"], efficiency)

#         explanation = get_explanation(
#             hosts_needed = allocation["hosts"],
#             adjusted_hosts = adjusted_hosts,
#             prefix = subnet.prefixlen,
#             usable_hosts = usable_hosts,
#             unused_hosts = unused_hosts,
#             efficiency = efficiency,
#             allocation_type = allocation["type"],
#             preference = allocation["preference"]
#         )


#         subnet_info = {
#             "name": allocation["name"],
#             "type": allocation["type"],
#             "preference": allocation["preference"],
#             "hosts_needed": allocation["hosts"],
#             "adjusted_hosts": adjusted_hosts,
#             "total_addresses": subnet.size,
#             "usable_hosts": usable_hosts,
#             "unused_hosts": unused_hosts,
#             "efficiency": round(efficiency, 2) if isinstance(efficiency, float) else efficiency,
#             "recommendation": recommendation,
#             "explanation": explanation,
#             "network": subnet.network,
#             "first_ip": first_ip,
#             "last_ip": last_ip,
#             "suggested_gateway": suggested_gateway,
#             "prefix": subnet.prefixlen,
#             "subnet_mask": subnet.netmask,
#             "wildcard": IPAddress(int(subnet.hostmask)),
#             "broadcast": subnet.broadcast,
#         }

#         planned_subnets.append(subnet_info)

#         current_ip = int(subnet.broadcast) + 1
#         print(f"Next Network Address: {IPAddress(current_ip)}")

#     return planned_subnets, current_ip


# def show_planned_subnets(planned_subnets):
#     table = Table(title="HOST-BASED ALLOCATION RESULT")
    
#     table.add_column("Name", justify="left")
#     table.add_column("Hosts Needed", justify="right")
#     table.add_column("Network", justify="left")
#     table.add_column("Prefix", justify="left")
#     table.add_column("Subnet Mask", justify="left")
#     table.add_column("Wildcard", justify="left")
#     table.add_column("Broadcast", justify="left")
#     table.add_column("Usable Hosts", justify="right")
#     table.add_column("First IP", justify="left")
#     table.add_column("Last IP", justify="left")
#     table.add_column("suggested Gateway", justify="left")
#     table.add_column("Unused Hosts", justify="right")
#     table.add_column("Preference", justify="left")
#     table.add_column("Adjusted Hosts", justify="right")
#     table.add_column("Efficiency %", justify="right")
#     table.add_column("Recommendation", justify="left")

#     for subnet_info in planned_subnets:
#         table.add_row(
#             subnet_info["name"],
#             str(subnet_info["hosts_needed"]),
#             str(subnet_info["network"]),
#             f"/{subnet_info['prefix']}",
#             str(subnet_info["subnet_mask"]),
#             str(subnet_info["wildcard"]),
#             str(subnet_info["broadcast"]),
#             str(subnet_info["usable_hosts"]),
#             str(subnet_info["first_ip"]),
#             str(subnet_info["last_ip"]),
#             str(subnet_info["suggested_gateway"]),
#             str(subnet_info["unused_hosts"]),
#             subnet_info["preference"],
#             str(subnet_info["adjusted_hosts"]),
#             f"{subnet_info['efficiency']}%" if subnet_info["efficiency"] != "N/A" else "N/A",
#             str(subnet_info["recommendation"]),
#         )

#     print(table)


# def show_explanations(planned_subnets):
#     print("\n[bold cyan]Allocation Explanations [/bold cyan]")

#     for subnet_info in planned_subnets:
#         print(f"\n[bold yellow]{subnet_info['name']} [/bold yellow]")
#         print(subnet_info["explanation"])


# def show_summary(base_network, planned_subnets, next_free_ip=None):
#     available_addresses = base_network.size

#     if next_free_ip is not None:
#         used_addresses = next_free_ip - int(base_network.network)
#     else:
#         used_addresses = sum(subnet["total_addresses"] for subnet in planned_subnets)

#     remaining_addresses = available_addresses - used_addresses

#     print("\n[bold blue]Allocation Summary[/bold blue]")
#     print(f"Allocations Planned: {len(planned_subnets)}")
#     print(f"Total Addresses Available: {available_addresses}")
#     print(f"Total Address Space Consumed: {used_addresses}")
#     print(f"Remaining Addresses: {remaining_addresses}")


# def show_remaining_range(base_network, next_free_ip):
#     if next_free_ip is None:
#         return

#     if next_free_ip > int(base_network.broadcast):
#         print("\n[bold yellow]No unallocated address space remains.[/bold yellow]")
#         return

#     start_ip = IPAddress(next_free_ip)
#     end_ip = base_network.broadcast

#     print("\n[bold cyan]Remaining Unallocated Range[/bold cyan]")
#     print(f"Start: {start_ip}")
#     print(f"End: {end_ip}")

#     remaining_blocks = list(IPRange(start_ip, end_ip).cidrs())

#     print("\n[bold cyan]Remaining Available CIDR Blocks[/bold cyan]")
#     for block in remaining_blocks:
#         usable_hosts = block.size - 2 if block.prefixlen < 31 else block.size
#         print(
#             f"{block} | Total Addresses: {block.size} | "
#             f"Usable Hosts: {usable_hosts}"
#         )

# def sanitize_sheet_name(name):
#     invalid_characters = ["\\", "/", "?", "*", "[", "]", ":"]

#     cleaned_name = str(name).strip()

#     for character in invalid_characters:
#         cleaned_name = cleaned_name.replace(character, "_")

#     if not cleaned_name:
#         cleaned_name = "Sheet"

#     return cleaned_name[:31]


# def get_unique_sheet_name(workbook, base_name):
#     sheet_name = sanitize_sheet_name(base_name)

#     if sheet_name not in workbook.sheetnames:
#         return sheet_name

#     counter = 1

#     while True:
#         suffix = f"_{counter}"
#         max_name_length = 31 - len(suffix)
#         candidate_name = f"{sheet_name[:max_name_length]}{suffix}"

#         if candidate_name not in workbook.sheetnames:
#             return candidate_name

#         counter += 1

# def get_remaining_cidr_blocks(base_network, next_free_ip):
#     if next_free_ip is None:
#         return []

#     if next_free_ip > int(base_network.broadcast):
#         return []

#     start_ip = IPAddress(next_free_ip)
#     end_ip = base_network.broadcast

#     return list(IPRange(start_ip, end_ip).cidrs())

# def format_worksheet(sheet):
#     header_fill = PatternFill("solid", fgColor="1F4E78")
#     header_font = Font(color="FFFFFF", bold=True)
#     title_font = Font(bold=True, size=12)

#     for row in sheet.iter_rows():
#         for cell in row:
#             cell.alignment = Alignment(vertical="top", wrap_text=True)

#     if sheet.title == "Plan Summary":
#         for cell in sheet["A"]:
#             if cell.value:
#                 cell.font = title_font
#         sheet.freeze_panes = "A2"

#     else:
#         for cell in sheet[1]:
#             cell.font = header_font
#             cell.fill = header_fill

#         sheet.freeze_panes = "A2"

#         if sheet.max_row > 1 and sheet.max_column > 1:
#             sheet.auto_filter.ref = sheet.dimensions

#     for column_cells in sheet.columns:
#         max_length = 0
#         column_letter = column_cells[0].column_letter

#         for cell in column_cells:
#             if cell.value is not None:
#                 max_length = max(max_length, len(str(cell.value)))

#         adjusted_width = min(max_length + 2, 45)
#         sheet.column_dimensions[column_letter].width = adjusted_width

# def safe_filename_part(value):
#     invalid_characters = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]

#     cleaned_value = str(value).strip()

#     for character in invalid_characters:
#         cleaned_value = cleaned_value.replace(character, "_")

#     return cleaned_value

# def export_to_excel(planned_subnets, base_network=None, next_free_ip=None, filename=None, include_ip_sheets=True):
#     try:
#         if filename is None:
#             timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#             if base_network is not None:
#                 network_part = safe_filename_part(str(base_network))
#                 filename = f"ip_plan_{network_part}_{timestamp}.xlsx"
#             else:
#                 filename = f"ip_plan_{timestamp}.xlsx"

#         workbook = Workbook()

#         summary_sheet = workbook.active
#         summary_sheet.title = "Plan Summary"

#         if base_network is not None:
#             total_available = base_network.size

#             if next_free_ip is not None:
#                 total_consumed = next_free_ip - int(base_network.network)
#             else:
#                 total_consumed = sum(subnet["total_addresses"] for subnet in planned_subnets)

#             remaining_addresses = total_available - total_consumed

#             summary_sheet.append(["Plan Summary", ""])
#             summary_sheet.append(["Base Network", str(base_network)])
#             summary_sheet.append(["Network Address", str(base_network.network)])
#             summary_sheet.append(["CIDR Prefix", f"/{base_network.prefixlen}"])
#             summary_sheet.append(["Subnet Mask", str(base_network.netmask)])
#             summary_sheet.append(["Wildcard", str(base_network.hostmask)])
#             summary_sheet.append(["Broadcast Address", str(base_network.broadcast)])
#             summary_sheet.append(["Total Addresses Available", total_available])
#             summary_sheet.append(["Total Address Space Consumed", total_consumed])
#             summary_sheet.append(["Remaining Addresses", remaining_addresses])
#             summary_sheet.append(["Generated On", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
#         else:
#             summary_sheet.append(["Plan Summary", ""])
#             summary_sheet.append(["Generated On", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

#         allocation_sheet = workbook.create_sheet(title="Allocations")

#         allocation_sheet.append([
#             "Name",
#             "Type",
#             "Hosts Needed",
#             "Network Address",
#             "Prefix",
#             "Subnet Mask",
#             "Wildcard",
#             "Broadcast Address",
#             "Total Addresses",
#             "Usable Hosts",
#             "First Usable IP",
#             "Last Usable IP",
#             "Suggested Gateway",
#             "Unused Hosts",
#             "Preference",
#             "Adjusted Hosts",
#             "Efficiency %",
#             "Recommendation",
#             "Explanation",
#         ])

#         for subnet_info in planned_subnets:
#             allocation_sheet.append([
#                 subnet_info["name"],
#                 subnet_info["type"],
#                 subnet_info["hosts_needed"],
#                 str(subnet_info["network"]),
#                 subnet_info["prefix"],
#                 str(subnet_info["subnet_mask"]),
#                 str(subnet_info["wildcard"]),
#                 str(subnet_info["broadcast"]),
#                 subnet_info["total_addresses"],
#                 subnet_info["usable_hosts"],
#                 str(subnet_info["first_ip"]),
#                 str(subnet_info["last_ip"]),
#                 str(subnet_info["suggested_gateway"]),
#                 subnet_info["unused_hosts"],
#                 subnet_info["preference"],
#                 subnet_info["adjusted_hosts"],
#                 subnet_info["efficiency"],
#                 subnet_info["recommendation"],
#                 subnet_info["explanation"],
#             ])

#         if base_network is not None and next_free_ip is not None:
#             remaining_sheet = workbook.create_sheet(title="Remaining Blocks")

#             remaining_sheet.append([
#                 "CIDR Block",
#                 "Network Address",
#                 "Prefix",
#                 "Subnet Mask",
#                 "Wildcard",
#                 "Broadcast Address",
#                 "Total Addresses",
#                 "Usable Hosts",
#                 "First Usable IP",
#                 "Last Usable IP",
#                 "Note",
#             ])

#             remaining_blocks = get_remaining_cidr_blocks(base_network, next_free_ip)

#             if not remaining_blocks:
#                 remaining_sheet.append([
#                     "N/A",
#                     "",
#                     "",
#                     "",
#                     "",
#                     "",
#                     0,
#                     0,
#                     "",
#                     "",
#                     "No unallocated address space remains.",
#                 ])
#             else:
#                 for block in remaining_blocks:
#                     usable_hosts = block.size - 2 if block.prefixlen < 31 else block.size
#                     first_ip = block[1] if block.prefixlen < 31 else block[0]
#                     last_ip = block[-2] if block.prefixlen < 31 else block[-1]

#                     remaining_sheet.append([
#                         str(block),
#                         str(block.network),
#                         block.prefixlen,
#                         str(block.netmask),
#                         str(block.hostmask),
#                         str(block.broadcast),
#                         block.size,
#                         usable_hosts,
#                         str(first_ip),
#                         str(last_ip),
#                         "Available for future allocation",
#                     ])

#         if include_ip_sheets:
#             for subnet_info in planned_subnets:
#                 sheet_name = get_unique_sheet_name(workbook, subnet_info["name"])
#                 dept_sheet = workbook.create_sheet(title=sheet_name)

#                 dept_sheet.append(["IP Address / Range", "Status", "Default Gateway", "Note"])

#                 if subnet_info["first_ip"] == "N/A" or subnet_info["last_ip"] == "N/A":
#                     dept_sheet.append([
#                         str(subnet_info["network"]),
#                         "Network",
#                         "",
#                         "No traditional usable host range available for this subnet.",
#                     ])
#                     continue

#                 if subnet_info["usable_hosts"] > 3000:
#                     dept_sheet.append([
#                         str(subnet_info["network"]),
#                         "Network Address",
#                         "",
#                         "Do not assign to a device",
#                     ])

#                     dept_sheet.append([
#                         str(subnet_info["suggested_gateway"]),
#                         "Default Gateway",
#                         str(subnet_info["suggested_gateway"]),
#                         "Assign to router, firewall, or Layer 3 switch interface",
#                     ])

#                     available_start = IPAddress(int(subnet_info["first_ip"]) + 1)

#                     dept_sheet.append([
#                         f"{available_start} - {subnet_info['last_ip']}",
#                         "Available Range",
#                         str(subnet_info["suggested_gateway"]),
#                         "Usable for hosts, servers, printers, APs, or DHCP pool",
#                     ])

#                     dept_sheet.append([
#                         str(subnet_info["broadcast"]),
#                         "Broadcast Address",
#                         "",
#                         "Do not assign to a device",
#                     ])

#                     dept_sheet.append([
#                         str(subnet_info["usable_hosts"]),
#                         "Usable Hosts",
#                         "",
#                         "Total assignable host addresses in this subnet",
#                     ])

#                 else:
#                     dept_sheet.append([
#                         str(subnet_info["network"]),
#                         "Network Address",
#                         "",
#                         "Do not assign to a device",
#                     ])

#                     first_ip = IPAddress(subnet_info["first_ip"])
#                     last_ip = IPAddress(subnet_info["last_ip"])
#                     gateway = IPAddress(subnet_info["suggested_gateway"])

#                     current_ip = int(first_ip)

#                     while current_ip <= int(last_ip):
#                         ip_address = IPAddress(current_ip)

#                         if ip_address == gateway:
#                             status = "Default Gateway"
#                             note = "Assign to router, firewall, or Layer 3 switch interface"
#                         else:
#                             status = "Available"
#                             note = "Available for host assignment"

#                         dept_sheet.append([
#                             str(ip_address),
#                             status,
#                             str(gateway),
#                             note,
#                         ])

#                         current_ip += 1

#                     dept_sheet.append([
#                         str(subnet_info["broadcast"]),
#                         "Broadcast Address",
#                         "",
#                         "Do not assign to a device",
#                     ])

#         for sheet in workbook.worksheets:
#             format_worksheet(sheet)

#         workbook.save(filename)
#         print(f"\n[bold green]Excel Export completed: {filename}[/bold green]")

#     except Exception as e:
#         print(f"[bold red]Excel export failed: {e}[/bold red]")


# def export_p2p_to_excel(network, filename=None):
#     try:
#         if filename is None:
#             timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#             network_part = safe_filename_part(str(network))
#             filename = f"p2p_plan_{network_part}_{timestamp}.xlsx"

#         workbook = Workbook()
#         sheet = workbook.active
#         sheet.title = "Point-to-Point"

#         sheet.append(["Field", "Value"])
#         sheet.append(["Network Address", str(network.network)])
#         sheet.append(["CIDR Prefix", f"/{network.prefixlen}"])
#         sheet.append(["Subnet Mask", str(network.netmask)])
#         sheet.append(["Wildcard", str(network.hostmask)])
#         sheet.append(["Broadcast Address", str(network.broadcast)])
#         sheet.append(["Total Addresses", network.size])

#         if network.prefixlen == 31:
#             sheet.append(["Usable IP 1", str(network[0])])
#             sheet.append(["Usable IP 2", str(network[1])])
#             sheet.append(["Usable Hosts", 2])
#             sheet.append(["Note", "/31 is commonly used for point-to-point links under RFC 3021."])
#         elif network.prefixlen == 30:
#             sheet.append(["First Usable IP", str(network[1])])
#             sheet.append(["Last Usable IP", str(network[-2])])
#             sheet.append(["Usable Hosts", 2])
#             sheet.append(["Note", "/30 provides two usable host addresses for point-to-point links."])

#         format_worksheet(sheet)

#         workbook.save(filename)
#         print(f"\n[bold green]Point-to-point Excel export completed: {filename}[/bold green]")

#     except Exception as e:
#         print(f"[bold red]Point-to-point Excel export failed: {e}[/bold red]")

# def show_p2p_result(network):
#     print("\n[bold green]POINT-TO-POINT RESULT[/bold green]")
#     print(f"Network Address: {network.network}")
#     print(f"CIDR Prefix: /{network.prefixlen}")
#     print(f"Subnet Mask: {network.netmask}")
#     print(f"Wildcard: {network.hostmask}")
#     print(f"Broadcast Address: {network.broadcast}")
#     print(f"Total Addresses: {network.size}")

#     if network.prefixlen == 31:
#         print(f"Usable IP 1: {network[0]}")
#         print(f"Usable IP 2: {network[1]}")
#         print("Usable Hosts: 2")
#     elif network.prefixlen == 30:
#         print(f"First Usable IP: {network[1]}")
#         print(f"Last Usable IP: {network[-2]}")
#         print("Usable Hosts: 2")


# def main():
#     while True:
#         print("\n[bold cyan]IP Network Planner[/bold cyan]")
#         print("1. Host-Based Allocation")
#         print("2. Point-to-Point Calculator")
#         print("3. Exit")

#         choice = input("Enter your choice: ").strip()

#         if choice == "1":
#             base_network = get_host_base_network()
#             show_network_info(base_network)

#             allocations = get_host_allocations()
#             sorted_allocations = sort_allocations_by_hosts(allocations)

#             print("\n[bold magenta]Sorted Allocation Requirements[/bold magenta]")
#             show_allocations(sorted_allocations)
#             show_allocation_prefixes(sorted_allocations)

#             if validate_capacity_before_allocation(base_network, sorted_allocations):
#                 planned_subnets, next_free_ip = allocate_subnets(base_network, sorted_allocations)

#                 if planned_subnets:
#                     show_planned_subnets(planned_subnets)
#                     show_explanations(planned_subnets)
#                     show_summary(base_network, planned_subnets, next_free_ip)
#                     show_remaining_range(base_network, next_free_ip)

#                     include_ip_sheets = get_yes_no_choice(
#                         "Include detailed IP assignment sheets in Excel? (y/n): "
#                     )

#                     export_to_excel(
#                         planned_subnets,
#                         base_network,
#                         next_free_ip,
#                         include_ip_sheets=include_ip_sheets
#                     )

#         elif choice == "2":
#             p2p_network = get_p2p_network()
#             show_p2p_result(p2p_network)

#             if get_yes_no_choice("Export point-to-point result to Excel? (y/n): "):
#                 export_p2p_to_excel(p2p_network)

#         elif choice == "3":
#             print("[bold green]Goodbye![/bold green]")
#             break

#         else:
#             print("[bold red]Invalid choice. Please try again.[/bold red]")

if __name__ == "__main__":
    main()