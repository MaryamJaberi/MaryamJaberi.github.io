import sys, json, base64, re
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
b = None
try:
    d = json.loads(s)
    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                r = walk(v)
                if r: return r
        elif isinstance(o, list):
            for v in o:
                r = walk(v)
                if r: return r
        elif isinstance(o, str) and len(o) > 10000: return o
    b = walk(d); print('json keys', list(d.keys()) if isinstance(d, dict) else type(d))
except Exception as e:
    m = max(re.findall(r'[A-Za-z0-9+/=_-]{10000,}', s), key=len); b = m; print('raw', e)
b = b.replace('-', '+').replace('_', '/')
raw = base64.b64decode(b + '=' * (-len(b) % 4))
open(out, 'wb').write(raw); print(len(raw), raw[:8])
