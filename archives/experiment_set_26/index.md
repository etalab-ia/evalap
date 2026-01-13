---
id: 26
name: "mfs_with_judge_gpt-4o-mini_v5"
date: 2025-03-28T14:08:34.757366
description: ""
tags: []
---

# Experiment Set: mfs_with_judge_gpt-4o-mini_v5 (ID: 26)

Comparing impact of judge in score calculation. Here : gpt-4o-mini

**Finished**: 99%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o-mini

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | answer_relevancy   | generation_time   | judge_completude   | judge_exactness   | judge_notator   | judge_precision   | judge_rambling   | judge_relevant   | nb_tokens_completion   | output_length   |
|:----------------------------------------------|:-------------------|:------------------|:-------------------|:------------------|:----------------|:------------------|:-----------------|:-----------------|:-----------------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.87 ± 0.04        | 19.32 ± 0.4       | 68.93 ± 1.26       | 0.59 ± 0.03       | 6.93 ± 0.16     | 0.66 ± 0.01       | 4.44 ± 0.16      | 7.63 ± 0.17      | 551.7 ± 4.09           | 359.06 ± 2.55   |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | nan ± nan          | 18.13 ± 0.28      | 62.02 ± 1.52       | 0.53 ± 0.04       | 6.34 ± 0.1      | 0.58 ± 0.05       | 4.6 ± 0.13       | 6.9 ± 0.21       | 449.58 ± 7.61          | 269.67 ± 4.62   |
| gpt-3.5-turbo                                 | 0.95 ± 0.02        | 3.97 ± 0.78       | 64.53 ± 0.52       | 0.64 ± 0.03       | 6.93 ± 0.05     | 0.56 ± 0.03       | 4.36 ± 0.14      | 7.15 ± 0.09      | 291.99 ± 52.72         | 169.24 ± 25.98  |
| meta-llama/Llama-3.3-70B-Instruct             | nan ± nan          | 13.4 ± 0.35       | 60.38 ± 1.24       | 0.5 ± 0.05        | 6.1 ± 0.22      | 0.53 ± 0.08       | 5.02 ± 0.2       | 6.56 ± 0.21      | 575.94 ± 13.51         | 344.95 ± 8.08   |
| google/gemma-2-9b-it                          | 0.85 ± 0.02        | 5.9 ± 0.14        | 58.89 ± 0.81       | 0.38 ± 0.0        | 5.89 ± 0.09     | 0.44 ± 0.03       | 4.99 ± 0.13      | 6.16 ± 0.09      | 344.79 ± 5.2           | 229.32 ± 4.3    |
| meta-llama/Llama-3.1-8B-Instruct              | 0.85 ± 0.06        | 6.68 ± 0.29       | 58.63 ± 1.69       | 0.32 ± 0.01       | 5.62 ± 0.01     | 0.44 ± 0.01       | 5.42 ± 0.01      | 5.95 ± 0.09      | 495.26 ± 10.68         | 299.51 ± 4.87   |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         |   answer_relevancy_support |   generation_time_support |   judge_completude_support |   judge_exactness_support |   judge_notator_support |   judge_precision_support |   judge_rambling_support | judge_relevant_support   |   nb_tokens_completion_support |   output_length_support |
|:----------------------------------------------|---------------------------:|--------------------------:|---------------------------:|--------------------------:|------------------------:|--------------------------:|-------------------------:|:-------------------------|-------------------------------:|------------------------:|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 |                         39 |                        39 |                         39 |                        39 |                      39 |                        39 |                       39 | 38.67 ± 0.58             |                             39 |                      39 |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   |                        nan |                        39 |                         39 |                        39 |                      39 |                        39 |                       39 | 39.0 ± 0.0               |                             39 |                      39 |
| gpt-3.5-turbo                                 |                         39 |                        39 |                         39 |                        39 |                      39 |                        39 |                       39 | 39.0 ± 0.0               |                             39 |                      39 |
| meta-llama/Llama-3.3-70B-Instruct             |                        nan |                        39 |                         39 |                        39 |                      39 |                        39 |                       39 | 39.0 ± 0.0               |                             39 |                      39 |
| google/gemma-2-9b-it                          |                         39 |                        39 |                         39 |                        39 |                      39 |                        39 |                       39 | 39.0 ± 0.0               |                             39 |                      39 |
| meta-llama/Llama-3.1-8B-Instruct              |                         39 |                        39 |                         39 |                        39 |                      39 |                        39 |                       39 | 39.0 ± 0.0               |                             39 |                      39 |



