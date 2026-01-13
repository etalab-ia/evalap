---
id: 109
name: "Comparing Mistral-Medium on piaf"
date: 2025-12-12T10:46:12.113794
description: ""
tags: []
---

# Experiment Set: Comparing Mistral-Medium on piaf (ID: 109)

Comparing Mistral-Medium in different instances on piaf dataset

**Finished**: 99%

## Scores

**Dataset**: piaf-v1.2 (Size: 9224)

**Judge model**: openai/gpt-oss-120b

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                   | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   | nb_tokens_prompt   |
|:------------------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|:-------------------|
| mistral-medium Albert   | 0.0001 ± 0.0         | 2.02 ± 0.64       | 0.0 ± 0.0         | 3.89 ± 0.01     | 0.1 ± 0.0         | 14.49 ± 0.06           | 25.94 ± 0.0        |
| mistral-medium Oustcale | 0.0001 ± 0.0         | 0.31 ± 0.03       | 0.0001 ± 0.0      | 3.89 ± 0.0      | 0.1 ± 0.0         | 15.93 ± 0.1            | 29.93 ± 0.0        |
| mistral-medium Cloud    | 0.0001 ± 0.0         | 1.07 ± 0.17       | 0.0001 ± 0.0      | 3.88 ± 0.0      | 0.09 ± 0.0        | 15.57 ± 0.02           | 29.93 ± 0.0        |


**Support**: the numbers of item on which the metrics is computed (total items = 9224)

| model                   |   energy_consumption_support | generation_time_support   |   gwp_consumption_support |   judge_notator_support |   judge_precision_support | nb_tokens_completion_support   | nb_tokens_prompt_support   |
|:------------------------|-----------------------------:|:--------------------------|--------------------------:|------------------------:|--------------------------:|:-------------------------------|:---------------------------|
| mistral-medium Albert   |                         9224 | 9076.5 ± 208.6            |                      9224 |                    9224 |                      9224 | 9049.5 ± 246.78                | 9211.5 ± 17.68             |
| mistral-medium Oustcale |                         9224 | 9224.0 ± 0.0              |                      9224 |                    9224 |                      9224 | 9224.0 ± 0.0                   | 9224.0 ± 0.0               |
| mistral-medium Cloud    |                         9224 | 9224.0 ± 0.0              |                      9224 |                    9224 |                      9224 | 9224.0 ± 0.0                   | 9224.0 ± 0.0               |



## Set Overview

|   Id | Name                                | Dataset   | Model                   | Model params                               | Status          | Created at                 |   Num try |   Num success |
|-----:|:------------------------------------|:----------|:------------------------|:-------------------------------------------|:----------------|:---------------------------|----------:|--------------:|
| 1694 | Comparing Mistral-Medium on piaf__0 | piaf-v1.2 | mistral-medium Albert   | {'temperature': 0.2, 'sys_prompt': 'b3cb'} | running_metrics | 2025-12-12T10:46:12.113794 |      9224 |          9224 |
| 1695 | Comparing Mistral-Medium on piaf__1 | piaf-v1.2 | mistral-medium Albert   | {'temperature': 0.2, 'sys_prompt': 'b3cb'} | running_metrics | 2025-12-12T10:46:12.113794 |      9224 |          9224 |
| 1696 | Comparing Mistral-Medium on piaf__2 | piaf-v1.2 | mistral-medium Oustcale | {'temperature': 0.2, 'sys_prompt': 'b3cb'} | running_metrics | 2025-12-12T10:46:12.113794 |      9224 |          9224 |
| 1697 | Comparing Mistral-Medium on piaf__3 | piaf-v1.2 | mistral-medium Oustcale | {'temperature': 0.2, 'sys_prompt': 'b3cb'} | running_metrics | 2025-12-12T10:46:12.113794 |      9224 |          9224 |
| 1698 | Comparing Mistral-Medium on piaf__4 | piaf-v1.2 | mistral-medium Cloud    | {'temperature': 0.2, 'sys_prompt': 'b3cb'} | running_metrics | 2025-12-12T10:46:12.113794 |      9224 |          9224 |
| 1699 | Comparing Mistral-Medium on piaf__5 | piaf-v1.2 | mistral-medium Cloud    | {'temperature': 0.2, 'sys_prompt': 'b3cb'} | running_metrics | 2025-12-12T10:46:12.113794 |      9224 |          9224 |


## Details by Experiment

- [Experiment 1694](details/experiment_1694.md) - Comparing Mistral-Medium on piaf__0
- [Experiment 1695](details/experiment_1695.md) - Comparing Mistral-Medium on piaf__1
- [Experiment 1696](details/experiment_1696.md) - Comparing Mistral-Medium on piaf__2
- [Experiment 1697](details/experiment_1697.md) - Comparing Mistral-Medium on piaf__3
- [Experiment 1698](details/experiment_1698.md) - Comparing Mistral-Medium on piaf__4
- [Experiment 1699](details/experiment_1699.md) - Comparing Mistral-Medium on piaf__5
