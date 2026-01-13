---
id: 23
name: "mfs_variability_prompt_v2"
date: 2025-03-28T08:40:36.975467
description: ""
tags: []
---

# Experiment Set: mfs_variability_prompt_v2 (ID: 23)

Comparing impact of prompt system with gpt-4o in judge.

**Finished**: 99%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | answer_relevancy   | generation_time   | judge_exactness   | judge_notator   | output_length   |
|:----------------------------------------------|:-------------------|:------------------|:------------------|:----------------|:----------------|
| gpt-3.5-turbo                                 | 0.94 ± 0.01        | 2.77 ± 0.98       | 0.22 ± 0.06       | 6.12 ± 0.59     | 118.9 ± 52.74   |
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.82 ± 0.02        | 14.64 ± 2.84      | 0.07 ± 0.02       | 5.83 ± 0.37     | 286.94 ± 56.72  |
| meta-llama/Llama-3.1-8B-Instruct              | 0.83 ± 0.02        | 5.96 ± 1.22       | 0.04 ± 0.03       | 3.84 ± 0.15     | 273.9 ± 58.48   |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         | answer_relevancy_support   |   generation_time_support |   judge_exactness_support |   judge_notator_support |   output_length_support |
|:----------------------------------------------|:---------------------------|--------------------------:|--------------------------:|------------------------:|------------------------:|
| gpt-3.5-turbo                                 | 38.89 ± 0.33               |                        39 |                        39 |                      39 |                      39 |
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 39.0 ± 0.0                 |                        39 |                        39 |                      39 |                      39 |
| meta-llama/Llama-3.1-8B-Instruct              | 39.0 ± 0.0                 |                        39 |                        39 |                      39 |                      39 |



## Set Overview

|   Id | Name                          | Dataset           | Model                                         | Model params                               | Status   | Created at                 |   Num try |   Num success |
|-----:|:------------------------------|:------------------|:----------------------------------------------|:-------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  480 | mfs_variability_prompt_v2__0  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-28T08:40:36.975467 |        39 |            39 |
|  481 | mfs_variability_prompt_v2__1  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-28T08:40:36.975467 |        39 |            39 |
|  482 | mfs_variability_prompt_v2__2  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-28T08:40:36.975467 |        39 |            39 |
|  483 | mfs_variability_prompt_v2__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                       | finished | 2025-03-28T08:40:36.975467 |        39 |            39 |
|  484 | mfs_variability_prompt_v2__4  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                       | finished | 2025-03-28T08:40:36.975467 |        39 |            39 |
|  485 | mfs_variability_prompt_v2__5  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                       | finished | 2025-03-28T08:40:36.975467 |        39 |            39 |
|  486 | mfs_variability_prompt_v2__6  | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2}                       | finished | 2025-03-28T08:40:36.975467 |        39 |            39 |
|  487 | mfs_variability_prompt_v2__7  | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2}                       | finished | 2025-03-28T08:40:36.975467 |        39 |            39 |
|  488 | mfs_variability_prompt_v2__8  | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2}                       | finished | 2025-03-28T08:40:36.975467 |        39 |            39 |
|  489 | mfs_variability_prompt_v2__9  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-28T08:50:48.095531 |        39 |            39 |
|  490 | mfs_variability_prompt_v2__11 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-28T08:50:48.165144 |        39 |            39 |
|  491 | mfs_variability_prompt_v2__13 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-28T08:50:48.224723 |        39 |            39 |
|  492 | mfs_variability_prompt_v2__15 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-28T08:50:48.277005 |        39 |            39 |
|  493 | mfs_variability_prompt_v2__17 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-28T08:50:48.330129 |        39 |            39 |
|  494 | mfs_variability_prompt_v2__19 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-28T08:50:48.380723 |        39 |            39 |
|  495 | mfs_variability_prompt_v2__21 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-28T08:50:48.431485 |        39 |            39 |
|  496 | mfs_variability_prompt_v2__23 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-28T08:50:48.482456 |        39 |            39 |
|  497 | mfs_variability_prompt_v2__25 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2, 'sys_prompt': 'f330'} | finished | 2025-03-28T08:50:48.535441 |        39 |            39 |
|  498 | mfs_variability_prompt_v2__18 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': 'a30c'} | finished | 2025-03-28T09:00:39.068912 |        39 |            39 |
|  499 | mfs_variability_prompt_v2__20 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': 'a30c'} | finished | 2025-03-28T09:00:39.129600 |        39 |            39 |
|  500 | mfs_variability_prompt_v2__22 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': 'a30c'} | finished | 2025-03-28T09:00:39.180661 |        39 |            39 |
|  501 | mfs_variability_prompt_v2__24 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': 'a30c'} | finished | 2025-03-28T09:00:39.234509 |        39 |            39 |
|  502 | mfs_variability_prompt_v2__26 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': 'a30c'} | finished | 2025-03-28T09:00:39.284214 |        39 |            39 |
|  503 | mfs_variability_prompt_v2__28 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'sys_prompt': 'a30c'} | finished | 2025-03-28T09:00:39.332377 |        39 |            39 |
|  504 | mfs_variability_prompt_v2__30 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2, 'sys_prompt': 'a30c'} | finished | 2025-03-28T09:00:39.379772 |        39 |            39 |
|  505 | mfs_variability_prompt_v2__32 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2, 'sys_prompt': 'a30c'} | finished | 2025-03-28T09:00:39.428604 |        39 |            39 |
|  506 | mfs_variability_prompt_v2__34 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2, 'sys_prompt': 'a30c'} | finished | 2025-03-28T09:00:39.478592 |        39 |            39 |


