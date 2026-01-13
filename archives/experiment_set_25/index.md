---
id: 25
name: "mfs_with_judge_gpt-4o_v5"
date: 2025-03-28T14:08:06.960615
description: ""
tags: []
---

# Experiment Set: mfs_with_judge_gpt-4o_v5 (ID: 25)

Comparing impact of judge in score calculation. Here : gpt-4o

**Finished**: 99%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | answer_relevancy   | generation_time   | judge_completude   | judge_exactness   | judge_notator   | judge_precision   | judge_rambling   | judge_relevant   | nb_tokens_completion   | output_length   |
|:----------------------------------------------|:-------------------|:------------------|:-------------------|:------------------|:----------------|:------------------|:-----------------|:-----------------|:-----------------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.82 ± 0.01        | 20.09 ± 0.87      | 35.98 ± 1.41       | 0.02 ± 0.03       | 5.32 ± 0.13     | 0.26 ± 0.01       | 3.85 ± 0.12      | 6.56 ± 0.09      | 553.91 ± 7.79          | 361.71 ± 5.48   |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | nan ± nan          | 17.36 ± 0.59      | 35.23 ± 1.73       | 0.07 ± 0.04       | 4.75 ± 0.09     | 0.24 ± 0.06       | 4.36 ± 0.07      | 5.65 ± 0.09      | 448.51 ± 12.46         | 268.66 ± 7.93   |
| gpt-3.5-turbo                                 | 0.95 ± 0.01        | 3.46 ± 0.5        | 41.92 ± 1.51       | 0.13 ± 0.03       | 5.48 ± 0.15     | 0.22 ± 0.01       | 3.52 ± 0.08      | 6.04 ± 0.1       | 250.96 ± 50.27         | 149.17 ± 24.33  |
| meta-llama/Llama-3.3-70B-Instruct             | nan ± nan          | 12.91 ± 0.13      | 30.64 ± 2.19       | 0.04 ± 0.01       | 4.35 ± 0.08     | 0.17 ± 0.03       | 4.7 ± 0.1        | 5.3 ± 0.18       | 559.22 ± 5.19          | 336.46 ± 3.28   |
| google/gemma-2-9b-it                          | 0.77 ± 0.02        | 6.19 ± 0.06       | 29.96 ± 0.59       | 0.06 ± 0.01       | 4.32 ± 0.04     | 0.12 ± 0.03       | 4.72 ± 0.14      | 5.12 ± 0.16      | 350.99 ± 3.85          | 232.92 ± 1.31   |
| meta-llama/Llama-3.1-8B-Instruct              | 0.85 ± 0.01        | 6.54 ± 0.14       | 27.44 ± 1.1        | 0.03 ± 0.01       | 3.53 ± 0.17     | 0.07 ± 0.01       | 5.36 ± 0.09      | 4.55 ± 0.23      | 488.32 ± 15.92         | 295.25 ± 9.66   |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         |   answer_relevancy_support | generation_time_support   | judge_completude_support   | judge_exactness_support   | judge_notator_support   | judge_precision_support   | judge_rambling_support   | judge_relevant_support   | nb_tokens_completion_support   | output_length_support   |
|:----------------------------------------------|---------------------------:|:--------------------------|:---------------------------|:--------------------------|:------------------------|:--------------------------|:-------------------------|:-------------------------|:-------------------------------|:------------------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 |                         39 | 39.0 ± 0.0                | 39.0 ± 0.0                 | 39.0 ± 0.0                | 39.0 ± 0.0              | 39.0 ± 0.0                | 39.0 ± 0.0               | 39.0 ± 0.0               | 39.0 ± 0.0                     | 39.0 ± 0.0              |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   |                        nan | 38.75 ± 0.5               | 38.75 ± 0.5                | 38.75 ± 0.5               | 38.75 ± 0.5             | 38.75 ± 0.5               | 38.75 ± 0.5              | 38.75 ± 0.5              | 38.75 ± 0.5                    | 38.75 ± 0.5             |
| gpt-3.5-turbo                                 |                         39 | 39.0 ± 0.0                | 39.0 ± 0.0                 | 39.0 ± 0.0                | 39.0 ± 0.0              | 39.0 ± 0.0                | 39.0 ± 0.0               | 39.0 ± 0.0               | 39.0 ± 0.0                     | 39.0 ± 0.0              |
| meta-llama/Llama-3.3-70B-Instruct             |                        nan | 39.0 ± 0.0                | 39.0 ± 0.0                 | 39.0 ± 0.0                | 39.0 ± 0.0              | 39.0 ± 0.0                | 39.0 ± 0.0               | 39.0 ± 0.0               | 39.0 ± 0.0                     | 39.0 ± 0.0              |
| google/gemma-2-9b-it                          |                         39 | 39.0 ± 0.0                | 39.0 ± 0.0                 | 39.0 ± 0.0                | 39.0 ± 0.0              | 39.0 ± 0.0                | 39.0 ± 0.0               | 39.0 ± 0.0               | 39.0 ± 0.0                     | 39.0 ± 0.0              |
| meta-llama/Llama-3.1-8B-Instruct              |                         39 | 39.0 ± 0.0                | 39.0 ± 0.0                 | 39.0 ± 0.0                | 39.0 ± 0.0              | 39.0 ± 0.0                | 39.0 ± 0.0               | 39.0 ± 0.0               | 39.0 ± 0.0                     | 39.0 ± 0.0              |



