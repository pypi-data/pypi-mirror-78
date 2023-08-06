"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA device detection library*

:details: SiLA Device detection is based on zeroconf / bonjour.
          s. zeroconf documentation for details.
          server looks for services in local network
          server chooses a free port
          server receives a logical name
          client can use this logicial name to address server

:file:    sila_device_detection.py
:authors: mark doerr (mark@uni-greifswald.de)
          Timm Severin
          Lukas Broming
              
:date: (creation)          20180530
:date: (last modification) 2019-11-09

.. note:: -
.. todo:: - check available ports and select first free port available
________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.0.6"

import socket
from zeroconf import ServiceInfo, Zeroconf

import logging

class SiLA2ServiceDetection():
    """ This class Registers the SiLA2 service in the given network"""
    def __init__ (self):
        """ Registering the SiLA2 service in the given network with zeroconfig"""

        self.service_tag = "_sila._tcp.local." # specified in SiLA standard, Part B
        self.zc: Zeroconf = Zeroconf()

    def register_service(self,
                        service_name="SiLATestDevice",
                        IP: str = "127.0.0.1",
                        port: int = None,
                        description: dict = {'version': __version__, 'descr1': 'zeroconf def. description 1', 'descr2': 'zeroconf def. description 2'},
                        server_uuid: str = None,
                        server_hostname: str = None) -> None:
        """ :param [param_name]: [description]"""
        """[summary]
        _param IP: [description], defaults to "127.0.0.1"
        :type IP: str, optional
        :param port: [description], defaults to None
        :type port: int, optional
        :param description: [description], defaults to {'version': __version__, 'descr1': 'zeroconf def. description 1', 'descr2': 'zeroconf def. description 2'}
        :type description: dict, optional
        :param server_uuid: [description], defaults to None
        :type server_uuid: str, optional
        :param server_hostname: [description], defaults to None
        :type server_hostname: str, optional
        :raises err: [description]
        :raises err: [description]
        :return: [description]
        :rtype: [type]
        """

        if server_hostname is None:
            server_hostname = socket.getfqdn()


        # This code only checks wheter a port is open or closed.
        # Todo: Implement code that checkks if the used open port is used otherwise to avoid
        # multiple use of ports.

        if port is not None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.bind(('', port))  ## Try to open port
            except OSError as err:
                if err.errno is 98:  ## Errorno 98 means address already bound
                    logging.error(f"Specified port {port} is already occupied - ({err})")
                    port = None
                else:
                    raise err
            s.close()

        if port is None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = 55001  # range(55001, ....)
            while True:
                try:
                    s.bind(('', port))  ## Try to open port
                except OSError as err:
                    if err.errno is 98:  ## Errorno 98 means address already bound
                        port += 1
                        continue
                    raise err
                s.close()
                logging.info(
                    f"No port specified or specified port is occupied. Registering Service on next free port: {port}")
                break

        # logging.debug("UUID: {}".format(server_uuid)) Deleted? Why? Not necessary I guess...
        self.service_info = ServiceInfo(type_=self.service_tag,
                                    name=f"{server_uuid}.{self.service_tag}",
                                    addresses=[socket.inet_aton(IP)], port=port, weight=0, priority=0,
                                    properties=description, server=f"{server_hostname}.local.") # do we need to add .local ? # Yes .local is necessary, LB

        logging.info(
            f"registering the SiLA2 service '{server_uuid}.{self.service_tag}' in the network at {IP} with port {port} as hostname '{server_hostname}''")

        try:
            self.zc.register_service(self.service_info)
        except Exception as err:  # should be more specific
            logging.error(f"{err}")
            raise

        logging.info("Zeroconf registration done ...")

    def unregister_service(self):
        logging.info(f"unregistering the SiLA2 service {self.service_info.name} in the network {self.service_info.server}")
        try:
            self.zc.unregister_service(self.service_info)
        except Exception as err:  # should be more specific
            logging.error(f"{err}")
            raise
        logging.info("Zeroconf service removed ...")

    def find_service_by_name(self, service_name=""):
        """ this method tries to find a given service by name and returns the connection parameters
        :param service_name [string]: service name to search for"""

        logging.info("not implemented yet ... just sending default values..")

        return { 'server_name':'localhost', 'port':50001  }

    def watch_for_new_services(self):
        """ new service watcher
        if server is removed from server list, send a gRPC ping (s. unitelabs implementation)
        this should be called every second
        :param [param_name]: [description]"""
        pass
