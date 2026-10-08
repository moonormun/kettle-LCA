"""Auditable partial LCI/GWP diagnostic; never substitutes missing inputs with zero."""
from pathlib import Path
import argparse,csv,json,zipfile,io,hashlib,xml.etree.ElementTree as ET
from collections import defaultdict,deque
import numpy as np

ROOT=Path(__file__).resolve().parent
SOURCE_ROOT=ROOT
US_URL='https://raw.githubusercontent.com/FLCAC-admin/uslci-content/dev/downloads/uslci_fy25_q2_01_olca2_4_1_elci_lib_json_ld.zip'
EL_URL='https://www.lcacommons.gov/lca-collaboration/ws/public/libraries/U.S._electricity_baseline_v1.2025-06.0'
US_HASH='55437502fc33d193236d50fd87a361880beea82a27139d1803be38ae0f0934b0'
METHOD='6209b35f-9447-40b5-b68c-a1099e3674a0'
MNS={'m':'http://lca.jrc.it/ILCD/LCIAMethod','c':'http://lca.jrc.it/ILCD/Common'}
BOM=[('Stainless steel',186,'Kettle'),('Brass',20.25,'Kettle'),('Copper',15,'Kettle'),('PP',350.25,'Kettle'),('PVC',43.5,'Kettle'),('Nylon',49.5,'Kettle'),('POM',9.75,'Kettle'),('PC',6.75,'Kettle'),('ABS',30,'Kettle'),('Silicone',12,'Kettle'),('LDPE',6.3,'Packaging'),('Cardboard',131.5,'Packaging')]
SELECT={'Stainless steel':'49f5324b-fc33-36e9-b5af-3c80d73492bd','PP':'89a2b59a-1ca2-34f5-acc8-a8eaaa6fa870','PVC':'3dbccdda-2014-4239-ad1f-4e15c034942b','ABS':'0e42a306-ee2d-362e-8bc3-580000096459','LDPE':'6a12cba1-889d-4515-90f8-89feb8d662f2','Cardboard':'226ed3c2-e020-4c95-b1fc-4559fc2d18ac'}

def dump(path,obj):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
def table(path,rows,keys=None):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys or list(rows[0]));w.writeheader();w.writerows(rows)
def varint(b,i):
 v=s=0
 while True:
  c=b[i];i+=1;v|=(c&127)<<s
  if c<128:return v,i
  s+=7
def fields(b):
 out=[];i=0
 while i<len(b):
  k,i=varint(b,i);wire=k&7
  if wire==0:v,i=varint(b,i)
  elif wire==2:n,i=varint(b,i);v=b[i:i+n];i+=n
  elif wire==1:v=b[i:i+8];i+=8
  elif wire==5:v=b[i:i+4];i+=4
  else:raise ValueError('Unsupported protobuf wire')
  out.append((k>>3,v))
 return dict(out)
def entries(b):
 i=0
 while i<len(b):
  k,i=varint(b,i);assert k==10
  n,i=varint(b,i);yield fields(b[i:i+n]);i+=n
def desc(b):
 f=fields(b);return {k:v.decode() for k,v in f.items() if isinstance(v,bytes)}
def normunit(u):return {'kg':1,'g':.001,'MJ':1,'kWh':3.6,'m3':1,'l':.001,'t*km':1}.get(u)
def ratio(source,target):
 if source==target:return 1.
 groups=[{'kg','g'},{'MJ','kWh'},{'m3','l'}]
 if any(source in g and target in g for g in groups):return normunit(source)/normunit(target)
 return None

def sparse_data(raw):
 z=np.load(io.BytesIO(raw));shape=tuple(z['shape']);fmt=z['format'].item().decode();indptr=z['indptr'];indices=z['indices'];data=z['data']
 if fmt=='csc':cols=np.repeat(np.arange(shape[1]),np.diff(indptr));rows=indices
 elif fmt=='csr':rows=np.repeat(np.arange(shape[0]),np.diff(indptr));cols=indices
 else:raise ValueError(fmt)
 return shape,rows,cols,data

