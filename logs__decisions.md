# 공개 데이터 실행 결정 로그

날짜: 2026-10-08 (Asia/Seoul).

1. 사용자: 교실 사이트 BOM으로 원재료·제조 LCA 계획 수립. README 10개 항목 반영 후 실제로 채워 달라고 요청.
2. TianGong CLI 0.1.27 npm 배포본을 확보했다. 패키지 관리자 realpath 오류로 작업 폴더에서 tarball integrity를 검증하여 로컬 추출했다. 인증 status는 login-required. 사용자에게 로그인 참여/공개 자료 선택을 물었고 공개 접근 가능한 자료 우선 진행 답변을 받았다.
3. USLCI 최신 웹 화면에 process 목록이 표시되지 않았다. 공식 다운로드 목록의 1.2025-06.0 JSON-LD를 선택하고 해시 고정. 최신 2026-09 릴리스와 구분.
4. TianGong 공개 과거 archive 0.2.0 확보, 4132개 XML process-name 검색. 이름 유사성만으로 섬유·여행가방·silicone monomer를 resin에 매칭하지 않았다. 구리 후보의 극단적 N2O 교환과 부족한 upstream은 원본 확인 대상으로 보류.
5. USLCI 6개 재료/부품을 선택. PP integrated molding 안의 resin·energy를 중복 추가하지 않음. shipping corrugate 제거는 원자료의 특정 제품에 맞춰 조정하라는 설명을 참고한 모델링 선택이며 실제 공급망의 포장 부재라는 증거는 아니다.
6. 전력 library의 JSON metadata는 배출 누락이 아니라 matrix storage. protobuf index 및 공식 B/INV를 해석하고 A@INV=I 검증.
7. 개발 오류 수정: 공정 reference amount와 활동량을 혼동하지 않도록 활동량을 기준 산출물 물량으로 통일. 초기 코드가 m3/kg 링크에서 중단했고 원자료 flow property factor로 변환 구현. 최종 독립 run 전 수정이며 이후 결과를 independent로 확정.
8. CF archive의 IPCC2021/2013 metadata 혼재를 기록. 네 기체만 diagnostic으로 적용하고 generic CO2/CH4 fossil 가정 명시. 전체 footprint는 null로 보존.
9. Steel yield 100%→90% 하나의 민감도 run 실행. 추가 스크랩 처리 미해결, 확률 불확실성 미산정.
10. 비공개 인증정보나 원본 DB 전체를 결과에 포함하지 않았다. copyright flag가 있는 원자료의 재배포는 수행하지 않고 공식 조회 링크와 hashes 제공.