## Details by Experiment

- [Experiment 480](details/experiment_480.md) - mfs_variability_prompt_v2__0
- [Experiment 481](details/experiment_481.md) - mfs_variability_prompt_v2__1
- [Experiment 482](details/experiment_482.md) - mfs_variability_prompt_v2__2
- [Experiment 483](details/experiment_483.md) - mfs_variability_prompt_v2__3
- [Experiment 484](details/experiment_484.md) - mfs_variability_prompt_v2__4
- [Experiment 485](details/experiment_485.md) - mfs_variability_prompt_v2__5
- [Experiment 486](details/experiment_486.md) - mfs_variability_prompt_v2__6
- [Experiment 487](details/experiment_487.md) - mfs_variability_prompt_v2__7
- [Experiment 488](details/experiment_488.md) - mfs_variability_prompt_v2__8
- [Experiment 489](details/experiment_489.md) - mfs_variability_prompt_v2__9
- [Experiment 490](details/experiment_490.md) - mfs_variability_prompt_v2__11
- [Experiment 491](details/experiment_491.md) - mfs_variability_prompt_v2__13
- [Experiment 492](details/experiment_492.md) - mfs_variability_prompt_v2__15
- [Experiment 493](details/experiment_493.md) - mfs_variability_prompt_v2__17
- [Experiment 494](details/experiment_494.md) - mfs_variability_prompt_v2__19
- [Experiment 495](details/experiment_495.md) - mfs_variability_prompt_v2__21
- [Experiment 496](details/experiment_496.md) - mfs_variability_prompt_v2__23
- [Experiment 497](details/experiment_497.md) - mfs_variability_prompt_v2__25
- [Experiment 498](details/experiment_498.md) - mfs_variability_prompt_v2__18
- [Experiment 499](details/experiment_499.md) - mfs_variability_prompt_v2__20
- [Experiment 500](details/experiment_500.md) - mfs_variability_prompt_v2__22
- [Experiment 501](details/experiment_501.md) - mfs_variability_prompt_v2__24
- [Experiment 502](details/experiment_502.md) - mfs_variability_prompt_v2__26
- [Experiment 503](details/experiment_503.md) - mfs_variability_prompt_v2__28
- [Experiment 504](details/experiment_504.md) - mfs_variability_prompt_v2__30
- [Experiment 505](details/experiment_505.md) - mfs_variability_prompt_v2__32
- [Experiment 506](details/experiment_506.md) - mfs_variability_prompt_v2__34
