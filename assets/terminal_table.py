from prettytable import PrettyTable

def get_data(endpoints, endpoint):
    index = endpoint - 1
    entries = endpoints
    entry_data = entries[index]
    return f"Endpoint {index}: {entry_data}"

def create_table(data):
    table = PrettyTable()
    table.field_names = ["IP Address", "Alive Status", "Ping Status", "Hostname Status", "MAC Address"]
    for endpoint in data:
        if endpoint["alive_status"] != "No":
            table.add_row(
                [endpoint["ip_address"], endpoint['alive_status'], endpoint["ping_status"], endpoint["hostname_status"],
                 endpoint["mac_address"]])

    return table