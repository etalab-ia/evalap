---
id: 49
name: "mfs_tooling_v6"
date: 2025-04-13T20:06:40.214492
description: ""
tags: []
---

# Experiment Set: mfs_tooling_v6 (ID: 49)

Evaluating tooling capabilities.
embedding model: bge-multilingual-gemma2
collections: chunks-v13-04-25, limit=8

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | judge_precision   | nb_tool_calls   | output_length   |
|:----------------------------------------------|:------------------|:------------------|:----------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 15.91 ± 2.51      | 0.35 ± 0.05       | 0.46 ± 0.34     | 241.44 ± 12.43  |
| meta-llama/Llama-3.1-8B-Instruct              | 6.8 ± 2.41        | 0.16 ± 0.06       | 0.75 ± 0.55     | 186.09 ± 44.58  |



## Set Overview

|   Id | Name                 | Dataset           | Model                                         | Model params                                                                            | Status   | Created at                 |   Num try |   Num success |
|-----:|:---------------------|:------------------|:----------------------------------------------|:----------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  917 | mfs_tooling_v6__0    | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-13T20:06:40.214492 |        39 |            39 |
|  918 | mfs_tooling_v6__1    | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-13T20:06:40.214492 |        39 |            39 |
|  919 | mfs_tooling_v6__2    | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-13T20:06:40.214492 |        39 |            39 |
|  920 | mfs_tooling_v6__3    | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-13T20:06:40.214492 |        39 |            39 |
|  921 | mfs_tooling_v6__4    | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-13T20:06:40.214492 |        39 |            39 |
|  922 | mfs_tooling_v6__5    | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-13T20:06:40.214492 |        39 |            39 |
|  923 | mfs_tooling_v6__6    | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-13T20:06:40.214492 |        39 |            39 |
|  924 | mfs_tooling_v6__7    | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-13T20:06:40.214492 |        39 |            39 |
|  941 | mfs_tooling_v6_X__8  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.380362 |        39 |            39 |
|  942 | mfs_tooling_v6_X__10 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.523270 |        39 |            39 |
|  943 | mfs_tooling_v6_X__12 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.576682 |        39 |            39 |
|  944 | mfs_tooling_v6_X__14 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.625924 |        39 |            39 |
|  945 | mfs_tooling_v6_X__16 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.675239 |        39 |            39 |
|  946 | mfs_tooling_v6_X__18 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.724204 |        39 |            39 |
|  947 | mfs_tooling_v6_X__20 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.772820 |        39 |            39 |
|  948 | mfs_tooling_v6_X__22 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.821573 |        39 |            39 |
|  949 | mfs_tooling_v6_X__24 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.870332 |        39 |            39 |
|  950 | mfs_tooling_v6_X__26 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.919053 |        39 |            39 |
|  951 | mfs_tooling_v6_X__28 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:14.968492 |        39 |            39 |
|  952 | mfs_tooling_v6_X__30 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:15.018883 |        39 |            39 |
|  953 | mfs_tooling_v6_X__32 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:15.071269 |        39 |            39 |
|  954 | mfs_tooling_v6_X__34 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:15.120879 |        39 |            39 |
|  955 | mfs_tooling_v6_X__36 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:15.169052 |        39 |            39 |
|  956 | mfs_tooling_v6_X__38 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:32:15.219633 |        39 |            39 |


## Details by Experiment

- [Experiment 917](details/experiment_917.md) - mfs_tooling_v6__0
- [Experiment 918](details/experiment_918.md) - mfs_tooling_v6__1
- [Experiment 919](details/experiment_919.md) - mfs_tooling_v6__2
- [Experiment 920](details/experiment_920.md) - mfs_tooling_v6__3
- [Experiment 921](details/experiment_921.md) - mfs_tooling_v6__4
- [Experiment 922](details/experiment_922.md) - mfs_tooling_v6__5
- [Experiment 923](details/experiment_923.md) - mfs_tooling_v6__6
- [Experiment 924](details/experiment_924.md) - mfs_tooling_v6__7
- [Experiment 941](details/experiment_941.md) - mfs_tooling_v6_X__8
- [Experiment 942](details/experiment_942.md) - mfs_tooling_v6_X__10
- [Experiment 943](details/experiment_943.md) - mfs_tooling_v6_X__12
- [Experiment 944](details/experiment_944.md) - mfs_tooling_v6_X__14
- [Experiment 945](details/experiment_945.md) - mfs_tooling_v6_X__16
- [Experiment 946](details/experiment_946.md) - mfs_tooling_v6_X__18
- [Experiment 947](details/experiment_947.md) - mfs_tooling_v6_X__20
- [Experiment 948](details/experiment_948.md) - mfs_tooling_v6_X__22
- [Experiment 949](details/experiment_949.md) - mfs_tooling_v6_X__24
- [Experiment 950](details/experiment_950.md) - mfs_tooling_v6_X__26
- [Experiment 951](details/experiment_951.md) - mfs_tooling_v6_X__28
- [Experiment 952](details/experiment_952.md) - mfs_tooling_v6_X__30
- [Experiment 953](details/experiment_953.md) - mfs_tooling_v6_X__32
- [Experiment 954](details/experiment_954.md) - mfs_tooling_v6_X__34
- [Experiment 955](details/experiment_955.md) - mfs_tooling_v6_X__36
- [Experiment 956](details/experiment_956.md) - mfs_tooling_v6_X__38
