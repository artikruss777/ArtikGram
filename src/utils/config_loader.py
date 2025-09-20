import os
import sys
import json
from pathlib import Path

def load_config():
    try:
        root_dir = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(root_dir))
        
        config_data = {}
        
        try:
            from config import TG_API_ID, TG_API_HASH, TDJSON_PATH
            config_data['TG_API_ID'] = TG_API_ID
            config_data['TG_API_HASH'] = TG_API_HASH
            config_data['TDJSON_PATH'] = TDJSON_PATH
        except ImportError:
            try:
                import config
                config_data['TG_API_ID'] = getattr(config, 'TG_API_ID', None)
                config_data['TG_API_HASH'] = getattr(config, 'TG_API_HASH', None)
                config_data['TDJSON_PATH'] = getattr(config, 'TDJSON_PATH', None)
            except ImportError:
                pass
        
        config_path = root_dir / 'config.json'
        if config_path.exists():
            with open(config_path, 'r') as f:
                json_config = json.load(f)
                if 'TG_API_ID' in json_config:
                    config_data['TG_API_ID'] = json_config['TG_API_ID']
                if 'TG_API_HASH' in json_config:
                    config_data['TG_API_HASH'] = json_config['TG_API_HASH']
                if 'TDJSON_PATH' in json_config:
                    config_data['TDJSON_PATH'] = json_config['TDJSON_PATH']
        
        env_path = root_dir / '.env'
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            if key == 'TG_API_ID':
                                try:
                                    config_data['TG_API_ID'] = int(value)
                                except ValueError:
                                    config_data['TG_API_ID'] = value
                            elif key == 'TG_API_HASH':
                                config_data['TG_API_HASH'] = value
                            elif key == 'TDJSON_PATH':
                                config_data['TDJSON_PATH'] = value
        
        if isinstance(config_data.get('TG_API_ID'), str):
            try:
                config_data['TG_API_ID'] = int(config_data['TG_API_ID'])
            except (ValueError, TypeError):
                pass
        
        return config_data.get('TG_API_ID'), config_data.get('TG_API_HASH')
            
    except Exception as e:
        print(f"Error loading config: {e}")
        return None, None

def get_tdjson_path():
    config = load_config()
    try:
        root_dir = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(root_dir))
        
        tdjson_path = None
        
        try:
            from config import TDJSON_PATH
            tdjson_path = TDJSON_PATH
        except ImportError:
            try:
                import config
                tdjson_path = getattr(config, 'TDJSON_PATH', None)
            except ImportError:
                pass
        
        if not tdjson_path:
            config_path = root_dir / 'config.json'
            if config_path.exists():
                with open(config_path, 'r') as f:
                    json_config = json.load(f)
                    tdjson_path = json_config.get('TDJSON_PATH')
        
        if not tdjson_path:
            env_path = root_dir / '.env'
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('TDJSON_PATH='):
                            tdjson_path = line.split('=', 1)[1].strip()
        
        if tdjson_path:
            if not Path(tdjson_path).is_absolute():
                tdjson_path = str(root_dir / tdjson_path)
            
            if os.path.exists(tdjson_path):
                return tdjson_path
    
    except Exception as e:
        print(f"Error getting TDJSON path: {e}")
    
    return None