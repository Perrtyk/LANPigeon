class Endpoint:

    def __init__(self, ip, alive,  hostname, ping, mac):
        self._ip = ip
        self._alive = alive
        self._hostname = hostname
        self._ping = ping
        self._mac = mac

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        self._ip = ip

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, alive):
        self._alive = alive

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        self._hostname = hostname

    @property
    def ping(self):
        return self._ping

    @ping.setter
    def ping(self, ping):
        self._ping = ping

    @property
    def mac(self):
        return self._mac

    @mac.setter
    def mac(self, mac):
        self._mac = mac

    def to_dict(self):
        if self._alive == 'Yes':
            return {
                "ip_address": self._ip,
                "alive_status": self._alive,
                "ping_status": self._hostname,
                "hostname_status": self._ping,
                "mac_address": self._mac
            }
        else:
            return {
                "ip_address": self._ip,
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
        return f"ip_address: {self._ip}\n" + f"alive_status: {self._alive}\n" +\
               f"ping_status: {self._ping}\n" + f"hostname_status: {self._hostname}\n" +\
               f"mac_address: {self._mac}\n"