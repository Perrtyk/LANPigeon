'''
- move stopscan to main function of the program


'''

import socket
import subprocess
from datetime import datetime
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp

class PigeonTool:
    def __init__(self):
        self.current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def print_debug(self, message):
        print(message)

    def ping(self, ip_address):
        ping_response = subprocess.Popen(['ping', '-n', '3', '-w', '350', ip_address],
                                         stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW).communicate()[0]
        if b'Reply from' in ping_response:
            ping_time = str(ping_response).split("Average =")[1].split("ms")[0] + ' ms'
            self.print_debug(f'[{self.current_time}] IP Scan ({ip_address}): Received ping response of{ping_time}.\n')
            return ping_time
        else:
            ping_time = 'Request timed out.'
            return ping_time

    def connect(self, ip_address):
        message_connect = f'[{self.current_time}] Connect ({ip_address}):'
        self.print_debug(f'{message_connect} Running connection test . . .\n')
        response = subprocess.Popen(['ping', '-n', '1', '-w', '250', str(ip_address)],
                                    stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW).communicate()[0]
        available, not_available = 'Yes', 'No'
        if b'Reply from' in response:
            result = f'{available}'
            self.print_debug(f'{message_connect} Complete, endpoint available: {result}.\n')
            return result
        else:
            result = f'{not_available}'
            self.print_debug(f'{message_connect} Complete, endpoint available: {result}.\n')
            return result

    def mac_address(self, ip_address):

        self.print_debug(f'[{self.current_time}] IP Scan ({ip_address}): Running MAC address process . . .\n')
        message_mac = f'[{self.current_time}]     MAC ({ip_address}):'

        # Create an ARP request packet for the given IP address
        self.print_debug(f'{message_mac} Attempting to gather MAC address via ARP . . .\n')
        arp_request = ARP(pdst=ip_address)

        # Create an Ethernet frame with the broadcast destination MAC address
        ether = Ether(dst='ff:ff:ff:ff:ff:ff')

        # Combine the ARP request packet and Ethernet frame
        packet = ether / arp_request

        try:
            # Send the packet and receive the response
            self.print_debug(f'{message_mac} Sending out packet and awaiting response . . .\n')
            result = srp(packet, timeout=3, verbose=0)[0]

            # Extract the MAC address from the response
            mac_address = result[0][1].hwsrc
            self.print_debug(f'{message_mac} Extracting MAC from response . . .\n')
        except IndexError:
            # Return 'N/A' if an index error occurs
            self.print_debug(f'{message_mac} Index error, return N/A . . .\n')
            mac_address = 'N/A'
        self.print_debug(f'{message_mac} Returned MAC address . . .\n')
        return mac_address


    def hostname(self, ip_address):
        self.print_debug(f'[{self.current_time}] IP Scan ({ip_address}): Gathering hostname . . .\n')
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            self.print_debug(f'[{self.current_time}] IP Scan ({ip_address}): Hostname is {hostname}\n')
            return hostname
        except socket.herror as e:
            self.print_debug(f'[{self.current_time}] IP Scan ({ip_address}): Error resolving hostname: {e}\n')
            hostname = 'N/A'
            return hostname
        except Exception as e:
            self.print_debug(f'[{self.current_time}] IP Scan ({ip_address}): Error: {e}\n')
            hostname = 'N/A'
            return hostname