## Set Overview

|   Id | Name                          | Dataset           | Model                                         | Model params         | Status   | Created at                 |   Num try |   Num success |
|-----:|:------------------------------|:------------------|:----------------------------------------------|:---------------------|:---------|:---------------------------|----------:|--------------:|
|  527 | mfs_vwith_judge_gpt-4o_v1__0  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  528 | mfs_vwith_judge_gpt-4o_v1__1  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  529 | mfs_vwith_judge_gpt-4o_v1__2  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  530 | mfs_vwith_judge_gpt-4o_v1__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  531 | mfs_vwith_judge_gpt-4o_v1__4  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  532 | mfs_vwith_judge_gpt-4o_v1__5  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  533 | mfs_vwith_judge_gpt-4o_v1__6  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  534 | mfs_vwith_judge_gpt-4o_v1__7  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  535 | mfs_vwith_judge_gpt-4o_v1__8  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  536 | mfs_vwith_judge_gpt-4o_v1__9  | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  537 | mfs_vwith_judge_gpt-4o_v1__10 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
|  538 | mfs_vwith_judge_gpt-4o_v1__11 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | finished | 2025-03-28T14:08:06.960615 |        39 |            39 |
| 1073 | mfs_with_judge_gpt-4o_v1__12  | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished | 2025-04-30T17:48:08.301352 |        39 |            39 |
| 1074 | mfs_with_judge_gpt-4o_v1__14  | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished | 2025-04-30T17:48:08.363746 |        39 |            39 |
| 1075 | mfs_with_judge_gpt-4o_v1__16  | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished | 2025-04-30T17:48:08.416596 |        39 |            39 |
| 1076 | mfs_with_judge_gpt-4o_v1__18  | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished | 2025-04-30T17:48:08.469601 |        39 |            38 |
| 1108 | mfs_with_judge_gpt-4o_v5__16  | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished | 2025-04-30T18:10:52.067463 |        39 |            39 |
| 1109 | mfs_with_judge_gpt-4o_v5__18  | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished | 2025-04-30T18:10:52.130343 |        39 |            39 |
| 1110 | mfs_with_judge_gpt-4o_v5__20  | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished | 2025-04-30T18:10:52.188552 |        39 |            39 |


## Details by Experiment

- [Experiment 527](details/experiment_527.md) - mfs_vwith_judge_gpt-4o_v1__0
- [Experiment 528](details/experiment_528.md) - mfs_vwith_judge_gpt-4o_v1__1
- [Experiment 529](details/experiment_529.md) - mfs_vwith_judge_gpt-4o_v1__2
- [Experiment 530](details/experiment_530.md) - mfs_vwith_judge_gpt-4o_v1__3
- [Experiment 531](details/experiment_531.md) - mfs_vwith_judge_gpt-4o_v1__4
- [Experiment 532](details/experiment_532.md) - mfs_vwith_judge_gpt-4o_v1__5
- [Experiment 533](details/experiment_533.md) - mfs_vwith_judge_gpt-4o_v1__6
- [Experiment 534](details/experiment_534.md) - mfs_vwith_judge_gpt-4o_v1__7
- [Experiment 535](details/experiment_535.md) - mfs_vwith_judge_gpt-4o_v1__8
- [Experiment 536](details/experiment_536.md) - mfs_vwith_judge_gpt-4o_v1__9
- [Experiment 537](details/experiment_537.md) - mfs_vwith_judge_gpt-4o_v1__10
- [Experiment 538](details/experiment_538.md) - mfs_vwith_judge_gpt-4o_v1__11
- [Experiment 1073](details/experiment_1073.md) - mfs_with_judge_gpt-4o_v1__12
- [Experiment 1074](details/experiment_1074.md) - mfs_with_judge_gpt-4o_v1__14
- [Experiment 1075](details/experiment_1075.md) - mfs_with_judge_gpt-4o_v1__16
- [Experiment 1076](details/experiment_1076.md) - mfs_with_judge_gpt-4o_v1__18
- [Experiment 1108](details/experiment_1108.md) - mfs_with_judge_gpt-4o_v5__16
- [Experiment 1109](details/experiment_1109.md) - mfs_with_judge_gpt-4o_v5__18
- [Experiment 1110](details/experiment_1110.md) - mfs_with_judge_gpt-4o_v5__20
