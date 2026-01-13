---
id: 56
name: "mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v5"
date: 2025-04-25T15:04:35.545588
description: ""
tags: []
---

# Experiment Set: mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v5 (ID: 56)

Comparing impact of judge in score calculation. Here : mistralai/Mistral-Small-3.1-24B-Instruct-2503

**Finished**: 64%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: mistralai/Mistral-Small-3.1-24B-Instruct-2503

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | judge_completude   | judge_exactness   | judge_notator   | judge_precision   |   judge_relevant | nb_tokens_completion   | output_length   |
|:----------------------------------------------|:------------------|:-------------------|:------------------|:----------------|:------------------|-----------------:|:-----------------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 31.04 ± 7.84      | 48.88 ± 1.02       | 0.27 ± 0.04       | 7.24 ± 0.17     | 0.67 ± 0.03       |                8 | 557.94 ± 9.38          | 362.69 ± 6.29   |
| meta-llama/Llama-3.3-70B-Instruct             | 12.85 ± 0.39      | 42.69 ± 1.37       | 0.12 ± 0.04       | 6.73 ± 0.08     | 0.55 ± 0.05       |              nan | 571.77 ± 16.96         | 343.33 ± 10.16  |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | 19.07 ± 3.27      | 44.43 ± 2.03       | 0.18 ± 0.04       | 6.82 ± 0.04     | 0.51 ± 0.06       |              nan | 457.17 ± 14.61         | 273.79 ± 8.93   |
| gpt-3.5-turbo                                 | 3.25 ± 1.1        | 47.13 ± 2.17       | 0.21 ± 0.0        | 7.04 ± 0.05     | 0.5 ± 0.04        |              nan | 250.32 ± 55.75         | 148.79 ± 27.93  |
| meta-llama/Llama-3.1-8B-Instruct              | 6.56 ± 0.15       | 40.42 ± 2.15       | 0.06 ± 0.04       | 6.39 ± 0.1      | 0.35 ± 0.04       |              nan | 487.13 ± 6.95          | 296.45 ± 4.01   |
| google/gemma-2-9b-it                          | nan ± nan         | nan ± nan          | nan ± nan         | nan ± nan       | nan ± nan         |              nan | nan ± nan              | nan ± nan       |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         | generation_time_support   | judge_completude_support   | judge_exactness_support   | judge_notator_support   | judge_precision_support   |   judge_relevant_support | nb_tokens_completion_support   | output_length_support   |
|:----------------------------------------------|:--------------------------|:---------------------------|:--------------------------|:------------------------|:--------------------------|-------------------------:|:-------------------------------|:------------------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 39.0 ± 0.0                | 38.67 ± 0.58               | 39.0 ± 0.0                | 39.0 ± 0.0              | 39.0 ± 0.0                |                        1 | 39.0 ± 0.0                     | 39.0 ± 0.0              |
| meta-llama/Llama-3.3-70B-Instruct             | 39.0 ± 0.0                | 35.0 ± 1.73                | 39.0 ± 0.0                | 39.0 ± 0.0              | 39.0 ± 0.0                |                      nan | 39.0 ± 0.0                     | 39.0 ± 0.0              |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | 38.0 ± 1.41               | 33.75 ± 2.99               | 38.0 ± 1.41               | 38.0 ± 1.41             | 38.0 ± 1.41               |                      nan | 38.0 ± 1.41                    | 38.0 ± 1.41             |
| gpt-3.5-turbo                                 | 39.0 ± 0.0                | 36.67 ± 0.58               | 39.0 ± 0.0                | 39.0 ± 0.0              | 39.0 ± 0.0                |                      nan | 39.0 ± 0.0                     | 39.0 ± 0.0              |
| meta-llama/Llama-3.1-8B-Instruct              | 39.0 ± 0.0                | 38.0 ± 0.0                 | 39.0 ± 0.0                | 39.0 ± 0.0              | 39.0 ± 0.0                |                      nan | 39.0 ± 0.0                     | 39.0 ± 0.0              |
| google/gemma-2-9b-it                          | nan ± nan                 | nan ± nan                  | nan ± nan                 | nan ± nan               | nan ± nan                 |                      nan | nan ± nan                      | nan ± nan               |



## Set Overview

|   Id | Name                                                                | Dataset           | Model                                         | Model params         | Status          | Created at                 |   Num try |   Num success |
|-----:|:--------------------------------------------------------------------|:------------------|:----------------------------------------------|:---------------------|:----------------|:---------------------------|----------:|--------------:|
| 1037 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__0  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-04-25T15:04:35.545588 |        39 |            39 |
| 1038 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__1  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-04-25T15:04:35.545588 |        39 |            39 |
| 1039 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__2  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2} | running_metrics | 2025-04-25T15:04:35.545588 |        39 |            39 |
| 1040 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-04-25T15:04:35.545588 |        39 |            39 |
| 1041 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__4  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-04-25T15:04:35.545588 |        39 |            39 |
| 1042 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__5  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | running_metrics | 2025-04-25T15:04:35.545588 |        39 |            39 |
| 1043 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__6  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | finished        | 2025-04-25T15:04:35.545588 |        39 |             0 |
| 1044 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__7  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | finished        | 2025-04-25T15:04:35.545588 |        39 |             0 |
| 1045 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__8  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2} | finished        | 2025-04-25T15:04:35.545588 |        39 |             0 |
| 1046 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__9  | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-04-25T15:04:35.545588 |        39 |            39 |
| 1047 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__10 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-04-25T15:04:35.545588 |        39 |            39 |
| 1048 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__11 | MFS_questions_v01 | gpt-3.5-turbo                                 | {'temperature': 0.2} | running_metrics | 2025-04-25T15:04:35.545588 |        39 |            39 |
| 1081 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__12 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:09.036731 |        39 |            36 |
| 1082 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__14 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:09.098329 |        39 |            38 |
| 1083 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__16 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:09.150027 |        39 |            39 |
| 1084 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__18 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2} | finished        | 2025-04-30T17:48:09.207659 |        39 |            39 |
| 1111 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v5__16 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:10:52.464015 |        39 |            39 |
| 1112 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v5__18 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:10:52.543960 |        39 |            39 |
| 1113 | mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v5__20 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2} | finished        | 2025-04-30T18:10:52.604653 |        39 |            39 |


## Details by Experiment

- [Experiment 1037](details/experiment_1037.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__0
- [Experiment 1038](details/experiment_1038.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__1
- [Experiment 1039](details/experiment_1039.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__2
- [Experiment 1040](details/experiment_1040.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__3
- [Experiment 1041](details/experiment_1041.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__4
- [Experiment 1042](details/experiment_1042.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__5
- [Experiment 1043](details/experiment_1043.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__6
- [Experiment 1044](details/experiment_1044.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__7
- [Experiment 1045](details/experiment_1045.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__8
- [Experiment 1046](details/experiment_1046.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__9
- [Experiment 1047](details/experiment_1047.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__10
- [Experiment 1048](details/experiment_1048.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__11
- [Experiment 1081](details/experiment_1081.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__12
- [Experiment 1082](details/experiment_1082.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__14
- [Experiment 1083](details/experiment_1083.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__16
- [Experiment 1084](details/experiment_1084.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v2__18
- [Experiment 1111](details/experiment_1111.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v5__16
- [Experiment 1112](details/experiment_1112.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v5__18
- [Experiment 1113](details/experiment_1113.md) - mfs_with_judge_mistralai/Mistral-Small-3.1-24B-Instruct-2503_v5__20
