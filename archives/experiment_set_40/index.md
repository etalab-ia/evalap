---
id: 40
name: "mfs_tooling_v2"
date: 2025-04-11T03:46:19.887042
description: ""
tags: []
---

# Experiment Set: mfs_tooling_v2 (ID: 40)

Evaluating tooling capabilities.

Interesting failed case, where we have the LLM that get stuck to a tool calling loop !

**Finished**: 99%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | contextual_relevancy   | faithfulness   | generation_time   | judge_exactness   | judge_notator   | nb_tool_calls   | output_length   |
|:----------------------------------------------|:-----------------------|:---------------|:------------------|:------------------|:----------------|:----------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.44 ± 0.05            | 0.93 ± 0.03    | 14.61 ± 1.35      | 0.1 ± 0.06        | 6.07 ± 0.22     | 0.31 ± 0.23     | 241.91 ± 7.89   |
| meta-llama/Llama-3.1-8B-Instruct              | 0.41 ± 0.04            | 0.93 ± 0.01    | 5.86 ± 0.91       | 0.08 ± 0.03       | 4.43 ± 0.35     | 1.12 ± 0.83     | 174.6 ± 45.5    |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         | contextual_relevancy_support   | faithfulness_support   |   generation_time_support | judge_exactness_support   | judge_notator_support   |   nb_tool_calls_support | output_length_support   |
|:----------------------------------------------|:-------------------------------|:-----------------------|--------------------------:|:--------------------------|:------------------------|------------------------:|:------------------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 18.25 ± 1.04                   | 18.25 ± 1.04           |                        39 | 39.0 ± 0.0                | 39.0 ± 0.0              |                      39 | 39.0 ± 0.0              |
| meta-llama/Llama-3.1-8B-Instruct              | 37.5 ± 0.53                    | 37.5 ± 0.53            |                        39 | 38.75 ± 0.45              | 38.75 ± 0.45            |                      39 | 38.75 ± 0.45            |



## Set Overview

|   Id | Name               | Dataset           | Model                                         | Model params                                                                            | Status          | Created at                 |   Num try |   Num success |
|-----:|:-------------------|:------------------|:----------------------------------------------|:----------------------------------------------------------------------------------------|:----------------|:---------------------------|----------:|--------------:|
|  761 | mfs_tooling_v2__0  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  762 | mfs_tooling_v2__1  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  763 | mfs_tooling_v2__2  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  764 | mfs_tooling_v2__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  765 | mfs_tooling_v2__4  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  766 | mfs_tooling_v2__5  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  767 | mfs_tooling_v2__6  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  768 | mfs_tooling_v2__7  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  769 | mfs_tooling_v2__8  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'e13c'} | running_metrics | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  770 | mfs_tooling_v2__9  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'e13c'} | running_metrics | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  771 | mfs_tooling_v2__10 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'e13c'} | running_metrics | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  772 | mfs_tooling_v2__11 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'e13c'} | running_metrics | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  773 | mfs_tooling_v2__12 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'e13c'} | running_metrics | 2025-04-11T03:46:19.887042 |        39 |            38 |
|  774 | mfs_tooling_v2__13 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'e13c'} | running_metrics | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  775 | mfs_tooling_v2__14 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'e13c'} | running_metrics | 2025-04-11T03:46:19.887042 |        39 |            38 |
|  776 | mfs_tooling_v2__15 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'e13c'} | running_metrics | 2025-04-11T03:46:19.887042 |        39 |            38 |
|  777 | mfs_tooling_v2__16 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'e13c'} | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  778 | mfs_tooling_v2__17 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'e13c'} | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  779 | mfs_tooling_v2__18 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'e13c'} | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  780 | mfs_tooling_v2__19 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'e13c'} | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  781 | mfs_tooling_v2__20 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'e13c'} | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  782 | mfs_tooling_v2__21 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'e13c'} | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  783 | mfs_tooling_v2__22 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'e13c'} | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |
|  784 | mfs_tooling_v2__23 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'e13c'} | finished        | 2025-04-11T03:46:19.887042 |        39 |            39 |


## Details by Experiment

- [Experiment 761](details/experiment_761.md) - mfs_tooling_v2__0
- [Experiment 762](details/experiment_762.md) - mfs_tooling_v2__1
- [Experiment 763](details/experiment_763.md) - mfs_tooling_v2__2
- [Experiment 764](details/experiment_764.md) - mfs_tooling_v2__3
- [Experiment 765](details/experiment_765.md) - mfs_tooling_v2__4
- [Experiment 766](details/experiment_766.md) - mfs_tooling_v2__5
- [Experiment 767](details/experiment_767.md) - mfs_tooling_v2__6
- [Experiment 768](details/experiment_768.md) - mfs_tooling_v2__7
- [Experiment 769](details/experiment_769.md) - mfs_tooling_v2__8
- [Experiment 770](details/experiment_770.md) - mfs_tooling_v2__9
- [Experiment 771](details/experiment_771.md) - mfs_tooling_v2__10
- [Experiment 772](details/experiment_772.md) - mfs_tooling_v2__11
- [Experiment 773](details/experiment_773.md) - mfs_tooling_v2__12
- [Experiment 774](details/experiment_774.md) - mfs_tooling_v2__13
- [Experiment 775](details/experiment_775.md) - mfs_tooling_v2__14
- [Experiment 776](details/experiment_776.md) - mfs_tooling_v2__15
- [Experiment 777](details/experiment_777.md) - mfs_tooling_v2__16
- [Experiment 778](details/experiment_778.md) - mfs_tooling_v2__17
- [Experiment 779](details/experiment_779.md) - mfs_tooling_v2__18
- [Experiment 780](details/experiment_780.md) - mfs_tooling_v2__19
- [Experiment 781](details/experiment_781.md) - mfs_tooling_v2__20
- [Experiment 782](details/experiment_782.md) - mfs_tooling_v2__21
- [Experiment 783](details/experiment_783.md) - mfs_tooling_v2__22
- [Experiment 784](details/experiment_784.md) - mfs_tooling_v2__23
