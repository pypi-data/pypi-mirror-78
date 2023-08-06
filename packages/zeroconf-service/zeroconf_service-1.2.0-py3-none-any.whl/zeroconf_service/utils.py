### System ###
import time
import atexit
import socket
import pickle
from collections import namedtuple, defaultdict

### zeroconf ###
from zeroconf import IPVersion, ServiceBrowser, Zeroconf, ServiceListener, ServiceInfo


SERVICES = defaultdict(list)
CAPABILITIES = defaultdict(list)
OWN_SERVICES = defaultdict(list)

Info = namedtuple("info", ("properties", "addresses", "service_info"))


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def better_listener_args(func):
    def listener_method_proxy(self, zc, type_, name):
        service_info = zc.get_service_info(type_, name)
        if service_info:
            try:
                properties = pickle.loads(service_info.text)
            except:
                properties = {}
            addresses = [(socket.inet_ntoa(addr), service_info.port) for addr in service_info.addresses]
            info = Info(properties, addresses, service_info)
        else:
            info = Info(None, None, None)
        name = name.rstrip(type_)
        func(self, zc, info, type_, name)
    return listener_method_proxy


class CustomListener(ServiceListener):

    @better_listener_args
    def add_service(self, zc, info, type_, name):
        if info.properties.get("application", None) == "TSM":
            SERVICES[name].append(info)
            capabilities = info.properties.get("capabilities", [])
            for cap in capabilities:
                CAPABILITIES[cap].append(info)

    @better_listener_args
    def remove_service(self, zc, info, type_, name):
        if name in SERVICES:
            SERVICES[name].remove(info)
            capabilities = info.properties.get("capabilities", [])
            for cap in capabilities:
                CAPABILITIES[cap].remove(info)

    @better_listener_args
    def update_service(self, zc, info, type_, name):
        if info.properties.get("application", None) == "TSM":
            SERVICES[name].remove(info)
            SERVICES[name].append(info)
            capabilities = info.properties.get("capabilities", [])
            for cap in capabilities:
                CAPABILITIES[cap].remove(info)
                CAPABILITIES[cap].append(info)


def get_service_by_name(name, block=True):
    while True:
        result = SERVICES.get(name, None)
        if not block or result:
            return list(sorted(result, key=lambda x: x.service_info.priority)) if result else None
        time.sleep(0.5)


def get_service_by_capability(capabilities, block=True):
    # TODO: Implement properly
    # Behavior:
    # Search each service against the desired capabilities
    # We may return more than one service if capabilities are only available split across them
    # For each desired capability, we create a list of services who have that capability
    # Within each list, we sort them by the closeness of the match to the desired capabilities
    # For example, if we desire [gps, imud] and we have two services:
    # S1: [gps]
    # S2: [gps, imud]
    # Then S2 would rank before S1
    # Return Value:
    # {cap: [services] for cap in capabilities}
    # TODO: Should block until all capabilities can be filled

    capabilities = set(capabilities)
    filled_capabilities = set()
    selected_services = {}

    while True:
        if filled_capabilities == capabilities:
            return selected_services
        for cap in capabilities - filled_capabilities:
            result = CAPABILITIES.get(cap)
            if result:
                selected_services[cap] = sorted(result, key=lambda x: x[1], reverse=True)[0]
                filled_capabilities.add(cap)
        if not block:
            return selected_services
        time.sleep(0.5)


def advertise_service(name, application, capabilities, port, address=None, type_="_http._tcp.local.", block=True):
    info = ServiceInfo(f"{type_}", f"{name}.{type_}",
                       addresses=[socket.inet_aton(address if address else get_ip_address())], port=port,
                       properties=pickle.dumps({"application": application, "capabilities": capabilities}, protocol=4))
    OWN_SERVICES[name].append(info)
    ZC.register_service(info)

    while block:
        time.sleep(1.0)


def unadvertise_service(name):
    for service in OWN_SERVICES[name]:
        ZC.unregister_service(service)


def cleanup():
    ZC.close()


atexit.register(cleanup)

ZC = Zeroconf(ip_version=IPVersion.V4Only)

BROWSER = ServiceBrowser(ZC, ["_http._tcp.local."], listener=CustomListener())
