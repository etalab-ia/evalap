---
id: 50
name: "mfs_tooling_v7"
date: 2025-04-14T00:58:16.320579
description: ""
tags: []
---

# Experiment Set: mfs_tooling_v7 (ID: 50)

Evaluating tooling capabilities.
embedding model: BAAI/bge-m3
collections: chunks-v6, limit=10

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | judge_precision   | nb_tool_calls   | output_length   |
|:----------------------------------------------|:------------------|:------------------|:----------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 17.15 ± 2.83      | 0.39 ± 0.07       | 0.47 ± 0.35     | 250.73 ± 8.61   |
| meta-llama/Llama-3.1-8B-Instruct              | 8.95 ± 4.51       | 0.2 ± 0.08        | 0.96 ± 0.71     | 185.96 ± 40.48  |



## Set Overview

|   Id | Name               | Dataset           | Model                                         | Model params                                                                            | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------|:------------------|:----------------------------------------------|:----------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  957 | mfs_tooling_v7__0  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  958 | mfs_tooling_v7__1  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  959 | mfs_tooling_v7__2  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  960 | mfs_tooling_v7__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  961 | mfs_tooling_v7__4  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  962 | mfs_tooling_v7__5  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  963 | mfs_tooling_v7__6  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  964 | mfs_tooling_v7__7  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  965 | mfs_tooling_v7__8  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  966 | mfs_tooling_v7__9  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  967 | mfs_tooling_v7__10 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  968 | mfs_tooling_v7__11 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  969 | mfs_tooling_v7__12 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  970 | mfs_tooling_v7__13 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  971 | mfs_tooling_v7__14 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  972 | mfs_tooling_v7__15 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  973 | mfs_tooling_v7__16 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  974 | mfs_tooling_v7__17 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  975 | mfs_tooling_v7__18 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  976 | mfs_tooling_v7__19 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  977 | mfs_tooling_v7__20 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  978 | mfs_tooling_v7__21 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  979 | mfs_tooling_v7__22 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |
|  980 | mfs_tooling_v7__23 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cc72'} | finished | 2025-04-14T00:58:16.320579 |        39 |            39 |


## Details by Experiment

- [Experiment 957](details/experiment_957.md) - mfs_tooling_v7__0
- [Experiment 958](details/experiment_958.md) - mfs_tooling_v7__1
- [Experiment 959](details/experiment_959.md) - mfs_tooling_v7__2
- [Experiment 960](details/experiment_960.md) - mfs_tooling_v7__3
- [Experiment 961](details/experiment_961.md) - mfs_tooling_v7__4
- [Experiment 962](details/experiment_962.md) - mfs_tooling_v7__5
- [Experiment 963](details/experiment_963.md) - mfs_tooling_v7__6
- [Experiment 964](details/experiment_964.md) - mfs_tooling_v7__7
- [Experiment 965](details/experiment_965.md) - mfs_tooling_v7__8
- [Experiment 966](details/experiment_966.md) - mfs_tooling_v7__9
- [Experiment 967](details/experiment_967.md) - mfs_tooling_v7__10
- [Experiment 968](details/experiment_968.md) - mfs_tooling_v7__11
- [Experiment 969](details/experiment_969.md) - mfs_tooling_v7__12
- [Experiment 970](details/experiment_970.md) - mfs_tooling_v7__13
- [Experiment 971](details/experiment_971.md) - mfs_tooling_v7__14
- [Experiment 972](details/experiment_972.md) - mfs_tooling_v7__15
- [Experiment 973](details/experiment_973.md) - mfs_tooling_v7__16
- [Experiment 974](details/experiment_974.md) - mfs_tooling_v7__17
- [Experiment 975](details/experiment_975.md) - mfs_tooling_v7__18
- [Experiment 976](details/experiment_976.md) - mfs_tooling_v7__19
- [Experiment 977](details/experiment_977.md) - mfs_tooling_v7__20
- [Experiment 978](details/experiment_978.md) - mfs_tooling_v7__21
- [Experiment 979](details/experiment_979.md) - mfs_tooling_v7__22
- [Experiment 980](details/experiment_980.md) - mfs_tooling_v7__23
