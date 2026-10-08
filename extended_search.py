import zipfile,json,xml.etree.ElementTree as E,pathlib,collections,csv
u=zipfile.ZipFile('work/uslci-2025-06.zip');t=zipfile.ZipFile('work/tiangong-public.zip')
out=pathlib.Path('work/deeper');out.mkdir(exist_ok=True)
ps=[json.loads(u.read(n)) for n in u.namelist() if n.startswith('processes/') and n.endswith('.json')]
co=[]
for n in u.namelist():
 if n.startswith('flows/') and n.endswith('.json'):
  f=json.loads(u.read(n))
  if f.get('name') in ['Carbon dioxide','Methane']:co.append(f)
(out/'carbon-flows.json').write_text(json.dumps(co,indent=2),encoding='utf8')
print('CARBON',[(f['@id'],f['name'],f.get('category'),f.get('description','')[:400]) for f in co])
matches=[]
needles=['polyoxymethylene','polyacetal','polycarbonate','silicone rubber','polydimethylsiloxane','polyamide','nylon','brass','copper production']
for n in t.namelist():
 if '/processes/' not in n or not n.endswith('.xml'):continue
 r=E.fromstring(t.read(n));en=[e.text for e in r.iter() if e.text and e.get('{http://www.w3.org/XML/1998/namespace}lang')=='en']
 full=' '.join(en);hit=[w for w in needles if w in full.lower()]
 if not hit:continue
 names='; '.join(e.text or '' for e in r.iter() if e.tag.split('}')[-1]=='baseName' and e.get('{http://www.w3.org/XML/1998/namespace}lang')=='en')
 ex=[e for e in r.iter() if e.tag.split('}')[-1]=='exchange']
 matches.append({'path':n,'name':names,'terms':hit,'exchanges':len(ex)})
(out/'fulltext-candidates.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2),encoding='utf8')
print('FULLTEXT MATCHES',len(matches))
for m in matches:
 if 'NESPS2' not in m['name']:print(m['path'].split('/')[-1],m['name'].encode('ascii','ignore').decode()[:160],m['terms'],m['exchanges'])
print('US copper bridge')
for p in ps:
 if p['@id']=='6373ec73-ca57-47bd-8284-2f3cc25b8637':print(json.dumps(p,ensure_ascii=True)[:14000])
