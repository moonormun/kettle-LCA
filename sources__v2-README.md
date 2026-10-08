# BC1 kettle: 공개 데이터 기반 원재료·제조 LCA 검토

**상태: 불완전 screening 계산. 전체 kettle GWP100은 미산정이다.** 데이터 검색, 공정 매칭, 부분 공급망 계산과 민감도 분석을 실행했다. 아래 4개 기체 진단 합계는 전체 제품 탄소발자국이나 하한값이 아니다. 빠진 재료·공정·공급자·기체를 0으로 확정하지 않았다.

## 1. Study identity and purpose

- 제목: BC1 1 L kettle의 원재료 생산·제조 영향과 공개 DB 적합성 검토.
- 공개 작업 별칭: kettle-public-study — 이 작업의 로컬 별칭이며 학생 신원은 아니다.
- 날짜: 2026-10-08, Asia/Seoul. 독립 run: `public-screening-20261008-baseline`. 수정 run: `public-screening-20261008-steel-yield-90`.
- 목표: 포장된 kettle 1대의 공장 출하까지 영향을 조사하고 주요 기여원과 모델 선택에 따른 변화를 확인한다.
- 저장소 URL: not applicable — 이 작업에서는 공개 저장소를 생성·게시하지 않았다. Git tag/commit SHA: not applicable — 로컬 산출물이며 커밋하지 않았다. 학생/그룹 공개 별칭: unknown — 사용자가 제공하지 않았다.
- 독립 결과는 [baseline](runs__baseline__summary.json), [수정 결과](runs__scenario__contributions.json)에 분리했다. 파일별 해시는 [run manifest](manifests__run-manifest.json)에 기록한다. 계산 코드는 기존 baseline을 덮어쓰지 않는다.

## 2. Product, declared unit and system boundary

