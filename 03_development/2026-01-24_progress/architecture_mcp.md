**변경 사유**

**현재 프롬프트 생성, 정규화, 검증 로직 등이 xFrame5, Spring 등 특정 기술 별로 소스코드에 구현되어 있음**

**문제: 향후 지원 범위가 확대됨에 따라 기존 코드 수정 후 빌드하여 배포해야 함**

**해결방안: MCP를 이용하여 각 기술 별 특화된 부분은 별도 MCP Server로 구현하여 설정을 통해 통합**

**Updated Architecture - 새 버전으로 분기하여 개발 착수**

  **After** 

  - MCP = Capabilities + Framework-specific rules                                                                     

  - Coder = Orchestration + Generic passes only                                                                       

                    CODER (ORCHESTRATION)

  Generic passes (in-process):

  - Output parsing

  - Symbol linking

  - Graph validation

  - Minimalism   

  Framework-specific (from MCP):

  - Generation (generate_xml, generate_js)

  - Canonicalization rules

  - API allowlist

  - Schema validation

  **The principle:**                                                                                                      

  - **Coder** owns **what** happens (orchestration, enforcement)                                                              

  - **MCP Servers** provide **how** it happens for each framework (rules)                                                                                                                                                                        

This achieves true framework decoupling - adding Vue or React requires only creating a new MCP server without changing coder's core logic.