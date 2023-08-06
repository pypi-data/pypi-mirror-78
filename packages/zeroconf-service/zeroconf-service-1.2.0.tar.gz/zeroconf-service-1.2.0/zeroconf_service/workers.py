### System ###
import socket
import pickle
import asyncio
import threading
import traceback
from abc import abstractmethod, ABC

### Logging ###
from logzero import logger

### Data Handling ###
import websockets
from compress_pickle import dumps

### zeroconf ###
from zeroconf import Zeroconf, ServiceInfo, IPVersion


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


class PullWorker(threading.Thread, ABC):

    def __init__(self):
        super(PullWorker, self).__init__()
        self.data = {}
        self.last_data = {}
        self.stop_flag = False
        self.name = type(self).__name__

    def run(self):
        logger.info(f"Starting {self.name}")

        try:
            self.execute()
        except Exception as e:
            logger.error(f"Encountered exception in {self.name}: {e}")
            traceback.print_exc()

        logger.info(f"Stopped {self.name}")

    @abstractmethod
    def execute(self):
        pass

    def get(self, ignore_cache=False):
        if ignore_cache and self.data is not None:
            return self.data
        elif self.data is not None and self.last_data is not self.data:
            self.last_data = self.data
            return self.data
        return None


class PushWorker(threading.Thread, ABC):

    SERVICE_NAME = None
    SERVICE_PORT = None
    SERVICE_APPLICATION = None
    SERVICE_CAPABILITIES = []

    def __init__(self, loop):
        super(PushWorker, self).__init__()
        self.loop = loop
        self.data = {}
        self.last_data = {}
        self.stop_flag = False
        self.name = type(self).__name__
        self.service_info = None
        if self.SERVICE_NAME and self.SERVICE_PORT and self.SERVICE_APPLICATION and self.SERVICE_CAPABILITIES:
            self.zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
            self.service_info = ServiceInfo(
                "_http._tcp.local.",
                f"{self.SERVICE_NAME}._http._tcp.local.",
                addresses=[socket.inet_aton(get_ip_address())],
                port=self.SERVICE_PORT,
                properties=pickle.dumps({
                    "application": self.SERVICE_APPLICATION,
                    "capabilities": self.SERVICE_CAPABILITIES
                }, protocol=4))

    def run(self):
        logger.info(f"Starting {self.name}")

        if self.service_info:
            logger.info(f"Registering service {self.SERVICE_NAME}")
            self.zeroconf.register_service(self.service_info)

        try:
            self.execute()
        except Exception as e:
            logger.error(f"Encountered exception in {self.name}: {e}")
            traceback.print_exc()
        finally:
            if self.service_info:
                logger.info(f"Unregistering service {self.SERVICE_NAME}")
                self.zeroconf.unregister_service(self.service_info)
                self.zeroconf.close()

        logger.info(f"Stopped {self.name}")

    @abstractmethod
    def execute(self):
        pass

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        try:
            await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected.remove(websocket)

    def send_data(self, data):
        dts = dumps(data, compression="lz4", protocol=4)
        for websocket in self.connected.copy():
            coro = websocket.send(dts)
            _ = asyncio.run_coroutine_threadsafe(coro, self.loop)
