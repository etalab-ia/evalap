---
id: 9
name: "SPP_experiments"
date: 2025-01-15T13:31:50.937246
description: ""
tags: []
---

# Experiment Set: SPP_experiments (ID: 9)

Testing different configurations for SPP : base models, finetuning, fulltuning, rag and no rag architectures.

**Finished**: 100%

## Scores

**Dataset**: SPP_Llama8B_31_LoRA_32_64_3____v2 (Size: 74)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics

| model                      |   judge_exactness |   judge_notator |
|:---------------------------|------------------:|----------------:|
| Llama3.1_lora_32_64_3___v2 |          0.121622 |         5.81081 |


**Dataset**: SPP_Llama8B_31_LoRA_32_64_3__v2 (Size: 74)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics

| model                     |   judge_exactness |   judge_notator |
|:--------------------------|------------------:|----------------:|
| Llama3.1_lora_32_64_3__v2 |          0.108108 |         5.82432 |


**Dataset**: SPP_Llama8B_31_LoRA_32_64_3_v2 (Size: 74)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics

| model                    |   judge_exactness |   judge_notator |
|:-------------------------|------------------:|----------------:|
| Llama3.1_lora_32_64_3_v2 |          0.108108 |         5.81081 |


**Dataset**: SPP_Llama8B_31_Fullfine_3 (Size: 89)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics

| model                                        |   judge_exactness |   judge_notator |
|:---------------------------------------------|------------------:|----------------:|
| Undefined model (SPP_Llama8B_3.1_Fullfine_3) |          0.146067 |         5.93258 |


**Dataset**: SPP_Llama8B_31_Fullfine (Size: 89)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics

| model                                        |   judge_exactness |   judge_notator |
|:---------------------------------------------|------------------:|----------------:|
| Undefined model (SPP_Llama8B_3.1_Fullfine_1) |          0.101124 |         5.50562 |


**Dataset**: SPP_Llama8B_31_LoRa_3264_3 (Size: 89)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics

| model                                         |   judge_exactness |   judge_notator |
|:----------------------------------------------|------------------:|----------------:|
| Undefined model (SPP_Llama8B_3.1_LoRa_3264_3) |         0.0898876 |          5.5618 |


**Dataset**: SPP_Albert_Prod (Size: 89)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics

| model                             |   judge_exactness |   judge_notator |
|:----------------------------------|------------------:|----------------:|
| Undefined model (SPP_Albert_Prod) |                 0 |         1.07865 |


**Dataset**: SPP_llama3.1_8B_finetune_lora_32_64_3_bigger (Size: 89)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics

| model                                                          |   judge_exactness |   judge_notator |
|:---------------------------------------------------------------|------------------:|----------------:|
| Undefined model (SPP_llama3.1_8B_finetune_lora_32_64_3_bigger) |          0.179775 |         5.95506 |



## Set Overview

|   Id | Name                                         | Dataset                                      | Model                      | Model params   | Status   | Created at                 |   Num try |   Num success |
|-----:|:---------------------------------------------|:---------------------------------------------|:---------------------------|:---------------|:---------|:---------------------------|----------:|--------------:|
|  182 | SPP_llama3.1_8B_finetune_lora_32_64_3_bigger | SPP_llama3.1_8B_finetune_lora_32_64_3_bigger |                            | {}             | finished | 2025-01-15T14:06:57.443140 |        89 |            89 |
|  185 | SPP_Albert_Prod                              | SPP_Albert_Prod                              |                            | {}             | finished | 2025-01-20T16:41:41.613850 |        89 |            89 |
|  186 | SPP_Llama8B_3.1_LoRa_3264_3                  | SPP_Llama8B_31_LoRa_3264_3                   |                            | {}             | finished | 2025-01-20T17:13:26.698223 |        89 |            89 |
|  187 | SPP_Llama8B_3.1_Fullfine_1                   | SPP_Llama8B_31_Fullfine                      |                            | {}             | finished | 2025-01-21T15:09:34.856637 |        89 |            89 |
|  188 | SPP_Llama8B_3.1_Fullfine_3                   | SPP_Llama8B_31_Fullfine_3                    |                            | {}             | finished | 2025-01-21T15:59:13.170151 |        89 |            89 |
|  408 | SPP_Llama8B_3.1_lora_32_64_3_v2              | SPP_Llama8B_31_LoRA_32_64_3_v2               | Llama3.1_lora_32_64_3_v2   | {}             | finished | 2025-03-24T15:34:06.598263 |        74 |            74 |
|  411 | SPP_Llama8B_3.1_lora_32_64_3__v2             | SPP_Llama8B_31_LoRA_32_64_3__v2              | Llama3.1_lora_32_64_3__v2  | {}             | finished | 2025-03-24T15:35:05.785479 |        74 |            74 |
|  414 | SPP_Llama8B_3.1_lora_32_64_3___v2            | SPP_Llama8B_31_LoRA_32_64_3____v2            | Llama3.1_lora_32_64_3___v2 | {}             | finished | 2025-03-24T15:35:25.701198 |        74 |            74 |


## Details by Experiment

- [Experiment 182](details/experiment_182.md) - SPP_llama3.1_8B_finetune_lora_32_64_3_bigger
- [Experiment 185](details/experiment_185.md) - SPP_Albert_Prod
- [Experiment 186](details/experiment_186.md) - SPP_Llama8B_3.1_LoRa_3264_3
- [Experiment 187](details/experiment_187.md) - SPP_Llama8B_3.1_Fullfine_1
- [Experiment 188](details/experiment_188.md) - SPP_Llama8B_3.1_Fullfine_3
- [Experiment 408](details/experiment_408.md) - SPP_Llama8B_3.1_lora_32_64_3_v2
- [Experiment 411](details/experiment_411.md) - SPP_Llama8B_3.1_lora_32_64_3__v2
- [Experiment 414](details/experiment_414.md) - SPP_Llama8B_3.1_lora_32_64_3___v2
