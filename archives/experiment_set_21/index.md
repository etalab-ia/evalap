---
id: 21
name: "mfs_vllm_arena_v2"
date: 2025-03-22T01:04:02.485131
description: ""
tags: []
---

# Experiment Set: mfs_vllm_arena_v2 (ID: 21)

Experiment set for mfs_vllm_arena

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | answer_relevancy   | generation_time   | judge_exactness   | judge_notator   | output_length   |
|:----------------------------------------------|:-------------------|:------------------|:------------------|:----------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.82 ± 0.02        | 15.51 ± 2.82      | 0.07 ± 0.04       | 5.7 ± 0.38      | 305.07 ± 59.58  |
| google/gemma-3-27b-it                         | 0.8 ± 0.03         | 18.26 ± 8.43      | 0.08 ± 0.07       | 5.52 ± 0.37     | 429.7 ± 203.35  |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | 0.89 ± 0.02        | 15.36 ± 1.79      | 0.09 ± 0.02       | 4.94 ± 0.37     | 227.52 ± 24.21  |
| meta-llama/Llama-3.1-8B-Instruct              | 0.81 ± 0.03        | 5.79 ± 0.67       | 0.04 ± 0.03       | 3.68 ± 0.2      | 264.15 ± 30.4   |



## Set Overview

|   Id | Name                  | Dataset           | Model                                         | Model params           | Status   | Created at                 |   Num try |   Num success |
|-----:|:----------------------|:------------------|:----------------------------------------------|:-----------------------|:---------|:---------------------------|----------:|--------------:|
|  399 | mfs_vllm_arena__0     | MFS_questions_v01 | google/gemma-3-27b-it                         | {}                     | finished | 2025-03-22T01:04:02.485131 |        39 |            39 |
|  400 | mfs_vllm_arena__1     | MFS_questions_v01 | google/gemma-3-27b-it                         | {}                     | finished | 2025-03-22T01:04:02.485131 |        39 |            39 |
|  401 | mfs_vllm_arena__2     | MFS_questions_v01 | google/gemma-3-27b-it                         | {}                     | finished | 2025-03-22T01:04:02.485131 |        39 |            39 |
|  402 | mfs_vllm_arena__3     | MFS_questions_v01 | google/gemma-3-27b-it                         | {}                     | finished | 2025-03-22T01:04:02.485131 |        39 |            39 |
|  403 | mfs_vllm_arena__4     | MFS_questions_v01 | google/gemma-3-27b-it                         | {}                     | finished | 2025-03-22T01:04:02.485131 |        39 |            39 |
|  404 | mfs_vllm_arena__5     | MFS_questions_v01 | google/gemma-3-27b-it                         | {'sys_prompt': '7341'} | finished | 2025-03-24T00:14:18.680363 |        39 |            39 |
|  405 | mfs_vllm_arena__7     | MFS_questions_v01 | google/gemma-3-27b-it                         | {'sys_prompt': '7341'} | finished | 2025-03-24T00:14:20.524853 |        39 |            39 |
|  406 | mfs_vllm_arena__9     | MFS_questions_v01 | google/gemma-3-27b-it                         | {'sys_prompt': '7341'} | finished | 2025-03-24T00:14:22.360999 |        39 |            39 |
|  407 | mfs_vllm_arena__11    | MFS_questions_v01 | google/gemma-3-27b-it                         | {'sys_prompt': '7341'} | finished | 2025-03-24T00:14:23.796879 |        39 |            39 |
|  448 | mfs_vllm_arena_v2__9  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                     | finished | 2025-03-27T18:28:07.368878 |        39 |            39 |
|  449 | mfs_vllm_arena_v2__11 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                     | finished | 2025-03-27T18:28:07.529234 |        39 |            39 |
|  450 | mfs_vllm_arena_v2__13 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                     | finished | 2025-03-27T18:28:07.614657 |        39 |            39 |
|  451 | mfs_vllm_arena_v2__15 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                     | finished | 2025-03-27T18:28:07.672850 |        39 |            39 |
|  452 | mfs_vllm_arena_v2__17 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                     | finished | 2025-03-27T18:28:07.730564 |        39 |            39 |
|  453 | mfs_vllm_arena_v2__19 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                     | finished | 2025-03-27T18:28:07.787025 |        39 |            39 |
|  454 | mfs_vllm_arena_v2__21 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                     | finished | 2025-03-27T18:28:07.846121 |        39 |            39 |
|  455 | mfs_vllm_arena_v2__23 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                     | finished | 2025-03-27T18:28:07.903038 |        39 |            39 |
|  456 | mfs_vllm_arena_v2__25 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {}                     | finished | 2025-03-27T18:28:07.954342 |        39 |            39 |
|  457 | mfs_vllm_arena_v2__27 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {}                     | finished | 2025-03-27T18:28:08.009866 |        39 |            39 |
|  458 | mfs_vllm_arena_v2__29 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {}                     | finished | 2025-03-27T18:28:08.066052 |        39 |            39 |
|  459 | mfs_vllm_arena_v2__31 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {}                     | finished | 2025-03-27T18:28:08.116673 |        39 |            39 |
|  460 | mfs_vllm_arena_v2__33 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {}                     | finished | 2025-03-27T18:28:08.165662 |        39 |            39 |
|  461 | mfs_vllm_arena_v2__35 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {}                     | finished | 2025-03-27T18:28:08.221689 |        39 |            39 |
|  462 | mfs_vllm_arena_v2__37 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {}                     | finished | 2025-03-27T18:28:08.287138 |        39 |            39 |
|  463 | mfs_vllm_arena_v2__39 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {}                     | finished | 2025-03-27T18:28:08.347136 |        39 |            39 |
|  464 | mfs_vllm_arena_v2__41 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.397707 |        39 |            39 |
|  465 | mfs_vllm_arena_v2__43 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.448650 |        39 |            39 |
|  466 | mfs_vllm_arena_v2__45 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.499385 |        39 |            39 |
|  467 | mfs_vllm_arena_v2__47 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.549803 |        39 |            39 |
|  468 | mfs_vllm_arena_v2__49 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.602949 |        39 |            39 |
|  469 | mfs_vllm_arena_v2__51 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.657390 |        39 |            39 |
|  470 | mfs_vllm_arena_v2__53 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.713078 |        39 |            39 |
|  471 | mfs_vllm_arena_v2__55 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.780367 |        39 |            39 |
|  472 | mfs_vllm_arena_v2__57 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.838999 |        39 |            39 |
|  473 | mfs_vllm_arena_v2__59 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.893624 |        39 |            39 |
|  474 | mfs_vllm_arena_v2__61 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.947195 |        39 |            39 |
|  475 | mfs_vllm_arena_v2__63 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:08.999505 |        39 |            39 |
|  476 | mfs_vllm_arena_v2__65 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:09.052426 |        39 |            39 |
|  477 | mfs_vllm_arena_v2__67 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:09.106594 |        39 |            39 |
|  478 | mfs_vllm_arena_v2__69 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:09.157407 |        39 |            39 |
|  479 | mfs_vllm_arena_v2__71 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8   | {'sys_prompt': '7341'} | finished | 2025-03-27T18:28:09.208276 |        39 |            39 |


