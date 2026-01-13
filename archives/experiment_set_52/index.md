---
id: 52
name: "mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v5"
date: 2025-04-15T13:52:22.141128
description: ""
tags: []
---

# Experiment Set: mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v5 (ID: 52)

Comparing impact of judge in score calculation. Here : deepseek-ai/DeepSeek-R1-Distill-Qwen-32B

**Finished**: 98%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: deepseek-ai/DeepSeek-R1-Distill-Qwen-32B

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | judge_completude   | judge_exactness   | judge_notator   | judge_precision   | judge_rambling   | judge_relevant   | nb_tokens_completion   | output_length   |
|:----------------------------------------------|:------------------|:-------------------|:------------------|:----------------|:------------------|:-----------------|:-----------------|:-----------------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 19.98 ± 1.68      | 64.06 ± 2.94       | 0.54 ± 0.07       | 7.91 ± 0.26     | 0.54 ± 0.07       | 5.29 ± 0.19      | 7.68 ± 0.34      | 552.35 ± 6.27          | 358.9 ± 3.83    |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | 17.44 ± 0.78      | 53.85 ± 3.91       | 0.41 ± 0.02       | 7.06 ± 0.16     | 0.39 ± 0.04       | 4.6 ± 0.14       | 7.05 ± 0.32      | 442.16 ± 3.7           | 265.19 ± 1.34   |
| gpt-3.5-turbo                                 | 3.06 ± 0.44       | 57.99 ± 3.31       | 0.42 ± 0.01       | 7.15 ± 0.17     | 0.34 ± 0.04       | 3.84 ± 0.25      | 6.77 ± 0.05      | 247.56 ± 56.23         | 146.21 ± 28.84  |
| google/gemma-2-9b-it                          | 7.93 ± 0.89       | 45.9 ± 3.21        | 0.29 ± 0.03       | 6.44 ± 0.18     | 0.28 ± 0.0        | 5.44 ± 0.28      | 5.8 ± 0.24       | 350.12 ± 9.29          | 232.49 ± 4.24   |
| meta-llama/Llama-3.1-8B-Instruct              | 6.64 ± 0.16       | 47.91 ± 2.97       | 0.22 ± 0.01       | 6.6 ± 0.2       | 0.24 ± 0.04       | 5.61 ± 0.28      | 5.51 ± 0.07      | 479.08 ± 6.2           | 291.74 ± 2.67   |
| meta-llama/Llama-3.3-70B-Instruct             | 15.38 ± 0.37      | 49.79 ± 2.18       | 0.33 ± 0.0        | 6.9 ± 0.11      | 0.24 ± 0.03       | 5.08 ± 0.41      | 6.03 ± 0.28      | 552.59 ± 6.85          | 333.32 ± 2.76   |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         |   generation_time_support |   judge_completude_support |   judge_exactness_support |   judge_notator_support |   judge_precision_support | judge_rambling_support   | judge_relevant_support   |   nb_tokens_completion_support |   output_length_support |
|:----------------------------------------------|--------------------------:|---------------------------:|--------------------------:|------------------------:|--------------------------:|:-------------------------|:-------------------------|-------------------------------:|------------------------:|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 |                        39 |                         39 |                        39 |                      39 |                        39 | 38.67 ± 0.58             | 36.0 ± 2.65              |                             39 |                      39 |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   |                        39 |                         39 |                        39 |                      39 |                        39 | 36.75 ± 0.96             | 33.25 ± 0.96             |                             39 |                      39 |
| gpt-3.5-turbo                                 |                        39 |                         39 |                        39 |                      39 |                        39 | 37.67 ± 1.15             | 35.0 ± 1.0               |                             39 |                      39 |
| google/gemma-2-9b-it                          |                        39 |                         39 |                        39 |                      39 |                        39 | 39.0 ± 0.0               | 37.33 ± 1.15             |                             39 |                      39 |
| meta-llama/Llama-3.1-8B-Instruct              |                        39 |                         39 |                        39 |                      39 |                        39 | 38.67 ± 0.58             | 36.0 ± 1.73              |                             39 |                      39 |
| meta-llama/Llama-3.3-70B-Instruct             |                        39 |                         39 |                        39 |                      39 |                        39 | 32.33 ± 0.58             | 28.0 ± 1.73              |                             39 |                      39 |



## Set Overview

|   Id | Name                                                           | Dataset           | Model                                         | Model params         | Status          | Created at                 |   Num try |   Num success |
|-----:|:---------------------------------------------------------------|:------------------|:----------------------------------------------|:---------------------|:----------------|:---------------------------|----------:|--------------:|
| 1005 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__0  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1006 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__1  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1007 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__2  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1008 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1009 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__4  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1010 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__5  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1011 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__6  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1012 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__7  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1013 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__8  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1014 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__9  | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1015 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__10 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1016 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__11 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-04-15T13:52:22.141128 |        39 |            39 |
| 1049 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__12 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:06.213012 |        39 |            39 |
| 1050 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__14 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:06.298350 |        39 |            39 |
| 1051 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__16 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:06.358382 |        39 |            39 |
| 1052 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__18 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:06.415016 |        39 |            39 |
| 1099 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v4__16 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:07:47.082393 |        39 |            39 |
| 1100 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v4__18 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:07:47.158772 |        39 |            39 |
| 1101 | mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v4__20 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:07:47.220089 |        39 |            39 |


## Details by Experiment

- [Experiment 1005](details/experiment_1005.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__0
- [Experiment 1006](details/experiment_1006.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__1
- [Experiment 1007](details/experiment_1007.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__2
- [Experiment 1008](details/experiment_1008.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__3
- [Experiment 1009](details/experiment_1009.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__4
- [Experiment 1010](details/experiment_1010.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__5
- [Experiment 1011](details/experiment_1011.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__6
- [Experiment 1012](details/experiment_1012.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__7
- [Experiment 1013](details/experiment_1013.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__8
- [Experiment 1014](details/experiment_1014.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__9
- [Experiment 1015](details/experiment_1015.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__10
- [Experiment 1016](details/experiment_1016.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__11
- [Experiment 1049](details/experiment_1049.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__12
- [Experiment 1050](details/experiment_1050.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__14
- [Experiment 1051](details/experiment_1051.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__16
- [Experiment 1052](details/experiment_1052.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v3__18
- [Experiment 1099](details/experiment_1099.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v4__16
- [Experiment 1100](details/experiment_1100.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v4__18
- [Experiment 1101](details/experiment_1101.md) - mfs_with_judge_deepseek-ai/DeepSeek-R1-Distill-Qwen-32B_v4__20
