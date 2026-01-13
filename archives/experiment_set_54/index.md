---
id: 54
name: "MFS ad-hoc RAG"
date: 2025-04-17T00:46:43.336604
description: ""
tags: []
---

# Experiment Set: MFS ad-hoc RAG (ID: 54)

MFS ad-hoc RAG (similar parametriation than expset 50)

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                                        |   answer_relevancy |   judge_exactness |   judge_notator |   judge_precision |   output_length |
|:-------------------------------------------------------------|-------------------:|------------------:|----------------:|------------------:|----------------:|
| gpt-oss-20b BraveSearch Mcp                                  |               0.81 |              0.1  |            6.56 |              0.64 |          596.31 |
| gpt-oss-20b Rag Service Public Mcp                           |               0.82 |              0.18 |            6.28 |              0.56 |          427.82 |
| Mistral-Small-3.1-24B-Instruct-2503-adhoc-rag                |             nan    |            nan    |          nan    |              0.49 |          363.08 |
| Llama-3.1-8B-Instruct-adhoc-rag                              |             nan    |            nan    |          nan    |              0.46 |          335.95 |
| Mistral 24b (albert-large) Rag Service Public Mcp            |               0.74 |              0.08 |            5.82 |              0.38 |          196.31 |
| llama3-instruct-guillaumetell-adhoc-rag                      |             nan    |            nan    |          nan    |              0.31 |          373.23 |
| Albert-Small MFS                                             |               0.75 |              0.1  |            5.41 |              0.28 |          354.74 |
| Assistant Service Public                                     |               0.81 |              0.15 |            5.9  |              0.28 |          141.97 |
| albert-large                                                 |               0.79 |              0.08 |            5.59 |              0.28 |          177.08 |
| assistant-service-public--recherche-approfondie- Pipeline V1 |               0.81 |              0.08 |            5.64 |              0.28 |          229.46 |
| Bobby                                                        |               0.7  |              0.05 |            5.03 |              0.26 |          219.77 |



## Set Overview

|   Id | Name                                                         | Dataset           | Model                                                        | Model params                               | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------------------------------------------------|:------------------|:-------------------------------------------------------------|:-------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1019 | MFS ad-hoc RAG__0                                            | MFS_questions_v01 | llama3-instruct-guillaumetell-adhoc-rag                      | {'temperature': 0.2, 'sys_prompt': '5901'} | finished | 2025-04-17T00:46:43.336604 |        39 |            39 |
| 1020 | MFS ad-hoc RAG__1                                            | MFS_questions_v01 | Llama-3.1-8B-Instruct-adhoc-rag                              | {'temperature': 0.2, 'sys_prompt': '5901'} | finished | 2025-04-17T00:46:43.336604 |        39 |            39 |
| 1021 | MFS ad-hoc RAG__2                                            | MFS_questions_v01 | Mistral-Small-3.1-24B-Instruct-2503-adhoc-rag                | {'temperature': 0.2, 'sys_prompt': '5901'} | finished | 2025-04-17T00:46:43.336604 |        39 |            39 |
| 1024 | Bobby                                                        | MFS_questions_v01 | Bobby                                                        | {}                                         | finished | 2025-04-17T12:38:48.356006 |        39 |            39 |
| 1242 | Assistant Service Public                                     | MFS_questions_v01 | Assistant Service Public                                     | {}                                         | finished | 2025-06-16T11:32:22.399949 |        39 |            39 |
| 1292 | Assistant Service Public — Pipeline V1                       | MFS_questions_v01 | albert-large                                                 | {}                                         | finished | 2025-08-07T15:40:00.390121 |        39 |            39 |
| 1328 | assistant-service-public--recherche-approfondie- Pipeline V1 | MFS_questions_v01 | assistant-service-public--recherche-approfondie- Pipeline V1 | {}                                         | finished | 2025-08-08T11:35:05.442196 |        39 |            39 |
| 1359 | Albert-Small MFS                                             | MFS_questions_v01 | Albert-Small MFS                                             | {}                                         | finished | 2025-09-09T15:03:22.528623 |        39 |            39 |
| 1360 | gpt-oss-20b BraveSearch Mcp                                  | MFS_questions_v01 | gpt-oss-20b BraveSearch Mcp                                  | {}                                         | finished | 2025-09-25T13:25:34.854244 |        39 |            39 |
| 1361 | gpt-oss-20b Rag Service Public Mcp                           | MFS_questions_v01 | gpt-oss-20b Rag Service Public Mcp                           | {}                                         | finished | 2025-09-26T11:07:34.008215 |        39 |            39 |
| 1440 | Mistral 24b (albert-large) Rag Service Public Mcp            | MFS_questions_v01 | Mistral 24b (albert-large) Rag Service Public Mcp            | {}                                         | finished | 2025-10-08T17:38:01.020954 |        39 |            39 |


## Details by Experiment

- [Experiment 1019](details/experiment_1019.md) - MFS ad-hoc RAG__0
- [Experiment 1020](details/experiment_1020.md) - MFS ad-hoc RAG__1
- [Experiment 1021](details/experiment_1021.md) - MFS ad-hoc RAG__2
- [Experiment 1024](details/experiment_1024.md) - Bobby
- [Experiment 1242](details/experiment_1242.md) - Assistant Service Public
- [Experiment 1292](details/experiment_1292.md) - Assistant Service Public — Pipeline V1
- [Experiment 1328](details/experiment_1328.md) - assistant-service-public--recherche-approfondie- Pipeline V1
- [Experiment 1359](details/experiment_1359.md) - Albert-Small MFS
- [Experiment 1360](details/experiment_1360.md) - gpt-oss-20b BraveSearch Mcp
- [Experiment 1361](details/experiment_1361.md) - gpt-oss-20b Rag Service Public Mcp
- [Experiment 1440](details/experiment_1440.md) - Mistral 24b (albert-large) Rag Service Public Mcp
