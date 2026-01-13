---
id: 42
name: "mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v5"
date: 2025-04-11T11:15:24.484366
description: ""
tags: []
---

# Experiment Set: mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v5 (ID: 42)

Comparing impact of judge in score calculation. Here : meta-llama/Llama-3.3-70B-Instruct

**Finished**: 96%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: meta-llama/Llama-3.3-70B-Instruct

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | judge_completude   | judge_exactness   | judge_notator   | judge_precision   | judge_rambling   | judge_relevant   | nb_tokens_completion   | output_length   |
|:----------------------------------------------|:------------------|:-------------------|:------------------|:----------------|:------------------|:-----------------|:-----------------|:-----------------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 18.7 ± 1.1        | 48.44 ± 1.81       | 0.39 ± 0.01       | 6.15 ± 0.13     | 0.32 ± 0.03       | 5.99 ± 0.14      | 6.83 ± 0.15      | 550.68 ± 13.75         | 361.31 ± 6.86   |
| meta-llama/Llama-3.3-70B-Instruct             | 14.24 ± 0.95      | 36.26 ± 1.35       | 0.32 ± 0.07       | 5.38 ± 0.18     | 0.3 ± 0.08        | 6.48 ± 0.28      | 5.5 ± 0.28       | 567.55 ± 11.61         | 340.9 ± 7.94    |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | 21.54 ± 2.59      | 39.29 ± 1.9        | 0.27 ± 0.05       | 5.76 ± 0.25     | 0.26 ± 0.06       | 6.03 ± 0.19      | 5.62 ± 0.29      | 449.17 ± 15.6          | 268.93 ± 8.29   |
| gpt-3.5-turbo                                 | 3.46 ± 0.34       | 38.61 ± 0.28       | 0.32 ± 0.03       | 6.13 ± 0.03     | 0.2 ± 0.01        | 4.81 ± 0.13      | 4.88 ± 0.13      | 319.65 ± 6.14          | 183.04 ± 2.42   |
| meta-llama/Llama-3.1-8B-Instruct              | 8.58 ± 3.49       | 28.21 ± 0.8        | 0.15 ± 0.03       | 4.49 ± 0.12     | 0.17 ± 0.04       | 7.27 ± 0.12      | 4.1 ± 0.1        | 477.04 ± 6.33          | 288.62 ± 2.47   |
| google/gemma-2-9b-it                          | 5.97 ± 0.04       | 29.79 ± 0.41       | 0.24 ± 0.04       | 4.71 ± 0.05     | 0.16 ± 0.04       | 6.74 ± 0.17      | 4.21 ± 0.07      | 345.63 ± 2.28          | 227.17 ± 1.18   |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         |   generation_time_support |   judge_completude_support |   judge_exactness_support |   judge_notator_support |   judge_precision_support | judge_rambling_support   | judge_relevant_support   |   nb_tokens_completion_support |   output_length_support |
|:----------------------------------------------|--------------------------:|---------------------------:|--------------------------:|------------------------:|--------------------------:|:-------------------------|:-------------------------|-------------------------------:|------------------------:|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 |                        39 |                         39 |                        39 |                      39 |                        39 | 32.67 ± 2.08             | 32.0 ± 1.73              |                             39 |                      39 |
| meta-llama/Llama-3.3-70B-Instruct             |                        39 |                         39 |                        39 |                      39 |                        39 | 30.67 ± 1.15             | 31.67 ± 1.53             |                             39 |                      39 |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   |                        39 |                         39 |                        39 |                      39 |                        39 | 32.0 ± 2.31              | 36.25 ± 0.96             |                             39 |                      39 |
| gpt-3.5-turbo                                 |                        39 |                         39 |                        39 |                      39 |                        39 | 32.0 ± 1.0               | 36.33 ± 1.53             |                             39 |                      39 |
| meta-llama/Llama-3.1-8B-Instruct              |                        39 |                         39 |                        39 |                      39 |                        39 | 27.33 ± 1.53             | 33.33 ± 0.58             |                             39 |                      39 |
| google/gemma-2-9b-it                          |                        39 |                         39 |                        39 |                      39 |                        39 | 30.0 ± 3.61              | 32.67 ± 1.15             |                             39 |                      39 |



## Set Overview

|   Id | Name                                                           | Dataset           | Model                                         | Model params         | Status          | Created at                 |   Num try |   Num success |
|-----:|:---------------------------------------------------------------|:------------------|:----------------------------------------------|:---------------------|:----------------|:---------------------------|----------:|--------------:|
|  797 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__0         | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  798 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__1         | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  799 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__2         | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  800 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__3         | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  801 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__4         | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  802 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__5         | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  803 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__6         | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  804 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__7         | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  805 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__8         | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  806 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__9         | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  807 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__10        | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
|  808 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__11        | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-04-11T11:15:24.484366 |        39 |            39 |
| 1057 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__12        | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:06.947841 |        39 |            39 |
| 1058 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__14        | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:07.016183 |        39 |            39 |
| 1059 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__16        | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:07.071238 |        39 |            39 |
| 1060 | mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__18        | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:07.126342 |        39 |            39 |
| 1102 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v5__16 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:09:55.657453 |        39 |            39 |
| 1103 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v5__18 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:09:55.744902 |        39 |            39 |
| 1104 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v5__20 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:09:55.825251 |        39 |            39 |


## Details by Experiment

- [Experiment 797](details/experiment_797.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__0
- [Experiment 798](details/experiment_798.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__1
- [Experiment 799](details/experiment_799.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__2
- [Experiment 800](details/experiment_800.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__3
- [Experiment 801](details/experiment_801.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__4
- [Experiment 802](details/experiment_802.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__5
- [Experiment 803](details/experiment_803.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__6
- [Experiment 804](details/experiment_804.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__7
- [Experiment 805](details/experiment_805.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__8
- [Experiment 806](details/experiment_806.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__9
- [Experiment 807](details/experiment_807.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__10
- [Experiment 808](details/experiment_808.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__11
- [Experiment 1057](details/experiment_1057.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__12
- [Experiment 1058](details/experiment_1058.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__14
- [Experiment 1059](details/experiment_1059.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__16
- [Experiment 1060](details/experiment_1060.md) - mfs_with_judge_meta-llama/Llama-3.3-70B-Instruct_v1__18
- [Experiment 1102](details/experiment_1102.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v5__16
- [Experiment 1103](details/experiment_1103.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v5__18
- [Experiment 1104](details/experiment_1104.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v5__20
