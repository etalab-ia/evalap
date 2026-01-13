---
id: 106
name: "Comparing Mistral-Medium"
date: 2025-12-10T12:58:49.831120
description: ""
tags: []
---

# Experiment Set: Comparing Mistral-Medium (ID: 106)

Comparing Mistral-Medium in different instance.

WARNING: the model Albert is not a mistral-medium but a mistral-small model, check the experiment detail to see the full model parameters list.

**Finished**: 100%

## Scores

**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                   | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt | output_length   |
|:------------------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|:----------------|
| mistral-medium Oustcale | 0.0056 ± 0.0001      | 9.22 ± 0.28       | 0.0034 ± 0.0001   | 6.79 ± 0.17     | 0.64 ± 0.02       | 964.51 ± 19.41         |              16.3  | 504.3 ± 4.77    |
| mistral-medium Cloud    | 0.0059 ± 0.0002      | 13.13 ± 0.95      | 0.0035 ± 0.0001   | 6.62 ± 0.05     | 0.62 ± 0.05       | 986.53 ± 21.54         |              16.3  | 513.33 ± 1.69   |
| mistral-medium Albert   | 0.0015 ± 0.0         | 11.77 ± 0.29      | 0.0002 ± 0.0      | 6.2 ± 0.03      | 0.5 ± 0.03        | 416.42 ± 5.52          |              12.59 | 250.13 ± 5.01   |


**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                   | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt | output_length   |
|:------------------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|:----------------|
| mistral-medium Oustcale | 0.0074 ± 0.0001      | 11.42 ± 0.02      | 0.0044 ± 0.0001   | 7.47 ± 0.02     | 0.69 ± 0.07       | 1269.15 ± 17.04        |              25.64 | 651.49 ± 6.27   |
| mistral-medium Cloud    | 0.0076 ± 0.0001      | 16.72 ± 1.74      | 0.0045 ± 0.0001   | 7.51 ± 0.15     | 0.65 ± 0.05       | 1264.29 ± 30.59        |              25.64 | 652.14 ± 12.85  |
| mistral-medium Albert   | 0.002 ± 0.0          | 16.4 ± 0.13       | 0.0002 ± 0.0      | 6.67 ± 0.04     | 0.5 ± 0.02        | 557.5 ± 2.67           |              21.9  | 327.18 ± 1.41   |



## Set Overview

|   Id | Name                         | Dataset           | Model                   | Model params         | Status   | Created at                 |   Num try |   Num success |
|-----:|:-----------------------------|:------------------|:------------------------|:---------------------|:---------|:---------------------------|----------:|--------------:|
| 1642 | Comparing Mistral-Medium__0  | MFS_questions_v01 | mistral-medium Albert   | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        39 |            39 |
| 1643 | Comparing Mistral-Medium__1  | MFS_questions_v01 | mistral-medium Albert   | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        39 |            39 |
| 1644 | Comparing Mistral-Medium__2  | MFS_questions_v01 | mistral-medium Oustcale | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        39 |            39 |
| 1645 | Comparing Mistral-Medium__3  | MFS_questions_v01 | mistral-medium Oustcale | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        39 |            39 |
| 1646 | Comparing Mistral-Medium__4  | MFS_questions_v01 | mistral-medium Cloud    | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        39 |            39 |
| 1647 | Comparing Mistral-Medium__5  | MFS_questions_v01 | mistral-medium Cloud    | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        39 |            39 |
| 1648 | Comparing Mistral-Medium__6  | Assistant IA - QA | mistral-medium Albert   | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        46 |            46 |
| 1649 | Comparing Mistral-Medium__7  | Assistant IA - QA | mistral-medium Albert   | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        46 |            46 |
| 1650 | Comparing Mistral-Medium__8  | Assistant IA - QA | mistral-medium Oustcale | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        46 |            46 |
| 1651 | Comparing Mistral-Medium__9  | Assistant IA - QA | mistral-medium Oustcale | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        46 |            46 |
| 1652 | Comparing Mistral-Medium__10 | Assistant IA - QA | mistral-medium Cloud    | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        46 |            46 |
| 1653 | Comparing Mistral-Medium__11 | Assistant IA - QA | mistral-medium Cloud    | {'temperature': 0.2} | finished | 2025-12-10T12:58:49.831120 |        46 |            46 |


## Details by Experiment

- [Experiment 1642](details/experiment_1642.md) - Comparing Mistral-Medium__0
- [Experiment 1643](details/experiment_1643.md) - Comparing Mistral-Medium__1
- [Experiment 1644](details/experiment_1644.md) - Comparing Mistral-Medium__2
- [Experiment 1645](details/experiment_1645.md) - Comparing Mistral-Medium__3
- [Experiment 1646](details/experiment_1646.md) - Comparing Mistral-Medium__4
- [Experiment 1647](details/experiment_1647.md) - Comparing Mistral-Medium__5
- [Experiment 1648](details/experiment_1648.md) - Comparing Mistral-Medium__6
- [Experiment 1649](details/experiment_1649.md) - Comparing Mistral-Medium__7
- [Experiment 1650](details/experiment_1650.md) - Comparing Mistral-Medium__8
- [Experiment 1651](details/experiment_1651.md) - Comparing Mistral-Medium__9
- [Experiment 1652](details/experiment_1652.md) - Comparing Mistral-Medium__10
- [Experiment 1653](details/experiment_1653.md) - Comparing Mistral-Medium__11
