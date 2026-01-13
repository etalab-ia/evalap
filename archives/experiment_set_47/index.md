---
id: 47
name: "mfs_tooling_v4"
date: 2025-04-12T00:11:55.348619
description: ""
tags: []
---

# Experiment Set: mfs_tooling_v4 (ID: 47)

Evaluating tooling capabilities.

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | contextual_relevancy   | generation_time   | judge_exactness   | judge_notator   | judge_precision   | nb_tool_calls   | output_length   |
|:----------------------------------------------|:-----------------------|:------------------|:------------------|:----------------|:------------------|:----------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.36 ± 0.04            | 14.78 ± 2.17      | 0.09 ± 0.03       | 5.93 ± 0.16     | 0.31 ± 0.05       | 0.14 ± 0.1      | 254.81 ± 8.2    |
| meta-llama/Llama-3.1-8B-Instruct              | 0.4 ± 0.03             | 5.93 ± 0.82       | 0.08 ± 0.03       | 4.36 ± 0.4      | 0.17 ± 0.05       | 0.93 ± 0.69     | 187.87 ± 41.78  |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         | contextual_relevancy_support   |   generation_time_support |   judge_exactness_support |   judge_notator_support |   judge_precision_support |   nb_tool_calls_support |   output_length_support |
|:----------------------------------------------|:-------------------------------|--------------------------:|--------------------------:|------------------------:|--------------------------:|------------------------:|------------------------:|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 8.12 ± 0.64                    |                        39 |                        39 |                      39 |                        39 |                      39 |                      39 |
| meta-llama/Llama-3.1-8B-Instruct              | 38.25 ± 0.46                   |                        39 |                        39 |                      39 |                        39 |                      39 |                      39 |



## Set Overview

|   Id | Name               | Dataset           | Model                                         | Model params                                                                            | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------|:------------------|:----------------------------------------------|:----------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  869 | mfs_tooling_v4__0  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  870 | mfs_tooling_v4__1  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  871 | mfs_tooling_v4__2  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  872 | mfs_tooling_v4__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  873 | mfs_tooling_v4__4  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  874 | mfs_tooling_v4__5  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  875 | mfs_tooling_v4__6  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  876 | mfs_tooling_v4__7  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '5901'}                                              | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  877 | mfs_tooling_v4__8  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  878 | mfs_tooling_v4__9  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  879 | mfs_tooling_v4__10 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  880 | mfs_tooling_v4__11 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  881 | mfs_tooling_v4__12 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  882 | mfs_tooling_v4__13 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  883 | mfs_tooling_v4__14 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  884 | mfs_tooling_v4__15 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  885 | mfs_tooling_v4__16 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  886 | mfs_tooling_v4__17 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  887 | mfs_tooling_v4__18 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  888 | mfs_tooling_v4__19 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  889 | mfs_tooling_v4__20 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  890 | mfs_tooling_v4__21 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  891 | mfs_tooling_v4__22 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |
|  892 | mfs_tooling_v4__23 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': 'cfe5'} | finished | 2025-04-12T00:11:55.348619 |        39 |            39 |


## Details by Experiment

- [Experiment 869](details/experiment_869.md) - mfs_tooling_v4__0
- [Experiment 870](details/experiment_870.md) - mfs_tooling_v4__1
- [Experiment 871](details/experiment_871.md) - mfs_tooling_v4__2
- [Experiment 872](details/experiment_872.md) - mfs_tooling_v4__3
- [Experiment 873](details/experiment_873.md) - mfs_tooling_v4__4
- [Experiment 874](details/experiment_874.md) - mfs_tooling_v4__5
- [Experiment 875](details/experiment_875.md) - mfs_tooling_v4__6
- [Experiment 876](details/experiment_876.md) - mfs_tooling_v4__7
- [Experiment 877](details/experiment_877.md) - mfs_tooling_v4__8
- [Experiment 878](details/experiment_878.md) - mfs_tooling_v4__9
- [Experiment 879](details/experiment_879.md) - mfs_tooling_v4__10
- [Experiment 880](details/experiment_880.md) - mfs_tooling_v4__11
- [Experiment 881](details/experiment_881.md) - mfs_tooling_v4__12
- [Experiment 882](details/experiment_882.md) - mfs_tooling_v4__13
- [Experiment 883](details/experiment_883.md) - mfs_tooling_v4__14
- [Experiment 884](details/experiment_884.md) - mfs_tooling_v4__15
- [Experiment 885](details/experiment_885.md) - mfs_tooling_v4__16
- [Experiment 886](details/experiment_886.md) - mfs_tooling_v4__17
- [Experiment 887](details/experiment_887.md) - mfs_tooling_v4__18
- [Experiment 888](details/experiment_888.md) - mfs_tooling_v4__19
- [Experiment 889](details/experiment_889.md) - mfs_tooling_v4__20
- [Experiment 890](details/experiment_890.md) - mfs_tooling_v4__21
- [Experiment 891](details/experiment_891.md) - mfs_tooling_v4__22
- [Experiment 892](details/experiment_892.md) - mfs_tooling_v4__23
