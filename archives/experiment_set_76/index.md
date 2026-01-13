---
id: 76
name: "Albert - RAG - (Assistant IA - QA) v4-10-25"
date: 2025-10-04T15:13:27.723003
description: ""
tags: []
---

# Experiment Set: Albert - RAG - (Assistant IA - QA) v4-10-25 (ID: 76)

Comparing Albert RAG Models on dataset Assistant IA - QA

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | contextual_relevancy   | generation_time   | judge_precision   | output_length   |
|:----------------------------------------------|:-----------------------|:------------------|:------------------|:----------------|
| albert-large-semantic-elastic-k10             | 0.57 ± 0.0             | 33.01 ± 0.74      | 0.72 ± 0.04       | 340.53 ± 3.17   |
| albert-large-semantic-elastic-k5              | 0.64 ± 0.0             | 24.05 ± 2.39      | 0.6 ± 0.09        | 305.29 ± 7.27   |
| albert-large-hybrid-elastic-k10               | 0.49 ± 0.02            | 31.31 ± 5.58      | 0.59 ± 0.04       | 328.63 ± 0.38   |
| albert-large-hybrid-elastic-k5                | 0.52 ± 0.01            | 32.06 ± 0.2       | 0.53 ± 0.02       | 294.29 ± 6.58   |
| mistralai/Mistral-Small-3.2-24B-Instruct-2506 | nan ± nan              | 34.4 ± 2.34       | 0.46 ± 0.04       | 324.81 ± 0.38   |



## Set Overview

|   Id | Name                                           | Dataset           | Model                                         | Model params                                                                                                    | Status   | Created at                 |   Num try |   Num success |
|-----:|:-----------------------------------------------|:------------------|:----------------------------------------------|:----------------------------------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1424 | Albert - RAG - (Assistant IA - QA) v4-10-25__0 | MFS_questions_v01 | albert-large-semantic-elastic-k5              | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 5}}  | finished | 2025-10-04T15:13:27.723003 |        39 |            39 |
| 1425 | Albert - RAG - (Assistant IA - QA) v4-10-25__1 | MFS_questions_v01 | albert-large-semantic-elastic-k5              | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 5}}  | finished | 2025-10-04T15:13:27.723003 |        39 |            39 |
| 1426 | Albert - RAG - (Assistant IA - QA) v4-10-25__2 | MFS_questions_v01 | albert-large-hybrid-elastic-k5                | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [784, 785], 'k': 5}}    | finished | 2025-10-04T15:13:27.723003 |        39 |            39 |
| 1427 | Albert - RAG - (Assistant IA - QA) v4-10-25__3 | MFS_questions_v01 | albert-large-hybrid-elastic-k5                | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [784, 785], 'k': 5}}    | finished | 2025-10-04T15:13:27.723003 |        39 |            39 |
| 1428 | Albert - RAG - (Assistant IA - QA) v4-10-25__4 | MFS_questions_v01 | albert-large-semantic-elastic-k10             | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-10-04T15:13:27.723003 |        39 |            39 |
| 1429 | Albert - RAG - (Assistant IA - QA) v4-10-25__5 | MFS_questions_v01 | albert-large-semantic-elastic-k10             | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-10-04T15:13:27.723003 |        39 |            39 |
| 1430 | Albert - RAG - (Assistant IA - QA) v4-10-25__6 | MFS_questions_v01 | albert-large-hybrid-elastic-k10               | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [784, 785], 'k': 10}}   | finished | 2025-10-04T15:13:27.723003 |        39 |            39 |
| 1431 | Albert - RAG - (Assistant IA - QA) v4-10-25__7 | MFS_questions_v01 | albert-large-hybrid-elastic-k10               | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [784, 785], 'k': 10}}   | finished | 2025-10-04T15:13:27.723003 |        39 |            39 |
| 1432 | Albert - RAG - (Assistant IA - QA) v4-10-25__8 | MFS_questions_v01 | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2}                                                                                            | finished | 2025-10-04T15:13:27.723003 |        39 |            39 |
| 1433 | Albert - RAG - (Assistant IA - QA) v4-10-25__9 | MFS_questions_v01 | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2}                                                                                            | finished | 2025-10-04T15:13:27.723003 |        39 |            39 |


## Details by Experiment

- [Experiment 1424](details/experiment_1424.md) - Albert - RAG - (Assistant IA - QA) v4-10-25__0
- [Experiment 1425](details/experiment_1425.md) - Albert - RAG - (Assistant IA - QA) v4-10-25__1
- [Experiment 1426](details/experiment_1426.md) - Albert - RAG - (Assistant IA - QA) v4-10-25__2
- [Experiment 1427](details/experiment_1427.md) - Albert - RAG - (Assistant IA - QA) v4-10-25__3
- [Experiment 1428](details/experiment_1428.md) - Albert - RAG - (Assistant IA - QA) v4-10-25__4
- [Experiment 1429](details/experiment_1429.md) - Albert - RAG - (Assistant IA - QA) v4-10-25__5
- [Experiment 1430](details/experiment_1430.md) - Albert - RAG - (Assistant IA - QA) v4-10-25__6
- [Experiment 1431](details/experiment_1431.md) - Albert - RAG - (Assistant IA - QA) v4-10-25__7
- [Experiment 1432](details/experiment_1432.md) - Albert - RAG - (Assistant IA - QA) v4-10-25__8
- [Experiment 1433](details/experiment_1433.md) - Albert - RAG - (Assistant IA - QA) v4-10-25__9
