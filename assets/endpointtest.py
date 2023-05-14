from endpoint import *
from endpoint_list import *

def test_constructor():
    print("Expect: " + "192.168.0.1, Yes, example.com, 10ms, 00:11:22:33:44:55")
    endpoint1 = Endpoint("192.168.0.1", 'Yes', "example.com", '10ms', "00:11:22:33:44:55")
    print(endpoint1)
    print()


def test_setter_getter():
    print('Testing Setter Getter')
    endpoint1 = Endpoint("192.168.0.1", 'Yes', "example.com", '10ms', "00:11:22:33:44:55")
    print("ip_address: " + endpoint1.ip)  # Get the IP address
    endpoint1.alive = 'No'  # Update the alive status
    print("alive_status: " + endpoint1.alive)
    endpoint1.hostname = "newhostname"  # Update the hostname
    print("hostname_status: " + endpoint1.hostname)
    endpoint1.ping = '20ms'  # Update the ping status
    print("ping_status: " + endpoint1.ping)
    endpoint1.mac = "AA:BB:CC:DD:EE:FF"  # Update the MAC address
    print("mac_address: " + endpoint1.mac)

def test_array():
    # Example usage
    print('testing array')
    endpoint1 = Endpoint("192.168.0.1", 'Yes', "host1", '5ms', "00:11:22:33:44:55")
    endpoint2 = Endpoint("192.168.0.2", 'No', "N/A", 'N/A', "N/A")
    endpoint3 = Endpoint("192.168.0.3", 'Yes', "host3", '4ms', "FF:GG:HH:II:JJ:KK")
    endpoints = [endpoint1, endpoint2, endpoint3]  # List of Endpoint objects
    array = EndpointArray(endpoints)
    print(array)

def test_endpoint():
    test_constructor()
    print()
    test_setter_getter()
    print()
    test_array()




test_endpoint()