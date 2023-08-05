from . import config


class DataAccess:
    def __init__(self, sshc=None):
        self._sshc = sshc
    
    def get_sshc(self):
        return self._sshc
    
    def set_sshc(self, sshc):
        self._sshc = sshc
    
    def fetch_agent_ids(self):
        swap_dir = config.RSSHT_SERVER_SWAP_DIR
        
        stdin, stdout, stderr = self._sshc.exec_command(
            f'find "{swap_dir}" -maxdepth 1 -type f -name "*.out" -printf "%f\\n"'
            f' | grep -Po ".*(?=.out$)"'
        )
        return stdout.read().decode('utf-8').splitlines()
    
    def fetch_agent_status(self, agent_id):
        stdin, stdout, stderr = self._sshc.exec_command(
            f'cat "{config.RSSHT_SERVER_SWAP_DIR}/{agent_id}.out"'
        )
        return stdout.read().decode('utf-8').strip()
    
    def push_cmdline(self, agent_id, cmdline_str):
        stdin, stdout, stderr = self._sshc.exec_command(
            f'tee "{config.RSSHT_SERVER_SWAP_DIR}/{agent_id}.in" > /dev/null'
        )
        stdin.write(cmdline_str.encode('utf-8'))
        stdin.close()
        stdout.read()  # wait for command to finish?
