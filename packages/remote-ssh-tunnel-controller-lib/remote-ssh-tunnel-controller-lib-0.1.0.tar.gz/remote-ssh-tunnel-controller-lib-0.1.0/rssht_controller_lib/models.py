import uuid
import datetime

from . import util


class CMDLine:
    def __init__(self, timestamp, controller_id, uuid_, cmd, *args):
        self._timestamp = timestamp
        self._controller_id = controller_id
        self._uuid = uuid_
        self._cmd = cmd
        self._args = args
        self._status = None
    
    def get_timestamp(self):
        return self._timestamp
    
    def get_controller_id(self):
        return self._controller_id
    
    def get_uuid(self):
        return self._uuid
    
    def get_cmd(self):
        return self._cmd
    
    def get_args(self):
        return self._args
    
    def get_status(self):
        return self._status
    
    def set_status(self, status):
        self._status = status
    
    def __eq__(self, cmdline2):
        return isinstance(cmdline2, self.__class__) and \
                self._uuid is not None and \
                self._uuid == cmdline2.get_uuid()
    
    def __str__(self):
        timestamp = int(self._timestamp.timestamp())
        controller_id = self._controller_id
        uuid_ = str(self._uuid)
        cmd = self._cmd
        args = ' '.join(map(str, self._args))
        
        return f'{timestamp} {controller_id} {uuid_} {cmd} {args}'
    
    @classmethod
    def from_str(cls, str_):
        list_ = str_.split()
        timestamp = datetime.datetime.fromtimestamp(int(list_[0]), 
                                                    datetime.timezone.utc)
        controller_id = list_[1]
        uuid_ = uuid.UUID(list_[2])
        cmd = list_[3]
        args = tuple(list_[4:])
        
        self = cls(timestamp, controller_id, uuid_, cmd, *args)
        return self


class RSSHTObject:
    def __init__(self, da):
        self._da = da
        self._disposed = False
    
    def get_da(self):
        return self._da
    
    def is_disposed(self):
        return self._disposed
    
    def dispose(self):
        """Should be called before destruction."""
        self._dispose()
        self._disposed = True
    
    def _dispose(self):
        """Called by self.dispose().
        
        Its functions (when applicable) are:
            1) RSSHTObject's parent = None
            2) child.dispose() for child in RSSHTObject's children
        """
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError


class RSSHTAgentStatus(RSSHTObject):
    def __init__(self, da, agent):
        super().__init__(da)
        self._agent = agent
        self._timestamp = None
        self._cmdline = None
    
    def get_agent(self):
        return self._agent
    
    def get_timestamp(self):
        return self._timestamp
    
    def get_cmdline(self):
        return self._cmdline
    
    def _dispose(self):
        self._agent = None
    
    @util.retry_on_exception([IndexError], max_retries=5)
    def update(self):
        status_list = self._da.fetch_agent_status(self._agent.get_id()).split()
        
        self._timestamp = datetime.datetime.fromtimestamp(int(status_list[0]), 
                                                        datetime.timezone.utc)
        if len(status_list) == 1:
            self._cmdline = None
            return
        
        cmdline = CMDLine.from_str(' '.join(status_list[2:]))
        cmdline.set_status(int(status_list[1]))
        
        if self._cmdline and self._cmdline == cmdline:
            self._cmdline.set_status(cmdline.get_status())
        else:
            self._cmdline = cmdline


class RSSHTAgent(RSSHTObject):
    def __init__(self, id_, da, controller):
        super().__init__(da)
        self._controller = controller
        self._id = id_
        self._status = None
        self._cmdline_history = []
    
    def get_controller(self):
        return self._controller
    
    def get_id(self):
        return self._id
    
    def get_status(self):
        return self._status
    
    def get_cmdline_history(self):
        return tuple(self._cmdline_history)
    
    def push_cmdline(self, cmdline):
        self._da.push_cmdline(self._id, str(cmdline))
        self._cmdline_history.append(cmdline)
    
    def push_rssht_cmdline(self, bind_port, dest_port):
        from .factories import RSSHTCMDLineFactory  # to avoid recursion
        
        self.push_cmdline(RSSHTCMDLineFactory.new_now(self._controller.get_id(), 
                                                        bind_port, dest_port))
    
    def push_term_rssht_cmdline(self):
        from .factories import TermRSSHTCMDLineFactory  # to avoid recursion
        
        self.push_cmdline(TermRSSHTCMDLineFactory.new_now(
                                                    self._controller.get_id()))
    
    def __repr__(self):
        return f'<{self.__class__.__name__}: {self._id}>'
    
    def _dispose(self):
        self._controller = None
        self._status.dispose()
    
    def update(self):
        if self._status is None:
            self._status = RSSHTAgentStatus(self._da, self)
        self._status.update()


class RSSHTController(RSSHTObject):
    def __init__(self, id_, da):
        super().__init__(da)
        self._id = id_
        self._agents = []
    
    def get_id(self):
        return self._id
    
    def get_agents(self):
        return tuple(self._agents)
    
    def _dispose(self):
        for agent in self._agents:
            agent.dispose()
    
    def update(self):
        cur_agent_ids = self._da.fetch_agent_ids()
        i = 0
        
        while i < len(self._agents):
            agent = self._agents[i]
            
            if agent.get_id() not in cur_agent_ids:
                agent.dispose()
                del self._agents[i]
            else:
                i += 1
        
        agent_ids = [agent.get_id() for agent in self._agents]
        
        for cur_agent_id in cur_agent_ids:
            if cur_agent_id not in agent_ids:
                agent = RSSHTAgent(cur_agent_id, self._da, self)
                self._agents.append(agent)
        
        for agent in self._agents:
            agent.update()
