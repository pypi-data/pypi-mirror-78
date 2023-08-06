import os


# Absolute path
_APP_HOME = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

CONFIG_FILENAME = os.path.expanduser('~/remote-ssh-tunnel-controller-qt.ini')

# In seconds
UPDATE_SLEEP_INTERVAL = 5

# In seconds
AGENT_LAST_SEEN_ALARM_THRESHOLD = 25
