---
id: 16
name: "mfs_variability_v3"
date: 2025-03-07T21:53:51.946211
description: ""
tags: []
---

# Experiment Set: mfs_variability_v3 (ID: 16)

Comparing some models variability.

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | answer_relevancy   | generation_time   | judge_exactness   | judge_notator   | output_length   |
|:----------------------------------------------|:-------------------|:------------------|:------------------|:----------------|:----------------|
| AgentPublic/llama3-instruct-guillaumetell     | 0.8 ± 0.02         | 5.72 ± 0.65       | 0.1 ± 0.03        | 5.39 ± 0.13     | 133.86 ± 2.83   |
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.81 ± 0.02        | 19.93 ± 3.2       | 0.06 ± 0.03       | 5.38 ± 0.07     | 366.9 ± 6.8     |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | 0.87 ± 0.03        | 18.14 ± 2.9       | 0.04 ± 0.01       | 4.74 ± 0.18     | 267.64 ± 4.95   |
| meta-llama/Llama-3.1-8B-Instruct              | 0.8 ± 0.06         | 5.88 ± 0.65       | 0.05 ± 0.04       | 4.34 ± 0.8      | 211.56 ± 86.58  |
| google/gemma-2-9b-it                          | 0.78 ± 0.03        | 5.92 ± 0.23       | 0.05 ± 0.03       | 4.27 ± 0.13     | 229.31 ± 6.48   |
| meta-llama/Llama-3.3-70B-Instruct             | 0.85 ± 0.02        | 12.71 ± 0.2       | 0.03 ± 0.03       | 4.15 ± 0.12     | 344.6 ± 3.0     |
| deepseek-ai/DeepSeek-R1-Distill-Qwen-32B      | 0.85 ± 0.03        | 18.86 ± 0.54      | 0.03 ± 0.01       | 3.99 ± 0.08     | 830.29 ± 21.77  |
| meta-llama/Llama-3.2-3B-Instruct              | 0.72 ± 0.06        | 2.72 ± 0.13       | 0.01 ± 0.01       | 2.87 ± 0.06     | 319.26 ± 12.72  |



## Set Overview

|   Id | Name                   | Dataset           | Model                                         | Model params                                             | Status   | Created at                 |   Num try |   Num success |
|-----:|:-----------------------|:------------------|:----------------------------------------------|:---------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  322 | mfs_variability_v3__0  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  323 | mfs_variability_v3__1  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  324 | mfs_variability_v3__2  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  325 | mfs_variability_v3__3  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  326 | mfs_variability_v3__4  | MFS_questions_v01 | google/gemma-2-9b-it                          | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  327 | mfs_variability_v3__5  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  328 | mfs_variability_v3__6  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  329 | mfs_variability_v3__7  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  330 | mfs_variability_v3__8  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  331 | mfs_variability_v3__9  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  332 | mfs_variability_v3__10 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct              | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  333 | mfs_variability_v3__11 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct              | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  334 | mfs_variability_v3__12 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct              | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  335 | mfs_variability_v3__13 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct              | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  336 | mfs_variability_v3__14 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct              | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  337 | mfs_variability_v3__15 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  338 | mfs_variability_v3__16 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  339 | mfs_variability_v3__17 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  340 | mfs_variability_v3__18 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  341 | mfs_variability_v3__19 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  342 | mfs_variability_v3__20 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  343 | mfs_variability_v3__21 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  344 | mfs_variability_v3__22 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  345 | mfs_variability_v3__23 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  346 | mfs_variability_v3__24 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct             | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  347 | mfs_variability_v3__25 | MFS_questions_v01 | deepseek-ai/DeepSeek-R1-Distill-Qwen-32B      | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  348 | mfs_variability_v3__26 | MFS_questions_v01 | deepseek-ai/DeepSeek-R1-Distill-Qwen-32B      | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  349 | mfs_variability_v3__27 | MFS_questions_v01 | deepseek-ai/DeepSeek-R1-Distill-Qwen-32B      | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  350 | mfs_variability_v3__28 | MFS_questions_v01 | deepseek-ai/DeepSeek-R1-Distill-Qwen-32B      | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  351 | mfs_variability_v3__29 | MFS_questions_v01 | deepseek-ai/DeepSeek-R1-Distill-Qwen-32B      | {'temperature': 0.2}                                     | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  352 | mfs_variability_v3__30 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  353 | mfs_variability_v3__31 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  354 | mfs_variability_v3__32 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  355 | mfs_variability_v3__33 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  356 | mfs_variability_v3__34 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  357 | mfs_variability_v3__35 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell     | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  358 | mfs_variability_v3__36 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell     | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  359 | mfs_variability_v3__37 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell     | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  360 | mfs_variability_v3__38 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell     | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  361 | mfs_variability_v3__39 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell     | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-03-07T21:53:51.946211 |        39 |            39 |
|  417 | mfs_variability_v3__40 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                                     | finished | 2025-03-26T09:40:02.802772 |        39 |            39 |
|  418 | mfs_variability_v3__42 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                                     | finished | 2025-03-26T09:40:02.939251 |        39 |            39 |
|  419 | mfs_variability_v3__44 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                                     | finished | 2025-03-26T09:40:03.019077 |        39 |            39 |
|  420 | mfs_variability_v3__46 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                                     | finished | 2025-03-26T09:40:03.075320 |        39 |            39 |
|  421 | mfs_variability_v3__48 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                                     | finished | 2025-03-26T09:40:03.129536 |        39 |            39 |


