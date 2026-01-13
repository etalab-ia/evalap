---
id: 7
name: "mfs_rag_limit_v1"
date: 2024-12-15T01:06:52.444204
description: ""
tags: []
---

# Experiment Set: mfs_rag_limit_v1 (ID: 7)

Comparing the impact of the `limit` parameters on a RAG model.

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o-mini

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                          | answer_relevancy   | generation_time   | judge_exactness   | judge_notator   | output_length   |
|:-------------------------------|:-------------------|:------------------|:------------------|:----------------|:----------------|
| AgentPublic/llama3-instruct-8b | 0.83 ± 0.04        | 4.42 ± 0.7        | 0.46 ± 0.13       | 5.97 ± 0.73     | 115.11 ± 17.0   |



## Set Overview

|   Id | Name                | Dataset           | Model                          | Model params                                              | Status   | Created at                 |   Num try |   Num success |
|-----:|:--------------------|:------------------|:-------------------------------|:----------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  139 | mfs_rag_limit_v1__0 | MFS_questions_v01 | AgentPublic/llama3-instruct-8b | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 1}}  | finished | 2024-12-15T01:06:52.444204 |        39 |            39 |
|  140 | mfs_rag_limit_v1__1 | MFS_questions_v01 | AgentPublic/llama3-instruct-8b | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 2}}  | finished | 2024-12-15T01:06:52.444204 |        39 |            39 |
|  141 | mfs_rag_limit_v1__2 | MFS_questions_v01 | AgentPublic/llama3-instruct-8b | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 3}}  | finished | 2024-12-15T01:06:52.444204 |        39 |            39 |
|  142 | mfs_rag_limit_v1__3 | MFS_questions_v01 | AgentPublic/llama3-instruct-8b | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 4}}  | finished | 2024-12-15T01:06:52.444204 |        39 |            39 |
|  143 | mfs_rag_limit_v1__4 | MFS_questions_v01 | AgentPublic/llama3-instruct-8b | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 5}}  | finished | 2024-12-15T01:06:52.444204 |        39 |            39 |
|  144 | mfs_rag_limit_v1__5 | MFS_questions_v01 | AgentPublic/llama3-instruct-8b | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}}  | finished | 2024-12-15T01:06:52.444204 |        39 |            39 |
|  145 | mfs_rag_limit_v1__6 | MFS_questions_v01 | AgentPublic/llama3-instruct-8b | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 10}} | finished | 2024-12-15T01:06:52.444204 |        39 |            39 |
|  146 | mfs_rag_limit_v1__7 | MFS_questions_v01 | AgentPublic/llama3-instruct-8b | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 15}} | finished | 2024-12-15T01:06:52.444204 |        39 |            39 |
|  147 | mfs_rag_limit_v1__8 | MFS_questions_v01 | AgentPublic/llama3-instruct-8b | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 20}} | finished | 2024-12-15T01:06:52.444204 |        39 |            39 |


## Details by Experiment

- [Experiment 139](details/experiment_139.md) - mfs_rag_limit_v1__0
- [Experiment 140](details/experiment_140.md) - mfs_rag_limit_v1__1
- [Experiment 141](details/experiment_141.md) - mfs_rag_limit_v1__2
- [Experiment 142](details/experiment_142.md) - mfs_rag_limit_v1__3
- [Experiment 143](details/experiment_143.md) - mfs_rag_limit_v1__4
- [Experiment 144](details/experiment_144.md) - mfs_rag_limit_v1__5
- [Experiment 145](details/experiment_145.md) - mfs_rag_limit_v1__6
- [Experiment 146](details/experiment_146.md) - mfs_rag_limit_v1__7
- [Experiment 147](details/experiment_147.md) - mfs_rag_limit_v1__8
