---
id: 75
name: "Albert - RAG - (MFS_questions_v01) v4-10-25"
date: 2025-10-04T15:13:26.909098
description: ""
tags: []
---

# Experiment Set: Albert - RAG - (MFS_questions_v01) v4-10-25 (ID: 75)

Comparing Albert RAG Models on dataset MFS_questions_v01

**Finished**: 97%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | contextual_relevancy   | generation_time   | judge_precision   | output_length   |
|:----------------------------------------------|:-----------------------|:------------------|:------------------|:----------------|
| albert-large-semantic-elastic-k10             | 0.56 ± 0.01            | 34.23 ± 3.99      | 0.64 ± 0.0        | 337.47 ± 8.03   |
| albert-large-semantic-elastic-k5              | 0.65 ± 0.02            | 34.85 ± 2.72      | 0.64 ± 0.04       | 311.76 ± 8.32   |
| albert-large-hybrid-elastic-k10               | 0.49 ± 0.01            | 23.15 ± 0.15      | 0.56 ± 0.04       | 333.06 ± 5.17   |
| albert-large-hybrid-elastic-k5                | 0.5 ± 0.01             | 28.28 ± 6.96      | 0.55 ± 0.02       | 301.29 ± 0.31   |
| mistralai/Mistral-Small-3.2-24B-Instruct-2506 | nan ± nan              | 30.15 ± 1.09      | 0.44 ± 0.04       | 320.09 ± 6.18   |



## Set Overview

|   Id | Name                                           | Dataset           | Model                                         | Model params                                                                                                    | Status          | Created at                 |   Num try |   Num success |
|-----:|:-----------------------------------------------|:------------------|:----------------------------------------------|:----------------------------------------------------------------------------------------------------------------|:----------------|:---------------------------|----------:|--------------:|
| 1414 | Albert - RAG - (MFS_questions_v01) v4-10-25__0 | MFS_questions_v01 | albert-large-semantic-elastic-k5              | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 5}}  | finished        | 2025-10-04T15:13:26.909098 |        39 |            39 |
| 1415 | Albert - RAG - (MFS_questions_v01) v4-10-25__1 | MFS_questions_v01 | albert-large-semantic-elastic-k5              | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 5}}  | finished        | 2025-10-04T15:13:26.909098 |        39 |            39 |
| 1416 | Albert - RAG - (MFS_questions_v01) v4-10-25__2 | MFS_questions_v01 | albert-large-hybrid-elastic-k5                | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [784, 785], 'k': 5}}    | finished        | 2025-10-04T15:13:26.909098 |        39 |            39 |
| 1417 | Albert - RAG - (MFS_questions_v01) v4-10-25__3 | MFS_questions_v01 | albert-large-hybrid-elastic-k5                | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [784, 785], 'k': 5}}    | finished        | 2025-10-04T15:13:26.909098 |        39 |            39 |
| 1418 | Albert - RAG - (MFS_questions_v01) v4-10-25__4 | MFS_questions_v01 | albert-large-semantic-elastic-k10             | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished        | 2025-10-04T15:13:26.909098 |        39 |            39 |
| 1419 | Albert - RAG - (MFS_questions_v01) v4-10-25__5 | MFS_questions_v01 | albert-large-semantic-elastic-k10             | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished        | 2025-10-04T15:13:26.909098 |        39 |            39 |
| 1420 | Albert - RAG - (MFS_questions_v01) v4-10-25__6 | MFS_questions_v01 | albert-large-hybrid-elastic-k10               | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [784, 785], 'k': 10}}   | finished        | 2025-10-04T15:13:26.909098 |        39 |            39 |
| 1421 | Albert - RAG - (MFS_questions_v01) v4-10-25__7 | MFS_questions_v01 | albert-large-hybrid-elastic-k10               | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [784, 785], 'k': 10}}   | finished        | 2025-10-04T15:13:26.909098 |        39 |            39 |
| 1422 | Albert - RAG - (MFS_questions_v01) v4-10-25__8 | MFS_questions_v01 | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2}                                                                                            | finished        | 2025-10-04T15:13:26.909098 |        39 |            39 |
| 1423 | Albert - RAG - (MFS_questions_v01) v4-10-25__9 | MFS_questions_v01 | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2}                                                                                            | running_metrics | 2025-10-04T15:13:26.909098 |        39 |            39 |


## Details by Experiment

- [Experiment 1414](details/experiment_1414.md) - Albert - RAG - (MFS_questions_v01) v4-10-25__0
- [Experiment 1415](details/experiment_1415.md) - Albert - RAG - (MFS_questions_v01) v4-10-25__1
- [Experiment 1416](details/experiment_1416.md) - Albert - RAG - (MFS_questions_v01) v4-10-25__2
- [Experiment 1417](details/experiment_1417.md) - Albert - RAG - (MFS_questions_v01) v4-10-25__3
- [Experiment 1418](details/experiment_1418.md) - Albert - RAG - (MFS_questions_v01) v4-10-25__4
- [Experiment 1419](details/experiment_1419.md) - Albert - RAG - (MFS_questions_v01) v4-10-25__5
- [Experiment 1420](details/experiment_1420.md) - Albert - RAG - (MFS_questions_v01) v4-10-25__6
- [Experiment 1421](details/experiment_1421.md) - Albert - RAG - (MFS_questions_v01) v4-10-25__7
- [Experiment 1422](details/experiment_1422.md) - Albert - RAG - (MFS_questions_v01) v4-10-25__8
- [Experiment 1423](details/experiment_1423.md) - Albert - RAG - (MFS_questions_v01) v4-10-25__9
