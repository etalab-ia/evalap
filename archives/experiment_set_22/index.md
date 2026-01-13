---
id: 22
name: "mfs_variability_prompt_v1"
date: 2025-03-27T13:53:24.725081
description: ""
tags: []
---

# Experiment Set: mfs_variability_prompt_v1 (ID: 22)

Comparing impact of prompt system.

**Finished**: 99%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | answer_relevancy   | generation_time   | judge_exactness   | judge_notator   | output_length   |
|:----------------------------------------------|:-------------------|:------------------|:------------------|:----------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.83 ± 0.04        | 18.19 ± 4.3       | 0.17 ± 0.22       | 5.85 ± 0.82     | 321.55 ± 56.24  |
| gpt-3.5-turbo                                 | 0.95 ± 0.01        | 2.67 ± 0.73       | 0.25 ± 0.21       | 5.83 ± 0.7      | 136.53 ± 46.05  |
| meta-llama/Llama-3.1-8B-Instruct              | 0.84 ± 0.02        | 5.98 ± 0.83       | 0.07 ± 0.1        | 4.0 ± 0.72      | 272.48 ± 36.52  |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         | answer_relevancy_support   |   generation_time_support |   judge_exactness_support |   judge_notator_support |   output_length_support |
|:----------------------------------------------|:---------------------------|--------------------------:|--------------------------:|------------------------:|------------------------:|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 39.0 ± 0.0                 |                        39 |                        39 |                      39 |                      39 |
| gpt-3.5-turbo                                 | 38.88 ± 0.35               |                        39 |                        39 |                      39 |                      39 |
| meta-llama/Llama-3.1-8B-Instruct              | 39.0 ± 0.0                 |                        39 |                        39 |                      39 |                      39 |



## Set Overview

|   Id | Name                          | Dataset           | Model                                         | Model params                               | Status   | Created at                 |   Num try |   Num success |
|-----:|:------------------------------|:------------------|:----------------------------------------------|:-------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  422 | mfs_variability_prompt_v1__0  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  423 | mfs_variability_prompt_v1__1  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  424 | mfs_variability_prompt_v1__2  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  425 | mfs_variability_prompt_v1__3  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  426 | mfs_variability_prompt_v1__4  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  427 | mfs_variability_prompt_v1__5  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  428 | mfs_variability_prompt_v1__6  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  429 | mfs_variability_prompt_v1__7  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  430 | mfs_variability_prompt_v1__8  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  431 | mfs_variability_prompt_v1__9  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  432 | mfs_variability_prompt_v1__10 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  433 | mfs_variability_prompt_v1__11 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  434 | mfs_variability_prompt_v1__12 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  435 | mfs_variability_prompt_v1__13 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  436 | mfs_variability_prompt_v1__14 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2}                       | finished | 2025-03-27T13:53:24.725081 |        39 |            39 |
|  437 | mfs_variability_prompt_v1__15 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-27T14:40:30.028545 |        39 |            39 |
|  438 | mfs_variability_prompt_v1__17 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-27T14:40:30.164281 |        39 |            39 |
|  439 | mfs_variability_prompt_v1__19 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-27T14:40:30.219165 |        39 |            39 |
|  440 | mfs_variability_prompt_v1__18 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': 'a1bc'} | finished | 2025-03-27T14:41:21.884742 |        39 |            39 |
|  441 | mfs_variability_prompt_v1__20 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': 'a1bc'} | finished | 2025-03-27T14:41:21.955086 |        39 |            39 |
|  442 | mfs_variability_prompt_v1__22 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2, 'sys_prompt': 'a1bc'} | finished | 2025-03-27T14:41:22.004665 |        39 |            39 |
|  443 | mfs_variability_prompt_v1__21 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '0d34'} | finished | 2025-03-27T15:03:11.628412 |        39 |            39 |
|  444 | mfs_variability_prompt_v1__23 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': '0d34'} | finished | 2025-03-27T15:03:11.721997 |        39 |            39 |
|  445 | mfs_variability_prompt_v1__25 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2, 'sys_prompt': '0d34'} | finished | 2025-03-27T15:03:11.779707 |        39 |            39 |


## Details by Experiment

- [Experiment 422](details/experiment_422.md) - mfs_variability_prompt_v1__0
- [Experiment 423](details/experiment_423.md) - mfs_variability_prompt_v1__1
- [Experiment 424](details/experiment_424.md) - mfs_variability_prompt_v1__2
- [Experiment 425](details/experiment_425.md) - mfs_variability_prompt_v1__3
- [Experiment 426](details/experiment_426.md) - mfs_variability_prompt_v1__4
- [Experiment 427](details/experiment_427.md) - mfs_variability_prompt_v1__5
- [Experiment 428](details/experiment_428.md) - mfs_variability_prompt_v1__6
- [Experiment 429](details/experiment_429.md) - mfs_variability_prompt_v1__7
- [Experiment 430](details/experiment_430.md) - mfs_variability_prompt_v1__8
- [Experiment 431](details/experiment_431.md) - mfs_variability_prompt_v1__9
- [Experiment 432](details/experiment_432.md) - mfs_variability_prompt_v1__10
- [Experiment 433](details/experiment_433.md) - mfs_variability_prompt_v1__11
- [Experiment 434](details/experiment_434.md) - mfs_variability_prompt_v1__12
- [Experiment 435](details/experiment_435.md) - mfs_variability_prompt_v1__13
- [Experiment 436](details/experiment_436.md) - mfs_variability_prompt_v1__14
- [Experiment 437](details/experiment_437.md) - mfs_variability_prompt_v1__15
- [Experiment 438](details/experiment_438.md) - mfs_variability_prompt_v1__17
- [Experiment 439](details/experiment_439.md) - mfs_variability_prompt_v1__19
- [Experiment 440](details/experiment_440.md) - mfs_variability_prompt_v1__18
- [Experiment 441](details/experiment_441.md) - mfs_variability_prompt_v1__20
- [Experiment 442](details/experiment_442.md) - mfs_variability_prompt_v1__22
- [Experiment 443](details/experiment_443.md) - mfs_variability_prompt_v1__21
- [Experiment 444](details/experiment_444.md) - mfs_variability_prompt_v1__23
- [Experiment 445](details/experiment_445.md) - mfs_variability_prompt_v1__25
