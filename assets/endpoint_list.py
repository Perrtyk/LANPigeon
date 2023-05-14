from endpoint import Endpoint

class EndpointArray:
    def __init__(self, array):
        self.__endpoints = []
        for endpoint in array:
            self.__endpoints.append(endpoint)


    @property
    def count(self):
        return len(self.__endpoints)

    def add_endpoint(self, endpoint):
        self.__endpoints.append(endpoint)

    def remove_endpoint(self, endpoint):
        self.__endpoints.remove(endpoint)

    def get_endpoints(self):
        return self.__endpoints

    def get_alive_endpoints(self):
        return [endpoint for endpoint in self.__endpoints if endpoint.alive]

    def get_ping_status(self):
        return [endpoint.ping for endpoint in self.__endpoints]

    def get_hostnames(self):
        return [endpoint.hostname for endpoint in self.__endpoints]

    def get_mac_addresses(self):
        return [endpoint.mac for endpoint in self.__endpoints]

    def __getitem__(self, index):
        return self.__endpoints[index]

    def __len__(self):
        """Allows a programmer to use the len function to get the length of a customer list"""
        return len(self.__endpoints)

    def __iter__(self):
        return iter(self.__endpoints)

    def __str__(self):
        return "\n".join(str(endpoint) for endpoint in self.__endpoints)

