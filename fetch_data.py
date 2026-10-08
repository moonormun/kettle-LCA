"""Download official public archives to an ignored cache; verify recorded hashes."""
from pathlib import Path
import urllib.request,json,hashlib,argparse
root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifests/data-manifest.json').read_text(encoding='utf8'))
p=argparse.ArgumentParser();p.add_argument('--cache',default=str(root/'cache'));args=p.parse_args();cache=Path(args.cache);cache.mkdir(parents=True,exist_ok=True)
for name,record in zip(['uslci-2025-06.zip','electricity-library.zip'],manifest['archives']):
 dest=cache/name
 if not dest.exists():
  tmp=dest.with_suffix('.part')
  with urllib.request.urlopen(record['URL'],timeout=60) as r,tmp.open('wb') as f:
   while b:=r.read(1024*1024):f.write(b)
  if hashlib.sha256(tmp.read_bytes()).hexdigest()!=record['sha256']:raise SystemExit('Archive changed; retain .part and inspect new release before use: '+name)
  tmp.replace(dest)
 if hashlib.sha256(dest.read_bytes()).hexdigest()!=record['sha256']:raise SystemExit('Checksum mismatch: '+name)
 print('verified',dest)
