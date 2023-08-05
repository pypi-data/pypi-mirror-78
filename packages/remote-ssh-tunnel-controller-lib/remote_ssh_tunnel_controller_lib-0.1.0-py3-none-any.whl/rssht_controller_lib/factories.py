import re
import uuid
import time
import datetime

import paramiko

from . import config
from . import models
from . import data_access


class CMDLineFactory:
    @classmethod
    def new_now(cls, controller_id, cmd, *args):
        timestamp = datetime.datetime.fromtimestamp(int(time.time()), 
                                                    datetime.timezone.utc)
        uuid_ = uuid.uuid4()
        
        cmdline = models.CMDLine(timestamp, controller_id, uuid_, cmd, *args)
        return cmdline


class RSSHTCMDLineFactory(CMDLineFactory):
    @classmethod
    def new(cls, timestamp, controller_id, uuid_, bind_port, dest_port):
        return models.CMDLine(timestamp, controller_id, uuid_, 
                                config.RSSHT_CMD, bind_port, dest_port)
    
    @classmethod
    def new_now(cls, controller_id, bind_port, dest_port):
        return super().new_now(controller_id, 
                                config.RSSHT_CMD, bind_port, dest_port)


class TermRSSHTCMDLineFactory(CMDLineFactory):
    @classmethod
    def new(cls, timestamp, controller_id, uuid_):
        return models.CMDLine(timestamp, controller_id, uuid_, 
                                config.TERM_RSSHT_CMD)
    
    @classmethod
    def new_now(cls, controller_id):
        return super().new_now(controller_id, config.TERM_RSSHT_CMD)


class SSHClientFactory:
    @classmethod
    def new_connected(cls, addr=None, port=None, username=None, key_filename=None):
        addr = config.RSSHT_SERVER_ADDR if addr is None else addr
        port = config.RSSHT_SERVER_PORT if port is None else port
        username = config.RSSHT_SERVER_USERNAME if username is None else username
        key_filename = config.KEY_FILENAME if key_filename is None else key_filename
        
        sshc = paramiko.SSHClient()
        sshc.load_system_host_keys()
        sshc.set_missing_host_key_policy(paramiko.WarningPolicy)
        sshc.connect(addr, port=port, username=username, 
                    key_filename=key_filename)
        return sshc


class DataAccessFactory:
    @classmethod
    def new_with_connected_sshc(cls, addr=None, port=None, username=None, key_filename=None):
        addr = config.RSSHT_SERVER_ADDR if addr is None else addr
        port = config.RSSHT_SERVER_PORT if port is None else port
        username = config.RSSHT_SERVER_USERNAME if username is None else username
        key_filename = config.KEY_FILENAME if key_filename is None else key_filename
        
        return data_access.DataAccess(SSHClientFactory.new_connected(addr, port, 
                                                        username, key_filename))


class RSSHTControllerFactory:
    @classmethod
    def new(cls, id_=None, da=None):
        if id_ is None:
            pub_key = open(f'{config.KEY_FILENAME}.pub').readline()
            id_ = re.search(r'^\S+ \S+ (.+)$', pub_key).group(1)
        
        if da is None:
            da = DataAccessFactory.new_with_connected_sshc()
        
        return models.RSSHTController(id_, da)
