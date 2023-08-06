import datetime
import configparser

from rssht_controller_lib import config as cconfig

from . import config


def timedelta_repr(td):
    conv_table = [
        (1, 'second'),
        (60, 'minute'),
        (60 * 60, 'hour'),
        (60 * 60 * 24, 'day'),
        (60 * 60 * 24 * 7, 'week'),
        (60 * 60 * 24 * 30, 'month'),
        (60 * 60 * 24 * 365, 'year'),
        (int(datetime.timedelta.max.total_seconds()) + 1, 'inf'),
    ]
    total_seconds = td.total_seconds()
    
    for i in range(1, len(conv_table)):
        seconds = conv_table[i][0]
        prev_seconds, prev_scale = conv_table[i - 1]
        
        if total_seconds < seconds:
            break
    
    magnitude = int(total_seconds / prev_seconds)
    repr_ = f'{magnitude} {prev_scale}'
    
    if magnitude != 1:
        repr_ = f'{repr_}s'
    
    return repr_


def load_config(filename=None):
    filename = config.CONFIG_FILENAME if filename is None else filename
    
    parser = configparser.ConfigParser()
    
    with open(filename) as f:
        parser.read_file(f)
    
    Null = object()
    
    server_address = parser.get('Settings', 'ServerAddress', fallback=Null)
    server_port = parser.get('Settings', 'ServerPort', fallback=Null)
    server_username = parser.get('Settings', 'ServerUsername', fallback=Null)
    key_filename = parser.get('Settings', 'KeyFilename', fallback=Null)
    server_swap_directory = parser.get('Settings', 'ServerSwapDirectory', fallback=Null)
    sleep_interval_secs = parser.get('Settings', 'SleepIntervalSecs', fallback=Null)
    last_seen_alarm_secs = parser.get('Settings', 'LastSeenAlarmSecs', fallback=Null)
    
    if server_port is not Null:
        server_port = int(server_port)
    if sleep_interval_secs is not Null:
        sleep_interval_secs = int(sleep_interval_secs)
    if last_seen_alarm_secs is not Null:
        last_seen_alarm_secs = int(last_seen_alarm_secs)
    
    if server_address is not Null:
        cconfig.RSSHT_SERVER_ADDR = server_address
    if server_port is not Null:
        cconfig.RSSHT_SERVER_PORT = server_port
    if server_username is not Null:
        cconfig.RSSHT_SERVER_USERNAME = server_username
    if key_filename is not Null:
        cconfig.KEY_FILENAME = key_filename
    if server_swap_directory is not Null:
        cconfig.RSSHT_SERVER_SWAP_DIR = server_swap_directory
    if sleep_interval_secs is not Null:
        config.UPDATE_SLEEP_INTERVAL = sleep_interval_secs
    if last_seen_alarm_secs is not Null:
        config.AGENT_LAST_SEEN_ALARM_THRESHOLD = last_seen_alarm_secs


def persist_config(filename=None):
    filename = config.CONFIG_FILENAME if filename is None else filename
    
    parser = configparser.ConfigParser()
    parser['Settings'] = {
        'ServerAddress': cconfig.RSSHT_SERVER_ADDR,
        'ServerPort': str(cconfig.RSSHT_SERVER_PORT),
        'ServerUsername': cconfig.RSSHT_SERVER_USERNAME,
        'KeyFilename': cconfig.KEY_FILENAME,
        'ServerSwapDirectory': cconfig.RSSHT_SERVER_SWAP_DIR,
        'SleepIntervalSecs': str(config.UPDATE_SLEEP_INTERVAL),
        'LastSeenAlarmSecs': str(config.AGENT_LAST_SEEN_ALARM_THRESHOLD),
    }
    
    with open(filename, 'w') as f:
        parser.write(f)
