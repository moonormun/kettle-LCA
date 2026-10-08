# BC1 kettle: 가정값을 보완한 원재료·제조 추정 평가

**중앙 추정: 4.759 kg CO₂e/대 (약 4.76).** 낮은 가정 3.680, 높은 가정 7.279. 이 범위는 신뢰구간이나 보장된 상·하한이 아니다. 자료와 가정이 혼합된 screening 결과이며 ISO 검증 탄소발자국 또는 동일 LCIA법으로 완결된 LCA로 주장하지 않는다.

## 1. Study identity and purpose

BC1 1 L 플라스틱 kettle의 원재료·제조 영향을 추정한다. 공개 별칭 moonormun, 저장소 https://github.com/moonormun/kettle-LCA, 날짜 2026-10-08. Run ID estimate-v3. 기존 독립 부분 run과 가정 보완 run을 함께 보존한다. 최종 commit SHA는 업로드 완료 후 제출 양식에 입력하며 README 자신의 미래 해시는 기입하지 않는다. 원래 목표는 TianGong/USLCI 기반 평가이며 이번 버전은 사용자 요청에 따라 공개 문헌과 가정도 추가했다.

## 2. Product, declared unit and system boundary

제조·포장된 BC1 1 L kettle 1대: 본체 723 g, 포장 137.8 g, 합계 860.8 g. 원재료 생산, 부품 가공, 조립·검사, 포장, 추가 입고운송과 제조 scrap 처리를 포함한다. 출하 후 유통·사용·제품 폐기는 제외한다. 설비는 별도 전경에서 제외하나 배경자료 포함분은 유지한다. 실제 공장·연도는 unknown, 미국 USLCI와 국제 문헌을 혼합한 가상 제품이다. [BOM](inputs__bom.csv), [원문 출처와 기존 검토](sources__v2-RESULTS.md). 원문 May 2021 Task4 PDF141–145쪽과 Table5-7 PDF169쪽에서 확인했다.

## 3. Foreground inventory and quantitative assumptions

수량은 BOM, 미계측 공정은 명시적인 가정이다. 구매량=완제품 질량/수율. steel 수율90%, PP 외 나머지95%. PP는 기존 통합 사출 모델의 투입·손실을 유지하며 일반 수율과 성형 전력을 중복 적용하지 않는다. 다른 수지 성형1.79 kWh/kg은 PP 공정6.444 MJ/kg÷3.6을 대용한 값으로 PVC 압출·실리콘 경화의 실제 계측값이 아니다. 별도 PP 배송용 골판지 제외라는 기존 가정도 유지한다.

| 파라미터(단위는 이름/아래 설명) | 낮음 | 중앙 | 높음 |
|---|---:|---:|---:|
| steel_yield | 0.98 | 0.9 | 0.75 |
| other_yield | 0.99 | 0.95 | 0.9 |
| electricity_kg_kWh | 0.2 | 0.5 | 0.8 |
| polymer_forming_kWh_kg | 0.8 | 1.79 | 3.0 |
| metal_forming_kWh_kg | 0.2 | 0.5 | 1.0 |
| smallmetal_forming_kWh_kg | 0.4 | 1.0 | 2.0 |
| assembly_kWh | 0.03 | 0.1 | 0.3 |
| packaging_kWh | 0.01 | 0.02 | 0.05 |
| inbound_km | 100 | 500 | 1500 |
| truck_kg_tkm | 0.06 | 0.1 | 0.2 |
| scrap_kg_kg | 0.2 | 2.0 | 3.5 |
| background_allowance_fraction | 0 | 0.1 | 0.3 |

yield 및 allowance는 비율, forming은 kWh/kg 완제품, assembly/packaging은 kWh/대, electricity는 kg CO₂e/kWh, inbound는 km, truck은 kg CO₂e/t·km, scrap은 kg CO₂e/kg scrap이다. 모든 범위는 분석자가 설정한 stress 조건으로 실측 분포가 아니다. 가격 기반 추정은 사용하지 않았다. 상세 근거는 [입력 JSON](inputs__estimate-assumptions.json).

## 4. Background data and matching decisions

