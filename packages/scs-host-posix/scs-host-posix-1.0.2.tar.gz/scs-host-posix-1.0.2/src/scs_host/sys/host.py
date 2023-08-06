"""
Created on 20 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://stackoverflow.com/questions/4271740/how-can-i-use-python-to-get-the-system-hostname
http://code.activestate.com/recipes/577972-disk-usage/
"""

import os
import socket

from pathlib import Path

from scs_core.sys.disk_usage import DiskUsage
from scs_core.sys.ipv4_address import IPv4Address
from scs_core.sys.node import Node


# --------------------------------------------------------------------------------------------------------------------

class Host(Node):
    """
    Any Darwin Mac or Linux
    """

    # ----------------------------------------------------------------------------------------------------------------
    # directories and files...

    OS_ENV_PATH =           'SCS_ROOT_PATH'

    __SCS_DIR =             "SCS"                               # hard-coded rel path

    __CONF_DIR =            "conf"                              # hard-coded rel path
    __AWS_DIR =             "aws"                               # hard-coded rel path
    __OSIO_DIR =            "osio"                              # hard-coded rel path

    __LATEST_UPDATE =       "latest_update.txt"                 # hard-coded rel path


    # ----------------------------------------------------------------------------------------------------------------
    # host acting as DHCP server...

    __SERVER_IPV4_ADDRESS =      None                           # had-coded abs path


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def software_update_report(cls):
        try:
            f = open(os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__LATEST_UPDATE))
            report = f.read().strip()
            f.close()

            return report

        except FileNotFoundError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        full_name = socket.gethostname()
        full_names = full_name.split('.')

        return full_names[0]


    @classmethod
    def server_ipv4_address(cls):
        return IPv4Address.construct(cls.__SERVER_IPV4_ADDRESS)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def ndir_spi_bus(cls):
        raise NotImplementedError


    @classmethod
    def ndir_spi_device(cls):
        raise NotImplementedError


    @classmethod
    def opc_spi_bus(cls):
        raise NotImplementedError


    @classmethod
    def opc_spi_device(cls):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def disk_usage(cls, volume):
        st = os.statvfs(volume)

        free = st.f_bavail * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        total = st.f_blocks * st.f_frsize

        return DiskUsage(volume, free, used, total)


    # ----------------------------------------------------------------------------------------------------------------

    def time_is_synchronized(self):
        raise NotImplementedError()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def home_dir(cls):
        return os.environ[cls.OS_ENV_PATH] if cls.OS_ENV_PATH in os.environ else str(Path.home())


    @classmethod
    def lock_dir(cls):
        raise NotImplementedError


    @classmethod
    def tmp_dir(cls):
        raise NotImplementedError


    @classmethod
    def command_dir(cls):
        raise NotImplementedError


    @classmethod
    def scs_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR)


    @classmethod
    def conf_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__CONF_DIR)


    @classmethod
    def aws_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__AWS_DIR)


    @classmethod
    def osio_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__OSIO_DIR)


    @classmethod
    def eep_image(cls):
        raise NotImplementedError
