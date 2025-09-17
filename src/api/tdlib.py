from ctypes.util import find_library
from ctypes import *
import json
import sys
import os
import platform

def find_tdjson_system():
    possible_paths = [
        '/usr/local/lib/libtdjson.so',
        '/usr/lib/libtdjson.so',
        '/usr/lib/x86_64-linux-gnu/libtdjson.so',
        '/usr/lib/aarch64-linux-gnu/libtdjson.so',
        '/usr/lib/arm-linux-gnueabihf/libtdjson.so',
        '/opt/td/lib/libtdjson.so',
        os.path.expanduser('~/td/build/libtdjson.so'),
        os.path.expanduser('~/td/lib/libtdjson.so'),
        os.path.expanduser('~/libtdjson.so'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    lib_path = find_library("tdjson")
    if lib_path:
        return lib_path
    
    return 'libtdjson.so'

tdjson_path = find_tdjson_system()

if tdjson_path is None:
    raise RuntimeError(
        "TDLib is not found on the system. "
        "Please, follow instructions at https://github.com/tdlib/td to build it."
    )

try:
    tdjson = CDLL(tdjson_path)
except Exception as e:
    raise RuntimeError(f"Failed to load TDLib library '{tdjson_path}': {str(e)}")

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
    print(f"TDLib library loaded from: {tdjson_path}")
    print(f"Platform: {platform.system()} {platform.machine()}")
    
    result = td_execute({"@type": "getOption", "name": "version"})
    if result:
        print(f"TDLib version: {result.get('value', 'Unknown')}")
    else:
        print("Failed to get TDLib version")