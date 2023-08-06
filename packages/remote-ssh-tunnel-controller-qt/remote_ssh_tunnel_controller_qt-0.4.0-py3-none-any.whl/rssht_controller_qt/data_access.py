import paramiko

from rssht_controller_lib import factories
from rssht_controller_lib import data_access


class ResetSSHCAndRetryOnException:
    def __init__(self, exceptions, sshc_factory=None):
        assert tuple(exceptions)
        
        self._exceptions = exceptions
        self._sshc_factory = sshc_factory or self.default_sshc_factory
    
    def default_sshc_factory(self, cur_sshc):
        new_sshc = factories.SSHClientFactory.new_connected()
        return new_sshc
    
    def __call__(self, func):
        def decorator(self2, *args, **kwargs):
            try:
                return func(self2, *args, **kwargs)
            except tuple(self._exceptions) as exception:
                cur_sshc = self2.get_sshc()
                new_sshc = self._sshc_factory(cur_sshc)
                self2.set_sshc(new_sshc)
                return func(self2, *args, **kwargs)
        return decorator


class RetryDataAccess(data_access.DataAccess):
    @ResetSSHCAndRetryOnException([ConnectionResetError, TimeoutError, paramiko.SSHException])
    def fetch_agent_ids(self, *args, **kwargs):
        return super().fetch_agent_ids(*args, **kwargs)
    
    @ResetSSHCAndRetryOnException([ConnectionResetError, TimeoutError, paramiko.SSHException])
    def fetch_agent_status(self, *args, **kwargs):
        return super().fetch_agent_status(*args, **kwargs)
    
    @ResetSSHCAndRetryOnException([ConnectionResetError, TimeoutError, paramiko.SSHException])
    def push_cmdline(self, *args, **kwargs):
        return super().push_cmdline(*args, **kwargs)
