import os
import sys
import json
from pathlib import Path

def load_config():
    try:
        root_dir = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(root_dir))
        
        try:
            from config import TG_API_ID, TG_API_HASH
            return TG_API_ID, TG_API_HASH
        except ImportError:
            config_path = root_dir / 'config.json'
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    return config.get('TG_API_ID'), config.get('TG_API_HASH')
            
            env_path = root_dir / '.env'
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('TG_API_ID='):
                            tg_api_id = line.split('=', 1)[1].strip()
                        elif line.startswith('TG_API_HASH='):
                            tg_api_hash = line.split('=', 1)[1].strip()
                    if 'tg_api_id' in locals() and 'tg_api_hash' in locals():
                        return tg_api_id, tg_api_hash
            
            return None, None
            
    except Exception as e:
        print(f"Error loading config: {e}")
        return None, None