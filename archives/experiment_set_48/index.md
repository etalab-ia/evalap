---
id: 48
name: "mfs_tooling_v5"
date: 2025-04-12T03:20:19.001408
description: ""
tags: []
---

# Experiment Set: mfs_tooling_v5 (ID: 48)

Evaluating tooling capabilities.

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | judge_precision   | nb_tool_calls   | output_length   |
|:----------------------------------------------|:------------------|:------------------|:----------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 16.99 ± 3.38      | 0.35 ± 0.05       | 0.41 ± 0.3      | 244.53 ± 7.58   |
| meta-llama/Llama-3.1-8B-Instruct              | 6.13 ± 0.89       | 0.18 ± 0.06       | 0.93 ± 0.69     | 192.72 ± 38.41  |



## Set Overview

|   Id | Name               | Dataset           | Model                                         | Model params                                                                            | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------|:------------------|:----------------------------------------------|:----------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  893 | mfs_tooling_v5__0  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  894 | mfs_tooling_v5__1  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  895 | mfs_tooling_v5__2  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  896 | mfs_tooling_v5__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  897 | mfs_tooling_v5__4  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  898 | mfs_tooling_v5__5  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  899 | mfs_tooling_v5__6  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  900 | mfs_tooling_v5__7  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  901 | mfs_tooling_v5__8  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  902 | mfs_tooling_v5__9  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  903 | mfs_tooling_v5__10 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  904 | mfs_tooling_v5__11 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  905 | mfs_tooling_v5__12 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  906 | mfs_tooling_v5__13 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  907 | mfs_tooling_v5__14 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  908 | mfs_tooling_v5__15 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  909 | mfs_tooling_v5__16 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  910 | mfs_tooling_v5__17 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  911 | mfs_tooling_v5__18 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  912 | mfs_tooling_v5__19 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  913 | mfs_tooling_v5__20 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  914 | mfs_tooling_v5__21 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  915 | mfs_tooling_v5__22 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |
|  916 | mfs_tooling_v5__23 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-12T03:20:19.001408 |        39 |            39 |


## Details by Experiment

- [Experiment 893](details/experiment_893.md) - mfs_tooling_v5__0
- [Experiment 894](details/experiment_894.md) - mfs_tooling_v5__1
- [Experiment 895](details/experiment_895.md) - mfs_tooling_v5__2
- [Experiment 896](details/experiment_896.md) - mfs_tooling_v5__3
- [Experiment 897](details/experiment_897.md) - mfs_tooling_v5__4
- [Experiment 898](details/experiment_898.md) - mfs_tooling_v5__5
- [Experiment 899](details/experiment_899.md) - mfs_tooling_v5__6
- [Experiment 900](details/experiment_900.md) - mfs_tooling_v5__7
- [Experiment 901](details/experiment_901.md) - mfs_tooling_v5__8
- [Experiment 902](details/experiment_902.md) - mfs_tooling_v5__9
- [Experiment 903](details/experiment_903.md) - mfs_tooling_v5__10
- [Experiment 904](details/experiment_904.md) - mfs_tooling_v5__11
- [Experiment 905](details/experiment_905.md) - mfs_tooling_v5__12
- [Experiment 906](details/experiment_906.md) - mfs_tooling_v5__13
- [Experiment 907](details/experiment_907.md) - mfs_tooling_v5__14
- [Experiment 908](details/experiment_908.md) - mfs_tooling_v5__15
- [Experiment 909](details/experiment_909.md) - mfs_tooling_v5__16
- [Experiment 910](details/experiment_910.md) - mfs_tooling_v5__17
- [Experiment 911](details/experiment_911.md) - mfs_tooling_v5__18
- [Experiment 912](details/experiment_912.md) - mfs_tooling_v5__19
- [Experiment 913](details/experiment_913.md) - mfs_tooling_v5__20
- [Experiment 914](details/experiment_914.md) - mfs_tooling_v5__21
- [Experiment 915](details/experiment_915.md) - mfs_tooling_v5__22
- [Experiment 916](details/experiment_916.md) - mfs_tooling_v5__23
