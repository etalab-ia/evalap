---
id: 24
name: "temperature_impact_v1"
date: 2025-03-28T12:14:03.815641
description: ""
tags: []
---

# Experiment Set: temperature_impact_v1 (ID: 24)

Compare models stability for different temperatures and prompts.

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | answer_relevancy   | generation_time   | judge_exactness   | judge_notator   | output_length   |
|:----------------------------------------------|:-------------------|:------------------|:------------------|:----------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.81 ± 0.02        | 15.69 ± 2.7       | 0.09 ± 0.03       | 5.7 ± 0.32      | 307.2 ± 56.3    |



## Set Overview

|   Id | Name                      | Dataset           | Model                                         | Model params                               | Status   | Created at                 |   Num try |   Num success |
|-----:|:--------------------------|:------------------|:----------------------------------------------|:-------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  507 | temperature_impact_v1__0  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                                         | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  508 | temperature_impact_v1__1  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                                         | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  509 | temperature_impact_v1__2  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                                         | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  510 | temperature_impact_v1__3  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                                         | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  511 | temperature_impact_v1__4  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {}                                         | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  512 | temperature_impact_v1__5  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'}                     | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  513 | temperature_impact_v1__6  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'}                     | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  514 | temperature_impact_v1__7  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'}                     | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  515 | temperature_impact_v1__8  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'}                     | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  516 | temperature_impact_v1__9  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'sys_prompt': '7341'}                     | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  517 | temperature_impact_v1__10 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  518 | temperature_impact_v1__11 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  519 | temperature_impact_v1__12 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  520 | temperature_impact_v1__13 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  521 | temperature_impact_v1__14 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  522 | temperature_impact_v1__15 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7341'} | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  523 | temperature_impact_v1__16 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7341'} | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  524 | temperature_impact_v1__17 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7341'} | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  525 | temperature_impact_v1__18 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7341'} | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |
|  526 | temperature_impact_v1__19 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '7341'} | finished | 2025-03-28T12:14:03.815641 |        39 |            39 |


## Details by Experiment

- [Experiment 507](details/experiment_507.md) - temperature_impact_v1__0
- [Experiment 508](details/experiment_508.md) - temperature_impact_v1__1
- [Experiment 509](details/experiment_509.md) - temperature_impact_v1__2
- [Experiment 510](details/experiment_510.md) - temperature_impact_v1__3
- [Experiment 511](details/experiment_511.md) - temperature_impact_v1__4
- [Experiment 512](details/experiment_512.md) - temperature_impact_v1__5
- [Experiment 513](details/experiment_513.md) - temperature_impact_v1__6
- [Experiment 514](details/experiment_514.md) - temperature_impact_v1__7
- [Experiment 515](details/experiment_515.md) - temperature_impact_v1__8
- [Experiment 516](details/experiment_516.md) - temperature_impact_v1__9
- [Experiment 517](details/experiment_517.md) - temperature_impact_v1__10
- [Experiment 518](details/experiment_518.md) - temperature_impact_v1__11
- [Experiment 519](details/experiment_519.md) - temperature_impact_v1__12
- [Experiment 520](details/experiment_520.md) - temperature_impact_v1__13
- [Experiment 521](details/experiment_521.md) - temperature_impact_v1__14
- [Experiment 522](details/experiment_522.md) - temperature_impact_v1__15
- [Experiment 523](details/experiment_523.md) - temperature_impact_v1__16
- [Experiment 524](details/experiment_524.md) - temperature_impact_v1__17
- [Experiment 525](details/experiment_525.md) - temperature_impact_v1__18
- [Experiment 526](details/experiment_526.md) - temperature_impact_v1__19