def run(us,el):
 uz=zipfile.ZipFile(us);ez=zipfile.ZipFile(el);mz=zipfile.ZipFile(io.BytesIO(ez.read('meta.zip')))
 assert hashlib.sha256(Path(us).read_bytes()).hexdigest()==US_HASH,'USLCI archive changed'
 ps={json.loads(uz.read(n))['@id']:json.loads(uz.read(n)) for n in uz.namelist() if n.startswith('processes/') and n.endswith('.json')}
 flowdefs={json.loads(uz.read(n))['@id']:json.loads(uz.read(n)) for n in uz.namelist() if n.startswith('flows/') and n.endswith('.json')}
 conversions=[]
 def exchange_ratio(e,pr):
  source=e['unit']['name'];target=pr['unit']['name'];simple=ratio(source,target)
  if simple is not None:return simple
  f=flowdefs.get(e['flow']['@id'],{});factors={x['flowProperty']['@id']:x for x in f.get('flowProperties',[])}
  sp=factors.get(e.get('flowProperty',{}).get('@id'));tp=factors.get(pr.get('flowProperty',{}).get('@id'))
  if not sp or not tp:return None
  a=ratio(source,sp['flowProperty'].get('refUnit'));b=ratio(target,tp['flowProperty'].get('refUnit'))
  if a is None or b is None or sp['conversionFactor']<=0 or tp['conversionFactor']<=0:return None
  value=a/sp['conversionFactor']*tp['conversionFactor']/b
  conversions.append({'flow_id':f['@id'],'source_unit':source,'target_unit':target,'source_property_factor':sp['conversionFactor'],'target_property_factor':tp['conversionFactor'],'quantity_multiplier':value,'source':'USLCI flowProperties conversionFactor'})
  return value
 refs={};providers=defaultdict(list)
 for pid,p in ps.items():
  rr=[e for e in p['exchanges'] if e.get('isQuantitativeReference')]
  if len(rr)!=1 or rr[0].get('isInput') or rr[0]['amount']<=0:continue
  refs[pid]=rr[0];providers[rr[0]['flow']['@id']].append(pid)
 # Library metadata is intentionally incomplete. Read inventories from matrix assets.
 ai={e.get(1,0):e for e in entries(ez.read('index_A.bin'))}
 bi={e.get(1,0):e for e in entries(ez.read('index_B.bin'))}
 ash,ar,ac,av=sparse_data(ez.read('A.npz'));bsh,br,bc,bv=sparse_data(ez.read('B.npz'))
 A=np.zeros(ash);np.add.at(A,(ar,ac),av)
 inv=np.load(io.BytesIO(ez.read('INV.npy')))
 residual=float(np.max(np.abs(A@inv-np.eye(A.shape[0]))))
 assert residual<1e-6,'Electricity library inverse failed validation'
 lib={desc(e[2])[1]:(i,desc(e[3])) for i,e in ai.items()}
 lbflows={i:desc(e[2]) for i,e in bi.items()}
 libcache={}
 def libinv(pid):
  if pid not in libcache:
   i,d=lib[pid];v=np.zeros(bsh[0]);np.add.at(v,br,bv*inv[bc,i]);out=defaultdict(float)
   for j in np.flatnonzero(v):
    f=lbflows[j];out[(f[1],f[2],f.get(3,''),f[5])]+=float(v[j])
   libcache[pid]=out
  return libcache[pid]
 # Retain original source data; remove component shipping corrugate in model only.
 overrides=[]
 for e in ps[SELECT['PP']]['exchanges']:
  if e['flow']['name'] in ['Corrugated product, average production, at mill','Disposal, corrugate packaging, to unspecified treatment']:
   overrides.append({'process':SELECT['PP'],'exchange':e['internalId'],'original_amount':e['amount'],'model_amount':0,'reason':'BOM packaging is modeled separately; component-shipping packaging excluded as declared modeling choice'})
 skip={x['exchange'] for x in overrides};edges={};boundary=[];library_edges={};visited=set();q=deque(SELECT.values())
 while q:
  pid=q.popleft()
  if pid in visited:continue
  visited.add(pid);p=ps[pid];r=refs[pid];edges[pid]=[];library_edges[pid]=[]
  for e in p['exchanges']:
   if pid==SELECT['PP'] and e['internalId'] in skip:continue
   if e.get('isQuantitativeReference') or e['flow'].get('flowType')=='ELEMENTARY_FLOW' or abs(e['amount'])<1e-15:continue
   row={'process_id':pid,'process_name':p['name'],'exchange':e['internalId'],'flow_id':e['flow']['@id'],'flow_name':e['flow']['name'],'amount_per_reference':e['amount']/r['amount'],'unit':e['unit']['name'],'direction':'input' if e.get('isInput') else 'output'}
   if not e.get('isInput'):
    row['reason']='unlinked waste/treatment or coproduct; no substitution credit';boundary.append(row);continue
   prov=e.get('defaultProvider',{}).get('@id');reason=''
   if prov in lib:
    i,lf=lib[prov]
    unitratio=ratio(e['unit']['name'],lf[5])
    if lf[1]==e['flow']['@id'] and unitratio is not None:
     library_edges[pid].append((prov,e['amount']/r['amount']*unitratio));continue
    reason='library provider reference-flow mismatch'
   elif prov in refs and refs[prov]['flow']['@id']==e['flow']['@id']:
    pr=refs[prov];unitratio=exchange_ratio(e,pr)
    if unitratio is not None:
     coef=e['amount']/r['amount']*unitratio;edges[pid].append((prov,coef,'default'));q.append(prov);continue
    reason='reference-flow units need verified density / flow-property conversion'
   elif prov:reason='default provider absent or reference-flow mismatch'
   else:
    choices=providers.get(e['flow']['@id'],[])
    if len(choices)==1:
     prov=choices[0];pr=refs[prov];unitratio=exchange_ratio(e,pr)
     if unitratio is not None:
      coef=e['amount']/r['amount']*unitratio;edges[pid].append((prov,coef,'unique reference-flow match'));q.append(prov);continue
     reason='unique provider requires verified density / flow-property conversion'
    else:reason=f'no default provider; {len(choices)} compatible reference-flow candidates'
   row['reason']=reason;boundary.append(row)
 ids=sorted(visited);ix={p:i for i,p in enumerate(ids)};mat=np.eye(len(ids))
 for pid,es in edges.items():
  for provider,coef,why in es:mat[ix[provider],ix[pid]]-=coef
 def inventory(steel_yield):
  results=[];stocks=defaultdict(float);scaledboundary=[];res=0
  for material,mass,part in BOM:
   if material not in SELECT:
    results.append({'material':material,'mass_g':mass,'diagnostic_4gas_kg_CO2eq':None,'status':'unmatched material'});continue
   pid=SELECT[material];qty=mass/1000/(steel_yield if material=='Stainless steel' else 1)
   demand=np.zeros(len(ids));demand[ix[pid]]=qty;activity=np.linalg.solve(mat,demand)
   res=max(res,float(np.max(np.abs(mat@activity-demand))));invout=defaultdict(float)
   for pp in ids:
    scale=activity[ix[pp]]/refs[pp]['amount']
    for e in ps[pp]['exchanges']:
     f=e['flow']
     if f.get('flowType')!='ELEMENTARY_FLOW':continue
     signed=-1 if e.get('isInput') else 1
     invout[(f['@id'],f['name'],f.get('category',''),e['unit']['name'])]+=signed*e['amount']*scale
    for provider,coef in library_edges[pp]:
     for key,amount in libinv(provider).items():invout[key]+=amount*activity[ix[pp]]*coef
   for key,v in invout.items():stocks[(material,*key)]+=v
   for row in boundary:
    amt=row['amount_per_reference']*activity[ix[row['process_id']]]
    if abs(amt)>1e-15:scaledboundary.append(dict(row,material=material,scaled_amount=amt))
   diag=0.;matched=0
   for (_,name,cat,unit),v in invout.items():
    if name in cf and '/emission/air' in cat.lower() and unit=='kg':diag+=v*cf[name];matched+=1
   results.append({'material':material,'mass_g':mass,'diagnostic_4gas_kg_CO2eq':diag,'status':'partial supply chain; 4-gas diagnostic only','characterized_flow_records':matched})
  return results,stocks,scaledboundary,res
 # The exact archived factors are sourced; fossil origin for generic USLCI gases is an assumption.
 mr=ET.parse(SOURCE_ROOT/'sources'/f'{METHOD}.xml').getroot();source_names={'Carbon dioxide':'carbon dioxide (fossil)','Methane':'methane (fossil)','Nitrous oxide':'nitrous oxide','Sulfur hexafluoride':'sulphur hexafluoride'};cf={};cfrows=[]
 for usname,tgname in source_names.items():
  wanted=tgname+' (Mass, kg, Emissions to air, unspecified)';found=[]
  for f in mr.findall('.//m:factor',MNS):
   name=f.findtext('m:referenceToFlowDataSet/c:shortDescription',namespaces=MNS)
   if name==wanted:found.append((float(f.findtext('m:meanValue',namespaces=MNS)),f.find('m:referenceToFlowDataSet',MNS).get('refObjectId')))
  assert len(found)==1,(wanted,found)
  cf[usname]=found[0][0];cfrows.append({'USLCI_name':usname,'TianGong_flow_name':wanted,'TianGong_flow_UUID':found[0][1],'factor_kg_CO2eq_per_kg':found[0][0],'mapping_status':'assumed fossil origin / air compartment generalized' if usname in ['Carbon dioxide','Methane'] else 'substance-name match; air compartment generalized'})
 base,stock,bounds,res=inventory(1.0);alt,_,_,_=inventory(.9)
 subtotal=sum(r['diagnostic_4gas_kg_CO2eq'] or 0 for r in base);altsub=sum(r['diagnostic_4gas_kg_CO2eq'] or 0 for r in alt)
 missing=[m for m,_,_ in BOM if m not in SELECT]
 summary={'run_id':'public-screening-20261008-baseline','status':'INCOMPLETE_SCREENING','full_kettle_GWP100_kg_CO2eq':None,'diagnostic_4gas_partial_subtotal_kg_CO2eq':subtotal,'warning':'NOT full kettle footprint, NOT lower bound; excludes unmapped materials, missing foreground processes, unresolved supply chain and uncharacterized gases. Generic CO2/CH4 assumed fossil including possible biogenic flows.','BOM_total_g':sum(x[1] for x in BOM),'mapped_BOM_mass_g':sum(m for n,m,_ in BOM if n in SELECT),'missing_materials':missing,'reachable_USLCI_process_count':len(ids),'reachable_library_provider_count':len(libcache),'unresolved_scaled_exchange_rows':len(bounds),'solver_max_abs_residual':res,'electricity_library_inverse_max_abs_residual':residual,'scenario':{'run_id':'public-screening-20261008-steel-yield-90','changed_decision':'steel yield 1.0 -> 0.9; additional scrap treatment still unresolved','diagnostic_partial_subtotal_kg_CO2eq':altsub,'difference_kg_CO2eq':altsub-subtotal,'difference_percent':100*(altsub-subtotal)/subtotal},'uncertainty':'not calculated; no defensible parameter distributions'}
 dump(Path('runs/baseline/summary.json'),summary);dump(Path('runs/baseline/contributions.json'),base);dump(Path('runs/scenario/contributions.json'),alt)
 table('runs/baseline/elementary-inventory.csv',[{'material':k[0],'flow_id':k[1],'flow_name':k[2],'category':k[3],'unit':k[4],'amount':v,'characterized_in_diagnostic':k[2] in cf and '/emission/air' in k[3].lower() and k[4]=='kg'} for k,v in stock.items()])
 table('runs/baseline/unresolved-exchanges.csv',bounds)
 table('mappings/characterization.csv',cfrows);dump(Path('inputs/overrides.json'),overrides)
 dump(Path('mappings/unit-conversions.json'),conversions)
 table('inputs/bom.csv',[{'material':m,'finished_mass_g':v,'part':p,'status':'sourced; transcribed from classroom site'} for m,v,p in BOM])
 mapping=[]
 for m,mass,part in BOM:
  pid=SELECT.get(m);p=ps.get(pid,{}) ;r=refs.get(pid,{})
  mapping.append({'material':m,'mass_g':mass,'database':'USLCI' if pid else 'TianGong snapshot / USLCI searched','release':'1.2025-06.0' if pid else 'no selected process','dataset_name':p.get('name','not matched'),'UUID':pid or 'unknown','version':p.get('version','unknown'),'geography':p.get('location',{}).get('name','unknown'),'year_description':p.get('processDocumentation',{}).get('timeDescription',p.get('processDocumentation',{}).get('validFrom','unknown')),'reference_flow':r.get('flow',{}).get('name','unknown'),'reference_amount':r.get('amount','unknown'),'reference_unit':r.get('unit',{}).get('name','unknown'),'source_URL':US_URL if pid else 'https://github.com/tiangong-lca/data','retrieval_date':'2026-10-08','file_sha256':hashlib.sha256(uz.read('processes/'+pid+'.json')).hexdigest() if pid else 'unknown','decision':'screening proxy / subject to supplier closure' if pid else 'unresolved; not replaced with arbitrary material','proxy_note':{'Stainless steel':'304 coil assumed; grade unconfirmed','PP':'integrated PP injection; shipping corrugate removed; resin/energy not added twice','PVC':'resin only; compound additives and forming missing','ABS':'resin only; forming missing','LDPE':'resin only; film extrusion missing','Cardboard':'US corrugated converted product assumed; board type unknown'}.get(m,'no defensible selected provider')})
 table('mappings/material-mapping.csv',mapping)
 table('mappings/provider-links.csv',[{'consumer':p,'provider':pr,'coefficient':c,'selection':why} for p,es in edges.items() for pr,c,why in es]+[{'consumer':p,'provider':pr,'coefficient':c,'selection':'electricity library B @ INV'} for p,es in library_edges.items() for pr,c in es])
 manifest={'archives':[{'name':'USLCI 1.2025-06.0','URL':US_URL,'sha256':US_HASH},{'name':'electricity 1.2025-06.0','URL':EL_URL,'sha256':hashlib.sha256(Path(el).read_bytes()).hexdigest()}],'method':{'database':'TianGong public historical snapshot','UUID':METHOD,'version':'01.00.000','sha256':hashlib.sha256((SOURCE_ROOT/'sources'/f'{METHOD}.xml').read_bytes()).hexdigest(),'metadata_warning':'generalComment says IPCC 2021; converted source says IPCC 2013. Preserve exact file; do not label independently verified full AR6 implementation.'},'runtime':{'python':__import__('platform').python_version(),'numpy':np.__version__},'processes':[{'UUID':p,'name':ps[p]['name'],'version':ps[p]['version'],'sha256':hashlib.sha256(uz.read('processes/'+p+'.json')).hexdigest(),'isCopyrightProtected':ps[p].get('processDocumentation',{}).get('isCopyrightProtected')} for p in ids]}
 dump(Path('manifests/data-manifest.json'),manifest)
 print(json.dumps(summary,ensure_ascii=True,indent=2))

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--uslci',required=True);a.add_argument('--electricity',required=True);a.add_argument('--output-dir',required=True);args=a.parse_args();ROOT=Path(args.output_dir).resolve()
 if (ROOT/'runs/baseline/summary.json').exists():raise SystemExit('Existing independent result is preserved. Choose a new --output-dir.')
 run(args.uslci,args.electricity)
