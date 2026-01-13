---
id: 44
name: "mfs_tooling_v3"
date: 2025-04-11T19:43:52.946237
description: ""
tags: []
---

# Experiment Set: mfs_tooling_v3 (ID: 44)

Evaluating tooling capabilities.

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | contextual_relevancy   | faithfulness   | generation_time   | judge_exactness   | judge_notator   | nb_tool_calls   | output_length   |
|:----------------------------------------------|:-----------------------|:---------------|:------------------|:------------------|:----------------|:----------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.12 ± 0.1             | 0.97 ± 0.06    | 12.48 ± 0.45      | 0.09 ± 0.03       | 6.04 ± 0.15     | 0.03 ± 0.02     | 233.81 ± 11.27  |
| meta-llama/Llama-3.1-8B-Instruct              | 0.41 ± 0.05            | 0.92 ± 0.01    | 10.27 ± 3.9       | 0.09 ± 0.03       | 4.74 ± 0.6      | 0.94 ± 0.7      | 207.66 ± 22.16  |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         | contextual_relevancy_support   | faithfulness_support   |   generation_time_support |   judge_exactness_support |   judge_notator_support |   nb_tool_calls_support |   output_length_support |
|:----------------------------------------------|:-------------------------------|:-----------------------|--------------------------:|--------------------------:|------------------------:|------------------------:|------------------------:|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 1.5 ± 0.76                     | 1.5 ± 0.76             |                        39 |                        39 |                      39 |                      39 |                      39 |
| meta-llama/Llama-3.1-8B-Instruct              | 37.5 ± 0.76                    | 37.5 ± 0.76            |                        39 |                        39 |                      39 |                      39 |                      39 |



## Set Overview

|   Id | Name               | Dataset           | Model                                         | Model params                                                                            | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------|:------------------|:----------------------------------------------|:----------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  833 | mfs_tooling_v3__0  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  834 | mfs_tooling_v3__1  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  835 | mfs_tooling_v3__2  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  836 | mfs_tooling_v3__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  837 | mfs_tooling_v3__4  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  838 | mfs_tooling_v3__5  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  839 | mfs_tooling_v3__6  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  840 | mfs_tooling_v3__7  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7328'}                                              | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  841 | mfs_tooling_v3__8  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  842 | mfs_tooling_v3__9  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  843 | mfs_tooling_v3__10 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  844 | mfs_tooling_v3__11 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  845 | mfs_tooling_v3__12 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  846 | mfs_tooling_v3__13 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  847 | mfs_tooling_v3__14 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  848 | mfs_tooling_v3__15 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  849 | mfs_tooling_v3__16 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  850 | mfs_tooling_v3__17 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  851 | mfs_tooling_v3__18 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  852 | mfs_tooling_v3__19 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  853 | mfs_tooling_v3__20 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  854 | mfs_tooling_v3__21 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  855 | mfs_tooling_v3__22 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |
|  856 | mfs_tooling_v3__23 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2'], 'sys_prompt': '7328'} | finished | 2025-04-11T19:43:52.946237 |        39 |            39 |


## Details by Experiment

- [Experiment 833](details/experiment_833.md) - mfs_tooling_v3__0
- [Experiment 834](details/experiment_834.md) - mfs_tooling_v3__1
- [Experiment 835](details/experiment_835.md) - mfs_tooling_v3__2
- [Experiment 836](details/experiment_836.md) - mfs_tooling_v3__3
- [Experiment 837](details/experiment_837.md) - mfs_tooling_v3__4
- [Experiment 838](details/experiment_838.md) - mfs_tooling_v3__5
- [Experiment 839](details/experiment_839.md) - mfs_tooling_v3__6
- [Experiment 840](details/experiment_840.md) - mfs_tooling_v3__7
- [Experiment 841](details/experiment_841.md) - mfs_tooling_v3__8
- [Experiment 842](details/experiment_842.md) - mfs_tooling_v3__9
- [Experiment 843](details/experiment_843.md) - mfs_tooling_v3__10
- [Experiment 844](details/experiment_844.md) - mfs_tooling_v3__11
- [Experiment 845](details/experiment_845.md) - mfs_tooling_v3__12
- [Experiment 846](details/experiment_846.md) - mfs_tooling_v3__13
- [Experiment 847](details/experiment_847.md) - mfs_tooling_v3__14
- [Experiment 848](details/experiment_848.md) - mfs_tooling_v3__15
- [Experiment 849](details/experiment_849.md) - mfs_tooling_v3__16
- [Experiment 850](details/experiment_850.md) - mfs_tooling_v3__17
- [Experiment 851](details/experiment_851.md) - mfs_tooling_v3__18
- [Experiment 852](details/experiment_852.md) - mfs_tooling_v3__19
- [Experiment 853](details/experiment_853.md) - mfs_tooling_v3__20
- [Experiment 854](details/experiment_854.md) - mfs_tooling_v3__21
- [Experiment 855](details/experiment_855.md) - mfs_tooling_v3__22
- [Experiment 856](details/experiment_856.md) - mfs_tooling_v3__23