기존 6개 재료는 USLCI 공개 배포본 공급망과 TianGong 과거 공개 특성화계수의 부분 결과를 재사용했다. UUID·버전·지역·연도·기준 흐름은 [재료 매핑](mappings__material-mapping.csv), [원본 manifest](manifests__data-manifest.json), [기존 방법](sources__v2-README.md)에 있다. 최신 TianGong 로그인 자료는 쓰지 않았다.

추가 계수(kg CO₂e/kg): Copper4.0은 [Copper Information Center 2023 공개 설명](https://help.copper.fyi/hc/en-us/articles/6318125638940-What-is-the-Copper-Environmental-Profile)의 cathode 평균값이다(1차·2차 혼합, 부산물 credit 포함). Brass4.0은 **구리 대체계수 가정**이며 실제 합금 비율·아연 영향을 계산한 값이 아니다. Nylon8.06, POM3.22, Silicone2.66은 [원문 PDF](sources__kettle-study-original.pdf) Annex E, PDF193쪽의 누적 영향계수다. Nylon/Silicone 배경은 ecoinvent3.6 cut-off, POM은 Industry data2.0이다. PC8.06은 **나일론 대체계수 가정**이며 검증된 PC 값이 아니다. 추가 여섯 계수의 낮음/높음은 모두 중앙±30%로 가정했다. 계수로 도입한 문헌자료의 UUID·reference exchange는 not applicable; 본 연구가 해당 원 LCI를 확보한 것은 아니다. 웹 확인일2026-10-08.

## 5. Calculation and impact-assessment methods

재료 영향=구매량×계수; 기존 부분 재료 영향은 수율로 나누어 확대한다. 추가 제조 영향=전력×가정 전력계수, 운송=구매량(tonne)×거리×계수, scrap=발생 질량×가정 처리계수. PP 손실0.01576125 kg 포함, 별도 recycling credit 없음. 중앙 scrap 0.053509 kg/대. PP 원본 물질수지 차이0.0084 kg/kg는 배합/흐름 오류 가능성이 남아 전체 원자수지가 닫혔다고 주장하지 않는다.

남은 배경 공급망·미특성화의 **보정 가정은 수율 반영된 기존 6재료 영향의10%**이며 실제 배출과 연결된 LCI가 아니다. 0/10/30%를 별도 시험한다. 이는 새 전경 제조·운송을 대상으로 하지 않지만 실제 미연결 흐름 구성상 중복/누락 가능성은 남는다. 보정 이전 물리 항목 합계 **4.427**, 보정액 **0.332 kg CO₂e/대**를 분리한다.

이전 계산 A s=f, g=B s, 네 기체 C g 결과와 문헌 GWP100·가정계수의 혼합이다. 기존 네 기체 CO₂/CH₄/N₂O/SF₆ 특성화, generic CO₂/CH₄ fossil 가정, 미연결 상류, biogenic 구분 미해결 상태는 유지된다. 10% 보정으로 이를 과학적으로 해결했다는 뜻은 아니다. 방법·지역·할당 차이는 미조화 상태다. 이전 버전에서 합산을 보류했던 문헌계수는 이번 사용자 승인으로 **가정 기반 혼합 시나리오에 한해서** 합산했다.

## 6. How to reproduce the analysis

Python3.12 표준 라이브러리로 새 가정 계산을 재현한다. 저장소 루트에서:

```powershell
python estimate.py --output-dir reproduced-estimate
```

입력: `inputs/estimate-assumptions.json`, `runs/baseline/contributions.json`. 출력: `summary.json`, `contributions.csv`. 기존 폴더를 덮어쓰지 않는다. 원래 USLCI 선형 계산부터 재현하는 명령과 NumPy2.3.5 설치·원자료 취득은 [보존된 기존 README](sources__v2-README.md)의6절에 있다. 과거 README의 상대 링크는 그 문서를 저장소 루트 기준으로 작성한 역사 기록이므로 현재 루트 경로를 사용한다. API 키·로그인 없이 공개 배포본 재현이 가능하다. 원문 PDF와 계산에 사용한 누적계수는 제공하지만 상용 원 LCI 전체는 제공하지 않는다. 난수·seed는 not applicable.

## 7. Results, checks and interpretation

| 항목 | kg CO₂e/대 |
|---|---:|
| Stainless steel | 1.625560 |
| Brass | 0.085263 |
| Copper | 0.063158 |
| PP | 1.147258 |
| PVC | 0.139437 |
| Nylon | 0.419968 |
| POM | 0.033047 |
| PC | 0.057268 |
| ABS | 0.092022 |
| Silicone | 0.033600 |
| LDPE | 0.017656 |
| Cardboard | 0.294476 |
| Other polymer forming | 0.141231 |
| Metal component forming | 0.064125 |
| Assembly and testing | 0.050000 |
| Packaging operation | 0.010000 |
| Additional inbound transport | 0.045863 |
| Manufacturing scrap treatment | 0.107019 |
| Unresolved background allowance | 0.331641 |
| **합계** | **4.758592** |

모든12개 BOM 재료에 수치를 부여했다. 이는 원 DB 공정 매칭100% 또는 환경영향 포괄률100%를 의미하지 않는다. 상위 물리 항목은 steel, PP, Nylon이다. 문헌의 동일 BC1 원재료·제조 약4 kg CO₂e/대는 비교 참고값이며 이 결과를 맞추기 위한 보정 목표로 사용하지 않았다. 원문4를 새 합계에 더하지 않았다.

BOM 합계·유한한 비음수 기여도·시나리오 순서·항목 합계를 검사한다. 기존 부분 계산의 독립 재실행 일치 기록은 `logs/validation.json`. 새 계산도 별도 폴더에서 재실행하고 동일 결과인지 확인했다. 공급망 closure, 실제 공정계측, 전체 LCIA 조화는 여전히 미검증이다. 공정별 비교·제품 환경성 주장에는 부적합하다.

## 8. Uncertainty and sensitivity

낮음 **3.680**, 중앙 **4.759**, 높음 **7.279 kg CO₂e/대**. 각 방향의 가정을 동시에 적용한 결정론적 시나리오다. 확률분포·상관관계·Monte Carlo는 사용하지 않아 평균·중앙값·P05/P95·90% 신뢰구간은 not calculated다. 한 번에 한 가정만 바꾼 민감도도 [summary](runs__estimate-v3__summary.json)의 one_at_a_time_sensitivity에 제공한다. 잔여 배경 불확실성이나 PC/황동 대체 오차가 이 범위 안에 든다는 보장은 없다.

## 9. Codex and human decisions

사용자가 원재료·제조 범위, 공개 자료 우선, 누락 항목을 근사·가정으로 보완하고 기록할 것을 요청했다. Codex가 대체 재료, 전력·수율·거리·보정 범위를 선택했으며 사용자/공장 실측값으로 표시하지 않았다. 사용자에게 개별 가정의 검증을 받았다는 주장도 하지 않는다. 모델은 GPT-6 기반 Codex, UI의 세부 버전·설정은 unknown. 사람 이름·이메일·제출코드는 공개 문서에 넣지 않았다. 실행일2026-10-08. 결정 로그는 이 README와 [가정 입력](inputs__estimate-assumptions.json), [이전 판단](logs__decisions.md).

## 10. Independent and revised runs

`runs/baseline`의 **3.126673** 부분 결과, steel90%만 변경한 `runs/scenario`, 문헌 확인 `runs/literature-reference`를 보존했다. 이번 `runs/estimate-v3`는 여러 미산정 항목을 보완한 별도 시나리오다. 중앙 결과 차이 **+1.631919 kg CO₂e/대 (+52.19%)**는 범위·가정 증가 때문이며 제품 성능 악화가 아니다. 기존 한 결정 변경 비교도 별도로 유지한다. 최초 로컬 run에는 Git commit/tag가 없었으며 공개 업로드 commit은 제출시 기록한다. 동료 결과를 보고 독립 값을 덮어쓰지 않았다.


## GitHub 파일 안내

브라우저 업로드본은 하위 폴더 경로를 `__`로 연결한 파일명으로 보관한다. estimate.py는 이 구조도 지원한다. 원래 폴더 구조 전체는 [전체 재현 패키지](kettle-public-study-v3.zip)에 있으며 원 USLCI 계산 재현시 이 ZIP을 압축 해제한 폴더에서 실행한다. 과거 로그·manifest 해시는 ZIP 내부 원본 기준이며 GitHub 표시용 링크 수정본의 해시가 아니다.