## Set Overview

|   Id | Name                               | Dataset           | Model                                         | Model params         | Status          | Created at                 |   Num try |   Num success |
|-----:|:-----------------------------------|:------------------|:----------------------------------------------|:---------------------|:----------------|:---------------------------|----------:|--------------:|
|  539 | mfs_vwith_judge_gpt-4o-mini_v1__0  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  540 | mfs_vwith_judge_gpt-4o-mini_v1__1  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  541 | mfs_vwith_judge_gpt-4o-mini_v1__2  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  542 | mfs_vwith_judge_gpt-4o-mini_v1__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  543 | mfs_vwith_judge_gpt-4o-mini_v1__4  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  544 | mfs_vwith_judge_gpt-4o-mini_v1__5  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  545 | mfs_vwith_judge_gpt-4o-mini_v1__6  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  546 | mfs_vwith_judge_gpt-4o-mini_v1__7  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  547 | mfs_vwith_judge_gpt-4o-mini_v1__8  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  548 | mfs_vwith_judge_gpt-4o-mini_v1__9  | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  549 | mfs_vwith_judge_gpt-4o-mini_v1__10 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
|  550 | mfs_vwith_judge_gpt-4o-mini_v1__11 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-03-28T14:08:34.757366 |        39 |            39 |
| 1065 | mfs_with_judge_gpt-4o-mini_v1__12  | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:07.564976 |        39 |            39 |
| 1066 | mfs_with_judge_gpt-4o-mini_v1__14  | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:07.625458 |        39 |            39 |
| 1067 | mfs_with_judge_gpt-4o-mini_v1__16  | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:07.683855 |        39 |            39 |
| 1068 | mfs_with_judge_gpt-4o-mini_v1__18  | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:07.740051 |        39 |            39 |
| 1105 | mfs_with_judge_gpt-4o-mini_v5__16  | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:10:51.600477 |        39 |            39 |
| 1106 | mfs_with_judge_gpt-4o-mini_v5__18  | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:10:51.659812 |        39 |            39 |
| 1107 | mfs_with_judge_gpt-4o-mini_v5__20  | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:10:51.715650 |        39 |            39 |


## Details by Experiment

- [Experiment 539](details/experiment_539.md) - mfs_vwith_judge_gpt-4o-mini_v1__0
- [Experiment 540](details/experiment_540.md) - mfs_vwith_judge_gpt-4o-mini_v1__1
- [Experiment 541](details/experiment_541.md) - mfs_vwith_judge_gpt-4o-mini_v1__2
- [Experiment 542](details/experiment_542.md) - mfs_vwith_judge_gpt-4o-mini_v1__3
- [Experiment 543](details/experiment_543.md) - mfs_vwith_judge_gpt-4o-mini_v1__4
- [Experiment 544](details/experiment_544.md) - mfs_vwith_judge_gpt-4o-mini_v1__5
- [Experiment 545](details/experiment_545.md) - mfs_vwith_judge_gpt-4o-mini_v1__6
- [Experiment 546](details/experiment_546.md) - mfs_vwith_judge_gpt-4o-mini_v1__7
- [Experiment 547](details/experiment_547.md) - mfs_vwith_judge_gpt-4o-mini_v1__8
- [Experiment 548](details/experiment_548.md) - mfs_vwith_judge_gpt-4o-mini_v1__9
- [Experiment 549](details/experiment_549.md) - mfs_vwith_judge_gpt-4o-mini_v1__10
- [Experiment 550](details/experiment_550.md) - mfs_vwith_judge_gpt-4o-mini_v1__11
- [Experiment 1065](details/experiment_1065.md) - mfs_with_judge_gpt-4o-mini_v1__12
- [Experiment 1066](details/experiment_1066.md) - mfs_with_judge_gpt-4o-mini_v1__14
- [Experiment 1067](details/experiment_1067.md) - mfs_with_judge_gpt-4o-mini_v1__16
- [Experiment 1068](details/experiment_1068.md) - mfs_with_judge_gpt-4o-mini_v1__18
- [Experiment 1105](details/experiment_1105.md) - mfs_with_judge_gpt-4o-mini_v5__16
- [Experiment 1106](details/experiment_1106.md) - mfs_with_judge_gpt-4o-mini_v5__18
- [Experiment 1107](details/experiment_1107.md) - mfs_with_judge_gpt-4o-mini_v5__20