- 선언단위: 제조·포장된 BC1 1 L 플라스틱 전기 kettle 1대, 공장 출하 시점. 대표 base case이며 특정 판매 제품이 아니다.
- BOM: 본체 723 g, 포장 137.8 g, 합계 860.8 g. [로컬 BOM](inputs__bom.csv).
- 출처: [교실 사이트 BOM](https://tiangong-lca-decision-lab.ecodino73.chatgpt.site/#bom), 확인일 2026-10-08. 사이트의 원출처는 EU Electric Kettles preparatory study (2020), Task 4, Tables 4-3, 4-4, 4-8, 인쇄 pp.26,27,30이다. 추가 조사에서 원문 PDF를 확보하고 Tables 4-3/4-4/4-8 및 5-7을 확인했다. 확보한 최종 보고서 표지 연도는 May 2021이다(사이트의 2020 표기와 구분). [원문](sources__kettle-study-original.pdf). CSV 직접 요청은 HTTP 403이므로 화면에서 전사했다.
- 목표 경계 포함: 자원 채취·정련, 재료 생산, 부품 제조, 조립·검사, 포장, 공장까지 운송, 제조 폐기물 처리. 출하 후 유통, 사용 및 제품 폐기는 제외한다. 건물·설비는 전경에서 제외하되 배경 데이터 내 포함 항목을 임의 제거하지 않는다.
- 실제 구현: 매칭된 6개 재료의 공개 USLCI 공급망 + PP 사출성형 + 골판지 가공. 나머지 재료와 부품 성형·조립·추가 운송은 미해결이다. 따라서 목표 경계 전체가 구현되었다고 주장하지 않는다.
- 지역: 북미/미국 배경 자료를 사용하는 가상 screening. 실제 kettle 제조 국가는 unknown. 기준 연도는 실제 제품 정보가 없어 unknown; 각 배경 데이터 연도는 별도 기록했다. 2026은 조회·연구 연도이지 모든 데이터의 생산 연도가 아니다.
- 작은 부품을 질량 기준으로 제외하지 않는다. 재료 미매칭은 cut-off 정책이 아니라 데이터 공백이다. 제품 사용·폐기 확장 계산은 not applicable.

## 3. Foreground inventory and quantitative assumptions

[전체 BOM](inputs__bom.csv), [매칭표](mappings__material-mapping.csv), [정확한 공정 수정](inputs__overrides.json), [단위 변환](mappings__unit-conversions.json)을 참조한다.

| 항목 | 값 | 단위 | 근거와 상태 |
|---|---:|---|---|
| 완제품·포장 | 860.8 | g/대 | 사이트 BOM, sourced |
| PP 완성 부품 | 0.35025 | kg/대 | 사이트 BOM, sourced |
| PP 사출 수지 투입 | 0.3621585 | kg/대 | USLCI의 1.034 kg/kg 부품 × BOM, proxy 데이터에 sourced |
| PP 사출 colorant | 0.00679485 | kg/대 | USLCI의 0.0194 kg/kg 부품, 실제 kettle 배합은 unknown |
| PP 사출 전력 | 2.257011 | MJ/대 | USLCI의 6.444 MJ/kg 부품; 0.6269475 kWh/대 |
| PP 사출 scrap | 0.01576125 | kg/대 | USLCI의 0.045 kg/kg 부품; 처리 공급자는 미연결 |
| PP 부품 운송용 골판지 | 원래 0.035025, 모델에서 제외 | kg/대 | 개별 kettle 포장 BOM을 별도 모델링하는 경계 선택, assumed |
| 스테인리스 기준 수율 | 1.0 | kg 완제품/kg 구매량 | 보수적 무손실 기준 가정; 실제 수율 아님 |
| 스테인리스 수정 수율 | 0.9 | kg 완제품/kg 구매량 | 민감도용 assumed, 추가 스크랩 처리 미해결 |
| 기타 매칭 수지의 구매/완제품 비율 | 1.0 | kg/kg | 성형 손실 자료 부재에 따른 screening 가정 |
| 조립·검사 전력 | unknown | kWh/대 | 자료 부재; 0으로 입력한 완전 공정이 아님 |
| 추가 부품 제조·운송·폐기물 처리 | unknown | 공정별 단위 | 미산정 |
| 가격 | not applicable | — | 금액 기반 proxy 사용하지 않음 |

구매량 = 완제품 질량/수율. PP는 통합 사출 데이터의 수지 투입 계수를 사용하므로 일반 수율을 중복 적용하지 않는다. g→kg는 1/1000, kWh→MJ는 3.6, l→m³는 0.001. 질량/부피 등 서로 다른 물성 간 변환은 USLCI `flowProperties.conversionFactor`가 있는 경우만 적용한다. 예를 들어 천연가스 1 kg=1.357 m³라는 해당 흐름의 계수를 사용하며 임의 밀도를 만들지 않는다.

PP 자료에는 수지·전력·열·운송이 이미 포함되어 있어 별도로 다시 추가하지 않는다. 스테인리스 coil의 압연도 추가하지 않는다. 사출 배합은 수지+colorant 1.0534 kg, 부품+scrap 1.045 kg으로 0.0084 kg/kg 차이가 있다. 평균 공정의 제품별 정확한 질량수지는 실패로 기록하며 임의 보정하지 않는다.

## 4. Background data and matching decisions

- [USLCI 공개 다운로드](https://github.com/FLCAC-admin/uslci-content/blob/dev/docs/release_info/release-downloads.md)의 **1.2025-06.0 JSON-LD**를 사용했다. 1.2026-09.0을 사용한 것으로 표기하지 않는다. 최신 웹 데이터 화면은 본 세션에서 정상적으로 데이터 목록을 표시하지 않았다.
- 전력: USLCI와 연결되는 **U.S. electricity baseline 1.2025-06.0** 라이브러리. JSON metadata에 실배출이 생략되어 있으므로 `B.npz @ INV.npy`를 사용했다. `A @ INV = I`도 검증했다.
- TianGong: 로그인 없는 공개 [과거 저장소](https://github.com/tiangong-lca/data)를 검색했다. archive의 `release.json`은 0.2.0이다. 저장소는 2026-06-21부터 과거 스냅샷으로 보존되어 최신 플랫폼 데이터와 다르다. 최신 CLI 0.1.27을 확보하고 인증 상태를 확인했으나 usable OAuth session이 없었다. 사용자 지시에 따라 로그인 없이 공개 자료를 사용했다.
- TianGong 생산 공정은 현재 baseline 공급자로 채택하지 않았다. TianGong에서 배포한 과거 Climate change LCIA 레코드의 4개 기체 계수를 진단 계산에 사용했다. 그러므로 '양쪽 DB 재료 데이터로 완성한 kettle LCA'라고 주장하지 않는다.
- 검색 대상: USLCI 962개, TianGong 4132개 공정. 기록된 영어 공정명 검색 후보는 152건이며 일부는 중복 재료 검색이다. 추가로 POM/PC/PA/silicone의 영어·중국어 동의어를 확인했으나 적합한 engineering resin 공급자를 확정하지 못했다. 검색은 완전한 다국어 의미 검색이 아니다.

개별 투입물의 이름, UUID, 버전, 지역·연도, 기준 흐름·양·단위, URL, 조회일·해시는 [material mapping](mappings__material-mapping.csv)에 있다. 후보·검색어·탈락 근거는 [candidate search](mappings__candidate-search.csv), 공급자 계수는 [provider links](mappings__provider-links.csv), 배경 공정 버전·해시는 [data manifest](manifests__data-manifest.json)에 있다.

주요 선택: 304 coil은 등급 가정, PP는 통합 사출성형, PVC/ABS/LDPE는 수지까지만, cardboard는 미국 평균 corrugated product proxy이다. 구리의 USLCI→USEEIO bridge에는 가격·산업·기준연도 메타데이터가 있다(추가 확인으로 정정). 그러나 외부 USEEIO 공급자가 연결되지 않아 직접 kg당 배출계수로 사용하지 않았다. Nylon 섬유나 polycarbonate를 쓰는 여행가방, silicone monomer를 해당 재료 생산으로 대신하지 않았다. TianGong 구리 후보 `2137ed25-4ae3-491f-af02-e8a33d76c380`는 4개 교환만 있고 N₂O amount 135000/reference copper 1000이라는 값이 있어 원문·단위 확인 없이 채택하지 않았다. 이는 오류 확정이 아닌 검증 보류 사유다.

원본 DB 전체를 산출물에 재배포하지 않았다. 접근 가능한 배경 공정 중에도 copyright flag가 있는 레코드가 있으므로 manifest 식별자·해시 및 공식 조회 절차를 제공한다. 공개 접근과 재배포 허용은 구분한다.

## 5. Calculation and impact-assessment methods

[calculate.py](calculate.py)는 공개 데이터로 구성한 부분 공급망을 실제 계산한다. 활동량은 각 공정의 기준 산출물 물량이다. 기준 산출량으로 교환을 정규화하여 `A s = f`를 NumPy `linalg.solve`로 풀고 기본흐름을 합산한다. 전력 라이브러리는 공식 sparse 배열과 protobuf index를 읽어 공급자별 누적 기본흐름을 적용한다. 기본 공급자의 기준 흐름 ID를 검증하며, 공급자 미지정일 때 동일 ID의 유일한 기준 산출 공정만 자동 연결한다. 다중 후보, 공급자 누락, 흐름·단위 불일치는 미연결로 남긴다.

진단 LCIA: [TianGong 배포 Climate change 레코드](https://github.com/tiangong-lca/data/blob/main/tiangong_lca_data/lciamethods/6209b35f-9447-40b5-b68c-a1099e3674a0.xml), UUID `6209b35f-9447-40b5-b68c-a1099e3674a0`, dataset version 01.00.000, GWP100, 100년. 로컬 원본은 [LCIA XML](sources__6209b35f-9447-40b5-b68c-a1099e3674a0.xml). 계수는 CO₂ fossil=1, CH₄ fossil=29.8, N₂O=273, SF₆=25200 kg CO₂-eq/kg이다. 파일에 IPCC 2021/변환 원출처 IPCC 2013이 함께 있어 완전히 검증된 AR6 구현으로 명명하지 않는다.

USLCI의 generic CO₂와 CH₄는 진단에서 fossil로 가정했다. 생물기원 CO₂ 분리가 안 되어 종이·바이오에너지 등에 왜곡 가능성이 있다. 네 기체 이외의 모든 흐름은 [미특성화 목록](runs__baseline__uncharacterized-flows.csv)에 남겼다. 이는 공통 방법을 완전히 적용한 full LCIA가 아니다. [특성화 매핑](mappings__characterization.csv)은 물질명·구획 일반화와 가정을 명시한다.

Attributional screening으로 원본 배경 할당을 유지하고 추가 부산물 대체 크레딧은 부여하지 않았다. 재생원료 함량은 원본 steel 자료를 따른다. 전경 스크랩은 별도 신재 대체 크레딧을 주지 않았으며 처리 미연결 상태를 기록했다. 폐기물·부산물 output은 공급망 공백 목록에 남긴다. 원본 배경 시스템 모델의 차이와 집계/단위공정 혼재는 제한사항이다.

## 6. How to reproduce the analysis

환경: Windows, PowerShell; Python 3.12.14, NumPy 2.3.5. 추가 solver 패키지는 없다. [requirements.txt](requirements.txt)와 [fetch_data.py](fetch_data.py)를 제공한다.

저장소/폴더 지도: `inputs/` BOM·override, `mappings/` 재료·후보·공급자·단위·LCIA, `manifests/` 데이터·run hash, `sources/` LCIA 원본, `runs/baseline/` 독립 부분 계산, `runs/scenario/` 수정 부분 계산, `logs/` 검색·결정·QA. README와 CSV는 일반 편집기·스프레드시트로 열 수 있다.

이 폴더를 작업 디렉터리로 두고 Python 3.12에서 실행한다:

```powershell
python -m pip install -r requirements.txt
python fetch_data.py
python calculate.py --uslci cache/uslci-2025-06.zip --electricity cache/electricity-library.zip --output-dir reproduced-run
```

기대 출력: `reproduced-run/runs/baseline/summary.json`, 기여도·기본흐름·미연결 목록 및 scenario 기여도. 공식 다운로드가 변경되면 해시 검증에서 중단한다. 기존 독립 baseline이 있는 output-dir은 거부한다. 이후 실행은 새 폴더를 사용한다.

재현 검증 명령은 `python validate.py --reproduced-root reproduced-run`이다. 실제로 별도 폴더에서 다시 계산했으며 기여도·기본흐름·미연결 목록·변환 기록이 동일했다. [검증 실행 기록](logs__validation.json)을 참조한다.

실제 실행에서는 번들 Python 경로 `C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`와 `--uslci ../work/uslci-2025-06.zip --electricity ../work/electricity-library.zip`을 사용했다. 입력 archive는 outputs 외부의 작업 cache에 보관했다. [data manifest](manifests__data-manifest.json)의 다운로드 URL과 hash로 재조회할 수 있다.

현재 공개 archive 경로에는 계정/API 키가 필요 없다. 최신 TianGong은 사용자의 브라우저 OAuth 로그인이 필요하며 `TIANGONG_LCA_SESSION_FILE`은 비공개 위치를 선택하는 변수다. 최신 LCA Commons API 사용 시 `DATA_GOV_API_KEY`를 사용자가 로컬 환경에 설정하는 방식을 향후 구현할 수 있으나 이 코드에서는 API를 호출하지 않는다. demo key로 자동 다운로드하지 않았다. 비밀번호·토큰·키·.env는 제공·저장소 포함하지 않는다. 난수 seed: not applicable — 결정론적 계산. 필요한 수동 단계는 잔여 재료·공정·공급자 검토와 carbon origin/LCIA 매핑이다.

최신 TianGong 플랫폼의 공개 시작 URL도 직접 확인했으며 `/user/login`으로 이동했다. 사용자 선택에 따라 로그인을 진행하지 않았다.

## 7. Results, checks and interpretation

추가 조사 결과는 [최종 결과 보고서](RESULTS.md)에 정리했다. 원출처 Table 5-7의 동일 BC1 원재료·제조 GWP100은 약 4 kg CO₂e/대(원문 정수 반올림)이다. 이는 EcoReport 문헌 참고값이며 아래 USLCI/TianGong 부분 진단값과 별도이다. 부록 E에서 실리콘·나일론·POM 계수를 확인했으며 [별도 계산](runs__literature-reference__result.json)에 보존했다. 원래 baseline/scenario 수치는 변경하지 않았다.


**전체 kettle GWP100: not calculated.** 아래 수치는 generic CO₂/CH₄를 fossil로 가정한 네 기체의 **미완성 부분 공급망 진단값**이다. 전체 제품 값이나 하한값으로 쓰지 않는다.

| 재료/부품 | BOM 질량(g) | 부분 진단 기여도(kg CO₂-eq/대) |
|---|---:|---:|
| Stainless steel | 186.00 | 1.463004 |
| Brass | 20.25 | 미산정 |
| Copper | 15.00 | 미산정 |
| PP | 350.25 | 1.147258 |
| PVC | 43.50 | 0.132465 |
| Nylon | 49.50 | 미산정 |
| POM | 9.75 | 미산정 |
| PC | 6.75 | 미산정 |
| ABS | 30.00 | 0.087421 |
| Silicone | 12.00 | 미산정 |
| LDPE | 6.30 | 0.016773 |
| Cardboard | 131.50 | 0.279752 |
| 매칭 항목 부분 합계 | 747.55 | 3.126673 |

부분 계산 내 상위 3개는 스테인리스, PP 사출 부품, 골판지다. 전체 제품의 상위 기여원으로 확정할 수 없다. 매칭 질량은 86.84%; 환경영향의 86.84%를 포괄한다는 뜻이 아니다. 미매칭 질량은 113.25 g이며 해당 영향은 unknown이다.

실행 연결: USLCI 194개 공정 및 전력 라이브러리 6개 공급자. 미연결 목록은 1652개 material-root별 교환 행이며 동일 배경 교환이 재료별로 반복되고 폐기물/부산물도 포함된다. 미특성화 비영(非零) material-flow 행은 12844개다. 이는 모두 GWP 관련 기체라는 뜻은 아니다.

[결과 summary](runs__baseline__summary.json), [전체 부분 기여도](runs__baseline__contributions.json), [기본흐름 인벤토리](runs__baseline__elementary-inventory.csv), [미연결 교환](runs__baseline__unresolved-exchanges.csv), [검증 보고서](runs__baseline__checks.json).

통과: BOM 산술, 진단 기여도 합계, 선형계 잔차(8.89e-17), 전력 inverse 잔차(3.55e-15), 명시된 중복 계산 방지. 실패/미완료: 전체 재료·제조 범위, 공급망 closure, 제품별 PP 물질수지, 전체 LCIA·생물기원 구분. 결과가 작은 이유를 효율성으로 해석하거나 DB 간 우열을 판단할 수 없다.

## 8. Uncertainty and sensitivity

확률 불확실성: not calculated — 근거 있는 수율·에너지 분포와 상관관계가 없다. 평균·중앙값·P05/P95·draw count·seed·수렴은 not applicable. 근거 없이 통계 구간을 만들지 않았다.

한 결정 변경: 스테인리스 수율 100%→90%. 예상은 구매량·관련 부분 영향 증가다. 구매량은 0.186→0.2066667 kg/대; 추가 손실 0.0206667 kg/대의 처리 영향은 아직 미산정이다. 실제 부분 진단 합계는 3.126673→3.289229 kg CO₂-eq/대, 차이 +0.162556, +5.199%. 전체 kettle의 변화율이 아니다.

공급자/방법 시나리오 비교는 데이터 공백으로 미완료; 반복 AI run 변동은 측정하지 않았다. 파라미터 민감도 결과와 DB/방법 차이·확률 불확실성을 구분한다.

## 9. Codex and human decisions

- 사용자 결정: 원재료·제조까지, TianGong/USLCI 사용, 10개 README 요구사항 반영, 실제 자료로 채우기, 인증 대신 공개 데이터 우선 사용.
- Codex 결정: 포장 포함 공장 출하 선언단위, 공개 과거 snapshot 선택, 재료·공정 proxy 선정·거절, component shipping corrugate 경계 조정, 원본 변환계수 사용, 라이브러리 행렬 계산, 네 기체 diagnostic 제한, 미연결을 0으로 확정하지 않기.
- 독립 확인: 질량 산술, reference-flow ID 및 단위, 라이브러리 inverse, 기여도 합계 및 재현 실행. 사람의 최종 매칭 승인·수동 수정: not applicable — 이 turn 중 개별 승인이나 수정은 없었다.
- 모델: 시스템에서 GPT-6 기반 Codex로 알려져 있다. 사용자 화면의 정확한 모델 선택명·버전, 세부 설정은 unknown. 버전 번호를 추정하지 않는다. 실행일 2026-10-08.
- 주요 프롬프트 및 선택은 [결정 로그](logs__decisions.md). 도움: 공식 데이터·문서와 Codex 코드 작성; 추가 사람 또는 subagent의 도움 없음.

## 10. Independent and revised runs

독립 결과는 `runs/baseline/`, 수정 결과는 `runs/scenario/`에 보존했다. 동일 폴더 덮어쓰기를 차단한다. 커밋/tag는 not applicable — 공개 저장소를 만들거나 제출하지 않았다. 동료 결과와 비교하지 않았다.

수정 선택은 수율 1.0→0.9 하나이며 이전 독립 run ID, 결과·차이·예상 효과를 [summary](runs__baseline__summary.json)에 담았다. 이는 대체 수율 가정이며 오류 수정이 아니다. 개발 중 단위 변환·solver 수정은 첫 독립 결과 확정 전 오류 수정으로 [결정 로그](logs__decisions.md)에 기록했다.

최종 full LCA를 완료하려면 미매칭 6개 재료의 적합 공급자, 실제 부품 가공·조립·검사·운송·스크랩 처리, 남은 공급자 closure, carbon origin과 전체 LCIA mapping을 해결해야 한다. 현재 공개자료 검토 결과만으로 이 항목을 임의 숫자로 채울 수 없다.
