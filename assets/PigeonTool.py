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

    def ping(self, ip_address):
        ping_response = subprocess.Popen(['ping', '-n', '3', '-w', '350', ip_address],
                                         stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW).communicate()[0]
        if b'Reply from' in ping_response:
            ping_time = str(ping_response).split("Average =")[1].split("ms")[0] + ' ms'
            return ping_time
        else:
            ping_time = 'Request timed out.'
            return ping_time

    def connect(self, ip_address):
        response = subprocess.Popen(['ping', '-n', '1', '-w', '350', str(ip_address)],
                                    stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW).communicate()[0]
        available, not_available = 'Yes', 'No'
        if b'Reply from' in response:
            result = f'{available}'
            return result
        else:
            result = f'{not_available}'
            return result

    def mac_address(self, ip_address):
        message_mac = f'[{self.current_time}]     MAC ({ip_address}):'

        # Create an ARP request packet for the given IP address
        arp_request = ARP(pdst=ip_address)

        # Create an Ethernet frame with the broadcast destination MAC address
        ether = Ether(dst='ff:ff:ff:ff:ff:ff')

        # Combine the ARP request packet and Ethernet frame
        packet = ether / arp_request

        try:
            # Send the packet and receive the response
            result = srp(packet, timeout=3, verbose=0)[0]

            # Extract the MAC address from the response
            mac_address = result[0][1].hwsrc
        except IndexError:
            # Return 'N/A' if an index error occurs
            mac_address = 'N/A'
        return mac_address


    def hostname(self, ip_address):
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except socket.herror as e:
            hostname = 'N/A'
            return hostname
        except Exception as e:
            hostname = 'N/A'
            return hostname
