from ctypes.util import find_library
from ctypes import *
import json
import sys
import os
import platform
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.config_loader import get_tdjson_path

def find_tdjson():
    config_path = get_tdjson_path()
    if config_path:
        print(f"Using TDLib path from config: {config_path}")
        return config_path

    system = platform.system().lower()
    machine = platform.machine().lower()
    
    lib_extensions = {
        'windows': '.dll',
        'darwin': '.dylib',
        'linux': '.so'
    }
    lib_extension = lib_extensions.get(system, '.so')
    
    arch_map = {
        'x86_64': 'x86_64',
        'amd64': 'x86_64',
        'i386': 'x86',
        'i686': 'x86',
        'arm64': 'arm64',
        'aarch64': 'arm64',
        'armv7l': 'arm',
        'armv6l': 'arm'
    }
    architecture = arch_map.get(machine, machine)
    
    project_root = Path(__file__).parent.parent.parent
    possible_paths = []
    
    tdlib_paths = [
        project_root / 'tdlib',
        project_root / 'td' / 'lib',
        project_root / 'libtdjson',
        project_root / 'libs' / 'tdlib',
        project_root / 'vendor' / 'tdlib',
        project_root / 'src' / 'api' / 'telegram' / 'tdlib',
    ]
    
    for base_path in tdlib_paths:
        if not base_path.exists():
            continue
            
        if system == 'windows':
            possible_paths.extend([
                base_path / f'tdjson{lib_extension}',
                base_path / 'bin' / f'tdjson{lib_extension}',
                base_path / architecture / f'tdjson{lib_extension}',
                base_path / 'bin' / architecture / f'tdjson{lib_extension}',
            ])
        
        else:
            possible_paths.extend([
                base_path / f'libtdjson{lib_extension}',
                base_path / f'libtdjson{lib_extension}.1',
                base_path / f'libtdjson{lib_extension}.1.8.0',
                base_path / 'build' / f'libtdjson{lib_extension}',
                base_path / 'build' / architecture / f'libtdjson{lib_extension}',
            ])
    
    system_paths = [
        f'/usr/local/build/libtdjson{lib_extension}',
        f'/usr/build/libtdjson{lib_extension}',
        f'/usr/build/{architecture}-linux-gnu/libtdjson{lib_extension}',
        f'/opt/td/build/libtdjson{lib_extension}',
        os.path.expanduser(f'~/td/build/libtdjson{lib_extension}'),
    ]
    
    possible_paths.extend([Path(p) for p in system_paths])
    
    for path in possible_paths:
        if path.exists():
            print(f"Found TDLib at: {path}")
            return str(path)
    
    lib_name = "tdjson" if system == "windows" else "tdjson"
    lib_path = find_library(lib_name)
    if lib_path:
        print(f"Found TDLib via system: {lib_path}")
        return lib_path
    
    default_names = {
        'windows': 'tdjson.dll',
        'darwin': 'libtdjson.dylib',
        'linux': 'libtdjson.so'
    }
    
    return default_names.get(system, 'libtdjson.so')

def load_tdjson():
    tdjson_path = find_tdjson()
    
    if not tdjson_path:
        raise RuntimeError(
            "TDLib is not found. Please:\n"
            "1. Download TDLib from https://github.com/tdlib/td\n"
            "2. Build it or download prebuilt binaries\n"
            "3. Place the library in project_root/tdlib/ directory\n"
            "4. Or set TDJSON_PATH in config.py/config.json/.env\n"
            f"Expected library name: {get_expected_lib_name()}"
        )
    
    try:
        if platform.system().lower() == 'windows' and os.path.dirname(tdjson_path):
            os.environ['PATH'] = os.path.dirname(tdjson_path) + os.pathsep + os.environ['PATH']
        
        tdjson = CDLL(tdjson_path)
        print(f"Successfully loaded TDLib from: {tdjson_path}")
        return tdjson
    except Exception as e:
        raise RuntimeError(f"Failed to load TDLib library '{tdjson_path}': {str(e)}")