## Details by Experiment

- [Experiment 322](details/experiment_322.md) - mfs_variability_v3__0
- [Experiment 323](details/experiment_323.md) - mfs_variability_v3__1
- [Experiment 324](details/experiment_324.md) - mfs_variability_v3__2
- [Experiment 325](details/experiment_325.md) - mfs_variability_v3__3
- [Experiment 326](details/experiment_326.md) - mfs_variability_v3__4
- [Experiment 327](details/experiment_327.md) - mfs_variability_v3__5
- [Experiment 328](details/experiment_328.md) - mfs_variability_v3__6
- [Experiment 329](details/experiment_329.md) - mfs_variability_v3__7
- [Experiment 330](details/experiment_330.md) - mfs_variability_v3__8
- [Experiment 331](details/experiment_331.md) - mfs_variability_v3__9
- [Experiment 332](details/experiment_332.md) - mfs_variability_v3__10
- [Experiment 333](details/experiment_333.md) - mfs_variability_v3__11
- [Experiment 334](details/experiment_334.md) - mfs_variability_v3__12
- [Experiment 335](details/experiment_335.md) - mfs_variability_v3__13
- [Experiment 336](details/experiment_336.md) - mfs_variability_v3__14
- [Experiment 337](details/experiment_337.md) - mfs_variability_v3__15
- [Experiment 338](details/experiment_338.md) - mfs_variability_v3__16
- [Experiment 339](details/experiment_339.md) - mfs_variability_v3__17
- [Experiment 340](details/experiment_340.md) - mfs_variability_v3__18
- [Experiment 341](details/experiment_341.md) - mfs_variability_v3__19
- [Experiment 342](details/experiment_342.md) - mfs_variability_v3__20
- [Experiment 343](details/experiment_343.md) - mfs_variability_v3__21
- [Experiment 344](details/experiment_344.md) - mfs_variability_v3__22
- [Experiment 345](details/experiment_345.md) - mfs_variability_v3__23
- [Experiment 346](details/experiment_346.md) - mfs_variability_v3__24
- [Experiment 347](details/experiment_347.md) - mfs_variability_v3__25
- [Experiment 348](details/experiment_348.md) - mfs_variability_v3__26
- [Experiment 349](details/experiment_349.md) - mfs_variability_v3__27
- [Experiment 350](details/experiment_350.md) - mfs_variability_v3__28
- [Experiment 351](details/experiment_351.md) - mfs_variability_v3__29
- [Experiment 352](details/experiment_352.md) - mfs_variability_v3__30
- [Experiment 353](details/experiment_353.md) - mfs_variability_v3__31
- [Experiment 354](details/experiment_354.md) - mfs_variability_v3__32
- [Experiment 355](details/experiment_355.md) - mfs_variability_v3__33
- [Experiment 356](details/experiment_356.md) - mfs_variability_v3__34
- [Experiment 357](details/experiment_357.md) - mfs_variability_v3__35
- [Experiment 358](details/experiment_358.md) - mfs_variability_v3__36
- [Experiment 359](details/experiment_359.md) - mfs_variability_v3__37
- [Experiment 360](details/experiment_360.md) - mfs_variability_v3__38
- [Experiment 361](details/experiment_361.md) - mfs_variability_v3__39
- [Experiment 417](details/experiment_417.md) - mfs_variability_v3__40
- [Experiment 418](details/experiment_418.md) - mfs_variability_v3__42
- [Experiment 419](details/experiment_419.md) - mfs_variability_v3__44
- [Experiment 420](details/experiment_420.md) - mfs_variability_v3__46
- [Experiment 421](details/experiment_421.md) - mfs_variability_v3__48
