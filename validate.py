from pathlib import Path
import json,math,argparse,hashlib
root=Path(__file__).resolve().parent
a=argparse.ArgumentParser();a.add_argument('--reproduced-root',required=True);args=a.parse_args();rep=Path(args.reproduced_root)
s=json.loads((root/'runs/baseline/summary.json').read_text());cs=json.loads((root/'runs/baseline/contributions.json').read_text());rs=json.loads((rep/'runs/baseline/summary.json').read_text())
assert s['full_kettle_GWP100_kg_CO2eq'] is None
assert math.isclose(s['BOM_total_g'],723+137.8,abs_tol=1e-10)
assert len([x for x in cs if x['diagnostic_4gas_kg_CO2eq'] is None])==6
assert math.isclose(sum(x['diagnostic_4gas_kg_CO2eq'] or 0 for x in cs),s['diagnostic_4gas_partial_subtotal_kg_CO2eq'],abs_tol=1e-12)
steel=next(x['diagnostic_4gas_kg_CO2eq'] for x in cs if x['material']=='Stainless steel')
assert math.isclose(steel*(1/.9-1),s['scenario']['difference_kg_CO2eq'],abs_tol=1e-12)
assert s['solver_max_abs_residual']<1e-10 and s['electricity_library_inverse_max_abs_residual']<1e-10
assert s==rs,'reproduced numeric summary differs'
matched=[]
for rel in ['runs/baseline/contributions.json','runs/scenario/contributions.json','runs/baseline/elementary-inventory.csv','runs/baseline/unresolved-exchanges.csv','mappings/unit-conversions.json']:
 assert (root/rel).read_bytes()==(rep/rel).read_bytes(),rel
 matched.append(rel)
conversions=json.loads((root/'mappings/unit-conversions.json').read_text())
gas=[x for x in conversions if x['flow_id']=='1a34bf95-f897-4af9-b70c-368fce9e41d6' and x['source_unit']=='m3' and x['target_unit']=='kg']
assert gas and all(math.isclose(x['quantity_multiplier'],1/1.357,abs_tol=1e-12) for x in gas)
result={'status':'passed for incomplete screening implementation','checks':['BOM arithmetic','missing materials remain null','contribution sum','analytic one-parameter sensitivity','linear residual','library inverse residual','recorded natural-gas property conversion','independent rerun equality'],'identical_artifacts':matched,'not_validated':['full product scope','supplier closure','complete LCIA','real product foreground assumptions']}
(root/'logs/validation.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
