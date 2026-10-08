"""Explicit hybrid screening assumptions; not a harmonized full LCA."""
from pathlib import Path
import json, csv, argparse, math
ROOT=Path(__file__).resolve().parent
def source(n):
 p=ROOT/n
 return p if p.exists() else ROOT/n.replace('/','__')
def run(p):
 base=json.loads(source('runs/baseline/contributions.json').read_text(encoding='utf8'))
 rows=[];scrap=0.;purchased=0.
 for b in base:
  m=b['material'];mass=b['mass_g']/1000
  y=p['steel_yield'] if m=='Stainless steel' else (1 if m=='PP' else p['other_yield'])
  q=mass/y;purchased+=q;scrap+=q-mass
  if b['diagnostic_4gas_kg_CO2eq'] is not None:
   val=b['diagnostic_4gas_kg_CO2eq']/y;status='inherited partial model; scaled purchase mass'
  else:
   val=q*p['material_factors'][m];status='published factor or explicitly assumed proxy'
  rows.append({'item':m,'finished_kg':mass,'purchased_kg':q,'kg_CO2eq':val,'status':status})
 # PP integrated process already includes resin loss and molding power.
 scrap+=.35025*.045
 purchased+=.35025*(1.034+.0194-1)
 pol=sum(b['mass_g']/1000 for b in base if b['material'] in ['PVC','Nylon','POM','PC','ABS','Silicone','LDPE'])
 metal=.186*p['metal_forming_kWh_kg']+(.02025+.015)*p['smallmetal_forming_kWh_kg']
 def add(name,v):rows.append({'item':name,'finished_kg':None,'purchased_kg':None,'kg_CO2eq':v,'status':'explicit assumption'})
 add('Other polymer forming',pol*p['polymer_forming_kWh_kg']*p['electricity_kg_kWh'])
 add('Metal component forming',metal*p['electricity_kg_kWh'])
 add('Assembly and testing',p['assembly_kWh']*p['electricity_kg_kWh'])
 add('Packaging operation',p['packaging_kWh']*p['electricity_kg_kWh'])
 add('Additional inbound transport',purchased/1000*p['inbound_km']*p['truck_kg_tkm'])
 add('Manufacturing scrap treatment',scrap*p['scrap_kg_kg'])
 physical=sum(x['kg_CO2eq'] for x in rows)
 inherited=sum(x['kg_CO2eq'] for x in rows if x['status'].startswith('inherited'))
 add('Unresolved background allowance',inherited*p['background_allowance_fraction'])
 return {'total_kg_CO2eq':sum(x['kg_CO2eq'] for x in rows),'before_background_allowance_kg_CO2eq':physical,'scrap_kg':scrap,'inbound_purchase_proxy_kg':purchased,'contributions':rows}
def main():
 a=argparse.ArgumentParser();a.add_argument('--output-dir',required=True);args=a.parse_args();out=Path(args.output_dir)
 if out.exists():raise SystemExit('Refusing to overwrite existing run')
 p=json.loads(source('inputs/estimate-assumptions.json').read_text(encoding='utf8'))
 results={k:run(v) for k,v in p['scenarios'].items()}
 central=p['scenarios']['central'];sens=[]
 for key in central:
  if key=='material_factors':continue
  for case in ['low','high']:
   q=dict(central);q[key]=p['scenarios'][case][key];v=run(q)['total_kg_CO2eq']
   sens.append({'parameter':key,'case':case,'value':q[key],'total_kg_CO2eq':v,'delta_kg_CO2eq':v-results['central']['total_kg_CO2eq']})
 for m in central['material_factors']:
  for case in ['low','high']:
   q=dict(central);q['material_factors']=dict(central['material_factors']);q['material_factors'][m]=p['scenarios'][case]['material_factors'][m]
   v=run(q)['total_kg_CO2eq'];sens.append({'parameter':'factor_'+m,'case':case,'value':q['material_factors'][m],'total_kg_CO2eq':v,'delta_kg_CO2eq':v-results['central']['total_kg_CO2eq']})
 assert len(results['central']['contributions'])==19
 assert all(math.isfinite(x['kg_CO2eq']) and x['kg_CO2eq']>=0 for v in results.values() for x in v['contributions'])
 assert results['low']['total_kg_CO2eq']<=results['central']['total_kg_CO2eq']<=results['high']['total_kg_CO2eq']
 assert math.isclose(sum(x['finished_kg'] or 0 for x in results['central']['contributions']),.8608,abs_tol=1e-12)
 out.mkdir(parents=True)
 summary={'status':'ASSUMPTION_FILLED_HYBRID_SCREENING','unit':'kg CO2-equivalent per manufactured packaged BC1 kettle','not_a_harmonized_full_LCA':True,'scenario_range_is_not_confidence_interval':True,'scenarios':results,'one_at_a_time_sensitivity':sens,'checks':'BOM mass, finite contributions, sum and scenario ordering passed'}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
 with (out/'contributions.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(results['central']['contributions'][0]));w.writeheader();w.writerows(results['central']['contributions'])
 print(json.dumps({k:v['total_kg_CO2eq'] for k,v in results.items()}))
if __name__=='__main__':main()
