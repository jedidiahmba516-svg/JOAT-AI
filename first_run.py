import json
from pathlib import Path
from datetime import datetime, timezone
STATE=Path('data/consent.json')
def accepted():
 try:return bool(json.loads(STATE.read_text()).get('terms_accepted'))
 except Exception:return False
def record():
 STATE.parent.mkdir(exist_ok=True)
 STATE.write_text(json.dumps({'terms_accepted':True,'privacy_accepted':True,'accepted_at':datetime.now(timezone.utc).isoformat()},indent=2),encoding='utf-8')