def get_expected_lib_name():
    system = platform.system().lower()
    lib_names = {
        'windows': 'tdjson.dll',
        'darwin': 'libtdjson.dylib',
        'linux': 'libtdjson.so'
    }
    return lib_names.get(system, 'libtdjson.so')

tdjson = load_tdjson()

td_json_client_create = tdjson.td_json_client_create
td_json_client_create.restype = c_void_p
td_json_client_create.argtypes = []

td_json_client_receive = tdjson.td_json_client_receive
td_json_client_receive.restype = c_char_p
td_json_client_receive.argtypes = [c_void_p, c_double]

td_json_client_send = tdjson.td_json_client_send
td_json_client_send.restype = None
td_json_client_send.argtypes = [c_void_p, c_char_p]

td_json_client_execute = tdjson.td_json_client_execute
td_json_client_execute.restype = c_char_p
td_json_client_execute.argtypes = [c_void_p, c_char_p]

td_json_client_destroy = tdjson.td_json_client_destroy
td_json_client_destroy.restype = None
td_json_client_destroy.argtypes = [c_void_p]

td_set_log_file_path = tdjson.td_set_log_file_path
td_set_log_file_path.restype = c_int
td_set_log_file_path.argtypes = [c_char_p]

td_set_log_max_file_size = tdjson.td_set_log_max_file_size
td_set_log_max_file_size.restype = None
td_set_log_max_file_size.argtypes = [c_longlong]

td_set_log_verbosity_level = tdjson.td_set_log_verbosity_level
td_set_log_verbosity_level.restype = None
td_set_log_verbosity_level.argtypes = [c_int]

fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
td_set_log_fatal_error_callback.restype = None
td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]

def on_fatal_error_callback(error_message):
    error_text = error_message.decode('utf-8') if error_message else "Unknown error"
    raise RuntimeError(f"TDLib fatal error: {error_text}")

td_set_log_verbosity_level(2)
c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
td_set_log_fatal_error_callback(c_on_fatal_error_callback)

class TDJsonClient:
    def __init__(self):
        self.client = td_json_client_create()
        if not self.client:
            raise RuntimeError("Failed to create TDLib client")
    
    def send(self, query):
        query_json = json.dumps(query).encode('utf-8')
        td_json_client_send(self.client, query_json)
    
    def receive(self, timeout=1.0):
        result = td_json_client_receive(self.client, timeout)
        if result:
            return json.loads(result.decode('utf-8'))
        return None
    
    def execute(self, query):
        query_json = json.dumps(query).encode('utf-8')
        result = td_json_client_execute(self.client, query_json)
        if result:
            return json.loads(result.decode('utf-8'))
        return None
    
    def destroy(self):
        if self.client:
            td_json_client_destroy(self.client)
            self.client = None
    
    def __del__(self):
        self.destroy()

try:
    client = TDJsonClient()
except Exception as e:
    print(f"Warning: Failed to create global client: {e}")
    client = None

def td_send(query):
    if client:
        client.send(query)
    else:
        raise RuntimeError("TDLib client not initialized")

def td_receive(timeout=1.0):
    if client:
        return client.receive(timeout)
    return None

def td_execute(query):
    if client:
        return client.execute(query)
    return None

def set_log_file_path(path):
    return td_set_log_file_path(path.encode('utf-8'))

def set_log_max_file_size(size):
    td_set_log_max_file_size(size)

def set_log_verbosity_level(level):
    td_set_log_verbosity_level(level)

if __name__ == "__main__":
    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Expected library name: {get_expected_lib_name()}")
    
    result = td_execute({"@type": "getOption", "name": "version"})
    if result:
        print(f"TDLib version: {result.get('value', 'Unknown')}")
    else:
        print("Failed to get TDLib version")