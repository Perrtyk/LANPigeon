
class Endpoint:

    def __init__(self, ip, alive,  hostname, ping, mac):
        self.__ip = ip
        self.__alive = alive
        self.__hostname = hostname
        self.__ping = ping
        self.__mac = mac

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, alive):
        self.__alive = alive

    @property
    def hostname(self):
        return self.__hostname

    @hostname.setter
    def hostname(self, hostname):
        self.__hostname = hostname

    @property
    def ping(self):
        return self.__ping

    @ping.setter
    def ping(self, ping):
        self.__ping = ping

    @property
    def mac(self):
        return self.__mac

    @mac.setter
    def mac(self, mac):
        self.__mac = mac

    def to_dict(self):
        if self.__alive == 'Yes':
            return {
                "ip_address": self.__ip,
                "alive_status": self.__alive,
                "ping_status": self.__hostname,
                "hostname_status": self.__ping,
                "mac_address": self.__mac
            }
        else:
            return {
                "ip_address": self.__ip,
                "alive_status": 'No',
                "ping_status": 'N/A',
                "hostname_status": 'N/A',
                "mac_address": 'N/A'}

    def __getitem__(self, key):
        if key == 'ip_address':
            return self.ip
        elif key == 'ping_status':
            return self.ping
        elif key == 'hostname_status':
            return self.hostname
        elif key == 'mac_address':
            return self.mac
        elif key == 'alive_status':
            return self.alive
        else:
            raise KeyError(f"'{key}' is not a valid key for Endpoint")

    def __str__(self):
        return f"ip_address: {self.__ip}\n" + f"alive_status: {self.__alive}\n" +\
               f"ping_status: {self.__ping}\n" + f"hostname_status: {self.__hostname}\n" +\
               f"mac_address: {self.__mac}\n"