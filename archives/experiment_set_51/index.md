---
id: 51
name: "mfs_tooling_v8"
date: 2025-04-14T01:35:55.645984
description: ""
tags: []
---

# Experiment Set: mfs_tooling_v8 (ID: 51)

Evaluating tooling capabilities.
embedding model: bge-multilingual-gemma2
collections: chunks-v13-04-25, limit=10

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | judge_precision   | nb_tool_calls   | output_length   |
|:----------------------------------------------|:------------------|:------------------|:----------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 17.8 ± 3.71       | 0.38 ± 0.05       | 0.46 ± 0.34     | 244.76 ± 11.57  |
| meta-llama/Llama-3.1-8B-Instruct              | 7.23 ± 1.93       | 0.19 ± 0.07       | 0.91 ± 0.67     | 196.97 ± 38.64  |



## Set Overview

|   Id | Name               | Dataset           | Model                                         | Model params                                                                            | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------|:------------------|:----------------------------------------------|:----------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  981 | mfs_tooling_v8__0  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  982 | mfs_tooling_v8__1  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  983 | mfs_tooling_v8__2  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  984 | mfs_tooling_v8__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  985 | mfs_tooling_v8__4  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  986 | mfs_tooling_v8__5  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  987 | mfs_tooling_v8__6  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  988 | mfs_tooling_v8__7  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  989 | mfs_tooling_v8__8  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  990 | mfs_tooling_v8__9  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  991 | mfs_tooling_v8__10 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  992 | mfs_tooling_v8__11 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  993 | mfs_tooling_v8__12 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  994 | mfs_tooling_v8__13 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  995 | mfs_tooling_v8__14 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  996 | mfs_tooling_v8__15 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  997 | mfs_tooling_v8__16 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  998 | mfs_tooling_v8__17 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
|  999 | mfs_tooling_v8__18 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
| 1000 | mfs_tooling_v8__19 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
| 1001 | mfs_tooling_v8__20 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
| 1002 | mfs_tooling_v8__21 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
| 1003 | mfs_tooling_v8__22 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |
| 1004 | mfs_tooling_v8__23 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T01:35:55.645984 |        39 |            39 |


## Details by Experiment

- [Experiment 981](details/experiment_981.md) - mfs_tooling_v8__0
- [Experiment 982](details/experiment_982.md) - mfs_tooling_v8__1
- [Experiment 983](details/experiment_983.md) - mfs_tooling_v8__2
- [Experiment 984](details/experiment_984.md) - mfs_tooling_v8__3
- [Experiment 985](details/experiment_985.md) - mfs_tooling_v8__4
- [Experiment 986](details/experiment_986.md) - mfs_tooling_v8__5
- [Experiment 987](details/experiment_987.md) - mfs_tooling_v8__6
- [Experiment 988](details/experiment_988.md) - mfs_tooling_v8__7
- [Experiment 989](details/experiment_989.md) - mfs_tooling_v8__8
- [Experiment 990](details/experiment_990.md) - mfs_tooling_v8__9
- [Experiment 991](details/experiment_991.md) - mfs_tooling_v8__10
- [Experiment 992](details/experiment_992.md) - mfs_tooling_v8__11
- [Experiment 993](details/experiment_993.md) - mfs_tooling_v8__12
- [Experiment 994](details/experiment_994.md) - mfs_tooling_v8__13
- [Experiment 995](details/experiment_995.md) - mfs_tooling_v8__14
- [Experiment 996](details/experiment_996.md) - mfs_tooling_v8__15
- [Experiment 997](details/experiment_997.md) - mfs_tooling_v8__16
- [Experiment 998](details/experiment_998.md) - mfs_tooling_v8__17
- [Experiment 999](details/experiment_999.md) - mfs_tooling_v8__18
- [Experiment 1000](details/experiment_1000.md) - mfs_tooling_v8__19
- [Experiment 1001](details/experiment_1001.md) - mfs_tooling_v8__20
- [Experiment 1002](details/experiment_1002.md) - mfs_tooling_v8__21
- [Experiment 1003](details/experiment_1003.md) - mfs_tooling_v8__22
- [Experiment 1004](details/experiment_1004.md) - mfs_tooling_v8__23