## Details by Experiment

- [Experiment 399](details/experiment_399.md) - mfs_vllm_arena__0
- [Experiment 400](details/experiment_400.md) - mfs_vllm_arena__1
- [Experiment 401](details/experiment_401.md) - mfs_vllm_arena__2
- [Experiment 402](details/experiment_402.md) - mfs_vllm_arena__3
- [Experiment 403](details/experiment_403.md) - mfs_vllm_arena__4
- [Experiment 404](details/experiment_404.md) - mfs_vllm_arena__5
- [Experiment 405](details/experiment_405.md) - mfs_vllm_arena__7
- [Experiment 406](details/experiment_406.md) - mfs_vllm_arena__9
- [Experiment 407](details/experiment_407.md) - mfs_vllm_arena__11
- [Experiment 448](details/experiment_448.md) - mfs_vllm_arena_v2__9
- [Experiment 449](details/experiment_449.md) - mfs_vllm_arena_v2__11
- [Experiment 450](details/experiment_450.md) - mfs_vllm_arena_v2__13
- [Experiment 451](details/experiment_451.md) - mfs_vllm_arena_v2__15
- [Experiment 452](details/experiment_452.md) - mfs_vllm_arena_v2__17
- [Experiment 453](details/experiment_453.md) - mfs_vllm_arena_v2__19
- [Experiment 454](details/experiment_454.md) - mfs_vllm_arena_v2__21
- [Experiment 455](details/experiment_455.md) - mfs_vllm_arena_v2__23
- [Experiment 456](details/experiment_456.md) - mfs_vllm_arena_v2__25
- [Experiment 457](details/experiment_457.md) - mfs_vllm_arena_v2__27
- [Experiment 458](details/experiment_458.md) - mfs_vllm_arena_v2__29
- [Experiment 459](details/experiment_459.md) - mfs_vllm_arena_v2__31
- [Experiment 460](details/experiment_460.md) - mfs_vllm_arena_v2__33
- [Experiment 461](details/experiment_461.md) - mfs_vllm_arena_v2__35
- [Experiment 462](details/experiment_462.md) - mfs_vllm_arena_v2__37
- [Experiment 463](details/experiment_463.md) - mfs_vllm_arena_v2__39
- [Experiment 464](details/experiment_464.md) - mfs_vllm_arena_v2__41
- [Experiment 465](details/experiment_465.md) - mfs_vllm_arena_v2__43
- [Experiment 466](details/experiment_466.md) - mfs_vllm_arena_v2__45
- [Experiment 467](details/experiment_467.md) - mfs_vllm_arena_v2__47
- [Experiment 468](details/experiment_468.md) - mfs_vllm_arena_v2__49
- [Experiment 469](details/experiment_469.md) - mfs_vllm_arena_v2__51
- [Experiment 470](details/experiment_470.md) - mfs_vllm_arena_v2__53
- [Experiment 471](details/experiment_471.md) - mfs_vllm_arena_v2__55
- [Experiment 472](details/experiment_472.md) - mfs_vllm_arena_v2__57
- [Experiment 473](details/experiment_473.md) - mfs_vllm_arena_v2__59
- [Experiment 474](details/experiment_474.md) - mfs_vllm_arena_v2__61
- [Experiment 475](details/experiment_475.md) - mfs_vllm_arena_v2__63
- [Experiment 476](details/experiment_476.md) - mfs_vllm_arena_v2__65
- [Experiment 477](details/experiment_477.md) - mfs_vllm_arena_v2__67
- [Experiment 478](details/experiment_478.md) - mfs_vllm_arena_v2__69
- [Experiment 479](details/experiment_479.md) - mfs_vllm_arena_v2__71
