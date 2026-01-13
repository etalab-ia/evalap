---
id: 18
name: "mfs_RAG_metrics_v3"
date: 2025-03-10T19:10:51.722408
description: ""
tags: []
---

# Experiment Set: mfs_RAG_metrics_v3 (ID: 18)

Evaluation of baseline models with RAG metrics (retriever_context).

**Finished**: 80%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                     | contextual_precision   | contextual_recall   | contextual_relevancy   | ragas       |
|:------------------------------------------|:-----------------------|:--------------------|:-----------------------|:------------|
| AgentPublic/llama3-instruct-guillaumetell | 0.56 ± 0.01            | 0.71 ± 0.01         | 0.41 ± 0.01            | 0.62 ± 0.04 |
| meta-llama/Llama-3.1-8B-Instruct          | 0.55 ± 0.03            | 0.74 ± 0.03         | 0.41 ± 0.01            | 0.42 ± 0.05 |
| google/gemma-2-9b-it                      | 0.51 ± 0.03            | 0.73 ± 0.03         | 0.42 ± 0.02            | 0.5 ± 0.05  |
| meta-llama/Llama-3.2-3B-Instruct          | nan ± nan              | nan ± nan           | nan ± nan              | nan ± nan   |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                     |   contextual_precision_support |   contextual_recall_support |   contextual_relevancy_support | ragas_support   |
|:------------------------------------------|-------------------------------:|----------------------------:|-------------------------------:|:----------------|
| AgentPublic/llama3-instruct-guillaumetell |                             39 |                          39 |                             39 | 20.67 ± 3.51    |
| meta-llama/Llama-3.1-8B-Instruct          |                             39 |                          39 |                             39 | 18.67 ± 5.01    |
| google/gemma-2-9b-it                      |                             39 |                          39 |                             39 | 18.67 ± 5.13    |
| meta-llama/Llama-3.2-3B-Instruct          |                            nan |                         nan |                            nan | nan ± nan       |



## Set Overview

|   Id | Name                   | Dataset           | Model                                     | Model params                                             | Status   | Created at                 |   Num try |   Num success |
|-----:|:-----------------------|:------------------|:------------------------------------------|:---------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  374 | mfs_RAG_metrics_v3__0  | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct          | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |             0 |
|  375 | mfs_RAG_metrics_v3__1  | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct          | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |             0 |
|  376 | mfs_RAG_metrics_v3__2  | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct          | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |             0 |
|  377 | mfs_RAG_metrics_v3__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct          | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |            39 |
|  378 | mfs_RAG_metrics_v3__4  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct          | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |            39 |
|  379 | mfs_RAG_metrics_v3__5  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct          | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |            39 |
|  380 | mfs_RAG_metrics_v3__6  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct          | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |            39 |
|  381 | mfs_RAG_metrics_v3__7  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct          | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |            39 |
|  382 | mfs_RAG_metrics_v3__8  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct          | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |            39 |
|  383 | mfs_RAG_metrics_v3__9  | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |            39 |
|  384 | mfs_RAG_metrics_v3__10 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |            39 |
|  385 | mfs_RAG_metrics_v3__11 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-10T19:10:51.722408 |        39 |            39 |
|  386 | mfs_RAG_metrics_v3__12 | MFS_questions_v01 | google/gemma-2-9b-it                      | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-11T09:30:48.747309 |        39 |            39 |
|  387 | mfs_RAG_metrics_v3__14 | MFS_questions_v01 | google/gemma-2-9b-it                      | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-11T09:30:48.975434 |        39 |            39 |
|  388 | mfs_RAG_metrics_v3__16 | MFS_questions_v01 | google/gemma-2-9b-it                      | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-11T09:30:49.329832 |        39 |            39 |


## Details by Experiment

- [Experiment 374](details/experiment_374.md) - mfs_RAG_metrics_v3__0
- [Experiment 375](details/experiment_375.md) - mfs_RAG_metrics_v3__1
- [Experiment 376](details/experiment_376.md) - mfs_RAG_metrics_v3__2
- [Experiment 377](details/experiment_377.md) - mfs_RAG_metrics_v3__3
- [Experiment 378](details/experiment_378.md) - mfs_RAG_metrics_v3__4
- [Experiment 379](details/experiment_379.md) - mfs_RAG_metrics_v3__5
- [Experiment 380](details/experiment_380.md) - mfs_RAG_metrics_v3__6
- [Experiment 381](details/experiment_381.md) - mfs_RAG_metrics_v3__7
- [Experiment 382](details/experiment_382.md) - mfs_RAG_metrics_v3__8
- [Experiment 383](details/experiment_383.md) - mfs_RAG_metrics_v3__9
- [Experiment 384](details/experiment_384.md) - mfs_RAG_metrics_v3__10
- [Experiment 385](details/experiment_385.md) - mfs_RAG_metrics_v3__11
- [Experiment 386](details/experiment_386.md) - mfs_RAG_metrics_v3__12
- [Experiment 387](details/experiment_387.md) - mfs_RAG_metrics_v3__14
- [Experiment 388](details/experiment_388.md) - mfs_RAG_metrics_v3__16
